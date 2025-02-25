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
                            {"area": "area name", "growth_rate": 15.5, "funding_volume": 1000000}
                        ],
                        "top_funders": [
                            {"name": "funder name", "focus_areas": ["area1", "area2"], "typical_amount": "amount range", "success_rate": 85}
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
                            "market_size": "$500B",
                            "growth_rate": "15%",
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
                        "sector_success_rates": {
                            "analysis": "Detailed analysis of success rates across sectors",
                            "rates": {
                                "Healthcare": 75,
                                "Technology": 65,
                                "Energy": 55,
                                "Manufacturing": 45,
                                "Agriculture": 40
                            },
                            "key_factors": [
                                {"factor": "Market Demand", "impact": "High"},
                                {"factor": "Technical Feasibility", "impact": "Medium"},
                                {"factor": "Competition Level", "impact": "High"}
                            ],
                            "recommendations": [
                                "recommendation1",
                                "recommendation2",
                                "recommendation3"
                            ]
                        },
                        "success_factors": ["factor1", "factor2"]
                    }
                    Note: growth_rate should be a float number (e.g. 15.5 for 15.5%)
                    funding_volume should be an integer representing the amount in dollars
                    success_rate should be an integer percentage (e.g. 85 for 85%)
                    All numerical values in distributions should be integers"""
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
                    "content": f"""Analyze funding landscape for {region}. Provide insights in the following JSON structure:
                {{
                    "overview": "Brief overview of funding landscape in the region",
                    "total_funding": "Total funding amount in billions",
                    "key_sectors": ["sector1", "sector2", "sector3"],
                    "top_funds": [
                        {{"name": "Fund name", "focus": "Main focus area", "typical_grant": "Average grant size"}}
                    ],
                    "funding_trends": [
                        {{"trend": "Trend description", "impact": "High/Medium/Low"}}
                    ]
                }}
                Keep it realistic and focused on current market conditions.
                """
                }],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error getting regional insights: {str(e)}")
            return {
                "overview": "Data currently unavailable",
                "total_funding": "N/A",
                "key_sectors": [],
                "top_funds": [],
                "funding_trends": []
            }

    def generate_opportunity_heatmap(self, opportunities: List[Dict]) -> None:
        """Generate a heatmap visualization of funding opportunities."""
        try:
            # Create a summary of opportunities by potential and timeline
            summary_data = {
                "potential": [],
                "timeline": [],
                "count": []
            }

            for opp in opportunities:
                potential = opp.get("potential", "Unknown")
                timeline = opp.get("timeline", "Unknown")

                # Find if this combination already exists
                found = False
                for i in range(len(summary_data["potential"])):
                    if summary_data["potential"][i] == potential and summary_data["timeline"][i] == timeline:
                        summary_data["count"][i] += 1
                        found = True
                        break

                if not found:
                    summary_data["potential"].append(potential)
                    summary_data["timeline"].append(timeline)
                    summary_data["count"].append(1)

            # Convert to DataFrame
            df = pd.DataFrame(summary_data)

            # Create heatmap
            fig = px.density_heatmap(
                df,
                x="timeline",
                y="potential",
                z="count",
                title="Opportunity Distribution by Potential and Timeline",
                labels={
                    "timeline": "Timeline",
                    "potential": "Potential Impact",
                    "count": "Number of Opportunities"
                }
            )

            # Customize layout
            fig.update_layout(
                xaxis_title="Timeline",
                yaxis_title="Potential Impact",
                coloraxis_colorbar_title="Count"
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
                        # Convert data to proper numeric types
                        for area in trending_areas:
                            try:
                                # Ensure growth_rate and funding_volume are numeric
                                area['growth_rate'] = float(str(area['growth_rate']).replace('%', ''))
                                area['funding_volume'] = float(str(area['funding_volume']).replace('$', '').replace(',', ''))
                            except (ValueError, TypeError) as e:
                                print(f"Error converting trending area values: {e}")
                                continue

                        df_trending = pd.DataFrame(trending_areas)
                        if not df_trending.empty:
                            fig_trending = px.scatter(
                                df_trending,
                                x="growth_rate",
                                y="funding_volume",
                                size=[1] * len(df_trending),  # Use constant size instead
                                text="area",
                                title="Trending Research Areas",
                                labels={
                                    "growth_rate": "Growth Rate (%)",
                                    "funding_volume": "Funding Volume ($)",
                                    "area": "Research Area"
                                }
                            )
                            st.plotly_chart(fig_trending)
                        else:
                            st.warning("No valid trending areas data available for visualization")

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
                st.markdown("#### 🎯 Sector Success Analysis")
                sector_success = trends.get("sector_success_rates", {})

                # AI Analysis
                st.markdown("**AI Analysis**")
                st.write(sector_success.get("analysis", ""))

                # Success Rates by Sector Bar Chart
                sector_rates = sector_success.get("rates", {})
                if sector_rates:
                    fig_success = px.bar(
                        x=list(sector_rates.keys()),
                        y=list(sector_rates.values()),
                        title="Success Rates by Sector",
                        labels={"x": "Sector", "y": "Success Rate (%)"},
                        color=list(sector_rates.values()),
                        color_continuous_scale="viridis"
                    )
                    fig_success.update_layout(showlegend=False)
                    st.plotly_chart(fig_success)

                # Key Success Factors
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Key Impact Factors**")
                    for factor in sector_success.get("key_factors", []):
                        st.markdown(f"• **{factor['factor']}**: {factor['impact']} Impact")

                with col2:
                    st.markdown("**Strategic Recommendations**")
                    for rec in sector_success.get("recommendations", []):
                        st.markdown(f"• {rec}")

                # Funding Cycles
                st.markdown("#### 📅 Funding Cycles")
                cycles_col1, cycles_col2 = st.columns(2)
                with cycles_col1:
                    st.markdown("**Peak Application Months**")
                    for month in trends.get("funding_cycles", {}).get("peak_months", []):
                        st.markdown(f"• {month}")
                with cycles_col2:
                    st.markdown("**Success Factors**")
                    for factor in trends.get("success_factors", []):
                        st.markdown(f"• {factor}")

        # Market Analysis Sub-tab
        with trend_tabs[2]:
            st.markdown("### 🌍 Market Analysis")
            if trends:
                # Market Metrics
                st.markdown("#### 📊 Market Overview")
                sector_analysis = trends.get("sector_analysis", {})

                # Market metrics in columns
                metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                with metrics_col1:
                    st.metric("Market Size", sector_analysis.get("market_size", "N/A"))
                with metrics_col2:
                    st.metric("Growth Rate", sector_analysis.get("growth_rate", "N/A"))
                with metrics_col3:
                    st.metric("Key Players", len(sector_analysis.get("key_players", [])))

                # Investment Distribution Chart
                st.markdown("#### 💰 Investment Distribution")
                investment_dist = sector_analysis.get("investment_distribution", {})
                if investment_dist:
                    fig_investment = px.pie(
                        values=list(investment_dist.values()),
                        names=list(investment_dist.keys()),
                        title="Investment Distribution by Category",
                        hole=0.4  # Makes it a donut chart
                    )
                    st.plotly_chart(fig_investment)

                # Regional Distribution Chart
                st.markdown("#### 🌐 Regional Distribution")
                regional_dist = sector_analysis.get("regional_distribution", {})
                if regional_dist:
                    fig_regional = px.bar(
                        x=list(regional_dist.keys()),
                        y=list(regional_dist.values()),
                        title="Regional Market Distribution",
                        labels={"x": "Region", "y": "Market Share (%)"},
                        color=list(regional_dist.values()),
                        color_continuous_scale="viridis"
                    )
                    fig_regional.update_layout(showlegend=False)
                    st.plotly_chart(fig_regional)

                # Emerging Opportunities
                st.markdown("#### 🚀 Emerging Opportunities")
                opportunities = trends.get("emerging_opportunities", [])
                if opportunities:
                    for opp in opportunities:
                        with st.expander(f"💡 {opp['opportunity']}"):
                            st.markdown(f"""
                            - **Potential Impact:** {opp['potential']}
                            - **Timeline:** {opp['timeline']}
                            """)

                # Key Players Analysis
                st.markdown("#### 🏢 Key Market Players")
                key_players = sector_analysis.get("key_players", [])
                if key_players:
                    st.write("Major organizations shaping the market:")
                    for player in key_players:
                        st.markdown(f"• {player}")

                # Add opportunity heatmap if available
                if opportunities:
                    st.markdown("#### 🗺️ Opportunity Distribution")
                    funding_agent.generate_opportunity_heatmap(opportunities)

    # Regional Insights Tab
    with main_tabs[2]:
        st.markdown("### 🌐 Regional Funding Landscape")
        if selected_region != "Global":
            with st.spinner(f"Analyzing {selected_region}'s funding landscape..."):
                insights = funding_agent.get_regional_insights(selected_region)

                if insights:
                    st.markdown("#### Overview")
                    st.write(insights["overview"])

                    st.metric("Total Available Funding", insights["total_funding"])

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("#### Key Sectors")
                        for sector in insights["key_sectors"]:
                            st.markdown(f"• {sector}")

                    with col2:
                        st.markdown("#### Top Funds")
                        for fund in insights["top_funds"]:
                            st.markdown(f"""
                            • **{fund['name']}**
                              - Focus: {fund['focus']}
                              - Typical Grant: {fund['typical_grant']}
                            """)

                    st.markdown("#### Current Trends")
                    for trend in insights["funding_trends"]:
                        st.markdown(f"""
                        • **{trend['trend']}**
                          Impact: {trend['impact']}
                        """)