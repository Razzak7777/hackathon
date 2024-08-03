import requests
import streamlit as st
import webbrowser

# Set up API endpoint and key directly in the code
API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "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"  # Replace with your actual API key

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Function to open YouTube links
def open_youtube_link(query):
    youtube_links = {
        "8 science youtube": "https://www.youtube.com/watch?v=DqtUDWW1x6c",
        "python youtube": "https://www.youtube.com/watch?v=vLqTf2b6GZw",
        "8 maths youtube ": "https://www.youtube.com/watch?v=2AmldBXnzvY&list=PLVLoWQFkZbhUPr3lid5ATpymNOAfpk9-c",
        "c language youtube": "https://www.youtube.com/watch?v=irqbmMNs2Bo",
        "python english youtube": "https://www.youtube.com/watch?v=XKHEtdqhLK8",
        "10th  maths youtube": "https://www.youtube.com/watch?v=mDa3R4StLkw&list=PLAODbdRxgpSMs4q0cidru2ajfxoPR44vJ",
        "10th science youtube": "https://www.youtube.com/watch?v=uuYN1M3ZGpY",
        "class 11th youtube": "https://www.youtube.com/watch?v=etykWjsMF7s&list=PLVLoWQFkZbhWF3ezaGYnkCKE0hHPaSbLO",
        "class 11th physics youtube": "https://www.youtube.com/watch?v=yF291D4XcMo&list=PLVLoWQFkZbhXCEo76NKI0C46ROnlSz7XE",
        "class 11th chemistry youtube": "https://www.youtube.com/watch?v=0mmxbFf05mI&list=PLCzaIJYXP5YcTsTTgbgCrcV2CYTFonHbE",
        "class 12th chemistry youtube": "https://www.youtube.com/watch?v=4PedE2KTCww&list=PLVLoWQFkZbhV5bQRjcJc9XDh_ekff6Xb3",
        "class 12th maths youtube": "https://www.youtube.com/watch?v=23a3rrNWmJ8&list=PLVLoWQFkZbhU5r5DlfxPc3gKw-QLLAvLn",
        "class 12th physicsyoutube": "https://www.youtube.com/watch?v=axedPR8TLa0&list=PLVLoWQFkZbhV-wpC6Z6bUWz9m3itDKmYe"
    }
    
    for key in youtube_links:
        if key in query.lower():
            webbrowser.open(youtube_links[key])
            return f"Opening YouTube link for {key}"
    
    return "No matching YouTube link found."

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
st.title("<EDUCATION AI>")

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

    # Check if the query is related to YouTube links
    youtube_response = open_youtube_link(user_input)
    if "Opening YouTube link" in youtube_response:
        st.session_state.messages.append({"role": "assistant", "content": youtube_response})

        # Display the assistant's response
        st.markdown(
            f'<div style="text-align: left; margin-bottom: 10px;"><strong>{assistant_emoji}</strong> {youtube_response}</div>',
            unsafe_allow_html=True,
        )
    else:
        # Call the Llama 3 API
        try:
            response = call_llama_api(st.session_state.messages)
            assistant_response = response["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            # Display the assistant's response
            st.markdown(
                f'<div style="text-align: left; margin-bottom: 10px;"><strong>{assistant_emoji}</strong> {assistant_response}</div>',
                unsafe_allow_html=True,
            )
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
        except KeyError:
            st.error("Unexpected response structure from API.")
