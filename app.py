import streamlit as st

import os
from datetime import datetime

import json

# Load environment variables


# Configure OpenAI
api_key = os.getenv('OPENAI_API_KEY')

# Page configuration
st.set_page_config(
    page_title="BuddyBot - Health Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px;
        font-weight: bold;
    }
    .stButton > button:hover {
        transform: scale(1.05);
    }
    .chat-message {
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .user-message {
        background-color: #e3f2fd;
        text-align: right;
    }
    .bot-message {
        background-color: #f3e5f5;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "api_calls" not in st.session_state:
    st.session_state.api_calls = 0

if "tokens_used" not in st.session_state:
    st.session_state.tokens_used = 0

# Sidebar Configuration
with st.sidebar:
    st.title("⚙️ BuddyBot Settings")
    st.divider()
    
    # API Key Input
    st.subheader("🔑 API Configuration")
    api_key_input = st.text_input("Enter  API Key", type="password", value=openai.api_key or "")
    
    if api_key_input:
        openai.api_key = api_key_input
        st.success("✅ API Key configured!")
    else:
        st.warning("⚠️ No API Key provided. Please enter your OpenAI API key.")
    
    st.divider()
    
    # Model Selection
    st.subheader("🎯 Model Settings")
    model = st.selectbox(
        "Select AI Model",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
        help="GPT-3.5 is faster and cheaper. GPT-4 is more intelligent."
    )
    
    # Temperature Control
    temperature = st.slider(
        "Temperature (Creativity)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Lower = more focused, Higher = more creative"
    )
    
    # Max Tokens
    max_tokens = st.slider(
        "Max Response Length",
        min_value=100,
        max_value=2000,
        value=500,
        step=100
    )
    
    st.divider()
    
    # System Prompt
    st.subheader("📝 System Prompt")
    system_prompt = st.text_area(
        "Customize BuddyBot's behavior:",
        value="""You are BuddyBot, a friendly and knowledgeable AI health assistant. Your role is to:
1. Provide reliable health tips and wellness advice
2. Explain health concepts in simple, easy-to-understand language
3. Encourage healthy lifestyle choices
4. Always remind users to consult healthcare professionals for medical emergencies
5. Be empathetic and supportive in your responses
6. Focus on preventive health and wellness

Important: Do NOT provide medical diagnosis or treatment plans. Always recommend consulting a doctor.""",
        height=150
    )
    
    st.divider()
    
    # Statistics
    st.subheader("📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("API Calls", st.session_state.api_calls)
    with col2:
        st.metric("Messages", len(st.session_state.messages))
    
    st.divider()
    
    # Clear Chat
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.success("Chat cleared!")
            st.rerun()
    
    with col2:
        if st.button("📥 Export Chat"):
            chat_json = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button(
                label="Download JSON",
                data=chat_json,
                file_name=f"buddybot_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

# Main Content
st.title("🤖 BuddyBot - Your AI Health Assistant")
st.markdown("💬 Get personalized health tips, wellness advice, and health-related information")

# Health Tips Section
with st.expander("💡 Quick Health Tips", expanded=False):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**💧 Hydration**\nDrink 8-10 glasses of water daily for optimal health.")
    
    with col2:
        st.success("**🏃 Exercise**\nGet 30 minutes of physical activity daily.")
    
    with col3:
        st.warning("**😴 Sleep**\nAim for 7-9 hours of quality sleep every night.")

st.divider()

# Chat Display
st.subheader("💬 Chat History")

# Display all messages
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.write(message["content"])

# Chat Input
st.divider()
st.subheader("🎤 Send Your Message")

user_input = st.chat_input(
    "Ask me about health, wellness, fitness, nutrition, mental health...",
    key="user_input"
)

if user_input and openai.api_key:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({
        "timestamp": datetime.now().isoformat(),
        "role": "user",
        "content": user_input
    })
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
    
    # Generate bot response
    try:
        with st.spinner("🤔 BuddyBot is thinking..."):
            # Prepare messages for API
            messages_for_api = [
                {"role": "system", "content": system_prompt}
            ] + st.session_state.messages
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages_for_api,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.9,
                frequency_penalty=0.0,
                presence_penalty=0.6
            )
        
        # Extract bot response
        bot_response = response.choices[0].message.content
        
        # Add to session state
        st.session_state.messages.append({
            "role": "assistant",
            "content": bot_response
        })
        
        st.session_state.chat_history.append({
            "timestamp": datetime.now().isoformat(),
            "role": "assistant",
            "content": bot_response,
            "model": model,
            "tokens_used": response.usage.total_tokens
        })
        
        st.session_state.api_calls += 1
        st.session_state.tokens_used += response.usage.total_tokens
        
        # Display bot response
        with st.chat_message("assistant", avatar="🤖"):
            st.write(bot_response)
        
        # Show usage info
        with st.expander("📊 API Usage Info"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Model Used", model)
            with col2:
                st.metric("Tokens Used", response.usage.total_tokens)
            with col3:
                st.metric("Total Session Tokens", st.session_state.tokens_used)
    
    except openai.error.AuthenticationError:
        st.error("❌ Invalid API Key. Please check your OpenAI API key.")
    except openai.error.RateLimitError:
        st.error("⚠️ Rate limit exceeded. Please try again later.")
    except openai.error.APIError as e:
        st.error(f"❌ API Error: {str(e)}")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

elif user_input and not openai.api_key:
    st.warning("⚠️ Please enter your OpenAI API key in the sidebar to use BuddyBot")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; margin-top: 20px;'>
    <p><strong>BuddyBot v1.0</strong> | Powered by OpenAI | Built with Streamlit</p>
    <p><em>⚠️ Disclaimer: BuddyBot provides general health information. Always consult healthcare professionals for medical advice.</em></p>
</div>
""", unsafe_allow_html=True)
