import streamlit as st
import plotly.express as px
from api_client import OpenAlexClient
from ai_analyzer import AIAnalyzer
from components import render_search_section, render_analysis_section, handle_pdf_export
from utils import setup_page

# Configure the page - this must be the first Streamlit command
st.set_page_config(
    page_title="Deep Crew",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the gradient background and styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(160deg, #b2ffff 0%, #48d1cc 100%);
    }
    .title {
        text-align: center;
        color: #2F4F4F;
        padding: 2rem 0;
        font-size: 4rem;
    }
    .search-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        background-color: white;
        border-radius: 25px;
        padding: 1rem;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Custom title using HTML
    st.markdown('<h1 class="title">Deep Crew</h1>', unsafe_allow_html=True)

    # Initialize clients
    openalex_client = OpenAlexClient()
    ai_analyzer = AIAnalyzer()

    # Initialize session state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
        st.session_state.analysis = None
        st.session_state.last_query = None

    # Centered search section
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    search_query = st.text_input("", placeholder="Search academic literature...", key="search")
    st.markdown('</div>', unsafe_allow_html=True)

    if search_query:
        if search_query != st.session_state.last_query:
            with st.spinner("Analyzing query and searching..."):
                keywords = ai_analyzer.generate_search_keywords(search_query)
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
            handle_pdf_export(st.session_state.search_results, st.session_state.analysis)
            render_analysis_section(st.session_state.analysis)

if __name__ == "__main__":
    main()