import os

code = """ 
import os

# Define the root project directory
root_dir = 'Real-time_tweet_sentiment_analysis'

# Define the directory structure
dir_structure = {
    'backend': {
        'app': {
            '__init__.py': '',
            'main.py': '',
        },
        'sentiment_analysis': {
            '__init__.py': '',
            'analyzer.py': '',
        },
        'requirements.txt': '',
        'Dockerfile': '',
    },
    'frontend': {
        '__init__.py': '',
        'app.py': '',
        'requirements.txt': '',
        'Dockerfile': '',
    },
    'README.md': '',
}

def create_dirs_and_files(path, structure):
    """Recursively create directories and files for a given structure."""
    for name, item in structure.items():
        item_path = os.path.join(path, name)
        if isinstance(item, dict):
            os.makedirs(item_path, exist_ok=True)
            create_dirs_and_files(item_path, item)
        elif isinstance(item, str):
            with open(item_path, 'w') as f:
                f.write(item)

# Create the project directory
os.makedirs(root_dir, exist_ok=True)

# Create the file structure
create_dirs_and_files(root_dir, dir_structure)

"""


#Create a temp dicrectory to store the code
os.makedirs("temp", exist_ok=True)