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

    # Page layout
    st.markdown('<h1 class="main-header">Research Pipeline System</h1>', unsafe_allow_html=True)

    # Search section with custom styling
    st.markdown("""
        <style>
        .search-container {
            background-color: white;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        search_query = st.text_input("", placeholder="Enter your research query", help="Type your research query here")
        st.markdown('</div>', unsafe_allow_html=True)

    # Initialize session state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
        st.session_state.analysis = None
        st.session_state.last_query = None
        st.session_state.selected_stages = []
        st.session_state.patent_results = None
        st.session_state.patent_analysis = None

    # Stage selection with custom styling
    st.markdown("""
        <style>
        .stage-grid {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1rem;
            margin: 2rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="stage-grid">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        research_agent = st.checkbox("Research Agent", value=True, key="research_checkbox", help="Academic literature analysis")
    with col2:
        patent_search = st.checkbox("Patent Search", key="patent_checkbox", help="Patent research and analysis")
    with col3:
        networking = st.checkbox("Networking", key="networking_checkbox", help="Research collaboration opportunities")
    with col4:
        funding = st.checkbox("Funding", key="funding_checkbox", help="Research funding opportunities")
    with col5:
        compliance = st.checkbox("Compliance", key="compliance_checkbox", help="Research compliance checking")

    st.markdown('</div>', unsafe_allow_html=True)

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
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            st.header("Research Agent Analysis")

            # Initialize clients
            openalex_client = OpenAlexClient()
            ai_analyzer = AIAnalyzer()

            # Search and analysis logic
            if search_query != st.session_state.last_query:
                with st.spinner("🔍 Analyzing query and searching..."):
                    keywords = ai_analyzer.generate_search_keywords(search_query)
                    st.markdown("🎯 **Generated search keywords:** " + ", ".join(keywords))

                    results = openalex_client.search(query=search_query, keywords=keywords)

                    if results:
                        st.session_state.search_results = results
                        st.session_state.analysis = ai_analyzer.analyze_results(results)
                        st.session_state.last_query = search_query
                    else:
                        st.warning("No results found. Try using more general academic terms.")
                        st.session_state.search_results = None
                        st.session_state.analysis = None

            # Display results
            if st.session_state.search_results:
                render_search_section(st.session_state.search_results)
                handle_pdf_export(st.session_state.search_results, st.session_state.analysis)
                render_analysis_section(st.session_state.analysis)

            st.markdown('</div>', unsafe_allow_html=True)

        if "Patent Search" in selected_stages:
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            st.header("Patent Search Analysis")

            patent_client = PatentSearchClient()

            if search_query != st.session_state.last_query or st.session_state.patent_results is None:
                with st.spinner("🔍 Searching patents..."):
                    patent_results = patent_client.search_patents(search_query)
                    if patent_results:
                        st.session_state.patent_results = patent_results
                        with st.spinner("🤖 Analyzing patents with AI..."):
                            st.session_state.patent_analysis = patent_client.analyze_patents(patent_results)
                    else:
                        st.warning("No patent results found. Try modifying your search terms.")
                        st.session_state.patent_results = None
                        st.session_state.patent_analysis = None

            if st.session_state.patent_results:
                st.subheader("Patent Search Results")

                total_patents = len(st.session_state.patent_results)
                unique_inventors = len(set([p['inventors'] for p in st.session_state.patent_results]))

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("📊 Total Patents", total_patents)
                with col2:
                    st.metric("👥 Unique Inventors", unique_inventors)

                for patent in st.session_state.patent_results:
                    with st.expander(f"📄 {patent.get('title', 'Untitled Patent')}"):
                        st.markdown(f"""
                        **Patent ID:** {patent.get('patent_id', 'N/A')}  
                        **Inventors:** {patent.get('inventors', 'N/A')}  
                        **Filing Date:** {patent.get('filing_date', 'N/A')}

                        **Abstract:**  
                        {patent.get('abstract', 'No abstract available')}
                        """)
                        if patent.get('url'):
                            st.markdown(f"[View Patent Details]({patent['url']}) 🔗")

                if st.session_state.patent_analysis:
                    st.subheader("AI Patent Analysis")

                    # Summary card
                    with st.container():
                        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                        st.markdown("### 🔬 Technology Landscape")
                        st.write(st.session_state.patent_analysis.get("summary", "Analysis not available"))
                        st.markdown('</div>', unsafe_allow_html=True)

                    # Trends card
                    with st.container():
                        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                        st.markdown("### 📈 Key Technology Trends")
                        trends = st.session_state.patent_analysis.get("trends", [])
                        for trend in trends:
                            st.markdown(f"• {trend}")
                        st.markdown('</div>', unsafe_allow_html=True)

                    # Opportunities card
                    with st.container():
                        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                        st.markdown("### 💡 Market Opportunities")
                        opportunities = st.session_state.patent_analysis.get("opportunities", [])
                        for opportunity in opportunities:
                            st.markdown(f"• {opportunity}")
                        st.markdown('</div>', unsafe_allow_html=True)

                    # Competition card
                    with st.container():
                        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                        st.markdown("### 🏢 Competitive Analysis")
                        st.write(st.session_state.patent_analysis.get("competition", "Analysis not available"))
                        st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        if "Networking" in selected_stages:
            st.markdown('<div class="section-container coming-soon">', unsafe_allow_html=True)
            st.header("Networking Analysis")
            st.info("🔄 Networking Agent - Coming Soon")
            st.markdown('</div>', unsafe_allow_html=True)

        if "Funding" in selected_stages:
            st.markdown('<div class="section-container coming-soon">', unsafe_allow_html=True)
            st.header("Funding Analysis")
            st.info("💰 Funding Agent - Coming Soon")
            st.markdown('</div>', unsafe_allow_html=True)

        if "Compliance" in selected_stages:
            st.markdown('<div class="section-container coming-soon">', unsafe_allow_html=True)
            st.header("Compliance Analysis")
            st.info("✓ Compliance Agent - Coming Soon")
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()