import streamlit as st
import requests
import helper
import concurrent.futures
import uuid
import pymongo
import uuid

api_host = helper.get_api_host()
access_token = st.session_state["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}



# Set page configuration
st.set_page_config(
    page_title="Data Engineering Project Generator",
    page_icon=":gear:",
    layout="wide"
)


#Fetch project status from mongo db
def fetch_project_status(project_id):
    client = pymongo.MongoClient("mongodb+srv://mohanku:@Team6lastride@pvm.54wtzjn.mongodb.net/?retryWrites=true&w=majority")
    #Keep fetching the status until it is success
    status = "In Progress"
    while "Success" != status:
        status = client["projects"]["status"].find_one({"project_id": project_id})["project_status"]
        st.write(status)

def create_project(selected_project, gpt_response, tools,project_id):
    """Create a new project based on user input."""
    url = f"{api_host}/create_project/"
    data = {"selected_project": selected_project, "gpt_response": gpt_response, "tools": tools, "project_id": project_id}
    response = requests.post(url, headers=headers,params=data).json()
    if response["status_code"] == 200:
        return response
    else:
        return "Something went wrong. Please try again later."

def get_project_suggestions(tools):
    # Check if the results are already stored in session state
    if "project_suggestions" in st.session_state:
        return st.session_state.project_suggestions

    # Otherwise, fetch the project suggestions from the API
    url = f"{api_host}/get_project_suggestions/"
    response = requests.post(url, headers=headers, params={"tools": tools}).json()
    list_of_projects = response.get("list_of_projects", [])
    gpt_response = response.get("gpt_response", "")

    # Store the results in session state
    st.session_state.project_suggestions = (list_of_projects, gpt_response)

    return list_of_projects, gpt_response


def project_generator(tools, project_id):

    #Fetch the project suggestions from session state
    list_of_projects, gpt_response = st.session_state.project_suggestions
    # Create a radio button to select the project
    selected_project = st.radio("Select a project", [""] + list_of_projects)

    # If a project is selected, create the project
    if selected_project and selected_project != "":
        response = create_project(selected_project, gpt_response, tools, project_id)
        if response["status_code"] == 200:
            url = response["detail"]
            st.success(f"Github URL: {url}")
        else:
            st.error(response)

def get_tools():
    """Get user input for tools to use."""
    tools = st.text_input("What tools do you want to use? (separate by commas)")
    
    if not tools:
        st.warning("Please enter some tools.")
    
    return tools.strip()

def main():
    if st.session_state["access_token"] == "":
        st.error("Please login to continue")
    else:
        st.title("Data Engineering Project Generator")
        tools = get_tools()
        
        if not tools:
            st.stop()

        # Get the list of projects and the GPT response
        get_project_suggestions(tools)


        #Generate a unique project id
        project_id = str(uuid.uuid4())
        project_generator(tools,project_id)


# Run the app
if __name__ == "__main__":
    main()