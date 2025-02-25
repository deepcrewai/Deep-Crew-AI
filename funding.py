import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
from openai import OpenAI
import os
import pandas as pd
import json

class FundingAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o"  # Latest model as of May 13, 2024

    def get_funding_opportunities(self, research_area: str, region: str = None) -> List[Dict]:
        """Find relevant funding opportunities based on research area and region."""
        try:
            prompt = {
                "research_area": research_area,
                "region": region if region else "global",
                "request": "Find relevant funding opportunities"
            }
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": """As a funding expert, analyze the research area and region to identify relevant funding opportunities. 
                    Return a JSON array of opportunities with the following structure:
                    {
                        "opportunities": [
                            {
                                "title": "Grant name",
                                "funder": "Organization name",
                                "amount": "Funding amount",
                                "deadline": "Application deadline",
                                "eligibility": "Eligibility criteria",
                                "link": "Application link",
                                "region": "Geographical region",
                                "success_rate": "Estimated success rate",
                                "priority_level": "High/Medium/Low match"
                            }
                        ]
                    }"""
                }, {
                    "role": "user",
                    "content": json.dumps(prompt)
                }],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content).get("opportunities", [])
        except Exception as e:
            print(f"Error finding funding opportunities: {str(e)}")
            return []
    
    def analyze_funding_trends(self, research_area: str) -> Dict:
        """Analyze current funding trends in the specified research area with enhanced AI analysis."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": """Analyze current funding trends in the specified research area. 
                    Return a JSON object with the following structure:
                    {
                        "trending_areas": [
                            {"area": "area name", "growth_rate": "percentage", "funding_volume": "amount"}
                        ],
                        "top_funders": [
                            {"name": "funder name", "focus_areas": ["area1", "area2"], "typical_amount": "amount range", "success_rate": "percentage"}
                        ],
                        "emerging_opportunities": [
                            {"opportunity": "description", "potential": "High/Medium/Low", "timeline": "Short/Medium/Long"}
                        ],
                        "funding_cycles": {
                            "peak_months": ["month1", "month2"],
                            "preparation_time": "recommended time",
                            "monthly_distribution": {"January": 10, "February": 15}
                        },
                        "sector_analysis": {
                            "market_size": "total market size",
                            "growth_rate": "annual growth rate",
                            "key_players": ["player1", "player2"],
                            "investment_distribution": {
                                "Research": 30,
                                "Development": 25,
                                "Commercialization": 45
                            },
                            "regional_distribution": {
                                "North America": 40,
                                "Europe": 30,
                                "Asia": 20,
                                "Others": 10
                            }
                        },
                        "success_factors": ["factor1", "factor2"]
                    }"""
                }, {
                    "role": "user",
                    "content": research_area
                }],
                response_format={"type": "json_object"}
            )

            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error analyzing funding trends: {str(e)}")
            return {}

    def get_regional_insights(self, region: str) -> Dict:
        """Get funding insights for a specific region."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": """Provide regional funding insights. 
                    Return a JSON object with the following structure:
                    {
                        "total_funding_available": "amount",
                        "key_organizations": ["org1", "org2"],
                        "regional_priorities": ["priority1", "priority2"],
                        "success_stories": ["story1", "story2"],
                        "local_resources": ["resource1", "resource2"],
                        "upcoming_deadlines": [
                            {"program": "name", "deadline": "date", "amount": "funding amount"}
                        ]
                    }"""
                }, {
                    "role": "user",
                    "content": region
                }],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error getting regional insights: {str(e)}")
            return {}
    
    def generate_opportunity_heatmap(self, opportunities: List[Dict]) -> None:
        """Generate a heatmap visualization of funding opportunities."""
        try:
            # Convert opportunities to DataFrame for visualization
            df = pd.DataFrame(opportunities)
            
            # Create a heatmap using plotly
            fig = px.density_heatmap(
                df,
                x="region",
                y="amount",
                title="Funding Opportunity Heatmap",
                labels={"region": "Region", "amount": "Funding Amount"},
                color_continuous_scale="Viridis"
            )
            
            # Display the heatmap
            st.plotly_chart(fig)
            
        except Exception as e:
            st.error(f"Error generating heatmap: {str(e)}")

def render_funding_section(research_query: str):
    """Render the funding section in the Streamlit app."""
    funding_agent = FundingAgent()

    st.markdown("## 💰 Funding Analysis")

    # Region selection
    regions = ["Global", "North America", "Europe", "Asia", "Africa", "South America", "Oceania"]
    selected_region = st.selectbox("Select Region", regions)

    # Main tabs
    main_tabs = st.tabs(["Funding Opportunities", "Funding Trends", "Regional Insights"])

    # Funding Opportunities Tab
    with main_tabs[0]:
        st.markdown("### Available Opportunities")
        with st.spinner("🔍 Finding funding opportunities..."):
            opportunities = funding_agent.get_funding_opportunities(research_query, selected_region)

        if opportunities:
            for opp in opportunities:
                with st.expander(f"{opp['title']} - {opp['funder']}"):
                    st.markdown(f"**Amount:** {opp['amount']}")
                    st.markdown(f"**Deadline:** {opp['deadline']}")
                    st.markdown(f"**Eligibility:** {opp['eligibility']}")
                    st.markdown(f"**Success Rate:** {opp['success_rate']}")
                    st.markdown(f"**Priority Level:** {opp['priority_level']}")
                    st.markdown(f"**[Apply Now]({opp['link']})**")

    # Funding Trends Tab
    with main_tabs[1]:
        trend_tabs = st.tabs(["Sector Analysis", "Success Rates", "Market Analysis"])

        # Sector Analysis Sub-tab
        with trend_tabs[0]:
            st.markdown("### 📊 Sector Analysis")
            with st.spinner("Analyzing sector trends..."):
                trends = funding_agent.analyze_funding_trends(research_query)

                if trends:
                    # AI Analysis Summary
                    st.markdown("#### 🤖 AI Analysis")
                    sector_analysis = trends.get("sector_analysis", {})

                    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                    with metrics_col1:
                        st.metric("Market Size", sector_analysis.get("market_size", "N/A"))
                    with metrics_col2:
                        st.metric("Growth Rate", sector_analysis.get("growth_rate", "N/A"))
                    with metrics_col3:
                        st.metric("Key Players", len(sector_analysis.get("key_players", [])))

                    # Investment Distribution Pie Chart
                    st.markdown("#### 📈 Investment Distribution")
                    investment_data = sector_analysis.get("investment_distribution", {})
                    if investment_data:
                        fig_investment = px.pie(
                            values=list(investment_data.values()),
                            names=list(investment_data.keys()),
                            title="Investment Distribution by Category"
                        )
                        st.plotly_chart(fig_investment)

                    # Regional Distribution Bar Chart
                    st.markdown("#### 🌍 Regional Distribution")
                    regional_data = sector_analysis.get("regional_distribution", {})
                    if regional_data:
                        fig_regional = px.bar(
                            x=list(regional_data.keys()),
                            y=list(regional_data.values()),
                            title="Funding Distribution by Region",
                            labels={"x": "Region", "y": "Percentage"}
                        )
                        st.plotly_chart(fig_regional)

                    # Trending Areas Bubble Chart
                    st.markdown("#### 🚀 Trending Areas")
                    trending_areas = trends.get("trending_areas", [])
                    if trending_areas:
                        df_trending = pd.DataFrame(trending_areas)
                        fig_trending = px.scatter(
                            df_trending,
                            x="growth_rate",
                            y="funding_volume",
                            size="funding_volume",
                            text="area",
                            title="Trending Research Areas",
                            labels={
                                "growth_rate": "Growth Rate",
                                "funding_volume": "Funding Volume",
                                "area": "Research Area"
                            }
                        )
                        st.plotly_chart(fig_trending)

                    # Funding Cycles Line Chart
                    st.markdown("#### 📅 Funding Cycles")
                    monthly_distribution = trends.get("funding_cycles", {}).get("monthly_distribution", {})
                    if monthly_distribution:
                        fig_cycles = px.line(
                            x=list(monthly_distribution.keys()),
                            y=list(monthly_distribution.values()),
                            title="Monthly Funding Distribution",
                            labels={"x": "Month", "y": "Funding Activity"}
                        )
                        st.plotly_chart(fig_cycles)

                    # Display key insights
                    st.markdown("#### 🔍 Key Insights")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Top Funders**")
                        for funder in trends.get("top_funders", []):
                            st.markdown(f"""
                            • **{funder['name']}**
                              - Focus: {', '.join(funder['focus_areas'])}
                              - Typical Amount: {funder['typical_amount']}
                              - Success Rate: {funder['success_rate']}
                            """)

                    with col2:
                        st.markdown("**Emerging Opportunities**")
                        for opp in trends.get("emerging_opportunities", []):
                            st.markdown(f"""
                            • **{opp['opportunity']}**
                              - Potential: {opp['potential']}
                              - Timeline: {opp['timeline']}
                            """)

        # Success Rates Sub-tab
        with trend_tabs[1]:
            st.markdown("### 📈 Success Rates Analysis")
            if trends:
                st.markdown("#### Funding Cycles")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Peak Application Months**")
                    for month in trends.get("funding_cycles", {}).get("peak_months", []):
                        st.markdown(f"• {month}")
                with col2:
                    st.markdown("**Success Factors**")
                    for factor in trends.get("success_factors", []):
                        st.markdown(f"• {factor}")

        # Market Analysis Sub-tab
        with trend_tabs[2]:
            st.markdown("### 🌍 Market Analysis")
            if trends:
                st.markdown("#### Emerging Opportunities")
                for opp in trends.get("emerging_opportunities", []):
                    st.markdown(f"• {opp}")

                # Add opportunity heatmap
                if opportunities:
                    st.markdown("#### Funding Distribution")
                    funding_agent.generate_opportunity_heatmap(opportunities)

    # Regional Insights Tab
    with main_tabs[2]:
        st.markdown("### 🌐 Regional Funding Landscape")
        if selected_region != "Global":
            with st.spinner(f"Getting insights for {selected_region}..."):
                insights = funding_agent.get_regional_insights(selected_region)

            if insights:
                st.markdown(f"**Total Available Funding:** {insights['total_funding_available']}")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### Key Organizations")
                    for org in insights.get("key_organizations", []):
                        st.markdown(f"• {org}")

                with col2:
                    st.markdown("#### Regional Priorities")
                    for priority in insights.get("regional_priorities", []):
                        st.markdown(f"• {priority}")

                st.markdown("#### Upcoming Deadlines")
                for deadline in insights.get("upcoming_deadlines", []):
                    st.markdown(f"• **{deadline['program']}**")
                    st.markdown(f"  - Deadline: {deadline['deadline']}")
                    st.markdown(f"  - Amount: {deadline['amount']}")