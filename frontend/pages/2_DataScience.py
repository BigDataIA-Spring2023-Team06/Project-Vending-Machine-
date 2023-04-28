import streamlit as st
import time
import requests 
import helper


api_host = helper.get_api_host()
access_token = st.session_state["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}
api_host = helper.get_api_host() 


# def process_data(user_input):
#     response_repo = requests.get(f"{api_host}/create_repo/", pa)
#     output_link = "https://www.example.com"
#     return output_link

def main():
    if st.session_state["access_token"] == "":
        st.error("Please login to continue")
    else:
        st.title("Data Science Projects")

        # User input form
        st.write("Enter the link to your data source:")
        user_input = st.text_input("Link")
        cols = st.text_input("Columns")
        
        if st.button("Submit"):
            # Display progress bar while processing data
            progress_bar = st.progress(0)

            data = {"repo_name": "eda", "description" : "This is a test"}
            response_repo = requests.post(f"{api_host}/create_repo/", params = data)
            # Process user input
            
            if response_repo.status_code == 200:
                output_link = response_repo.json()["repo_link"]
                repo_name = output_link.split("/")[-1]
                data_note = {"link":user_input, "columns":cols, "repo_name":repo_name, "message" : f"EDA for dataset {user_input}", "filename" : "eda"}
                response_nb = requests.post(f"{api_host}/notebook/", params = data_note)
                
                st.write(output_link)
                st.write(repo_name)
            

            # Display output
            progress_bar.empty()
            # st.write("Output Link:")
            # st.write(output_link)

if __name__ == "__main__":
    if "access_token" in st.session_state: 
        main()
    else:
        st.error("Please Login First")
