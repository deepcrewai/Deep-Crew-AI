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

def create_stage_button(icon_class: str, label: str, stage_key: str) -> str:
    """Create HTML for a stage button"""
    is_selected = stage_key in st.session_state.get('selected_stages', set())
    selected_class = "selected" if is_selected else ""
    return f"""
        <div class="stage-selector {selected_class}">
            <i class="{icon_class}"></i>
            <div class="stage-label">{label}</div>
        </div>
    """

def main():
    setup_page()

    # Add Font Awesome and custom styles
    st.markdown("""
        <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        </head>
        <div style='text-align: center; padding: 2rem 0;'>
            <div class='deep-crew-title'>DEEP CREW</div>
            <h1 class='main-header'>Research & Innovation Hub</h1>
            <p style='font-size: 1.2rem; color: #64748B; max-width: 600px; margin: 0 auto;'>
                Discover insights, analyze patents, and explore funding opportunities with AI-powered research tools
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Search input
    search_query = st.text_input(
        "",
        placeholder="Enter your research topic...",
        help="Type your research query here",
        label_visibility="collapsed"
    )

    # Initialize session state for selected stages
    if 'selected_stages' not in st.session_state:
        st.session_state.selected_stages = set()

    # Create stage selectors
    st.markdown("### Choose Research Stages")
    col1, col2, col3, col4, col5 = st.columns(5)

    stages = {
        'research': ('fas fa-search', 'Research'),
        'patents': ('fas fa-file-contract', 'Patents'),
        'funding': ('fas fa-hand-holding-usd', 'Funding'),
        'network': ('fas fa-network-wired', 'Network'),
        'compliance': ('fas fa-shield-alt', 'Compliance')
    }

    columns = {'research': col1, 'patents': col2, 'funding': col3, 'network': col4, 'compliance': col5}

    for stage_key, (icon, label) in stages.items():
        with columns[stage_key]:
            st.markdown(create_stage_button(icon, label, stage_key), unsafe_allow_html=True)
            if st.button(label, key=f"btn_{stage_key}"):
                if stage_key in st.session_state.selected_stages:
                    st.session_state.selected_stages.remove(stage_key)
                else:
                    st.session_state.selected_stages.add(stage_key)
                st.rerun()

    selected_stages = list(st.session_state.selected_stages)

    # Create tabs for selected stages if we have a search query
    if search_query:
        # Check if any stages are selected
        if not selected_stages:
            st.warning("Please select at least one research stage to proceed.")
            return

        # Only add Results tab if more than one stage is selected
        if len(selected_stages) > 1:
            selected_stages.append("results")

        # Create tabs for selected stages
        tabs = st.tabs([stage.capitalize() for stage in selected_stages])

        for idx, tab in enumerate(tabs):
            with tab:
                if selected_stages[idx] == "research":
                    openalex_client = OpenAlexClient()
                    ai_analyzer = AIAnalyzer()

                    if search_query != st.session_state.get('last_query', ''):
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

                    if st.session_state.get('search_results'):
                        render_search_section(st.session_state.search_results)
                        render_analysis_section(st.session_state.analysis)

                elif selected_stages[idx] == "patents":
                    patent_client = PatentSearchClient()

                    if search_query != st.session_state.get('last_query', '') or st.session_state.get('patent_results') is None:
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

                    if st.session_state.get('patent_results'):
                        render_patent_results(st.session_state.patent_results, st.session_state.patent_analysis)
                        # AI Analysis for Patents 
                        if st.session_state.get('patent_analysis'):
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

                elif selected_stages[idx] == "results":
                    if st.session_state.get('combined_analysis') is None:
                        with st.spinner("🔄 Generating comprehensive analysis..."):
                            ai_analyzer = AIAnalyzer()
                            research_data = st.session_state.get('search_results') if st.session_state.get('search_results') else []
                            patent_data = st.session_state.get('patent_results') if st.session_state.get('patent_results') else []
                            st.session_state.combined_analysis = ai_analyzer.analyze_combined_results(
                                research_data,
                                patent_data
                            )

                    if st.session_state.get('combined_analysis'):
                        render_combined_results(
                            st.session_state.get('search_results') or [],
                            st.session_state.get('patent_results') or [],
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

                elif selected_stages[idx] == "network":
                    st.info("🔄 Coming Soon")
                elif selected_stages[idx] == "funding":
                    render_funding_section(search_query)
                elif selected_stages[idx] == "compliance":
                    st.info("✓ Coming Soon")
    else:
        st.info("Enter a search query to begin your research journey.")

if __name__ == "__main__":
    main()