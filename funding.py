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
        self.analysis_prompt = """As an AI funding analyst, provide detailed insights for the following data.
        Focus on:
        - Key trends and patterns
        - Success factors and risks
        - Strategic recommendations
        - Market dynamics and competitive analysis
        - Future outlook and opportunities
        Return analysis in JSON format with 'summary', 'key_points', and 'recommendations' fields."""

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
        insights = {
            "North America": {
                "overview": "North America leads in technological innovation and research funding, with strong emphasis on AI, biotech, and clean energy.",
                "total_funding": "$15.2B",
                "funding_distribution": {
                    "Research Grants": 35,
                    "Venture Capital": 30,
                    "Government Funding": 20,
                    "Corporate Innovation": 10,
                    "Other Sources": 5
                },
                "key_sectors": [
                    "Artificial Intelligence",
                    "Biotechnology",
                    "Clean Energy",
                    "Digital Health",
                    "Space Technology"
                ],
                "sector_growth": [
                    {"sector": "AI/ML", "growth_rate": 28.5},
                    {"sector": "Biotech", "growth_rate": 22.3},
                    {"sector": "Clean Energy", "growth_rate": 18.7},
                    {"sector": "Digital Health", "growth_rate": 15.9},
                    {"sector": "Space Tech", "growth_rate": 12.4}
                ],
                "success_metrics": {
                    "average_success_rate": 75,
                    "total_projects_funded": 2800,
                    "average_funding_size": "$2.5M",
                    "yoy_growth": 18
                }
            },
            "Europe": {
                "overview": "European funding landscape emphasizes sustainable development, digital transformation, and cross-border collaboration.",
                "total_funding": "$12.8B",
                "funding_distribution": {
                    "EU Programs": 40,
                    "National Funding": 25,
                    "Private Investment": 20,
                    "Research Institutes": 10,
                    "Other Sources": 5
                },
                "key_sectors": [
                    "Green Technology",
                    "Digital Innovation",
                    "Health Sciences",
                    "Smart Cities",
                    "Sustainable Agriculture"
                ],
                "sector_growth": [
                    {"sector": "Green Tech", "growth_rate": 24.5},
                    {"sector": "Digital Innovation", "growth_rate": 20.8},
                    {"sector": "Health Sciences", "growth_rate": 16.9},
                    {"sector": "Smart Cities", "growth_rate": 14.2},
                    {"sector": "Sustainable Ag", "growth_rate": 12.1}
                ],
                "success_metrics": {
                    "average_success_rate": 70,
                    "total_projects_funded": 2400,
                    "average_funding_size": "$2.1M",
                    "yoy_growth": 15
                }
            },
            "Asia": {
                "overview": "Asia shows rapid growth in tech innovation funding, with strong focus on digital transformation and smart manufacturing.",
                "total_funding": "$10.5B",
                "funding_distribution": {
                    "Government Initiatives": 35,
                    "Private Sector": 30,
                    "International Funding": 20,
                    "Research Grants": 10,
                    "Other Sources": 5
                },
                "key_sectors": [
                    "Advanced Manufacturing",
                    "Digital Commerce",
                    "Smart Cities",
                    "Fintech",
                    "Robotics"
                ],
                "sector_growth": [
                    {"sector": "Advanced Mfg", "growth_rate": 26.7},
                    {"sector": "Digital Commerce", "growth_rate": 23.4},
                    {"sector": "Smart Cities", "growth_rate": 19.8},
                    {"sector": "Fintech", "growth_rate": 17.2},
                    {"sector": "Robotics", "growth_rate": 15.5}
                ],
                "success_metrics": {
                    "average_success_rate": 68,
                    "total_projects_funded": 2200,
                    "average_funding_size": "$1.8M",
                    "yoy_growth": 22
                }
            }
        }

        if region == "Global":
            # Calculate global metrics
            total_funding = 38.5  # Sum of all regions
            total_projects = sum(reg["success_metrics"]["total_projects_funded"] for reg in insights.values())
            avg_success_rate = sum(reg["success_metrics"]["average_success_rate"] for reg in insights.values()) / len(insights)

            # Combine all sector growth data
            all_sector_growth = []
            for reg in insights.values():
                all_sector_growth.extend(reg["sector_growth"])

            # Calculate average funding distribution
            global_distribution = {
                "Research & Grants": 30,
                "Venture Capital": 25,
                "Government Funding": 20,
                "Corporate Innovation": 15,
                "International Funding": 10
            }

            return {
                "overview": "Global funding landscape shows strong growth across all regions, with particular emphasis on technological innovation, sustainability, and digital transformation. North America leads in total funding, while Asia shows the highest growth rates.",
                "total_funding": f"${total_funding}B",
                "funding_distribution": global_distribution,
                "key_sectors": [
                    "Artificial Intelligence",
                    "Clean Technology",
                    "Digital Transformation",
                    "Healthcare Innovation",
                    "Smart Infrastructure"
                ],
                "sector_growth": [
                    {"sector": "AI & Digital", "growth_rate": 25.5},
                    {"sector": "Clean Tech", "growth_rate": 22.8},
                    {"sector": "Healthcare", "growth_rate": 18.9},
                    {"sector": "Smart Cities", "growth_rate": 16.5},
                    {"sector": "Fintech", "growth_rate": 15.2}
                ],
                "success_metrics": {
                    "average_success_rate": round(avg_success_rate),
                    "total_projects_funded": total_projects,
                    "average_funding_size": "$2.1M",
                    "yoy_growth": 18
                }
            }

        return insights.get(region, {
            "overview": "Data not available for this region",
            "total_funding": "N/A",
            "funding_distribution": {
                "Category 1": 0,
                "Category 2": 0,
                "Category 3": 0
            },
            "key_sectors": [],
            "sector_growth": [],
            "success_metrics": {
                "average_success_rate": 0,
                "total_projects_funded": 0,
                "average_funding_size": "N/A",
                "yoy_growth": 0
            }
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

    def analyze_with_ai(self, data: Dict) -> Dict:
        """Perform AI analysis on funding data."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.analysis_prompt},
                    {"role": "user", "content": json.dumps(data)}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error in AI analysis: {str(e)}")
            return {
                "summary": "AI analysis unavailable",
                "key_points": [],
                "recommendations": []
            }


def render_funding_section(research_query: str):
    """Render the funding section in the Streamlit app."""
    funding_agent = FundingAgent()

    st.markdown("""
        <div class='results-container'>
            <h2>💰 Funding Analysis</h2>
    """, unsafe_allow_html=True)

    # Region selection
    regions = [
        "Global",
        "North America",
        "Europe",
        "Asia",
        "Africa",
        "South America",
        "Oceania",
        "Middle East",
        "Southeast Asia"
    ]
    selected_region = st.selectbox("Select Region", regions)

    # Main tabs
    main_tabs = st.tabs(["Funding Opportunities", "Funding Trends", "Regional Insights"])

    # Funding Opportunities Tab
    with main_tabs[0]:
        st.markdown("""
            <div class='content-section'>
                <h3>Available Opportunities</h3>
            </div>
        """, unsafe_allow_html=True)
        with st.spinner("🔍 Finding and analyzing funding opportunities..."):
            opportunities = funding_agent.get_funding_opportunities(research_query, selected_region)

            if opportunities:
                # AI Analysis of opportunities
                ai_analysis = funding_agent.analyze_with_ai({
                    "opportunities": opportunities,
                    "context": {"query": research_query, "region": selected_region}
                })

                # Display AI Insights
                st.markdown("### 🤖 AI Analysis")
                st.markdown(f"**Summary:** {ai_analysis.get('summary', 'No summary available')}")

                with st.expander("📊 Key Insights"):
                    for point in ai_analysis.get('key_points', []):
                        st.markdown(f"• {point}")

                with st.expander("🎯 Strategic Recommendations"):
                    for rec in ai_analysis.get('recommendations', []):
                        st.markdown(f"• {rec}")

                st.markdown("### 📑 Available Opportunities")
                for opp in opportunities:
                    with st.expander(f"{opp['title']} - {opp['funder']}"):
                        st.markdown(f"""
                            **Amount:** {opp['amount']}  
                            **Deadline:** {opp['deadline']}  
                            **Eligibility:** {opp['eligibility']}  
                            **Success Rate:** {opp['success_rate']}  
                            **Priority Level:** {opp['priority_level']}  
                            **[Apply Now]({opp['link']})**
                        """)

    # Funding Trends Tab
    with main_tabs[1]:
        trend_tabs = st.tabs(["Sector Analysis", "Success Rates", "Market Analysis"])

        # Sector Analysis Sub-tab
        with trend_tabs[0]:
            st.markdown("""
                <div class='content-section'>
                    <h3>📊 Sector Analysis</h3>
                </div>
            """, unsafe_allow_html=True)
            with st.spinner("Analyzing sector trends with AI..."):
                trends = funding_agent.analyze_funding_trends(research_query)

                if trends:
                    # AI Analysis
                    ai_sector_analysis = funding_agent.analyze_with_ai({
                        "trends": trends,
                        "context": {"query": research_query}
                    })

                    # Display AI Analysis
                    st.markdown("#### 🤖 AI Insights")
                    st.markdown(f"**Market Analysis:** {ai_sector_analysis.get('summary', 'No analysis available')}")

                    with st.expander("🔍 Detailed Analysis"):
                        for point in ai_sector_analysis.get('key_points', []):
                            st.markdown(f"• {point}")

                    with st.expander("📈 Growth Strategies"):
                        for rec in ai_sector_analysis.get('recommendations', []):
                            st.markdown(f"• {rec}")

                    # Existing metrics and charts remain unchanged
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
                            title="Investment Distribution by Category",
                            hole=0.4
                        )
                        st.plotly_chart(fig_investment)

                    # Regional Distribution Chart
                    st.markdown("#### 🌍 Regional Distribution")
                    regional_data = sector_analysis.get("regional_distribution", {})
                    if regional_data:
                        fig_regional = px.bar(
                            x=list(regional_data.keys()),
                            y=list(regional_data.values()),
                            title="Regional Market Distribution",
                            labels={"x": "Region", "y": "Market Share (%)"},
                            color=list(regional_data.values()),
                            color_continuous_scale="viridis"
                        )
                        st.plotly_chart(fig_regional)

        # Success Rates Sub-tab
        with trend_tabs[1]:
            st.markdown("""
                <div class='content-section'>
                    <h3>📈 Success Rates Analysis</h3>
                </div>
            """, unsafe_allow_html=True)
            if trends:
                sector_success = trends.get("sector_success_rates", {})

                # AI Analysis
                st.markdown("**AI Analysis**")
                st.write(sector_success.get("analysis", ""))

                # Success Rates Chart
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
                    st.plotly_chart(fig_success)

        # Market Analysis Sub-tab
        with trend_tabs[2]:
            st.markdown("""
                <div class='content-section'>
                    <h3>🌍 Market Analysis</h3>
                </div>
            """, unsafe_allow_html=True)
            if trends:
                sector_analysis = trends.get("sector_analysis", {})

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### Key Insights")
                    st.write(sector_analysis.get("overview", ""))

                with col2:
                    st.markdown("#### Market Metrics")
                    st.metric("Market Size", sector_analysis.get("market_size", "N/A"))
                    st.metric("Growth Rate", sector_analysis.get("growth_rate", "N/A"))

    # Regional Insights Tab
    with main_tabs[2]:
        st.markdown("""
            <div class='content-section'>
                <h3>🌐 Regional Funding Landscape</h3>
            </div>
        """, unsafe_allow_html=True)
        with st.spinner(f"Analyzing {selected_region}'s funding landscape..."):
            insights = funding_agent.get_regional_insights(selected_region)

            if insights:
                # Overview and Total Funding
                st.markdown("#### 📊 Market Overview")
                st.write(insights["overview"])

                # Success Metrics in columns
                metrics = insights.get("success_metrics", {})
                met_col1, met_col2, met_col3, met_col4 = st.columns(4)
                with met_col1:
                    st.metric("Success Rate", f"{metrics.get('average_success_rate', 0)}%")
                with met_col2:
                    st.metric("Projects Funded", metrics.get('total_projects_funded', 0))
                with met_col3:
                    st.metric("Avg Funding", metrics.get('average_funding_size', 'N/A'))
                with met_col4:
                    st.metric("YoY Growth", f"{metrics.get('yoy_growth', 0)}%")

                # Funding Distribution Pie Chart
                st.markdown("#### 💰 Funding Distribution")
                dist_data = insights.get("funding_distribution", {})
                if dist_data:
                    fig_dist = px.pie(
                        values=list(dist_data.values()),
                        names=list(dist_data.keys()),
                        title="Funding Sources Distribution",
                        hole=0.4
                    )
                    st.plotly_chart(fig_dist)

                # Sector Growth Bar Chart
                st.markdown("#### 📈 Sector Growth Rates")
                sector_growth = insights.get("sector_growth", [])
                if sector_growth:
                    fig_growth = px.bar(
                        sector_growth,
                        x="sector",
                        y="growth_rate",
                        title="Growth Rates by Sector",
                        labels={"sector": "Sector", "growth_rate": "Growth Rate (%)"},
                        color="growth_rate",
                        color_continuous_scale="viridis"
                    )
                    st.plotly_chart(fig_growth)

                # Key Information in Columns
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 🎯 Key Sectors")
                    for sector in insights.get("key_sectors", []):
                        st.markdown(f"• {sector}")

                with col2:
                    st.markdown("#### 🔄 Market Trends")
                    trends = [
                        "Growing investment in research and development",
                        "Increased focus on sustainable technologies",
                        "Rising cross-border collaborations",
                        "Emphasis on digital transformation"
                    ]
                    for trend in trends:
                        st.markdown(f"• {trend}")

    st.markdown("</div>", unsafe_allow_html=True)