import streamlit as st
import requests
import helper

#initilize token
st.session_state["access_token"] = ""

host_url_api = helper.get_api_host()


def add_to_session_state(new, value):
        st.session_state[new] = value
        
# Define the Streamlit app
def is_authorized(username, password):
    url_token = f"{host_url_api}/token"
    data = {'username': username, 'password': password}
    response_token = requests.post(url_token, data=data)
    # print(response_token.json())
    if response_token.status_code == 200:
        add_to_session_state("access_token", response_token.json()["access_token"])
        return True
    else:
        return False

def get_token(username, password):
    url_token = f"{host_url_api}/token"
    data = {'username': username, 'password': password}
    response_token = requests.post(url_token, data=data)
    response_token = response_token.json()["access_token"]
    return response_token


# Define the Streamlit app
def app():
    api_host = helper.get_api_host()
    # Add a cover image
    st.title('ProjectVendingMachine')
    st.header("Data as a Service")
    #st.image("images/cover.png", width=500)

    # Add a login form
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        
        st.write(is_authorized(username, password))
        
        if is_authorized(username, password):
            st.success("Logged in as {}".format(username))
            
            # Open the link in a new tab
            #st.markdown(f'<meta http-equiv="refresh" content="0; url={host_url}"/HOME.py>', unsafe_allow_html=True)
        else:
            st.error("Invalid username or password")

    # Add a register form
    register_option = st.selectbox("Don't have an account?", ["Select an option", "Register here"])
    if register_option == "Register here":

        new_username = st.text_input("New username", key="new_username_input")
        new_name = st.text_input("Full Name", key="new_name_input")
        new_password = st.text_input("New password", type="password", key="new_password_input")
        if st.button("Register"):
            payload = {
                        "USERNAME": new_username,
                        "FULL_NAME": new_name,
                        "TIER": 1,
                        "HASHED_PASSWORD": new_password,
                        "DISABLED": False
                    }

            headers = {
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    }

            response = requests.post(f"{api_host}/create_user/", json=payload, headers=headers)
            # responses = requests.post(, user={"USERNAME": new_username, "FULL_NAME":new_name,"tier": service_plan,"password": new_password,"DISABLED": False})
            response = response.json()
            if response['status'] == True:
                st.success("User created")
            else:
                st.error("This username is already taken")

    # # Add a change password form
    # change_password_option = st.selectbox("Change password?", ["Select an option", "Change password"])
    # if change_password_option == "Change password":

    #     ch_old_password = st.text_input("Old password", type="password", key="old_pw_change_password")
    #     ch_new_password = st.text_input("New password", type="password", key="new_pw_change_password")
    # if st.button("Change password"):
    #     header={"Authorization": f"Bearer {st.session_state['access_token']}"}
    #     response = requests.post(f"{host_url_api}/update_user/?old_password={ch_old_password}&new_password={ch_new_password}", headers=header)
    #     response = response.json()
    #     if response['status'] == True:
    #         st.success("Password changed successfully")
    #     else:
    #         st.error("Passwords don't match")



if __name__ == '__main__':
    app()
