import streamlit as st
import plotly.express as px
from utils import setup_page
import logging
import sys
from api_client import OpenAlexClient
from ai_analyzer import AIAnalyzer
from patent_client import PatentSearchClient
from components import (render_search_section, render_analysis_section,
                        render_patent_results, render_combined_results,
                        render_network_section)
from funding import render_funding_section

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def init_session_state():
    """Initialize session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        logger.info("Session state initialized")


def reset_app():
    """Reset all session state variables"""
    try:
        for key in [
                'selected_stages', 'search_results', 'analysis', 'last_query',
                'patent_results', 'patent_analysis', 'combined_analysis', 'funding_data'
        ]:
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
        """,
                    unsafe_allow_html=True)

        # Add reset button
        col_search, col_reset = st.columns([6, 1])

        with col_search:
            search_query = st.text_input(
                "Search",
                placeholder="Enter your research topic...",
                help="Type your research query here",
                label_visibility="collapsed")

        with col_reset:
            if st.button("🔄 Reset", help="Reset search and selected stages"):
                reset_app()
                st.rerun()

        if 'selected_stages' not in st.session_state:
            st.session_state.selected_stages = set()

        # Create stage buttons using columns for horizontal layout
        col1, col2, col3, col4, col5 = st.columns(5)

        stages = {
            'research': 'Research',
            'patents': 'Patents',
            'funding': 'Funding',
            'network': 'Network',
            'compliance': 'Legal'
        }

        columns = [col1, col2, col3, col4, col5]

        for idx, (stage_key, label) in enumerate(stages.items()):
            with columns[idx]:
                is_selected = stage_key in st.session_state.selected_stages
                if st.button(label,
                             key=f"btn_{stage_key}",
                             help=f"Click to select {label}",
                             use_container_width=True,
                             type="secondary" if is_selected else "primary"):
                    if stage_key in st.session_state.selected_stages:
                        st.session_state.selected_stages.remove(stage_key)
                    else:
                        st.session_state.selected_stages.add(stage_key)
                    st.rerun()

        selected_stages = list(st.session_state.selected_stages)

        # Create tabs for selected stages if we have a search query
        if search_query:
            if not selected_stages:
                st.warning(
                    "Please select at least one research stage to proceed.")
                return

            # Only add Results tab if more than one stage is selected
            if len(selected_stages) > 1:
                selected_stages.append("results")  # Add results tab last

            # Create tabs
            tabs = st.tabs([
                stages.get(stage, stage.capitalize())  # Get stage name from stages dict or capitalize
                for stage in selected_stages
            ])

            for idx, tab in enumerate(tabs):
                with tab:
                    try:
                        current_stage = selected_stages[idx]  # Get current stage

                        if current_stage == "research":
                            with st.spinner("🔍 Analyzing Research..."):
                                openalex_client = OpenAlexClient()
                                ai_analyzer = AIAnalyzer()

                                if search_query != st.session_state.get(
                                        'last_query', ''):
                                    keywords = ai_analyzer.generate_search_keywords(
                                        search_query)
                                    results = openalex_client.search(
                                        query=search_query, keywords=keywords)

                                    if results:
                                        st.session_state.search_results = results
                                        st.session_state.analysis = ai_analyzer.analyze_results(
                                            results)
                                        st.session_state.last_query = search_query
                                    else:
                                        st.warning(
                                            "No results found. Try different terms."
                                        )
                                        st.session_state.search_results = None
                                        st.session_state.analysis = None

                                # Create sub-tabs for Documents and AI Analysis
                                doc_tab, analysis_tab = st.tabs(
                                    ["Documents", "AI Analysis"])

                                if st.session_state.get('search_results'):
                                    with doc_tab:
                                        render_search_section(
                                            st.session_state.search_results)
                                    with analysis_tab:
                                        render_analysis_section(
                                            st.session_state.analysis, section_type="research")

                        elif current_stage == "patents":
                            with st.spinner("🔍 Searching patents..."):
                                patent_client = PatentSearchClient()
                                if search_query != st.session_state.get(
                                        'last_query',
                                        '') or st.session_state.get(
                                            'patent_results') is None:
                                    patent_results = patent_client.search_patents(
                                        search_query)
                                    if patent_results:
                                        st.session_state.patent_results = patent_results
                                        with st.spinner(
                                                "🤖 Analyzing patents..."):
                                            st.session_state.patent_analysis = patent_client.analyze_patents(
                                                patent_results)
                                    else:
                                        st.warning("No patent results found.")
                                        st.session_state.patent_results = None
                                        st.session_state.patent_analysis = None

                                # Create sub-tabs for Documents and AI Analysis
                                patent_tab, analysis_tab = st.tabs(
                                    ["Documents", "AI Analysis"])

                                with patent_tab:
                                    if st.session_state.get('patent_results'):
                                        render_patent_results(
                                            st.session_state.patent_results,
                                            st.session_state.patent_analysis,
                                            context="standalone")

                                with analysis_tab:
                                    if st.session_state.get('patent_analysis'):
                                        render_analysis_section(
                                            st.session_state.patent_analysis,
                                            section_type="patent_standalone")

                        elif current_stage == "funding":
                            if 'funding_data' not in st.session_state:
                                from funding import FundingAgent  # Import the correct class
                                funding_agent = FundingAgent()  # Use FundingAgent instead of FundingClient
                                st.session_state.funding_data = funding_agent.get_funding_opportunities(search_query)
                            render_funding_section(search_query, st.session_state.funding_data)

                        elif current_stage == "network":
                            render_network_section(st.session_state.get('search_results', []))

                        elif current_stage == "compliance":
                            st.info("✓ Coming Soon")

                        elif current_stage == "results":
                            if not st.session_state.get('combined_analysis'):
                                # Get AI analyzer instance
                                ai_analyzer = AIAnalyzer()

                                # Collect all available data
                                research_data = st.session_state.get('search_results') or []
                                patent_data = st.session_state.get('patent_results') or []
                                funding_data = st.session_state.get('funding_data', {})

                                # Extract network data
                                network_data = []
                                if research_data:
                                    network_data = [
                                        {
                                            'author': authorship.get('author', {}).get('display_name'),
                                            'orcid': authorship.get('author', {}).get('orcid'),
                                            'institution': authorship.get('institutions', [{}])[0].get('display_name')
                                        }
                                        for paper in research_data
                                        for authorship in paper.get('authorships', [])
                                    ]

                                # Generate combined analysis
                                st.session_state.combined_analysis = ai_analyzer.analyze_combined_results(
                                    research_data,
                                    patent_data,
                                    funding_data,
                                    network_data
                                )

                            # Render combined results
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
        st.error(
            "A critical error occurred. Please check the logs for details.")