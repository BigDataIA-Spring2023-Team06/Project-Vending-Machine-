# Project-Vending-Machine
### Important Links
[APP Link](http://18.219.140.115:8081) <br>
[API Link](http://18.219.140.115:8000/docs) <br>
[Code Labs](https://codelabs-preview.appspot.com/?file_id=1o8MDDTwOHbqMEI7V0mA9TQ2dELlGQYqSJbtKeRW_Dek/edit#0) <br>
[User Manual](https://codelabs-preview.appspot.com/?file_id=1o8MDDTwOHbqMEI7V0mA9TQ2dELlGQYqSJbtKeRW_Dek/edit#0) <br>
[Demo Video](https://youtu.be/cicxeubgKac)

##### The primary objective of the Project Vending Machine is to simplify the process of creating a Github portfolio for job seekers. By automating the initial setup and configuration of data science and data engineering projects, the platform aims to reduce the time and effort required to create a portfolio. Additionally, the platform aims to help users identify the right skills to include in their portfolio by suggesting relevant projects based on their requirements and preferences. By achieving these objectives, the platform can help users to showcase their skills and experience more effectively, improving their chances of getting their desired job role.

## Architecture Diagram:

![Architecture Diagram](https://github.com/BigDataIA-Spring2023-Team06/Documentation/blob/main/fds.drawio.png)

## APPLICATION FEATURES

Our application, the "Portfolio Vending Machine," offers several unique features to simplify the process of creating a Github portfolio.

###### Personalized Portfolio Generation: 
The application generates a personalized Github portfolio for the user based on their resume and dream job role. This is achieved by using advanced natural language processing techniques to analyze the user's resume and identify relevant skills and experiences that should be included in their portfolio.
###### Project Creation: 
Our application allows the user to create data engineering and data science projects with ease. All the user has to do is upload a link to their dataset, and the data science project will be created, including all the analysis, and directly uploaded into their Github repository. For the data engineering projects, the user needs to upload the technologies they need to use in their project based on the job description or the company's tech stack. Our application provides suggestions for projects, and when the user selects a project, it gets created and uploaded into their Github repository.
###### Dashboard: 
Our application provides a dashboard where the user can enter any company's URL and get analytics based on the data available on the Explorium API. Additionally, our dashboard provides the entire tech stack of the company's tech stack from the Explorium data. This feature helps job seekers identify the most in-demand technologies used by companies and adjust their portfolios accordingly.
###### Integration with Github: 
Our application seamlessly integrates with Github, allowing users to create repositories and upload their projects directly from the application.
###### Streamlit Platform: 
Our application is running on the Streamlit platform, providing an interactive user interface and a simple navigation experience.
###### Containerization with Docker: 
Our application is containerized with Docker, enabling easy deployment, management, and scaling of the application.
###### Deployment with CI/CD on EC2 instance:
Our application supports continuous integration and deployment using github actions

## How to replicate the project?
* Clone the repository
* Run the docker dameon on your machine. Run the follwing command in your root.
```
docker compose up
```
* Update the following in secrets .env in your root with all credentials.
```
OPENAI_API_KEY=""
GITHUB_ACCESS_TOKEN=""
SNOWFLAKE_USER=""
SNOWFLAKE_PASSWORD=""
SNOWFLAKE_ACCOUNT=""
SNOWFLAKE_DATABASE=""
SNOWFLAKE_WAREHOUSE=""
SNOWFLAKE_SCHEMA=""
MONGODB_USER=""
MONGODB_PASSWORD=""
```
* Now run the following command on terminal
```
docker compose --env-file secrets.env up
```
* Run your app on localhost:8000 and localhost:8502

#### Attestations
WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT

AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK

Contribution: 

* Midhun Mohan Kudayattutharayil: 25%
* Sanjay Kashyap: 25%
* Snehil Aryan: 25%
* Vikash Singh: 25%



