import streamlit as st
import plotly.express as px
from utils import setup_page
import logging
import sys
from api_client import OpenAlexClient
from ai_analyzer import AIAnalyzer
from patent_client import PatentSearchClient
from components import (render_search_section, render_analysis_section,
                        render_patent_results, render_network_section,
                        render_synthesis_section)

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
        st.session_state.warning_message = "Choose Your Agent"
        st.session_state.progress = 0
        st.session_state.show_game = False
        logger.info("Session state initialized")

def reset_app():
    """Reset all session state variables"""
    try:
        for key in [
                'selected_stages', 'search_results', 'analysis', 'last_query',
                'patent_results', 'patent_analysis', 'funding_data', 'progress', 'show_game'
        ]:
            if key in st.session_state:
                del st.session_state[key]
        logger.info("App state reset successfully")
    except Exception as e:
        logger.error(f"Error resetting app state: {str(e)}")

def show_loading_game():
    """Show loading game in a modal while processing"""
    st.markdown("""
        <style>
        .loading-modal {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 9999;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
            width: 80%;
            max-width: 800px;
            height: 80vh;
        }
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.2);
            z-index: 9998;
            cursor: pointer;
        }
        .close-button {
            position: absolute;
            top: 10px;
            right: 10px;
            cursor: pointer;
            font-size: 24px;
            color: #666;
            background: none;
            border: none;
            padding: 5px;
        }
        .close-button:hover {
            color: #333;
        }
        iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
        </style>
        <div class="modal-overlay" onclick="closeModal()"></div>
        <div class="loading-modal">
            <button class="close-button" onclick="closeModal()">×</button>
            <iframe src="https://deep-crew.ai/game/" allow="fullscreen"></iframe>
        </div>
        <script>
        function closeModal() {
            const modal = document.querySelector('.loading-modal');
            const overlay = document.querySelector('.modal-overlay');
            if (modal) modal.style.display = 'none';
            if (overlay) overlay.style.display = 'none';
        }
        </script>
    """, unsafe_allow_html=True)

