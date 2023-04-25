import os
import openai
import re
import shutil

openai.api_key = os.getenv("OPENAI_API_KEY")

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
    return res1, gpt_response

def get_project_structure_code(selected_project: str,full_response: str):
    #Convert res1 list to a string
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages = [{"role": "system", "content" : "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-03-02"},
    {"role": "user", "content" : "give me suggestions of data engineering projects using FastAPI, Streamlit and AWS"},
    {"role": "assistant", "content" : full_response},
    {"role": "user", "content" : f"give me python code to create the file structure and empty files in each folder for this project:{selected_project}"}]
    )

    res2 = completion["choices"][0]["message"]["content"]
    
    pattern = r"```(.+?)```"
    code = re.search(pattern, res2, re.DOTALL).group(1)
    if "python" in code:
        code = code.replace("python", " ")

    return code


def generate_file_dictionary(code):
    #create a temp directory to store the .py file
    os.makedirs("temp", exist_ok=True)
    #Store the code in a python file in the temp directory
    with open("temp/file_structure.py", "w") as f:
        f.write(code)
    #Set the current working directory to the temp directory
    os.chdir("temp")
    #Run the python file to create the file structure in the temp directory
    os.system("python file_structure.py")
    #Delete the python file
    os.remove("file_structure.py")
    #Set the names of all folders and files in the temp directory to a dictionary with folders as keys and files as values
    output_dict = {}
    for root, dirs, files in os.walk("."):
        if root != ".":
            output_dict[root[2:]] = files
    #Set the current working directory back to the root directory
    os.chdir("..")
    #Delete the temp directory
    shutil.rmtree("temp")
    return output_dict
