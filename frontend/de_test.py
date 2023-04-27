import streamlit as st
import requests
from streamlit import session_state

# Define SessionState class
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Set page configuration
st.set_page_config(
    page_title="Data Engineering Project Generator",
    page_icon=":gear:",
    layout="wide"
)

# Define functions
def get_project_suggestions(tools):
    """Get project suggestions based on user input."""
    url = "http://localhost:8000/get_project_suggestions/"
    #Show the loading message
    with st.spinner("Generating project suggestions..."):
        response = requests.post(url, params={"tools": tools}).json()
        return response.get("list_of_projects", []), response.get("gpt_response", "")

def create_project(selected_project, gpt_response, tools):
    """Create a new project based on user input."""
    url = "http://localhost:8000/create_project/"
    response = requests.post(url, params={"selected_project": selected_project, "gpt_response": gpt_response, "tools": tools}).json()
    return response.get("url", "")

def create_buttons(list_of_projects):
    """Show project selection interface and call create_project function."""
    counter = 0
    buttons =[]
    for project in list_of_projects:
        buttons.append(st.button(project, key={f"Project-{counter}"}))
        counter += 1
    return buttons

def get_git_url(buttons,gpt_response,tools):
    for i,button in enumerate(buttons):
        if button:
            with st.spinner("Creating project..."):
                url = create_project(buttons, gpt_response, tools)
                st.success(f"Github URL: {url}")


def get_tools():
    """Get user input for tools to use."""
    tools = st.text_input("What tools do you want to use? (separate by commas)")
    if not tools:
        st.warning("Please enter some tools.")
    else:
        return tools.strip()

# # Define main function
# def main():
#     # Get tools from user input
#     tools = get_tools()
#     if not tools:
#         return

#     list_of_projects, gpt_response = get_project_suggestions(tools)
#     buttons = create_buttons(list_of_projects)

#     for i, button in enumerate(buttons):
#         if button:
#             with st.spinner("Creating project..."):
#                 url = create_project(buttons[i], gpt_response, tools)
#             st.success(f"Github URL: {url}")
#             break

# Run the app
if __name__ == "__main__":
    tools = get_tools()
    if not tools:
        st.stop()
    list_of_projects, gpt_response = get_project_suggestions(tools)
    for i in (create_buttons(list_of_projects)):
        if i:
            get_git_url(list_of_projects,gpt_response,tools)
            break
    
    
    
