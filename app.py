import streamlit as st

# Title of the app
st.title('BuddyBot Health Chatbot')

# Description
st.write('AI-powered responses for health queries.')

# Chat function
def chat_with_buddybot(user_input):
    # Here you would integrate your AI model or logic
t    # For demonstration, we will return a static response.
    return "BuddyBot: How can I assist you with your health today?"

# User input
user_input = st.text_input('You:', '')

if user_input:
    response = chat_with_buddybot(user_input)
    st.write(response)
