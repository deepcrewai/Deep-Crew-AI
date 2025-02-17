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
    search_query = st.text_input("", placeholder="Search", help="Type your research query here.", label_visibility="collapsed")

    # Initialize session state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
        st.session_state.analysis = None
        st.session_state.last_query = None
        st.session_state.selected_stages = []
        st.session_state.patent_results = None
        st.session_state.patent_analysis = None
        st.session_state.combined_analysis = None

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

    # Add Results tab if any stage is selected
    if len(selected_stages) > 0:
        selected_stages.append("Results")

    st.session_state.selected_stages = selected_stages

    if search_query:
        # Create tabs for selected stages
        tabs = st.tabs(selected_stages)

        for idx, tab in enumerate(tabs):
            with tab:
                if selected_stages[idx] == "Research Agent":
                    openalex_client = OpenAlexClient()
                    ai_analyzer = AIAnalyzer()

                    if search_query != st.session_state.last_query:
                        with st.spinner("Analyzing..."):
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
                        # Sort results by similarity score
                        sorted_results = sorted(
                            st.session_state.search_results,
                            key=lambda x: x.get('similarity_score', 0),
                            reverse=True
                        )
                        # Take top results
                        top_results = sorted_results[:10]  # Show top 10 most similar results

                        st.markdown("### 🎯 Most Relevant Research Papers")
                        for result in top_results:
                            similarity_score = result.get('similarity_score', 0)
                            st.markdown(f"""
                            ---
                            #### 📄 {result.get('title', 'Untitled')}
                            **Similarity Score:** {similarity_score:.2f}

                            **Authors:** {', '.join(result.get('authors', []))}

                            **Abstract:** {result.get('abstract', 'No abstract available')}

                            **Year:** {result.get('publication_year', 'N/A')}

                            **DOI:** {result.get('doi', 'No DOI available')}
                            """)

                        render_analysis_section(st.session_state.analysis)

                elif selected_stages[idx] == "Patent Search":
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
                        render_patent_results(st.session_state.patent_results, st.session_state.patent_analysis)

                        # AI Analysis for Patents
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

                elif selected_stages[idx] == "Results":
                    # Generate combined analysis if not already done
                    if st.session_state.combined_analysis is None:
                        with st.spinner("🔄 Generating comprehensive analysis..."):
                            ai_analyzer = AIAnalyzer()
                            research_data = st.session_state.search_results if st.session_state.search_results else []
                            patent_data = st.session_state.patent_results if st.session_state.patent_results else []
                            st.session_state.combined_analysis = ai_analyzer.analyze_combined_results(
                                research_data,
                                patent_data
                            )

                    if st.session_state.combined_analysis:
                        render_combined_results(
                            st.session_state.search_results or [],
                            st.session_state.patent_results or [],
                            st.session_state.combined_analysis
                        )
                    else:
                        st.info("Please perform a search in Research Agent or Patent Search to view combined analysis.")

                elif selected_stages[idx] == "Networking":
                    st.info("🔄 Coming Soon")
                elif selected_stages[idx] == "Funding":
                    st.info("💰 Coming Soon")
                elif selected_stages[idx] == "Compliance":
                    st.info("✓ Coming Soon")

if __name__ == "__main__":
    main()