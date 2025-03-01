import streamlit as st
import plotly.express as px
from utils import setup_page
import logging
import sys
from api_client import OpenAlexClient
from ai_analyzer import AIAnalyzer
from patent_client import PatentSearchClient
from components import (
    render_search_section, 
    render_analysis_section,
    render_patent_results,
    render_combined_results
)
from funding import render_funding_section

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

def reset_app():
    """Reset all session state variables"""
    try:
        for key in ['selected_stages', 'search_results', 'analysis', 'last_query', 
                    'patent_results', 'patent_analysis', 'combined_analysis']:
            if key in st.session_state:
                del st.session_state[key]
        logger.info("App state reset successfully")
    except Exception as e:
        logger.error(f"Error resetting app state: {str(e)}")

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

        # Add reset button
        col_search, col_reset = st.columns([6, 1])

        with col_search:
            search_query = st.text_input(
                "Search",
                placeholder="Enter your research topic...",
                help="Type your research query here",
                label_visibility="collapsed"
            )

        with col_reset:
            if st.button("🔄 Reset", help="Reset search and selected stages"):
                reset_app()
                st.rerun()

        if 'selected_stages' not in st.session_state:
            st.session_state.selected_stages = set()

        # Create stage buttons using columns for horizontal layout
        col1, col2, col3, col4, col5 = st.columns(5)

        stages = {
            'research': 'Litarature',
            'patents': 'Patent',
            'funding': 'Funding',
            'network': 'Collabration',
            'compliance': 'Legal'
        }

        columns = [col1, col2, col3, col4, col5]

        for idx, (stage_key, label) in enumerate(stages.items()):
            with columns[idx]:
                is_selected = stage_key in st.session_state.selected_stages
                if st.button(
                    label,
                    key=f"btn_{stage_key}",
                    help=f"Click to select {label}",
                    use_container_width=True,
                    type="secondary" if is_selected else "primary"
                ):
                    if stage_key in st.session_state.selected_stages:
                        st.session_state.selected_stages.remove(stage_key)
                    else:
                        st.session_state.selected_stages.add(stage_key)
                    st.rerun()

        selected_stages = list(st.session_state.selected_stages)

        # Create tabs for selected stages if we have a search query
        if search_query:
            if not selected_stages:
                st.warning("Please select at least one research stage to proceed.")
                return

            # Only add Results tab if more than one stage is selected
            if len(selected_stages) > 1:
                selected_stages.append("results")

            # Create tabs
            tabs = st.tabs([stage.capitalize() for stage in selected_stages])

            for idx, tab in enumerate(tabs):
                with tab:
                    try:
                        if selected_stages[idx] == "research":
                            with st.spinner("🔍 Analyzing..."):
                                openalex_client = OpenAlexClient()
                                ai_analyzer = AIAnalyzer()

                                if search_query != st.session_state.get('last_query', ''):
                                    keywords = ai_analyzer.generate_search_keywords(search_query)
                                    results = openalex_client.search(query=search_query, keywords=keywords)

                                    if results:
                                        st.session_state.search_results = results
                                        st.session_state.analysis = ai_analyzer.analyze_results(results)
                                        st.session_state.last_query = search_query
                                    else:
                                        st.warning("No results found. Try different terms.")
                                        st.session_state.search_results = None
                                        st.session_state.analysis = None

                                if st.session_state.get('search_results'):
                                    render_search_section(st.session_state.search_results)
                                    render_analysis_section(st.session_state.analysis)

                        elif selected_stages[idx] == "patents":
                            with st.spinner("🔍 Searching patents..."):
                                patent_client = PatentSearchClient()
                                if search_query != st.session_state.get('last_query', '') or st.session_state.get('patent_results') is None:
                                    patent_results = patent_client.search_patents(search_query)
                                    if patent_results:
                                        st.session_state.patent_results = patent_results
                                        with st.spinner("🤖 Analyzing patents..."):
                                            st.session_state.patent_analysis = patent_client.analyze_patents(patent_results)
                                    else:
                                        st.warning("No patent results found.")
                                        st.session_state.patent_results = None
                                        st.session_state.patent_analysis = None

                                if st.session_state.get('patent_results'):
                                    render_patent_results(st.session_state.patent_results, st.session_state.patent_analysis)

                        elif selected_stages[idx] == "funding":
                            render_funding_section(search_query)

                        elif selected_stages[idx] == "network":
                            st.info("🔄 Coming Soon")

                        elif selected_stages[idx] == "compliance":
                            st.info("✓ Coming Soon")

                        elif selected_stages[idx] == "results":
                            if not st.session_state.get('combined_analysis'):
                                st.session_state.combined_analysis = {}

                            render_combined_results(
                                st.session_state.get('search_results') or [],
                                st.session_state.get('patent_results') or [],
                                st.session_state.combined_analysis
                            )

                    except Exception as e:
                        logger.error(f"Error in tab {selected_stages[idx]}: {str(e)}")
                        st.error(f"An error occurred in {selected_stages[idx]} tab: {str(e)}")

        else:
            st.info("Please choose below your agents.")

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