import streamlit as st
import requests
import helper


access_token = st.session_state["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}
api_host = helper.get_api_host() 

# Set page configuration
st.set_page_config(
    page_title="Data Engineering Project Generator",
    page_icon=":gear:",
    layout="wide"
)

def create_project(selected_project, gpt_response, tools):
    """Create a new project based on user input."""
    url = f"{api_host}/create_project/"
    data = {"selected_project": selected_project, "gpt_response": gpt_response, "tools": tools}
    response = requests.post(url, params=data, headers=headers).json()
    return response

def get_project_suggestions(tools):
    url = f"{api_host}/get_project_suggestions/"
    #Show the loading message
    # with st.spinner("Generating project suggestions..."):
    response = requests.post(url, params={"tools": tools}, headers=headers).json()
    # Get the list of projects and the GPT response
    list_of_projects = response.get("list_of_projects", [])
    gpt_response = response.get("gpt_response", "")
    return list_of_projects, gpt_response


def project_generator(list_of_projects, gpt_response, tools):
    #Create a radio button to select the project
    selected_project = st.radio("Select a project", list_of_projects)

    #If a project is selected, create the project
    if selected_project:
        url = create_project(selected_project, gpt_response, tools)
        st.success(f"Github URL: {url}")

def get_tools():
    """Get user input for tools to use."""
    tools = st.text_input("What tools do you want to use? (separate by commas)")
    
    if not tools:
        st.warning("Please enter some tools.")
    
    return tools.strip()

def main():
    st.title("Data Engineering Project Generator")
    tools = get_tools()
    
    if not tools:
        st.stop()

    # Get the list of projects and the GPT response
    list_of_projects, gpt_response = get_project_suggestions(tools)

    # Check if the list of projects is empty
    if not list_of_projects:
        st.warning("No projects found.")
        st.stop()
    else:
        project_generator(list_of_projects, gpt_response, tools)



# Run the app
if __name__ == "__main__":
    
    if "access_token" in st.session_state: 
        main()
    else:
        st.error("Please Login First")

