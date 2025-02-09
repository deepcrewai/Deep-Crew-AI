import streamlit as st
import plotly.express as px
from api_client import OpenAlexClient
from ai_analyzer import AIAnalyzer
from components import render_search_section, render_analysis_section, handle_pdf_export
from utils import setup_page

def main():
    setup_page()

    st.title("AI-Powered Academic Literature Analysis")
    st.markdown("""
    Analyze academic literature using AI and bibliometric data from OpenAlex.
    Get insights, trends, and recommendations for your research.
    """)

    # Initialize clients
    openalex_client = OpenAlexClient()
    ai_analyzer = AIAnalyzer()

    # Initialize session state for storing results
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
        st.session_state.analysis = None
        st.session_state.last_query = None

    # Main search section
    search_query = st.text_input("Enter your search query")

    if search_query:
        # Only perform search if it's a new query
        if search_query != st.session_state.last_query:
            with st.spinner("Analyzing query and searching..."):
                # First, generate optimized search keywords using AI
                keywords = ai_analyzer.generate_search_keywords(search_query)

                # Show the generated keywords
                st.write("🔍 Generated search keywords:", ", ".join(keywords))

                # Get results from OpenAlex using keywords for similarity ranking
                results = openalex_client.search(query=search_query, keywords=keywords)

                if results:
                    # Store results and analysis in session state
                    st.session_state.search_results = results
                    st.session_state.analysis = ai_analyzer.analyze_results(results)
                    st.session_state.last_query = search_query
                else:
                    st.warning("""No results found. Your query might be too specific. 
                    Try using more general academic terms.""")
                    st.session_state.search_results = None
                    st.session_state.analysis = None

        # Use stored results for display and PDF export
        if st.session_state.search_results:
            # Render search results
            render_search_section(st.session_state.search_results)

            # Handle PDF export
            handle_pdf_export(st.session_state.search_results, st.session_state.analysis)

            # Render analysis
            render_analysis_section(st.session_state.analysis)

if __name__ == "__main__":
    main()