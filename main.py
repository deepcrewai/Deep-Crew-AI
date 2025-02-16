import streamlit as st
import plotly.express as px
from api_client import OpenAlexClient
from ai_analyzer import AIAnalyzer
from components import render_search_section, render_analysis_section, handle_pdf_export
from utils import setup_page
import base64

def load_css():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def add_logo():
    with open('attached_assets/deep-crew-logo.png', "rb") as f:
        data = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{data}" width="150px">
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    st.set_page_config(
        page_title="Deep Crew Research Agent",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    load_css()

    # Add logo
    add_logo()

    # Initialize clients
    openalex_client = OpenAlexClient()
    ai_analyzer = AIAnalyzer()

    # Sidebar navigation
    with st.sidebar:
        st.markdown("### Navigation")
        page = st.radio(
            "",
            ["Research", "Analysis", "Export"],
            label_visibility="collapsed"
        )

    # Initialize session state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
        st.session_state.analysis = None
        st.session_state.last_query = None

    # Main content area
    if page == "Research":
        st.markdown("""
        <h1 style='color: white;'>AI-Powered Research Agent</h1>
        <p style='color: #B0B0B0;'>Analyze academic literature using AI and bibliometric data from OpenAlex.
        Get insights, trends, and recommendations for your research.</p>
        """, unsafe_allow_html=True)

        # Search section
        search_query = st.text_input("Enter your research query", key="search_input")

        if search_query:
            if search_query != st.session_state.last_query:
                with st.spinner("Analyzing query and searching..."):
                    keywords = ai_analyzer.generate_search_keywords(search_query)

                    st.markdown("""
                    <div class="analysis-section">
                        <h3>🔍 Generated Keywords</h3>
                        <p>{}</p>
                    </div>
                    """.format(", ".join(keywords)), unsafe_allow_html=True)

                    results = openalex_client.search(query=search_query, keywords=keywords)

                    if results:
                        st.session_state.search_results = results
                        st.session_state.analysis = ai_analyzer.analyze_results(results)
                        st.session_state.last_query = search_query
                    else:
                        st.warning("No results found. Try using more general academic terms.")
                        st.session_state.search_results = None
                        st.session_state.analysis = None

            if st.session_state.search_results:
                render_search_section(st.session_state.search_results)

    elif page == "Analysis":
        if st.session_state.analysis:
            render_analysis_section(st.session_state.analysis)
        else:
            st.info("Please perform a search first to see analysis.")

    elif page == "Export":
        if st.session_state.search_results and st.session_state.analysis:
            handle_pdf_export(st.session_state.search_results, st.session_state.analysis)
        else:
            st.info("Please perform a search first to export results.")

if __name__ == "__main__":
    main()