import streamlit as st
import requests
import json
import base64
 
 
# Custom CSS for better appearance
def apply_custom_css():
    st.markdown("""
<style>
        /* Main container styling */
        .main {
            background-color: #f8f9fa;
            padding: 20px;
        }
        /* Header styling */
        .title-container {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .app-title {
            color: #2c3e50;
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0;
        }
        .app-subtitle {
            color: #7f8c8d;
            font-size: 1.1rem;
            font-weight: 400;
        }
        /* Chat message styling */
        .user-message {
            background-color: #e3f2fd;
            border-left: 5px solid #2196f3;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .assistant-message {
            background-color: #f1f8e9;
            border-left: 5px solid #8bc34a;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        /* Button styling */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px 15px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        /* Chat input styling */
        .stTextInput>div>div>input {
            border-radius: 20px;
            padding: 10px 15px;
            border: 1px solid #ddd;
        }
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #f0f2f6;
            padding: 20px 10px;
        }
        /* Info box styling */
        .stAlert {
            border-radius: 8px;
        }
</style>
    """, unsafe_allow_html=True)
 
# Set page configuration
st.set_page_config(
    page_title="ComponentCortex - Electronic Components Assistant",
    page_icon="🔌",
    layout="wide"
)
 
# Apply custom CSS
apply_custom_css()
 
# App header with logo
st.markdown("""
<div class="title-container">
<div style="margin-right: 20px;">
<img src="https://img.icons8.com/fluency/96/electronics.png" width="60" />
</div>
<div>
<h1 class="app-title">ComponentCortex</h1>
<p class="app-subtitle">Your Electronic Components Assistant</p>
</div>
</div>
""", unsafe_allow_html=True)
# Initialize chat history in session state if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []
# API Gateway URL - replace with your actual endpoint
API_ENDPOINT = "https://ks8u4ml2wj.execute-api.us-west-2.amazonaws.com/prod"
 
# Create a container for the chat history with a subtle background
chat_container = st.container()
with chat_container:
    # Display chat history with improved styling
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
<div class="user-message">
<strong>You:</strong><br>
                {message["content"]}
</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div class="assistant-message">
<strong>ComponentCortex:</strong><br>
                {message["content"]}
</div>
            """, unsafe_allow_html=True)
# Input for user question with improved styling
st.markdown("<br>", unsafe_allow_html=True)
prompt = st.chat_input("What would you like to know about electronic components?")
 
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message with custom styling
    with chat_container:
        st.markdown(f"""
<div class="user-message">
<strong>You:</strong><br>
            {prompt}
</div>
        """, unsafe_allow_html=True)
    # Display assistant response with a spinner while loading
    with chat_container:
        with st.spinner("ComponentCortex is thinking..."):
            try:
                # Call the API Gateway endpoint
                response = requests.get(
                    API_ENDPOINT,
                    params={"query": prompt},
                    timeout=30
                )
                if response.status_code == 200:
                    result = response.json()
                    # Extract the answer from the response
                    full_response = result.get("answer", "I couldn't find information about that.")
                else:
                    full_response = f"Error: Received status code {response.status_code}"
            except Exception as e:
                full_response = f"Error: {str(e)}"
        # Display the full response with custom styling
        st.markdown(f"""
<div class="assistant-message">
<strong>ComponentCortex:</strong><br>
            {full_response}
</div>
        """, unsafe_allow_html=True)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
# Enhanced sidebar with information
with st.sidebar:
    # Add logo to sidebar
    st.image("https://img.icons8.com/fluency/96/electronics.png", width=80)
    st.markdown("### About ComponentCortex")
    st.info("""
    This intelligent chatbot uses Amazon Bedrock to provide detailed information about electronic components. 
    Ask questions about:
    - Resistors, capacitors, transistors
    - Circuit design principles
    - Component specifications
    - Troubleshooting advice
    """)
    st.markdown("---")
    # System status indicator
    st.markdown("### System Status")
    st.markdown("✅ Connected to Amazon Bedrock")
    st.markdown("✅ API Gateway Online")
    st.markdown("---")
    # Chat controls
    st.markdown("### Chat Controls")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    # Export chat option if there are messages
    if st.session_state.messages:
        if st.button("📥 Export Conversation"):
            chat_export = ""
            for msg in st.session_state.messages:
                prefix = "You: " if msg["role"] == "user" else "ComponentCortex: "
                chat_export += f"{prefix}{msg['content']}\n\n"
            # Create a download link
            b64 = base64.b64encode(chat_export.encode()).decode()
            href = f'<a href="data:text/plain;base64,{b64}" download="componentcortex_chat.txt">Download chat history</a>'
            st.markdown(href, unsafe_allow_html=True)
    st.markdown("---")
    # Footer
    st.markdown("##### © 2025 ComponentCortex")
    st.markdown("AWS Hackathon Edition")