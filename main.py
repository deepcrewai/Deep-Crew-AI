import streamlit as st
import plotly.express as px
from api_client import OpenAlexClient
from ai_analyzer import AIAnalyzer
from patent_client import PatentSearchClient
from components import render_search_section, render_analysis_section, handle_pdf_export
from utils import setup_page

def main():
    setup_page()

    # Load custom CSS
    with open(".streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Add logo
    st.markdown("""
        <div class="logo-container">
            <img src="attached_assets/deep-crew-logo.png" alt="Deep Crew Logo">
        </div>
    """, unsafe_allow_html=True)

    # Simple header
    st.markdown('<h1 class="main-header">Dive Deep into Discovery</h1>', unsafe_allow_html=True)

    # Search input
    search_query = st.text_input("", placeholder="Search", help="Type your research query here.")

    # Initialize session state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
        st.session_state.analysis = None
        st.session_state.last_query = None
        st.session_state.selected_stages = []
        st.session_state.patent_results = None
        st.session_state.patent_analysis = None

    # Stage selection
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
            openalex_client = OpenAlexClient()
            ai_analyzer = AIAnalyzer()

            if search_query != st.session_state.last_query:
                with st.spinner("Analizing"):
                    keywords = ai_analyzer.generate_search_keywords(search_query)
                    st.markdown("Researching...")
                    results = openalex_client.search(query=search_query, keywords=keywords)

                    if results:
                        st.session_state.search_results = results
                        st.session_state.analysis = ai_analyzer.analyze_results(results)
                        st.session_state.last_query = search_query
                    else:
                        st.warning("No results found. Try different terms.")
                        st.session_state.search_results = None
                        st.session_state.analysis = None

            if st.session_state.search_results:
                render_search_section(st.session_state.search_results)
                handle_pdf_export(st.session_state.search_results, st.session_state.analysis)
                render_analysis_section(st.session_state.analysis)

        if "Patent Search" in selected_stages:
            st.header("Patent Search")
            patent_client = PatentSearchClient()

            if search_query != st.session_state.last_query or st.session_state.patent_results is None:
                with st.spinner("🔍 Searching patents..."):
                    patent_results = patent_client.search_patents(search_query)
                    if patent_results:
                        st.session_state.patent_results = patent_results
                        with st.spinner("🤖 Analyzing patents..."):
                            st.session_state.patent_analysis = patent_client.analyze_patents(patent_results)
                    else:
                        st.warning("No patent results found.")
                        st.session_state.patent_results = None
                        st.session_state.patent_analysis = None

            if st.session_state.patent_results:
                # Patent Results
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Patents", len(st.session_state.patent_results))
                with col2:
                    st.metric("Inventors", len(set([p['inventors'] for p in st.session_state.patent_results])))

                # Display patents
                for patent in st.session_state.patent_results:
                    with st.expander(f"📄 {patent.get('title', 'Untitled Patent')}"):
                        st.markdown(f"""
                        **ID:** {patent.get('patent_id', 'N/A')}  
                        **Inventors:** {patent.get('inventors', 'N/A')}  
                        **Filing Date:** {patent.get('filing_date', 'N/A')}

                        {patent.get('abstract', 'No abstract available')}

                        {f"[View Details]({patent['url']})" if patent.get('url') else ''}
                        """)

                # AI Analysis
                if st.session_state.patent_analysis:
                    st.subheader("AI Analysis")

                    st.markdown("### 🔬 Overview")
                    st.write(st.session_state.patent_analysis.get("summary", ""))

                    st.markdown("### 📈 Trends")
                    for trend in st.session_state.patent_analysis.get("trends", []):
                        st.markdown(f"• {trend}")

                    st.markdown("### 💡 Opportunities")
                    for opp in st.session_state.patent_analysis.get("opportunities", []):
                        st.markdown(f"• {opp}")

                    st.markdown("### 🏢 Competition")
                    st.write(st.session_state.patent_analysis.get("competition", ""))

        if "Networking" in selected_stages:
            st.header("Networking")
            st.info("🔄 Coming Soon")

        if "Funding" in selected_stages:
            st.header("Funding")
            st.info("💰 Coming Soon")

        if "Compliance" in selected_stages:
            st.header("Compliance")
            st.info("✓ Coming Soon")

if __name__ == "__main__":
    main()