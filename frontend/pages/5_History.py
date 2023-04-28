import streamlit as st
import pandas as pd
import helper
import requests
import json
from datetime import datetime

api_host = helper.get_api_host()
access_token = st.session_state["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}

#Function to fetch the project data from mongo db
def fetch_project_data():
    url = f"{api_host}/project_history/"
    if st.session_state["access_token"] == "":
        st.error("Please login to continue")
    else:
        response = requests.get(url, headers=headers)
        try:
            #Convert the response to json
            response_json = response.json()
            #Convert the response to dataframe
            df = pd.DataFrame(response_json,columns=['created','project_name','project_link'])
            # convert the "created" column to a datetime object
            for _, d in df.iterrows():
                try:
                    d["created"] = datetime.strptime(d["created"], "%Y-%m-%d %H:%M:%S.%f")
                except ValueError:
                    st.warning(f"Invalid value in created column: {d['created']}")
            df["created"] = df["created"].apply(lambda x: datetime.strftime(x, "%Y-%m-%d %H:%M:%S"))
            #Display the dataframe
            st.dataframe(df)
        except ValueError:
            st.error("Unable to retrieve project data from the server")



def project_history():
    # Set page configuration
    st.set_page_config(
        page_title="Project History",
        page_icon=":gear:",
        layout="wide"
    )
    st.title("Project History")
    #Fetch the project data from mongo db
    fetch_project_data()

if __name__ == "__main__":
    if "access_token" in st.session_state:
        project_history()
    else:
        st.error("Please Login First")

