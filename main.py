import streamlit as st
import plotly.express as px
from api_client import OpenAlexClient
from ai_analyzer import AIAnalyzer
from patent_client import PatentSearchClient
from components import (
    render_search_section, 
    render_analysis_section,
    render_patent_results,
    render_combined_results,
    handle_pdf_export
)
from utils import setup_page
from funding import render_funding_section, FundingAgent

def create_stage_button(icon_class: str, label: str, stage_key: str) -> str:
    """Create HTML for a modernized stage button"""
    is_selected = stage_key in st.session_state.get('selected_stages', set())
    selected_class = "selected" if is_selected else ""
    return f"""
        <div class="stage-selector {selected_class}">
            {label}
        </div>
    """

def main():
    setup_page()

    # Add modern styling
    st.markdown("""
        <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

                /* Modern styling */
                .main-container {
                    max-width: 800px;
                    margin: 3rem auto;
                    text-align: center;
                    font-family: 'Inter', sans-serif;
                }

                .logo-title {
                    font-size: 1.75rem;
                    font-weight: 600;
                    color: #1a73e8;
                    margin-bottom: 0.5rem;
                }

                .main-header {
                    font-size: 2.5rem;
                    font-weight: 500;
                    color: #202124;
                    margin: 1rem 0;
                }

                .subtitle {
                    font-size: 1.1rem;
                    color: #5f6368;
                    margin-bottom: 2rem;
                }

                /* Search box styling */
                .stTextInput > div > div {
                    background-color: #fff;
                    border-radius: 24px !important;
                    border: 1px solid #dfe1e5;
                    box-shadow: none;
                    padding: 0 1rem;
                    transition: all 0.3s ease;
                }

                .stTextInput > div > div:hover,
                .stTextInput > div > div:focus-within {
                    box-shadow: 0 1px 6px rgba(32,33,36,.28);
                    border-color: rgba(223,225,229,0);
                }

                /* Stage selector styling */
                .stage-selectors {
                    display: flex;
                    justify-content: center;
                    gap: 1.5rem;
                    margin: 2rem 0;
                    flex-wrap: wrap;
                }

                /* Button styling */
                .stButton > button {
                    background-color: #fff !important;
                    border-radius: 12px !important;
                    padding: 1rem !important;
                    border: 1px solid #dfe1e5 !important;
                    color: #202124 !important;
                    font-weight: 500 !important;
                    transition: all 0.2s ease;
                    width: 100%;
                    display: flex !important;
                    align-items: center;
                    justify-content: center;
                    gap: 0.5rem;
                }

                .stButton > button:hover {
                    box-shadow: 0 1px 6px rgba(32,33,36,.28);
                    border-color: rgba(223,225,229,0) !important;
                }

                .stButton > button i {
                    font-size: 1.2rem;
                }

                .stButton > button.selected {
                    background-color: #e8f0fe !important;
                    border-color: #1a73e8 !important;
                    color: #1a73e8 !important;
                }

                /* Tab styling */
                .stTabs {
                    background: #fff;
                    border-radius: 12px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.12);
                    margin-top: 2rem;
                }
            </style>
        </head>
        <div class="main-container">
            <div class="logo-title">DEEP CREW</div>
            <h1 class="main-header">Research & Innovation Hub</h1>
            <p class="subtitle">
                Discover insights, analyze patents, and explore funding opportunities with AI-powered research tools
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Search input with modern styling
    search_query = st.text_input(
        "",
        placeholder="Enter your research topic...",
        help="Type your research query here",
        label_visibility="collapsed"
    )

    # Initialize session state for selected stages
    if 'selected_stages' not in st.session_state:
        st.session_state.selected_stages = set()

    # Create columns for stage buttons
    cols = st.columns(5)

    stages = {
        'research': ('fas fa-search', 'Research'),
        'patents': ('fas fa-file-contract', 'Patents'),
        'funding': ('fas fa-hand-holding-usd', 'Funding'),
        'network': ('fas fa-network-wired', 'Network'),
        'compliance': ('fas fa-shield-alt', 'Compliance')
    }

    for idx, (stage_key, (icon, label)) in enumerate(stages.items()):
        with cols[idx]:
            is_selected = stage_key in st.session_state.selected_stages
            button_label = f'<i class="{icon}"></i> {label}'
            if st.button(
                button_label,
                key=f"btn_{stage_key}",
                use_container_width=True,
                help=f"Click to select {label}",
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

        # Create tabs with modern styling
        tabs = st.tabs([stage.capitalize() for stage in selected_stages])

        for idx, tab in enumerate(tabs):
            with tab:
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

                elif selected_stages[idx] == "results":
                    render_combined_results(
                        st.session_state.get('search_results') or [],
                        st.session_state.get('patent_results') or [],
                        st.session_state.combined_analysis if 'combined_analysis' in st.session_state else None
                    )

                elif selected_stages[idx] == "network":
                    st.info("🔄 Coming Soon")
                elif selected_stages[idx] == "funding":
                    render_funding_section(search_query)
                elif selected_stages[idx] == "compliance":
                    st.info("✓ Coming Soon")
    else:
        st.info("Enter a search query to begin your research journey.")

if __name__ == "__main__":
    main()