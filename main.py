import streamlit as st
import plotly.express as px
from api_client import OpenAlexClient
from ai_analyzer import AIAnalyzer
from patent_client import PatentSearchClient
from components import render_search_section, render_analysis_section, handle_pdf_export
from utils import setup_page

def main():
    setup_page()

    st.title("Research Pipeline System")
    st.markdown("""
    Welcome to our comprehensive research pipeline system. This platform offers a 5-stage approach to research:
    1. Research Agent - Academic literature analysis
    2. Patent Search Genius - Patent research and analysis
    3. Networking Agent - Research collaboration opportunities
    4. Funding Agent - Research funding opportunities
    5. Compliance Agent - Research compliance checking
    """)

    # Initialize session state for storing results and selections
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
        st.session_state.analysis = None
        st.session_state.last_query = None
        st.session_state.selected_stages = []
        st.session_state.patent_results = None

    # Main search section
    search_query = st.text_input("Enter your research query")

    # Stage selection
    st.subheader("Select Research Stages")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        research_agent = st.checkbox("Research Agent", value=True)
    with col2:
        patent_search = st.checkbox("Patent Search")
    with col3:
        networking = st.checkbox("Networking")
    with col4:
        funding = st.checkbox("Funding")
    with col5:
        compliance = st.checkbox("Compliance")

    # Store selected stages
    selected_stages = []
    if research_agent:
        selected_stages.append("Research Agent")
    if patent_search:
        selected_stages.append("Patent Search")
    if networking:
        selected_stages.append("Networking")
    if funding:
        selected_stages.append("Funding")
    if compliance:
        selected_stages.append("Compliance")

    st.session_state.selected_stages = selected_stages

    if search_query:
        if "Research Agent" in selected_stages:
            st.header("Research Agent Analysis")
            # Initialize clients for Research Agent
            openalex_client = OpenAlexClient()
            ai_analyzer = AIAnalyzer()

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

        if "Patent Search" in selected_stages:
            st.header("Patent Search Analysis")

            # Initialize Patent Search client
            patent_client = PatentSearchClient()

            # Only perform patent search if it's a new query
            if search_query != st.session_state.last_query or st.session_state.patent_results is None:
                with st.spinner("Searching patents..."):
                    patent_results = patent_client.search_patents(search_query)
                    st.session_state.patent_results = patent_results

            # Display patent results
            if st.session_state.patent_results:
                st.subheader("Patent Search Results")
                for patent in st.session_state.patent_results:
                    with st.expander(f"{patent.get('title', 'Untitled Patent')}"):
                        st.write(f"Patent ID: {patent.get('patent_id', 'N/A')}")
                        st.write(f"Inventors: {patent.get('inventors', 'N/A')}")
                        st.write(f"Filing Date: {patent.get('filing_date', 'N/A')}")
                        st.write(f"Abstract: {patent.get('abstract', 'No abstract available')}")
                        if patent.get('url'):
                            st.write(f"🔗 [View Patent Details]({patent['url']})")
            else:
                st.info("No patent results found. Try modifying your search terms.")

        if "Networking" in selected_stages:
            st.header("Networking Analysis")
            st.info("Networking Agent - Coming Soon")

        if "Funding" in selected_stages:
            st.header("Funding Analysis")
            st.info("Funding Agent - Coming Soon")

        if "Compliance" in selected_stages:
            st.header("Compliance Analysis")
            st.info("Compliance Agent - Coming Soon")

if __name__ == "__main__":
    main()