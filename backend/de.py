import os
import openai
import re
import shutil
import time
import uuid
from github import Github, GithubException
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
import pymongo
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from helper_functions import login
import snowflake.connector
from snowflake.connector import DictCursor, ProgrammingError
from fastapi.requests import Request
from typing import Optional
from datetime import datetime, timedelta
import codegen


# # Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

app = FastAPI()

####################Login and User APIs############################

app = FastAPI()
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "b6033f6c2ecf769b8f9dc310302c6f3401e82e657cab28759b34937c469f98e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str 


class User(BaseModel):
    USERNAME: str
    FULL_NAME: str 
    TIER:str
    HASHED_PASSWORD:str
    DISABLED: bool 

class UserInDB(User):
    HASHED_PASSWORD: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(username: str, password: str):
    user_db = login.get_users()
    user = get_user(user_db, username)
    if not user:
        return False
    if not verify_password(password, user.HASHED_PASSWORD):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user_db = login.get_users()
    user = get_user(user_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.DISABLED:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.USERNAME}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
###########################################################################################
async def get_user_info(user: User):
    return {"username": user.USERNAME, "tier": user.TIER, "hashed_password": user.HASHED_PASSWORD}

async def get_user_password(user: User):
            return {"username": user.USERNAME, "hashed_password": user.HASHED_PASSWORD}

###########################################################################################
#API for Creating a new user 
@app.post("/create_user/")
async def create_user(user: User):
    #Check if the user already exists
    check_user = login.check_user_exists(user.USERNAME)
    if check_user == True:
        return {"status": False,"Response": "Already Exists"}
    else:
        login.create_user(full_name = user.FULL_NAME, username = user.USERNAME, hashed_password = pwd_context.hash(user.HASHED_PASSWORD), tier = user.TIER)
        return {"status": True, "Response":"User created successfully!"}


#API for Deleting a user
@app.post("/delete_user/")
async def delete_user(user: User):
    #Check if the user exists
    if login.check_user_exists(user):
        return login.delete_user(user)
    else:
        return {"status":"User does not exists"}

#API for Updating a user
@app.post("/update_user/")
async def update_user(old_password: str, new_password: str,current_user: User = Depends(get_current_active_user)):
    user_details = await get_user_info(current_user)
    new_password_hash = pwd_context.hash(new_password)
    if new_password == old_password:
        return {"status":False, "response": "New password and old password can't be same"}
    else:
        if verify_password(old_password, user_details["hashed_password"]):
            response = login.update_user_password(new_password_hash,current_user.USERNAME)
            if response:
                return {"status":True, "response": "Password updated successfully"}    
        else:
                return {"status":False, "response": "Old password doesn't match"}

#API for getting the list of users
@app.get("/get_users/")
async def get_users(current_user: User = Depends(get_current_active_user)):
    return login.get_users()



################Application Feature APIs ###############################

def get_project_structure_code(selected_project: str,full_response: str,tools: str):
    #Convert res1 list to a string
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages = [{"role": "system", "content" : "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-03-02"},
    {"role": "user", "content" : f"give me suggestions of 5 data engineering projects using {tools}"},
    {"role": "assistant", "content" : full_response},
    {"role": "user", "content" : f"give me python code to create the file structure and empty files in each folder for this project and I should be able to run the code without any changes:{selected_project}"}]
    )

    res2 = completion["choices"][0]["message"]["content"]
    
    pattern = r"```(.+?)```"
    code = re.search(pattern, res2, re.DOTALL).group(1)
    if "python" in code:
        code = code.replace("python", " ")
    return code

def project_suggestions(tools):
    query = f"give me detailed suggestions of 5 data engineering projects using {tools}"

    response =  openai.ChatCompletion.create(
            model = "gpt-3.5-turbo", 
            messages = [
                {"role" : "user", "content" : query }
            ],
            temperature = 1.0
        )
    res1 = response["choices"][0]["message"]["content"]
    gpt_response = res1
    # Convert res1 to a list where bullet numbers start
    res1 = re.sub(r'(\n\d+\.)', r'\n\n\1', res1)
    #Convert res1 to a list by splitting on bullet numbers
    res1 = re.split(r'\n\d+\.', res1)
    #remove \n from every element in the list
    res1 = [i.replace('\n', '') for i in res1]
    #remove the first character from every element in the list if it is a number
    res1 = [i[1:] if i[0].isdigit() else i for i in res1]
    #Remove any . from the beginning of every element in the list
    res1 = [i[1:] if i[0] == '.' else i for i in res1]
    #Remove any empty elements from the list
    res1 = [i for i in res1 if i != '']
    return res1,gpt_response

