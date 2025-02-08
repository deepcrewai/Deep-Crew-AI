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

    # Sidebar for filters
    st.sidebar.title("Search Filters")
    search_type = st.sidebar.selectbox(
        "Search Type",
        ["Keywords", "Author", "Institution", "Field"]
    )
    
    years = st.sidebar.slider(
        "Year Range",
        min_value=1950,
        max_value=2024,
        value=(2010, 2024)
    )

    # Main search section
    search_query = st.text_input("Enter your search query")
    
    if search_query:
        with st.spinner("Searching and analyzing..."):
            # Get results from OpenAlex
            results = openalex_client.search(
                query=search_query,
                search_type=search_type,
                year_range=years
            )
            
            if results:
                # Render search results
                render_search_section(results)
                
                # Perform AI analysis
                analysis = ai_analyzer.analyze_results(results)
                
                # Render analysis
                render_analysis_section(analysis)
            else:
                st.warning("No results found. Try adjusting your search criteria.")

if __name__ == "__main__":
    main()
