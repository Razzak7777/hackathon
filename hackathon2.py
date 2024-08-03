import requests
import streamlit as st
import json

# Set up API endpoint and key directly in the code
API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "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"  # Replace with your actual API key

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Initialize the session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Function to send messages to the Llama 3 API and receive a response
def call_llama_api(messages):
    payload = {
        "model": "llama3-8b-8192",
        "messages": messages
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Sidebar with a button to clear chat history
with st.sidebar:
    if st.button("Clear Chat History"):
        st.session_state["messages"] = []

# Display the chat title
st.title("CODER AI 🤖")

# Style for user messages in a green box
user_message_style = """
    <style>
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 10px;
    }
    .user-message .message {
        background-color: #e1ffc7;  /* Light green background */
        color: #000;
        border-radius: 8px;
        padding: 8px;
        max-width: 60%;
        margin-right: 10px;
        word-wrap: break-word;
    }
    </style>
"""
st.markdown(user_message_style, unsafe_allow_html=True)

# Emojis
user_emoji = "🧑‍💻"  # Replace with your preferred emoji for the user
assistant_emoji = "🤖"  # Replace with your preferred emoji for the assistant

# Iterate over the messages and display them in the chat interface
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f'<div class="user-message"><div class="message"><strong>{user_emoji}</strong> {message["content"]}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        # Handle code formatting for assistant's response
        if "" in message["content"]:
            st.markdown(
                f'<div style="text-align: left; margin-bottom: 10px;"><strong>{assistant_emoji}</strong></div>',
                unsafe_allow_html=True,
            )
            st.code(message["content"].strip(''), language='python')  # Assuming the response is Python code
        else:
            st.markdown(
                f'<div style="text-align: left; margin-bottom: 10px;"><strong>{assistant_emoji}</strong> {message["content"]}</div>',
                unsafe_allow_html=True,
            )

# Input field for user to enter a message
if user_input := st.chat_input("Ask me anything!"):
    # Add the user's input to the session state
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display the user's input immediately in a green box
    st.markdown(
        f'<div class="user-message"><div class="message"><strong>{user_emoji}</strong> {user_input}</div></div>',
        unsafe_allow_html=True,
    )

    # Call the Llama 3 API
    try:
        response = call_llama_api(st.session_state.messages)
        assistant_response = response["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

        # Display the assistant's response
        # Check if the assistant's response contains code
        if "" in assistant_response:
            code_snippet = assistant_response.split("")[1]  # Extract the code block
            st.markdown(
                f'<div style="text-align: left; margin-bottom: 10px;"><strong>{assistant_emoji}</strong></div>',
                unsafe_allow_html=True,
            )
            st.code(code_snippet, language='python')  # Assuming the response is Python code
        else:
            st.markdown(
                f'<div style="text-align: left; margin-bottom: 10px;"><strong>{assistant_emoji}</strong> {assistant_response}</div>',
                unsafe_allow_html=True,
            )
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
    except KeyError:
        st.error("Unexpected response structure from API.")
