import streamlit as st
from utils import setup_page
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        setup_page()

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

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        logger.info("Starting application...")
        main()
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")