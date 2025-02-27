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

def main():
    setup_page()

    st.markdown("""
        <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
            <style>
                /* Modern corporate styling */
                :root {
                    --primary-color: #2C3E50;
                    --secondary-color: #34495E;
                    --accent-color: #3498DB;
                    --text-color: #2C3E50;
                    --light-bg: #F7F9FC;
                    --border-color: #E5E9F2;
                }

                body {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                    color: var(--text-color);
                    background-color: var(--light-bg);
                }

                .corporate-container {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 2rem;
                }

                .logo-section {
                    text-align: center;
                    margin-bottom: 3rem;
                }

                .logo-title {
                    font-size: 2.5rem;
                    font-weight: 700;
                    color: var(--primary-color);
                    margin: 0;
                    letter-spacing: -0.5px;
                }

                .subtitle {
                    font-size: 1.1rem;
                    color: var(--secondary-color);
                    margin: 1rem 0 2rem;
                    font-weight: 400;
                }

                /* Search box styling */
                .search-container {
                    background: white;
                    border-radius: 12px;
                    padding: 1.5rem;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    margin-bottom: 2rem;
                }

                .stTextInput > div > div {
                    background-color: var(--light-bg);
                    border-radius: 8px !important;
                    border: 1px solid var(--border-color) !important;
                    padding: 0.75rem 1rem;
                }

                /* Stage buttons */
                .stage-button {
                    background-color: white;
                    border: 1px solid var(--border-color);
                    border-radius: 8px;
                    padding: 0.75rem;
                    color: var(--text-color);
                    transition: all 0.2s ease;
                    width: 100%;
                    margin: 0.25rem 0;
                }

                .stage-button:hover {
                    border-color: var(--accent-color);
                    color: var(--accent-color);
                    transform: translateY(-1px);
                }

                .stage-button[data-selected="true"] {
                    background-color: var(--accent-color);
                    color: white;
                    border-color: var(--accent-color);
                }

                /* Tab styling */
                .stTabs {
                    background: white;
                    border-radius: 12px;
                    padding: 1rem;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                }

                .stTab {
                    color: var(--text-color);
                    font-weight: 500;
                }

                .stTab[aria-selected="true"] {
                    color: var(--accent-color);
                    border-bottom-color: var(--accent-color);
                }
            </style>
        </head>
        <div class="corporate-container">
            <div class="logo-section">
                <h1 class="logo-title">DEEP CREW</h1>
                <p class="subtitle">
                    Advanced Research & Innovation Platform
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Search section
    with st.container():
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        search_query = st.text_input(
            "",
            placeholder="Enter your research topic...",
            help="Type your research query here",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Initialize session state
    if 'selected_stages' not in st.session_state:
        st.session_state.selected_stages = set()

    # Stage selection buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    stages = {
        'research': {'label': 'Research', 'icon': '📚'},
        'patents': {'label': 'Patents', 'icon': '📋'},
        'funding': {'label': 'Funding', 'icon': '💰'},
        'network': {'label': 'Network', 'icon': '🔗'},
        'compliance': {'label': 'Compliance', 'icon': '✓'}
    }

    for idx, (stage_key, info) in enumerate(stages.items()):
        with [col1, col2, col3, col4, col5][idx]:
            is_selected = stage_key in st.session_state.selected_stages
            if st.button(
                f"{info['icon']} {info['label']}",
                key=f"btn_{stage_key}",
                help=f"Click to select {info['label']}",
                use_container_width=True,
                type="secondary" if is_selected else "primary"
            ):
                if stage_key in st.session_state.selected_stages:
                    st.session_state.selected_stages.remove(stage_key)
                else:
                    st.session_state.selected_stages.add(stage_key)
                st.rerun()

    selected_stages = list(st.session_state.selected_stages)

    if search_query:
        if not selected_stages:
            st.warning("Please select at least one research stage to proceed.")
            return

        if len(selected_stages) > 1:
            selected_stages.append("results")

        tabs = st.tabs([stages[stage]['icon'] + ' ' + stage.capitalize() 
                       if stage in stages else '📊 ' + stage.capitalize() 
                       for stage in selected_stages])

        for idx, tab in enumerate(tabs):
            with tab:
                if selected_stages[idx] == "research":
                    with st.spinner("🔍 Analyzing research papers..."):
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
                    with st.spinner("🔍 Analyzing patents..."):
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
                    if (st.session_state.get('search_results') and 
                        st.session_state.get('patent_results') and 
                        'combined_analysis' not in st.session_state):
                        with st.spinner("🔄 Generating comprehensive analysis..."):
                            ai_analyzer = AIAnalyzer()
                            funding_results = st.session_state.get('funding_results', [])
                            st.session_state.combined_analysis = ai_analyzer.analyze_combined_results(
                                st.session_state.search_results,
                                st.session_state.patent_results,
                                funding_results
                            )

                    combined_analysis = st.session_state.get('combined_analysis', {})
                    render_combined_results(
                        st.session_state.get('search_results', []),
                        st.session_state.get('patent_results', []),
                        combined_analysis
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