#######Data Science

@app.post("/create_repo/")
async def create_repo(repo_name, description):
    """
    Creates a repository 
    """
    x = codegen.create_repo(repo_name, description)
    return {"repo_link" : x[0], "repo_name" : x[1]}


@app.post("/notebook/")
async def push_notebook(link,columns, repo_name, message, filename):
    """
    Creates a notebook and pushes it to a repository
    """
    
    nb = codegen.get_ipynb(link, columns)
    codegen.push_notebook(repo_name, message, nb, filename)
    

######Data Engineering
#API to test the connection with a test input and output
@app.get("/test/")
def test(name):
    return {"name":f"Hello {name}"}

# Define the function to get the project suggestions
@app.post("/get_project_suggestions/")
def get_project_suggestions(tools: str, current_user: User = Depends(get_current_active_user)):
    #Generate the project suggestions and check if res1 has a length less than or equal to 1
    res1,gpt_response = project_suggestions(tools)
    while len(res1) <= 1:
        res1,gpt_response = project_suggestions(tools)

    #Return the list of projects and the gpt_response
    return {"list_of_projects":res1,"gpt_response":gpt_response}


#Function to create the project for the selected project suggestion
@app.post("/create_project/")
def create_project(selected_project,gpt_response,tools, current_user: User = Depends(get_current_active_user)):
    # Create a temporary directory to store the file structure
    temp_dir = f"temp_{uuid.uuid4().hex}"
    os.makedirs(temp_dir, exist_ok=True)

    # Get the code to create the file structure
    code = get_project_structure_code(selected_project,gpt_response,tools)
    
    try:
        # Write the code to a Python file in the temporary directory
        with open(f"{temp_dir}/file_structure.py", "w") as f:
            f.write(code)
            #Close the file
            f.close()

        # Run the Python file to create the file structure in the temporary directory
        os.chdir(temp_dir)
        os.system("python file_structure.py")

        # Return a dictionary mapping directories to files
        output_dict = {}
        for root, dirs, files in os.walk("."):
            if root != ".":
                output_dict[root[2:]] = files
        #if output_dict is empty, run generate_project_structure_code function again and and do it until output_dict is not empty
        while output_dict == {}:
            code = get_project_structure_code(selected_project,gpt_response,tools)
            with open(f"{temp_dir}/file_structure.py", "w") as f:
                f.write(code)
            os.chdir(temp_dir)
            os.system("python file_structure.py")
            for root, dirs, files in os.walk("."):
                if root != ".":
                    output_dict[root[2:]] = files

        # Go through each value in the dictionary and send requests to the OpenAI API to generate code for each file and add into the file
        for key, value in output_dict.items():
            for file in value:
                if value != []:
                    code_base = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", 
                    messages = [{"role": "system", "content" : "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-03-02"},
                {"role": "user", "content" : f"give me suggestions of 5 data engineering projects using {tools}"},
                {"role": "assistant", "content" : gpt_response},
                {"role": "user", "content" : f"give me python code to create the file structure and empty files in each folder for this project:{selected_project}"},
                {"role": "assistant", "content" : code},
                {"role": "user", "content" : f"give me python code for each file: {file} in the folder: {key}"}]
                )
                    generated_code = code_base["choices"][0]["message"]["content"]

                    pattern = r"```(.+?)```"
                    matches = re.findall(pattern, generated_code, re.DOTALL)
                    #Remove python from the code
                    generated_code = generated_code.replace("python", " ")

                    if matches:
                        generated_code = matches[0]
                    else:
                        # Handle the case where no matches are found
                        generated_code = ""

                    # Write the code to the file
                    with open(f"{key}/{file}", "w") as f:
                        f.write(generated_code)

        # Create a GitHub repository and upload the file structure
        g = Github(GITHUB_ACCESS_TOKEN)
        user = g.get_user()
        repo_name = f"Project-{int(time.time())}"
        repo = user.create_repo(repo_name)
        for root, dirs, files in os.walk("."):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                try:
                    repo.create_file(file_path[2:], f"Add {file}", content, branch="main")
                except GithubException as e:
                    print(f"Error uploading file {file_path}: {e}")

        # remove file_structure.py
        os.remove("file_structure.py")

        # Return the GitHub repository URL
        return {"url": f"{repo.html_url}"}

    finally:
        # Clean up the temporary directory
        os.chdir("..")
        shutil.rmtree(temp_dir)


