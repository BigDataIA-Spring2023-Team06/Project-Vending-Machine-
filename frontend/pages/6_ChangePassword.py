import streamlit as st
import requests
import helper

api_host = helper.get_api_host()
access_token = st.session_state["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}


def change_password():
    # Check if the user is logged in
    if st.session_state["access_token"] == "":
        st.error("Please login to continue")
    else:
        change_password_option = st.selectbox("Change password?", ["Select an option", "Change password"])
        if change_password_option == "Change password":

            ch_old_password = st.text_input("Old password", type="password", key="old_pw_change_password")
            ch_new_password = st.text_input("New password", type="password", key="new_pw_change_password")
        if st.button("Change password"):
            header={"Authorization": f"Bearer {st.session_state['access_token']}"}
            response = requests.post(f"{api_host}/update_user/?old_password={ch_old_password}&new_password={ch_new_password}", headers=header)
            response = response.json()
            if response['status'] == True:
                st.success("Password changed successfully")
            else:
                st.error("Passwords don't match")


if __name__ == '__main__':
    change_password()