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

                /* Stage buttons styling */
                .stage-buttons {
                    display: flex;
                    justify-content: space-between;
                    gap: 1rem;
                    margin: 2rem 0;
                    flex-direction: row;
                    flex-wrap: nowrap;
                }

                .stage-button {
                    background-color: #fff;
                    border: 1px solid #dfe1e5;
                    border-radius: 12px;
                    padding: 0.75rem 1.5rem;
                    color: #202124;
                    font-weight: 500;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    flex: 1;
                    text-align: center;
                    text-decoration: none;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-width: 120px;
                }

                .stage-button:hover {
                    box-shadow: 0 1px 6px rgba(32,33,36,.28);
                    border-color: rgba(223,225,229,0);
                }

                .stage-button.selected {
                    background-color: #e8f0fe;
                    border-color: #1a73e8;
                    color: #1a73e8;
                }

                .stage-button i {
                    margin-right: 0.5rem;
                }

                /* Tab styling */
                .stTabs {
                    background: #fff;
                    border-radius: 12px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.12);
                    margin-top: 2rem;
                }
            </style>
            <script>
                function toggleStage(stageKey) {
                    const buttons = document.querySelectorAll('.stage-button');
                    buttons.forEach(button => {
                        button.classList.remove('selected'); // Remove selection from all buttons
                    });
                    const button = document.querySelector(`[data-stage="${stageKey}"]`);
                    if (button) {
                        button.classList.add('selected'); // Add selection to the clicked button
                    }

                    // Send message to Streamlit
                    window.parent.postMessage({
                        type: 'streamlit:setComponentValue',
                        value: stageKey
                    }, '*');
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

    # Stage buttons container
    st.markdown('<div class="stage-buttons">', unsafe_allow_html=True)

    stages = {
        'research': ('fas fa-search', 'Research'),
        'patents': ('fas fa-file-contract', 'Patents'),
        'funding': ('fas fa-hand-holding-usd', 'Funding'),
        'network': ('fas fa-network-wired', 'Network'),
        'compliance': ('fas fa-shield-alt', 'Compliance')
    }

    for stage_key, (icon, label) in stages.items():
        selected_class = "selected" if stage_key in st.session_state.selected_stages else ""
        st.markdown(
            f"""<button 
                class="stage-button {selected_class}" 
                onclick="toggleStage('{stage_key}')"
                data-stage="{stage_key}">
                <i class="{icon}"></i>{label}
            </button>""",
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Handle stage selection from JavaScript
    if st.session_state.get('last_clicked'):
        stage_key = st.session_state.last_clicked
        if stage_key in st.session_state.selected_stages:
            st.session_state.selected_stages.remove(stage_key)
        else:
            st.session_state.selected_stages.add(stage_key)
        del st.session_state.last_clicked
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