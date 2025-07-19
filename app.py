
"""
Chemical Engineering Bot - Streamlit Application
Main application file for the ChemE Bot with Gemini API integration
"""

import streamlit as st
import time
import os
import sys
from datetime import datetime

# Fix import path for Streamlit Cloud
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import bot components
from src.bot_engine import ChemEBot
from src.utils import validate_input

# Page configuration
st.set_page_config(
    page_title="ChemE Bot - Chemical Engineering Assistant",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Rest of your code continues here...


# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f4e79;
    text-align: center;
    margin-bottom: 2rem;
}

.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}

.user-message {
    background-color: #e3f2fd;
    border-left: 4px solid #2196f3;
}

.bot-message {
    background-color: #f1f8e9;
    border-left: 4px solid #4caf50;
}

.sidebar-info {
    background-color: #f5f5f5;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}

.error-message {
    background-color: #ffebee;
    color: #c62828;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #f44336;
}

.success-message {
    background-color: #e8f5e8;
    color: #2e7d32;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #4caf50;
}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'bot' not in st.session_state:
        st.session_state.bot = None
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'api_key_valid' not in st.session_state:
        st.session_state.api_key_valid = False
    
    if 'show_sources' not in st.session_state:
        st.session_state.show_sources = True
    
    if 'web_search_enabled' not in st.session_state:
        st.session_state.web_search_enabled = True

def setup_api_key():
    """Setup and validate API key"""
    try:
        # Try to get API key from Streamlit secrets
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        
        if not api_key:
            st.error("⚠️ Gemini API key not found in secrets. Please add GEMINI_API_KEY to your Streamlit secrets.")
            st.info("💡 For local development, add your API key to `.streamlit/secrets.toml`")
            return False
        
        # Initialize bot if not already done
        if st.session_state.bot is None:
            st.session_state.bot = ChemEBot(api_key)
            
        if st.session_state.bot.is_initialized:
            st.session_state.api_key_valid = True
            return True
        else:
            st.error("❌ Failed to initialize the AI bot. Please check your API key.")
            return False
            
    except Exception as e:
        st.error(f"❌ Error setting up API key: {str(e)}")
        return False

def display_header():
    """Display application header"""
    st.markdown('<h1 class="main-header">⚗️ ChemE Bot</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align: center; color: #666; font-size: 1.2rem;">Your AI-powered Chemical Engineering Assistant</p>',
        unsafe_allow_html=True
    )
    st.markdown("---")

def display_sidebar():
    """Display sidebar with controls and information"""
    with st.sidebar:
        st.header("🔧 Controls")
        
        # Settings
        st.session_state.web_search_enabled = st.checkbox(
            "🌐 Enable Web Search", 
            value=st.session_state.web_search_enabled,
            help="Include current information from the web in responses"
        )
        
        st.session_state.show_sources = st.checkbox(
            "📚 Show Sources", 
            value=st.session_state.show_sources,
            help="Display source information for responses"
        )
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            if st.session_state.bot:
                st.session_state.bot.clear_history()
            st.rerun()
        
        st.markdown("---")
        
        # Bot information
        st.header("ℹ️ About ChemE Bot")
        st.markdown("""
        <div class="sidebar-info">
        <strong>Capabilities:</strong>
        <ul>
        <li>Process design & optimization</li>
        <li>Unit operations calculations</li>
        <li>Thermodynamics & kinetics</li>
        <li>Safety protocols & HAZOP</li>
        <li>Equipment design & selection</li>
        <li>Current industry information</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Statistics
        if st.session_state.bot and st.session_state.chat_history:
            st.header("📊 Session Stats")
            stats = {
                'Questions Asked': len(st.session_state.chat_history),
                'Bot Responses': len([msg for msg in st.session_state.chat_history if msg['role'] == 'assistant'])
            }
            
            for key, value in stats.items():
                st.metric(key, value)
        
        # Example questions
        st.header("💡 Example Questions")
        example_questions = [
            "What is distillation and how does it work?",
            "How do I calculate reactor volume for a CSTR?",
            "What are the safety considerations for benzene?",
            "Explain the McCabe-Thiele method",
            "How do I size a heat exchanger?"
        ]
        
        for i, question in enumerate(example_questions):
            if st.button(f"📝 {question[:30]}...", key=f"example_{i}"):
                st.session_state.example_question = question
                st.rerun()

def display_chat_history():
    """Display chat conversation history"""
    if not st.session_state.chat_history:
        st.info("👋 Welcome! Ask me any chemical engineering question to get started.")
        return
    
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            with st.chat_message("user"):
                st.write(message['content'])
        
        elif message['role'] == 'assistant':
            with st.chat_message("assistant"):
                st.write(message['content'])
                
                # Show sources if enabled and available
                if (st.session_state.show_sources and 
                    'sources' in message and 
                    message['sources']):
                    
                    with st.expander("📚 Sources"):
                        for source in message['sources']:
                            st.write(f"• {source}")
                
                # Show metadata
                if 'metadata' in message:
                    metadata = message['metadata']
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if 'question_type' in metadata:
                            st.caption(f"Type: {metadata['question_type'].title()}")
                    
                    with col2:
                        if 'processing_time' in metadata:
                            st.caption(f"Time: {metadata['processing_time']:.1f}s")
                    
                    with col3:
                        if 'web_context_used' in metadata:
                            st.caption(f"Web: {'✅' if metadata['web_context_used'] else '❌'}")

def handle_user_input():
    """Handle user input and generate bot response"""
    # Check for example question
    if hasattr(st.session_state, 'example_question'):
        user_question = st.session_state.example_question
        delattr(st.session_state, 'example_question')
    else:
        # Get user input from chat input
        user_question = st.chat_input("Ask me anything about chemical engineering...")
    
    if user_question:
        # Add user message to chat history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_question,
            'timestamp': datetime.now()
        })
        
        # Display user message immediately
        with st.chat_message("user"):
            st.write(user_question)
        
        # Generate bot response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    # Get response from bot
                    response_data = st.session_state.bot.ask(
                        question=user_question,
                        include_web_search=st.session_state.web_search_enabled
                    )
                    
                    # Display response
                    st.write(response_data['answer'])
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response_data['answer'],
                        'sources': response_data.get('sources', []),
                        'metadata': {
                            'question_type': response_data.get('question_type', 'unknown'),
                            'processing_time': response_data.get('processing_time', 0),
                            'web_context_used': response_data.get('web_context_used', False)
                        },
                        'timestamp': datetime.now()
                    })
                    
                    # Show sources if enabled
                    if (st.session_state.show_sources and 
                        response_data.get('sources')):
                        
                        with st.expander("📚 Sources"):
                            for source in response_data['sources']:
                                st.write(f"• {source}")
                    
                    # Show processing info
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.caption(f"Type: {response_data.get('question_type', 'unknown').title()}")
                    with col2:
                        st.caption(f"Time: {response_data.get('processing_time', 0):.1f}s")
                    with col3:
                        web_used = response_data.get('web_context_used', False)
                        st.caption(f"Web: {'✅' if web_used else '❌'}")
                
                except Exception as e:
                    error_msg = f"❌ Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    
                    # Add error to chat history
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': error_msg,
                        'timestamp': datetime.now()
                    })

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Setup API key and bot
    if not setup_api_key():
        st.stop()
    
    # Display success message when bot is ready
    if st.session_state.api_key_valid and st.session_state.bot:
        st.success("🤖 ChemE Bot is ready! Ask me any chemical engineering question.")
    
    # Create two columns: main chat and sidebar
    display_sidebar()
    
    # Main chat area
    with st.container():
        # Display chat history
        display_chat_history()
        
        # Handle user input
        handle_user_input()

if __name__ == "__main__":
    main()
