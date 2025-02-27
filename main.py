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

    # Initialize session state for accessibility settings
    if 'high_contrast' not in st.session_state:
        st.session_state.high_contrast = False
    if 'negative_contrast' not in st.session_state:
        st.session_state.negative_contrast = False
    if 'light_background' not in st.session_state:
        st.session_state.light_background = False
    if 'links_underline' not in st.session_state:
        st.session_state.links_underline = False
    if 'readable_font' not in st.session_state:
        st.session_state.readable_font = False

    st.markdown("""
        <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
            <style>
                /* Accessibility Menu Styles */
                .accessibility-button {
                    position: fixed;
                    top: 0.5rem;
                    left: 1rem;
                    z-index: 99999;
                    background: none;
                    border: none;
                    cursor: pointer;
                    padding: 10px;
                    font-size: 24px;
                    color: #1a73e8;
                    border-radius: 50%;
                    width: 48px;
                    height: 48px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: white;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }

                .accessibility-button:hover {
                    background: #f0f3f6;
                }

                .accessibility-menu {
                    position: fixed;
                    top: 4rem;
                    left: 1rem;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    padding: 15px;
                    z-index: 99998;
                    display: none;
                    min-width: 200px;
                }

                .accessibility-menu.show {
                    display: block;
                }

                .accessibility-option {
                    display: flex;
                    align-items: center;
                    padding: 8px;
                    cursor: pointer;
                    transition: background 0.2s;
                    border-radius: 4px;
                    color: #202124;
                }

                .accessibility-option:hover {
                    background: #f0f3f6;
                }

                .accessibility-option i {
                    margin-right: 8px;
                    width: 20px;
                    text-align: center;
                }

                /* Existing styles... */
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
                @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;500;600;700&display=swap');
                @import url('https://fonts.googleapis.com/css2?family=OpenDyslexic:wght@400;700&display=swap');
                .st-bt {
                    background-color: transparent !important;
                }

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

                /* High Contrast Mode */
                body.high-contrast {
                    background: black !important;
                    color: white !important;
                }

                body.high-contrast * {
                    background: black !important;
                    color: white !important;
                    border-color: white !important;
                }

                /* Negative Contrast */
                body.negative-contrast {
                    filter: invert(100%);
                }

                /* Light Background */
                body.light-background {
                    background: #ffffff !important;
                    color: #000000 !important;
                }

                /* Links Underline */
                body.links-underline a {
                    text-decoration: underline !important;
                }

                /* Readable Font */
                body.readable-font {
                    font-family: 'OpenDyslexic', sans-serif !important;
                }

                body.readable-font * {
                    font-family: 'OpenDyslexic', sans-serif !important;
                }
            </style>

            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    // Create and append the accessibility button and menu to the body
                    const button = document.createElement('button');
                    button.className = 'accessibility-button';
                    button.setAttribute('aria-label', 'Accessibility Options');
                    button.innerHTML = '<i class="fas fa-universal-access"></i>';

                    const menu = document.createElement('div');
                    menu.className = 'accessibility-menu';
                    menu.innerHTML = `
                        <div class="accessibility-option" onclick="toggleAccessibility('high-contrast')">
                            <i class="fas fa-adjust"></i> High Contrast
                        </div>
                        <div class="accessibility-option" onclick="toggleAccessibility('negative-contrast')">
                            <i class="fas fa-moon"></i> Negative Contrast
                        </div>
                        <div class="accessibility-option" onclick="toggleAccessibility('light-background')">
                            <i class="fas fa-sun"></i> Light Background
                        </div>
                        <div class="accessibility-option" onclick="toggleAccessibility('links-underline')">
                            <i class="fas fa-underline"></i> Links Underline
                        </div>
                        <div class="accessibility-option" onclick="toggleAccessibility('readable-font')">
                            <i class="fas fa-font"></i> Readable Font
                        </div>
                        <div class="accessibility-option" onclick="resetAccessibility()">
                            <i class="fas fa-undo"></i> Reset
                        </div>
                    `;

                    document.body.appendChild(button);
                    document.body.appendChild(menu);

                    button.addEventListener('click', function() {
                        menu.classList.toggle('show');
                    });
                });

                function toggleAccessibility(option) {
                    document.body.classList.toggle(option);
                    const streamlit = window.parent.streamlit;
                    streamlit.setComponentValue({
                        option: option,
                        state: document.body.classList.contains(option)
                    });
                }

                function resetAccessibility() {
                    ['high-contrast', 'negative-contrast', 'light-background', 'links-underline', 'readable-font'].forEach(option => {
                        document.body.classList.remove(option);
                    });
                    const streamlit = window.parent.streamlit;
                    streamlit.setComponentValue({
                        option: 'reset',
                        state: true
                    });
                }
            </script>
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