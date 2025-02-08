import streamlit as st
import plotly.express as px
from api_client import OpenAlexClient
from ai_analyzer import AIAnalyzer
from components import render_search_section, render_analysis_section
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

    # Main search section
    search_query = st.text_input("Enter your search query")

    if search_query:
        with st.spinner("Analyzing query and searching..."):
            # First, generate optimized search keywords using AI
            keywords = ai_analyzer.generate_search_keywords(search_query)

            # Show the generated keywords
            st.write("🔍 Generated search keywords:", ", ".join(keywords))

            # Use the first few keywords for search
            combined_query = " ".join(keywords[:3])  # Use top 3 keywords

            # Get results from OpenAlex
            results = openalex_client.search(query=combined_query)

            if results:
                # Render search results
                render_search_section(results)

                # Perform AI analysis
                analysis = ai_analyzer.analyze_results(results)

                # Render analysis
                render_analysis_section(analysis)
            else:
                st.warning("No results found. Try adjusting your search query.")

if __name__ == "__main__":
    main()