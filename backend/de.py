import os
import openai
import re
import shutil
import time
import uuid
from github import Github, GithubException
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import HTMLResponse


# # Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

app = FastAPI()

def get_project_structure_code(selected_project: str,full_response: str,tools: str):
    #Convert res1 list to a string
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages = [{"role": "system", "content" : "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-03-02"},
    {"role": "user", "content" : f"give me suggestions of data engineering projects using {tools}"},
    {"role": "assistant", "content" : full_response},
    {"role": "user", "content" : f"give me python code to create the file structure and empty files in each folder for this project and I should be able to run the code without any changes:{selected_project}"}]
    )

    res2 = completion["choices"][0]["message"]["content"]
    
    pattern = r"```(.+?)```"
    code = re.search(pattern, res2, re.DOTALL).group(1)
    if "python" in code:
        code = code.replace("python", " ")
    return code

#API to test the connection with a test input and output
@app.get("/test/")
def test(name):
    return {"name":f"Hello {name}"}

# Define the function to get the project suggestions
@app.post("/get_project_suggestions/")
def get_project_suggestions(tools: str):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
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
    return {"list_of_projects":res1,"gpt_response":gpt_response}


#Function to create the project for the selected project suggestion
@app.post("/create_project/")
def create_project(selected_project: str,gpt_reponse: str,tools: str):
    # Create a temporary directory to store the file structure
    temp_dir = f"temp_{uuid.uuid4().hex}"
    os.makedirs(temp_dir, exist_ok=True)

    # Get the code to create the file structure
    code = get_project_structure_code(selected_project,gpt_reponse,tools)
    
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
            code = get_project_structure_code(selected_project,gpt_reponse,tools)
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
                {"role": "user", "content" : f"give me suggestions of data engineering projects using {tools}"},
                {"role": "assistant", "content" : gpt_reponse},
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


