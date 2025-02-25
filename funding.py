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
        """Get funding insights for a specific region with realistic data."""
        insights = {
            "North America": {
                "total_funding_available": "$15.2B",
                "key_organizations": [
                    "National Science Foundation (NSF)",
                    "National Institutes of Health (NIH)",
                    "DARPA",
                    "Bill & Melinda Gates Foundation",
                    "Canadian Institutes of Health Research"
                ],
                "regional_priorities": [
                    "AI and Machine Learning",
                    "Climate Technology",
                    "Healthcare Innovation",
                    "Clean Energy",
                    "Quantum Computing"
                ],
                "success_stories": [
                    "AI-driven drug discovery startup secured $50M Series A",
                    "Renewable energy project received $100M government grant",
                    "Healthcare tech company expanded with $75M funding"
                ],
                "upcoming_deadlines": [
                    {"program": "NSF Innovation Corps", "deadline": "March 15, 2025", "amount": "$50,000"},
                    {"program": "NIH R01 Research Grant", "deadline": "April 5, 2025", "amount": "$250,000"},
                    {"program": "Clean Tech Innovation Fund", "deadline": "May 1, 2025", "amount": "$150,000"}
                ]
            },
            "Europe": {
                "total_funding_available": "€12.8B",
                "key_organizations": [
                    "European Research Council",
                    "Horizon Europe",
                    "European Innovation Council",
                    "German Research Foundation",
                    "French National Research Agency"
                ],
                "regional_priorities": [
                    "Green Technology",
                    "Digital Transformation",
                    "Sustainable Agriculture",
                    "Smart Cities",
                    "Circular Economy"
                ],
                "success_stories": [
                    "Green hydrogen project secured €40M EU grant",
                    "Smart city initiative received €25M funding",
                    "Agritech startup raised €30M Series B"
                ],
                "upcoming_deadlines": [
                    {"program": "EIC Accelerator", "deadline": "March 20, 2025", "amount": "€2.5M"},
                    {"program": "Horizon Europe Green Deal", "deadline": "April 15, 2025", "amount": "€1.5M"},
                    {"program": "Digital Europe Programme", "deadline": "May 10, 2025", "amount": "€500,000"}
                ]
            },
            "Asia": {
                "total_funding_available": "$10.5B",
                "key_organizations": [
                    "Asian Development Bank",
                    "Japan Science and Technology Agency",
                    "Singapore National Research Foundation",
                    "Korean Research Foundation",
                    "China Natural Science Foundation"
                ],
                "regional_priorities": [
                    "Advanced Manufacturing",
                    "5G/6G Technology",
                    "Smart Transportation",
                    "Robotics",
                    "Urban Solutions"
                ],
                "success_stories": [
                    "Robotics company secured $30M Series A",
                    "Smart manufacturing platform raised $45M",
                    "Urban mobility startup received $25M funding"
                ],
                "upcoming_deadlines": [
                    {"program": "Asian Innovation Fund", "deadline": "March 30, 2025", "amount": "$1M"},
                    {"program": "Smart City Initiative", "deadline": "April 20, 2025", "amount": "$500,000"},
                    {"program": "Tech Startup Grant", "deadline": "May 15, 2025", "amount": "$250,000"}
                ]
            },
            "Africa": {
                "total_funding_available": "$5.8B",
                "key_organizations": [
                    "African Development Bank",
                    "Tony Elumelu Foundation",
                    "African Innovation Foundation",
                    "Nigeria Science Foundation",
                    "South African Research Foundation"
                ],
                "regional_priorities": [
                    "Agricultural Innovation",
                    "Healthcare Access",
                    "Renewable Energy",
                    "Education Technology",
                    "Financial Inclusion"
                ],
                "success_stories": [
                    "Agritech platform secured $15M funding",
                    "Healthcare access project received $20M grant",
                    "EdTech startup raised $10M Series A"
                ],
                "upcoming_deadlines": [
                    {"program": "Africa Innovation Prize", "deadline": "April 1, 2025", "amount": "$100,000"},
                    {"program": "AgriTech Fund", "deadline": "May 1, 2025", "amount": "$250,000"},
                    {"program": "Healthcare Innovation Grant", "deadline": "June 1, 2025", "amount": "$150,000"}
                ]
            },
            "South America": {
                "total_funding_available": "$4.2B",
                "key_organizations": [
                    "Inter-American Development Bank",
                    "Brazilian Innovation Agency",
                    "Start-Up Chile",
                    "Argentina Research Council",
                    "Colombian Science Foundation"
                ],
                "regional_priorities": [
                    "Sustainable Agriculture",
                    "Clean Energy",
                    "Biodiversity",
                    "Social Innovation",
                    "Digital Inclusion"
                ],
                "success_stories": [
                    "Sustainable agriculture project received $12M",
                    "Clean energy initiative secured $18M funding",
                    "Social impact startup raised $8M"
                ],
                "upcoming_deadlines": [
                    {"program": "LatAm Tech Fund", "deadline": "April 10, 2025", "amount": "$200,000"},
                    {"program": "Social Impact Grant", "deadline": "May 5, 2025", "amount": "$150,000"},
                    {"program": "Green Innovation Fund", "deadline": "June 15, 2025", "amount": "$300,000"}
                ]
            },
            "Oceania": {
                "total_funding_available": "$3.5B",
                "key_organizations": [
                    "Australian Research Council",
                    "New Zealand Innovation Agency",
                    "Pacific Development Program",
                    "Commonwealth Scientific Organisation",
                    "Queensland Innovation Hub"
                ],
                "regional_priorities": [
                    "Marine Conservation",
                    "Climate Resilience",
                    "Indigenous Innovation",
                    "Agricultural Technology",
                    "Renewable Energy"
                ],
                "success_stories": [
                    "Marine tech project secured $10M grant",
                    "Climate resilience initiative received $15M",
                    "Indigenous innovation program raised $8M"
                ],
                "upcoming_deadlines": [
                    {"program": "Pacific Innovation Fund", "deadline": "April 15, 2025", "amount": "$250,000"},
                    {"program": "Marine Tech Grant", "deadline": "May 20, 2025", "amount": "$180,000"},
                    {"program": "Climate Action Fund", "deadline": "June 10, 2025", "amount": "$300,000"}
                ]
            }
        }

        return insights.get(region, {
            "total_funding_available": "N/A",
            "key_organizations": [],
            "regional_priorities": [],
            "success_stories": [],
            "upcoming_deadlines": []
        })

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

                st.markdown("#### Success Stories")
                for story in insights.get("success_stories",[]):
                    st.markdown(f"• {story}")

                st.markdown("#### Upcoming Deadlines")
                for deadline in insights.get("upcoming_deadlines", []):
                    st.markdown(f"• **{deadline['program']}**")
                    st.markdown(f"  - Deadline: {deadline['deadline']}")
                    st.markdown(f"  - Amount: {deadline['amount']}")