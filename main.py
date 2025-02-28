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

def reset_app():
    """Reset all session state variables"""
    for key in ['selected_stages', 'search_results', 'analysis', 'last_query', 
                'patent_results', 'patent_analysis', 'combined_analysis']:
        if key in st.session_state:
            del st.session_state[key]

def main():
    setup_page()

    st.markdown("""
        <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
                @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;500;600;700&display=swap');

                .st-bt {
                    background-color: transparent !important;
                }

                /* Modern styling */
                .main-container {
                    max-width: 800px;
                    margin: 3rem auto;
                    text-align: center;
                    font-family: 'Inter', sans-serif;
                }

                .logo-title {
                    font-size: 2.75rem;
                    font-weight: 700;
                    padding: 1.25rem 0px 1rem;
                    font-family: "Source Sans Pro", sans-serif;
                    color: black;
                }

                .main-header {
                    font-size: 2.5rem;
                    font-weight: 500;
                    color: #202124;
                    margin: 1rem 0;
                    font-family: 'Inter', sans-serif;
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
                    border: none !important;
                    box-shadow: none;
                    padding: 0 1rem;
                    transition: all 0.3s ease;
                }

                .stTextInput > div > div:hover,
                .stTextInput > div > div:focus-within {
                    box-shadow: 0 1px 6px rgba(32,33,36,.28);
                }

                /* Reset button styling */
                .reset-button {
                    position: absolute;
                    top: 1rem;
                    right: 1rem;
                    padding: 0.5rem 1rem;
                    background-color: #f8f9fa;
                    border: 1px solid #dfe1e5;
                    border-radius: 8px;
                    color: #5f6368;
                    font-size: 0.9rem;
                    cursor: pointer;
                    transition: all 0.2s ease;
                }

                .reset-button:hover {
                    background-color: #f1f3f4;
                    box-shadow: 0 1px 3px rgba(32,33,36,.12);
                }
                /* Stage buttons container */
                .stage-buttons {
                    display: flex;
                    justify-content: space-between;
                    margin: 2rem 0;
                    gap: 1rem;
                }

                /* Custom button styling */
                div[data-testid="stHorizontalBlock"] > div[data-testid="column"] button {
                    background-color: rgb(255, 255, 255);
                    border: 1px solid #dfe1e5;
                    border-radius: 8px;
                    padding: 0.75rem 1.5rem;
                    color: #202124;
                    font-weight: 500;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    width: 100%;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    gap: 0.5rem;
                }

                div[data-testid="stHorizontalBlock"] > div[data-testid="column"] button:hover {
                    box-shadow: 0 1px 6px rgba(32,33,36,.28);
                    border-color: rgb(31, 119, 180);
                    color: rgb(31, 119, 180);
                }

                div[data-testid="stHorizontalBlock"] > div[data-testid="column"] button[data-selected="true"] {
                    background-color: rgb(31, 119, 180);
                    border-color: rgb(31, 119, 180);
                    color: white;
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
        if st.button("🔄 Sıfırla", help="Aramayı ve seçili aşamaları sıfırla"):
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
        'compliance': 'Compliance'
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
                    if not st.session_state.get('combined_analysis'):
                        st.session_state.combined_analysis = {}

                    render_combined_results(
                        st.session_state.get('search_results') or [],
                        st.session_state.get('patent_results') or [],
                        st.session_state.combined_analysis
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