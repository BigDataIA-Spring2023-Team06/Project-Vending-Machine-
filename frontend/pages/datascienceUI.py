import streamlit as st
import time

def process_data(user_input):
    # TODO: Process data and return output link
    output_link = "https://www.example.com"
    return output_link

def main():
    st.title("Data Science Projects")

    # User input form
    st.write("Enter the link to your data source:")
    user_input = st.text_input("Link")
    if st.button("Submit"):
        # Display progress bar while processing data
        progress_bar = st.progress(0)
        for i in range(10):
            progress_bar.progress(i + 1)
            time.sleep(0.1)

        # Process user input
        output_link = process_data(user_input)

        # Display output
        progress_bar.empty()
        st.write("Output Link:")
        st.write(output_link)

if __name__ == "__main__":
    if "access_token" in st.session_state: 
        main()
    else:
        st.error("Please Login First")
