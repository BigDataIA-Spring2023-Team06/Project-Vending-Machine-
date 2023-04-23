from github import Github
import os
import openai
import nbformat
from nbformat.v4 import new_notebook, new_code_cell
import json


openai.api_key = "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"
g = Github("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")
user = g.get_user()


import nbformat

with open('test.ipynb', 'r') as f:
    nb = nbformat.read(f, as_version=4)

# print(type(nb))
# print(nb)
# print(str(nb))
x = json.dumps(nb)
repo = user.get_repo("my-new-repo")
commit_message = 'Add example file'
repo.create_file("testing3298.ipynb", "This is the first try from Python", x)