def main():
    try:
        # Initialize session state
        init_session_state()

        # Setup page configuration
        setup_page()

        # Main content
        st.markdown("""
            <style>
            div.stAlert {
                text-align: center;
                max-width: 750px;
                margin: 1rem auto;
            }
            </style>
            <div class="main-container">
                <div class="logo-container" style="text-align: center; width: 100%;">
                    <img src="https://deep-crew.ai/wp-content/uploads/2025/03/9128379182739812873.png" 
                         alt="Deep Crew Logo" 
                         style="max-width: 350px; height: auto; margin: 30px auto;">
                </div>
            </div>
        """,
                    unsafe_allow_html=True)

        # Add search section
        col_search, col_button = st.columns([6, 1])

        with col_search:
            search_query = st.text_input(
                "Search",
                placeholder="Enter your research topic...",
                help="Type your research query here",
                label_visibility="collapsed")

        with col_button:
            search_clicked = st.button("Search", help="Start searching with selected stages", use_container_width=True)

        if 'selected_stages' not in st.session_state:
            st.session_state.selected_stages = set()

        # Add progress bar
        if search_query or search_clicked:
            progress_bar = st.progress(st.session_state.progress)
            if st.session_state.progress < 1.0:
                # Add game button under progress bar
                if st.button("Analysis in Progress... But No Need to Get Bored! 🎮"):
                    st.session_state.show_game = True
                    show_loading_game()



        # Display dynamic warning/info message
        st.info(st.session_state.warning_message)

        # Create stage buttons using columns for horizontal layout
        col1, col2, col3, col4, col5 = st.columns(5)

        stages = {
            'research': 'Research',
            'patents': 'Patents',
            'funding': 'Funding',
            'collaboration': 'Collaboration',
            'compliance': 'Legal'
        }

        columns = [col1, col2, col3, col4, col5]

        # Synthesis otomatik seçim kontrolü
        visible_stages = ['research', 'patents', 'funding', 'collaboration', 'compliance']
        selected_count = len([stage for stage in visible_stages if stage in st.session_state.selected_stages])

        # En az 2 modül seçiliyse synthesis'i otomatik ekle
        if selected_count >= 2 and 'synthesis' not in st.session_state.selected_stages:
            st.session_state.selected_stages.add('synthesis')
        # 2'den az modül seçiliyse synthesis'i kaldır
        elif selected_count < 2 and 'synthesis' in st.session_state.selected_stages:
            st.session_state.selected_stages.remove('synthesis')

        # Görünür butonları oluştur
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
        if search_query or search_clicked:  # Added search_clicked condition
            if not selected_stages:
                st.session_state.warning_message = "Please select at least one research stage to proceed."
                return

            # Reset progress at the start of new search
            st.session_state.progress = 0
            progress_bar.progress(st.session_state.progress)

            # Calculate progress step based on number of selected stages
            progress_step = 1.0 / (len(selected_stages) + 1)  # +1 for initial setup

            # Update progress for search initialization
            st.session_state.progress += progress_step
            progress_bar.progress(st.session_state.progress)

            # Sort stages in the desired order
            ordered_stages = []
            preferred_order = ['research', 'patents', 'funding', 'collaboration', 'synthesis', 'compliance']

            # First add stages in preferred order if they are selected
            for stage in preferred_order:
                if stage in selected_stages:
                    ordered_stages.append(stage)

            # Create tabs with the ordered stages
            tabs = st.tabs([stages.get(stage, stage.capitalize()) if stage != 'synthesis' else 'Synthesis'
                            for stage in ordered_stages])

            # Process each tab
            for idx, tab in enumerate(tabs):
                with tab:
                    try:
                        current_stage = ordered_stages[idx]  # Use ordered_stages here

                        if current_stage == "research":
                            with st.spinner("Analyzing Research..."):
                                openalex_client = OpenAlexClient()
                                ai_analyzer = AIAnalyzer()

                                if (search_query != st.session_state.get('last_query', '') or
                                        'search_results' not in st.session_state):
                                    try:
                                        keywords = ai_analyzer.generate_search_keywords(search_query)
                                        results = openalex_client.search(query=search_query, keywords=keywords)

                                        if results:
                                            st.session_state.search_results = results
                                            st.session_state.analysis = ai_analyzer.analyze_results(results)
                                            st.session_state.last_query = search_query
                                        else:
                                            st.session_state.warning_message = "No results found. Try different terms."
                                            st.session_state.search_results = []
                                            st.session_state.analysis = None

                                        # Update progress after research
                                        st.session_state.progress += progress_step
                                        progress_bar.progress(st.session_state.progress)

                                    except Exception as e:
                                        logger.error(f"Error in research search: {str(e)}")
                                        st.session_state.warning_message = f"An error occurred during search: {str(e)}"
                                        st.session_state.search_results = []
                                        st.session_state.analysis = None

                                # Create sub-tabs for Documents and AI Analysis
                                doc_tab, analysis_tab = st.tabs(["Documents", "AI Analysis"])

                                # Show results if we have them
                                if st.session_state.get('search_results'):
                                    with doc_tab:
                                        render_search_section(st.session_state.search_results)
                                    with analysis_tab:
                                        if st.session_state.get('analysis'):
                                            render_analysis_section(st.session_state.analysis, section_type="research")

                        elif current_stage == "patents":
                            with st.spinner("Searching patents..."):
                                patent_client = PatentSearchClient()
                                if search_query != st.session_state.get('last_query', '') or st.session_state.get(
                                        'patent_results') is None:
                                    patent_results = patent_client.search_patents(search_query)
                                    if patent_results:
                                        st.session_state.patent_results = patent_results
                                        with st.spinner("Analyzing patents..."):
                                            st.session_state.patent_analysis = patent_client.analyze_patents(
                                                patent_results)
                                    else:
                                        st.session_state.warning_message = "No patent results found."
                                        st.session_state.patent_results = None
                                        st.session_state.patent_analysis = None

                                    # Update progress after patents
                                    st.session_state.progress += progress_step
                                    progress_bar.progress(st.session_state.progress)

                                # Create sub-tabs for Documents and AI Analysis
                                patent_tab, analysis_tab = st.tabs(["Documents", "AI Analysis"])

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
                                from funding import FundingAgent
                                funding_agent = FundingAgent()
                                st.session_state.funding_data = funding_agent.get_funding_opportunities(search_query)

                                # Update progress after funding
                                st.session_state.progress += progress_step
                                progress_bar.progress(st.session_state.progress)

                            render_funding_section(search_query, st.session_state.funding_data)

                        elif current_stage == "collaboration":
                            render_network_section(st.session_state.get('search_results', []))

                            # Update progress after collaboration
                            st.session_state.progress += progress_step
                            progress_bar.progress(st.session_state.progress)

                        elif current_stage == "synthesis":
                            with st.spinner("Synthesizing insights..."):
                                render_synthesis_section(
                                    research_data=st.session_state.get('search_results', []),
                                    patent_data=st.session_state.get('patent_results', []),
                                    funding_data=st.session_state.get('funding_data', []),
                                    selected_stages=selected_stages
                                )

                                # Update progress after synthesis
                                st.session_state.progress += progress_step
                                progress_bar.progress(st.session_state.progress)

                        elif current_stage == "compliance":
                            st.info("Coming Soon")

                            # Update progress after compliance
                            st.session_state.progress += progress_step
                            progress_bar.progress(st.session_state.progress)

                    except Exception as e:
                        logger.error(f"Error in tab {current_stage}: {str(e)}")
                        st.session_state.warning_message = f"An error occurred in {current_stage} tab: {str(e)}"

        else:
            pass

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