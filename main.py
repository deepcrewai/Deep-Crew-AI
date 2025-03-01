import streamlit as st
from utils import setup_page
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def init_session_state():
    """Initialize session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        logger.info("Session state initialized")

def main():
    try:
        # Initialize session state
        init_session_state()

        # Setup page configuration
        setup_page()

        # Main content
        st.markdown("""
            <div class="main-container">
                <div class="logo-title">DEEP CREW</div>
                <h1 class="main-header">Research & Innovation Hub</h1>
                <p class="subtitle">
                    Discover insights, analyze patents, and explore funding opportunities with AI-powered research tools
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.write("Application is running successfully!")
        logger.info("Main content rendered successfully")

    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        logger.info("Starting application...")
        main()
    except Exception as e:
        logger.error(f"Critical error: {str(e)}", exc_info=True)
        st.error("A critical error occurred. Please check the logs for details.")