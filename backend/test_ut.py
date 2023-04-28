import requests
import uuid
from nbformat.v4 import new_notebook, new_code_cell

URL = "http://localhost:8000"

data = {'username': "aryan", 'password': "secret"}
response_token = requests.post(f'{URL}/token', data=data)   

access_token = response_token.json()["access_token"]

headers = {"Authorization": f"Bearer {access_token}"}

#Test Project Sugesstions
def test_project_suggestions():
    response = requests.post(f'{URL}/get_project_suggestions/', headers=headers, params={'tools':'Streamlit,Python,Heroku'})
    assert response.status_code == 200

#Test Fetch Project History from MongoDB
def test_fetch_project_history():
    response = requests.get(f'{URL}/project_history/', headers=headers)
    assert response.status_code == 200

#Test Create Project
def test_create_project():
    selected_project = "Time Series Analysis Dashboard: Build a time series analysis dashboard using streamlit and Python that can display real-time data streams from different sources such as sensor data, stock market data, social media data, website traffic, and more. Use AWS to deploy the dashboard and store the data in a scalable data warehouse like Amazon Redshift or Amazon S3 for easy access and management."
    gpt_response = "1. Time Series Analysis Dashboard: Build a time series analysis dashboard using streamlit and Python that can display real-time data streams from different sources such as sensor data, stock market data, social media data, website traffic, and more. Use AWS to deploy the dashboard and store the data in a scalable data warehouse like Amazon Redshift or Amazon S3 for easy access and management.\n\n2. Sentiment Analysis and Visualisation: Build a machine learning-powered sentiment analysis tool to perform real-time sentiment analysis on social media posts, news articles, and other text-based data sources. Use streamlit to create a custom dashboard that displays the results of the analysis in real-time, and AWS to deploy the tool and store the data in an S3 bucket. Visualize the data using interactive charts and graphs to enable better insights.\n\n3. Real-Time Fraud Detection: Build a real-time fraud detection system that uses machine learning to flag fraudulent transactions as they happen, and sends alerts to the appropriate parties in real-time. Use streamlit to create a custom dashboard that displays the analysis results, AWS for deployment, and a scalable data warehouse like Amazon Redshift to store the data.\n\n4. Data Analysis and Reporting Tool: Build a data analysis and reporting tool using Streamlit to help companies monitor their performance and create reports based on their data. Use AWS to deploy the tool and store the data in a scalable data warehouse like Amazon Redshift or Amazon S3 to enable easy access and analysis.\n\n5. Predictive Analytics Dashboard: Build a predictive analytics dashboard using streamlit and Python to help businesses make better decisions based on real-time data streams. Use machine learning models to predict trends, identify patterns, and forecast future outcomes. Use AWS to deploy the tool and store data in a scalable data warehouse like Amazon Redshift or Amazon S3. Display the results on an interactive dashboard that enables real-time updates and insights."
    
    unique_id = uuid.uuid4()
    response = requests.post(f'{URL}/create_project/', headers=headers, params={'selected_project':selected_project, 'gpt_response':gpt_response, 'tools':'Streamlit,Python,Heroku', 'project_id':unique_id})
    assert response.status_code == 200

#Test Create Repo
def test_create_repo():
    num = uuid.uuid4()
    response = requests.post(f'{URL}/create_repo/', headers=headers, params={'repo_name':f'Py_test_repo-{num}', 'description':'Test repo for Pytest'})
    assert response.status_code == 200

#Test Push Notebook to Repo
def test_push_notebook_to_repo():
    link = "https://github.com/midhunmohank/INFO6105/blob/main/advertising.csv"
    columns = "['A', 'B', 'C']"
    repo_name = "Py_test_repo-a77a8900-6b60-4c1d-97fb-7560a3721029-1682683515"
    message = "Test commit"
    num = uuid.uuid4()
    filename = f"EDA-{num}"
    response = requests.post(f'{URL}/notebook/', headers=headers, params={'link':link, 'columns':columns, 'repo_name':repo_name, 'message':message, 'filename':filename})
    assert response.status_code == 200


