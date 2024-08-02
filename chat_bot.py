import streamlit as st
# from dotenv import load_dotenv
import os
import time
import google.generativeai as genai

# Load the env variables
# load_dotenv()

# Configure gen ai
genai.configure(api_key="AIzaSyCYVv2N2xDvVoxM6iNMbnIg9zcXg58uzf0")


# Function to animate writing
def writing(welcome):
    for word in welcome.split(" "):
        yield word + " "
        time.sleep(0.2)


st.set_page_config(page_title="Chat Bot", page_icon=":smart_toy:")
st.title("Chat Bot")


# Function to take user input
def user_input():
    question = st.chat_input("Enter your question")
    return question


# Function to get response from generative AI
def genaiAnswer(question):
    if not question:
        return "Please enter a question."
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"


# Function to process input and display response
def answer():
    chats = "chats"
    if chats not in st.session_state:
        st.session_state[chats] = ["Hey! How can I help you?"]

    for i, chat in enumerate(st.session_state[chats]):
        if i % 2 == 0:
            st.chat_message("assistant").write(chat)
        else:
            st.chat_message("human").write(chat)

    question = user_input()

    if question:
        st.session_state[chats].append(question)
        st.chat_message("human").write(question)
        response = genaiAnswer(question)
        st.session_state[chats].append(response)
        st.chat_message("assistant").write_stream(writing(response))
        st.balloons()
        st.snow()

add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )


with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")

    with st.spinner("Loading..."):
        time.sleep(5)
    st.success("Done!")


if __name__ == "__main__":
    answer()
