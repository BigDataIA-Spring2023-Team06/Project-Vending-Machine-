from fastapi import FastAPI
import codegen


app = FastAPI()


@app.post("/create_repo/")
async def create_repo(repo_name, description):
    """
    Creates a repository 
    """
    return {"repo_link" : codegen.create_repo(repo_name, description)}


@app.post("/notebook/")
async def push_notebook(link,columns, repo_name, message, filename):
    """
    Creates a notebook and pushes it to a repository
    """
    
    nb = codegen.get_ipynb(link, columns)
    codegen.push_notebook(repo_name, message, nb, filename)
    
    
