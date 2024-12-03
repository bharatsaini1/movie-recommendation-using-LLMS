import streamlit as st
from groq import Groq

# App title and configuration
st.set_page_config(page_title="🎬 Movie Chatbot", page_icon="🎥", layout="centered")
st.title("🎬 Movie Chatbot")

# Predefined Groq API key (replace with your actual API key)
GROQ_API_KEY = "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"

# System prompt for the chatbot
movie_prompt = (
    "You are a chatbot that only talks about movies. "
    "Answer the user's questions about movies, provide movie recommendations, trivia, or anything related to movies."
)

# Initialize conversation history in session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = [{"role": "system", "content": movie_prompt}]

# Function to interact with the Groq API
def generate_response(user_message):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        chat_completion = client.chat.completions.create(
            messages=st.session_state.conversation_history,
            model="llama3-8b-8192",
        )
        response = chat_completion.choices[0].message.content
        return response
    except Exception as e:
        return f"Error: {e}"

# Chat history display
st.markdown("### Chat Conversation")
with st.container():
    for message in st.session_state.conversation_history[1:]:  # Skip system prompt
        if message["role"] == "user":
            st.chat_message("user").markdown(f"**You**: {message['content']}")
        else:
            st.chat_message("assistant").markdown(f"**Bot**: {message['content']}")

# Separator for UI
st.markdown("---")

# User input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "Enter your message:",
        placeholder="Ask about movies, recommendations, or trivia!",
    )
    submitted = st.form_submit_button("Send")

    if submitted and user_input.strip():
        # Add user input to the conversation history
        st.session_state.conversation_history.append({"role": "user", "content": user_input})

        # Generate and add the bot response to the conversation history
        bot_response = generate_response(user_input)
        st.session_state.conversation_history.append({"role": "assistant", "content": bot_response})

        # No explicit rerun required; Streamlit handles it automatically
