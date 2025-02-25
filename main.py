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

    # Load custom CSS
    with open(".streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Modern header with description
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <div class='deep-crew-title'>DEEP CREW</div>
            <h1 class='main-header'>Research & Innovation Hub</h1>
            <p style='font-size: 1.2rem; color: #64748B; max-width: 600px; margin: 0 auto;'>
                Discover insights, analyze patents, and explore funding opportunities with AI-powered research tools
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Search input with better styling
    search_query = st.text_input(
        "",
        placeholder="Enter your research topic...",
        help="Type your research query here",
        label_visibility="collapsed"
    )

    # Initialize session state for icon selections if not exists
    if 'selected_icons' not in st.session_state:
        st.session_state.selected_icons = {
            'research': False,
            'patents': False,
            'funding': False,
            'network': False,
            'compliance': False
        }

    # Initialize other session states
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'analysis' not in st.session_state:
        st.session_state.analysis = None
    if 'last_query' not in st.session_state:
        st.session_state.last_query = None
    if 'patent_results' not in st.session_state:
        st.session_state.patent_results = None
    if 'patent_analysis' not in st.session_state:
        st.session_state.patent_analysis = None
    if 'combined_analysis' not in st.session_state:
        st.session_state.combined_analysis = None

    # Stage selection with better layout
    st.markdown("### Choose Research Stages")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        is_research_selected = st.session_state.selected_icons.get('research', False)
        container = st.container()
        with container:
            st.markdown(f"""
                <div class="icon-card{' selected' if is_research_selected else ''}">
                    <i class="fas fa-search"></i>
                    <span>Research</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Research", key="research_btn", help="Select Research stage"):
                st.session_state.selected_icons['research'] = not is_research_selected
                st.experimental_rerun()

    with col2:
        is_patents_selected = st.session_state.selected_icons.get('patents', False)
        container = st.container()
        with container:
            st.markdown(f"""
                <div class="icon-card{' selected' if is_patents_selected else ''}">
                    <i class="fas fa-file-contract"></i>
                    <span>Patents</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Patents", key="patents_btn", help="Select Patents stage"):
                st.session_state.selected_icons['patents'] = not is_patents_selected
                st.experimental_rerun()

    with col3:
        is_funding_selected = st.session_state.selected_icons.get('funding', False)
        container = st.container()
        with container:
            st.markdown(f"""
                <div class="icon-card{' selected' if is_funding_selected else ''}">
                    <i class="fas fa-hand-holding-usd"></i>
                    <span>Funding</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Funding", key="funding_btn", help="Select Funding stage"):
                st.session_state.selected_icons['funding'] = not is_funding_selected
                st.experimental_rerun()

    with col4:
        is_network_selected = st.session_state.selected_icons.get('network', False)
        container = st.container()
        with container:
            st.markdown(f"""
                <div class="icon-card{' selected' if is_network_selected else ''}">
                    <i class="fas fa-network-wired"></i>
                    <span>Network</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Network", key="network_btn", help="Select Network stage"):
                st.session_state.selected_icons['network'] = not is_network_selected
                st.experimental_rerun()

    with col5:
        is_compliance_selected = st.session_state.selected_icons.get('compliance', False)
        container = st.container()
        with container:
            st.markdown(f"""
                <div class="icon-card{' selected' if is_compliance_selected else ''}">
                    <i class="fas fa-shield-alt"></i>
                    <span>Compliance</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Compliance", key="compliance_btn", help="Select Compliance stage"):
                st.session_state.selected_icons['compliance'] = not is_compliance_selected
                st.experimental_rerun()

    # Get selected stages based on icon selections
    selected_stages = []
    for icon, is_selected in st.session_state.selected_icons.items():
        if is_selected:
            selected_stages.append(icon.capitalize())

    # Create tabs for selected stages if we have a search query
    if search_query:
        # Check if any stages are selected
        if not selected_stages:
            st.warning("Please select at least one research stage to proceed.")
            return

        # Only add Results tab if more than one stage is selected
        if len(selected_stages) > 1:
            selected_stages.append("Results")

        # Create tabs for selected stages
        tabs = st.tabs(selected_stages)

        for idx, tab in enumerate(tabs):
            with tab:
                if selected_stages[idx] == "Research":
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
                        render_search_section(st.session_state.search_results)
                        render_analysis_section(st.session_state.analysis)

                elif selected_stages[idx] == "Patents":
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
                        # Funding Analysis
                        st.markdown("## 💰 Global Funding Analysis")
                        funding_agent = FundingAgent()
                        global_insights = funding_agent.get_regional_insights("Global")

                        # Overview
                        st.markdown("### 📊 Market Overview")
                        st.write(global_insights["overview"])

                        # Success Metrics
                        metrics = global_insights.get("success_metrics", {})
                        met_col1, met_col2, met_col3, met_col4 = st.columns(4)
                        with met_col1:
                            st.metric("Success Rate", f"{metrics.get('average_success_rate', 0)}%")
                        with met_col2:
                            st.metric("Projects Funded", metrics.get('total_projects_funded', 0))
                        with met_col3:
                            st.metric("Avg Funding", metrics.get('average_funding_size', 'N/A'))
                        with met_col4:
                            st.metric("YoY Growth", f"{metrics.get('yoy_growth', 0)}%")

                        # Funding Distribution
                        st.markdown("### 💰 Global Funding Distribution")
                        dist_data = global_insights.get("funding_distribution", {})
                        if dist_data:
                            fig_dist = px.pie(
                                values=list(dist_data.values()),
                                names=list(dist_data.keys()),
                                title="Global Funding Sources Distribution",
                                hole=0.4
                            )
                            st.plotly_chart(fig_dist)

                        # Sector Growth
                        st.markdown("### 📈 Global Sector Growth")
                        sector_growth = global_insights.get("sector_growth", [])
                        if sector_growth:
                            fig_growth = px.bar(
                                sector_growth,
                                x="sector",
                                y="growth_rate",
                                title="Global Growth Rates by Sector",
                                labels={"sector": "Sector", "growth_rate": "Growth Rate (%)"},
                                color="growth_rate",
                                color_continuous_scale="viridis"
                            )
                            st.plotly_chart(fig_growth)

                        # Key Sectors and Trends
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("### 🎯 Key Global Sectors")
                            for sector in global_insights.get("key_sectors", []):
                                st.markdown(f"• {sector}")

                        with col2:
                            st.markdown("### 🔄 Global Market Trends")
                            trends = [
                                "Growing investment in research and development",
                                "Increased focus on sustainable technologies",
                                "Rising cross-border collaborations",
                                "Emphasis on digital transformation"
                            ]
                            for trend in trends:
                                st.markdown(f"• {trend}")
                    else:
                        st.info("Please perform a search in Research Agent or Patent Search to view combined analysis.")

                elif selected_stages[idx] == "Network":
                    st.info("🔄 Coming Soon")
                elif selected_stages[idx] == "Funding":
                    render_funding_section(search_query)
                elif selected_stages[idx] == "Compliance":
                    st.info("✓ Coming Soon")
    else:
        st.info("Enter a search query to begin your research journey.")

if __name__ == "__main__":
    main()