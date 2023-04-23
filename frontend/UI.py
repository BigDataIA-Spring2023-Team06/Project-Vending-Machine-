import os
import smtplib
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def login():
    st.title("User Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        # check if the email and password match a registered user
        with open("users.txt", "r") as f:
            for line in f:
                user, pw = line.strip().split(",")
                if email == user and password == pw:
                    st.success("Login successful!")
                    return
        st.warning("Invalid email or password")


def register():
    st.title("Register Now")
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    register_button = st.button("Register")

    if register_button:
        # add the new user's info to the file
        with open("users.txt", "a") as f:
            f.write(f"{new_email},{new_password}\n")
        st.success("Registration successful!")


def send_email(email, password):
    # Set up the Gmail API credentials
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.compose'])
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/gmail.compose'])
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Send email through Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = creds.email
    receiver_email = email
    password = creds.token
    message = f"""\
    Subject: Password reminder

    Your password is: {password}"""

    context = smtplib.SMTP(smtp_server, smtp_port)
    context.starttls()
    context.login(sender_email, password)
    context.sendmail(sender_email, receiver_email, message)
    context.quit()


def forgot_password():
    st.title("Forgot Password")
    email = st.text_input("Enter your email")
    send_button = st.button("Send Password")

    if send_button:
        # check if the email is registered
        with open("users.txt", "r") as f:
            for line in f:
                user, pw = line.strip().split(",")
                if email == user:
                    send_email(email, pw)
                    st.success("Password sent to email!")
                    return
        st.warning("Email address not found")


st.set_page_config(page_title="Project Vending Machine")
menu = ["Login", "Register Now", "Forgot Password"]
choice = st.sidebar.selectbox("Select an option", menu)

if choice == "Login":
    login()
elif choice == "Register Now":
    register()
elif choice == "Forgot Password":
    forgot_password()
