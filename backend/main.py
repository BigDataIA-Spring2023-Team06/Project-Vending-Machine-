import os
import openai
import nbformat
from nbformat.v4 import new_notebook, new_code_cell

openai.api_key = os.getenv("OPENAI_API_KEY")



def get_ipynb(link,columns):
    query= f"""{{"Dataset Link": "{link}",
"columns of the dataset":
"{columns}",
"prompt":"write code to Do eda on this dataset with check for nulls, plots, distribution etc. Also add a comment for  each code block so I can split the code into a Jupyter notebook"}}"""
    
    response =  openai.ChatCompletion.create(
        model = "gpt-3.5-turbo", 
        messages = [
            {"role" : "user", "content" : query }
        ]
    )
    response= response["choices"][0]["message"]["content"]

    #Break response into a list of code blocks by the # separator without removing the separator
    code_blocks = response.split('#')

    #Add # to the beginning of each code block
    code_blocks = ['#' + code_block for code_block in code_blocks]

    # Create a new notebook
    notebook = new_notebook()

    for code in code_blocks:
        cell = new_code_cell(code)
        notebook['cells'].append(cell)

    # Save the notebook to a file
    nbformat.write(notebook, 'EDA.ipynb')
    
    #Return the notebook
    return notebook


get_ipynb("https://raw.githubusercontent.com/midhunmohank/INFO6105/main/advertising.csv","TV,Radio,Newspaper,Sales")


