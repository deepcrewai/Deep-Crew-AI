import streamlit as st
from utils import setup_page
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Starting Streamlit application...")
        print("Starting Streamlit application...", file=sys.stderr)

        setup_page()
        logger.info("Page setup completed")

        st.title("Deep Crew - Test Page")
        st.write("Bu bir test sayfasıdır.")
        logger.info("Basic content rendered")

        if st.button("Test Butonu"):
            st.success("Buton çalışıyor!")
            logger.info("Button clicked")
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    logger.info("Script started")
    main()
    logger.info("Script completed")