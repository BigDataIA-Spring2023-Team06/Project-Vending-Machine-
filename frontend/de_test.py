import streamlit as st
import requests


# Streamlit app to suggest data engineering projects based on the user's input
st.set_page_config(
    page_title="Data Engineering Project Generator",
    page_icon=":gear:",
    layout="wide"
)
css = '''
<style>
    [data-testid="stSidebar"]{
        min-width: 400px;
        max-width: 800px;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)
st.title("Data Engineering Project Generator")

# Set the width of the sidebar


# Helper functions
def get_project_suggestions(tools):
    url = "http://localhost:8000/get_project_suggestions/"
    payload = {"tools": tools}
    response = requests.post(url, params=payload)
    response = response.json()
    list_of_projects = response.get("list_of_projects", [])
    gpt_response = response.get("gpt_response", "")
    return list_of_projects, gpt_response

def create_project(selected_project, gpt_response, tools):
    url = "http://localhost:8000/create_project/"
    payload = {"selected_project": selected_project, "gpt_response": gpt_response, "tools": tools}
    response = requests.post(url, params=payload)
    response = response.json()
    return response

# UI layout
st.sidebar.subheader("Enter the tools you want to use separated by commas:")
tools = st.sidebar.text_input("", "")
if not tools:
    st.sidebar.warning("Please enter at least one tool.")

if st.sidebar.button("Get Project Suggestions"):
    list_of_projects, gpt_response = get_project_suggestions(tools)
    if not list_of_projects:
        st.warning("No project suggestions found with the given tools.")
    else:
        st.write("Here are some project suggestions:")
        selected_project = st.selectbox("Select the project you want to create", list_of_projects, key="project_selector")
        if st.button("Create Project"):
            response = create_project(selected_project, gpt_response, tools)
            st.success("Project created successfully!")
            st.write(f"Project Name: {response.get('project_name')}")
            st.write(f"Project Description: {response.get('project_description')}")
            st.write(f"Tools Used: {response.get('tools')}")

