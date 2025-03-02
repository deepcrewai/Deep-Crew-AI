import streamlit as st
import plotly.express as px
from utils import format_citation, calculate_metrics
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
from reportlab.lib.utils import ImageReader

def generate_pdf_report(results, analysis):
    """Generate a PDF report of AI analysis."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    page_width, page_height = letter

    def add_page_footer():
        """Add date and link to bottom of page"""
        c.setFont("Helvetica", 10)
        # Add date to bottom left
        c.drawString(50, 30, datetime.now().strftime('%Y-%m-%d'))
        # Add link to bottom right
        c.setFillColorRGB(0, 0, 1)  # Blue color for link
        c.drawString(page_width - 150, 30, "deep-crew.ai")

    # Add logo to top right
    logo = ImageReader("attached_assets/deep-crew.jpg")
    c.drawImage(logo, page_width - 250, page_height - 100, width=200, preserveAspectRatio=True)

    y = page_height - 150  # Start after logo and spacing

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "AI Analysis Report")
    y -= 30

    # Date
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 40

    # Analysis Summary
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Research Summary")
    y -= 20

    c.setFont("Helvetica", 10)
    summary = analysis.get("summary", "No summary available")
    summary_lines = [summary[i:i+80] for i in range(0, len(summary), 80)]
    for line in summary_lines:
        if y < 100:  # Check if we need a new page
            add_page_footer()
            c.showPage()
            y = page_height - 50

        c.drawString(50, y, line)
        y -= 15
    y -= 20

    # Research Trends
    if y < 200:  # Ensure enough space for trends section
        add_page_footer()
        c.showPage()
        y = page_height - 50

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Research Trends")
    y -= 20

    trends = analysis.get("trends", {})
    c.setFont("Helvetica", 10)

    # Emerging Topics
    c.drawString(50, y, "Emerging Topics:")
    y -= 20
    for topic in trends.get("emerging_topics", []):
        if y < 100:
            add_page_footer()
            c.showPage()
            y = page_height - 50
        c.drawString(70, y, f"• {topic}")
        y -= 15
    y -= 20

    # Declining Topics
    c.drawString(50, y, "Declining Topics:")
    y -= 20
    for topic in trends.get("declining_topics", []):
        if y < 100:
            add_page_footer()
            c.showPage()
            y = page_height - 50
        c.drawString(70, y, f"• {topic}")
        y -= 15
    y -= 20

    # Research Gaps
    if y < 200:
        add_page_footer()
        c.showPage()
        y = page_height - 50

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Research Gaps")
    y -= 20

    c.setFont("Helvetica", 10)
    for gap in analysis.get("gaps", []):
        if y < 100:
            add_page_footer()
            c.showPage()
            y = page_height - 50
        c.drawString(70, y, f"• {gap}")
        y -= 15
    y -= 20

    # Complexity Assessment
    if y < 200:
        add_page_footer()
        c.showPage()
        y = page_height - 50

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Complexity Assessment")
    y -= 20

    c.setFont("Helvetica", 10)
    complexity = analysis.get("complexity", {})
    score = complexity.get("complexity_score", 0)
    c.drawString(50, y, f"Complexity Score: {score}/10")
    y -= 15

    explanation = complexity.get("explanation", "No explanation available")
    explanation_lines = [explanation[i:i+80] for i in range(0, len(explanation), 80)]
    for line in explanation_lines:
        if y < 100:
            add_page_footer()
            c.showPage()
            y = page_height - 50
        c.drawString(50, y, line)
        y -= 15

    # Add footer to the last page
    add_page_footer()

    c.save()
    buffer.seek(0)
    return buffer

def generate_patent_pdf_report(results, analysis):
    """Generate a PDF report of patent analysis."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    page_width, page_height = letter

    def add_page_footer():
        """Add date and link to bottom of page"""
        c.setFont("Helvetica", 10)
        c.drawString(50, 30, datetime.now().strftime('%Y-%m-%d'))
        c.setFillColorRGB(0, 0, 1)
        c.drawString(page_width - 150, 30, "deep-crew.ai")

    # Add logo
    logo = ImageReader("attached_assets/deep-crew.jpg")
    c.drawImage(logo, page_width - 250, page_height - 100, width=200, preserveAspectRatio=True)

    y = page_height - 150

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Patent Analysis Report")
    y -= 30

    # Date
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 40

    # Overview
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Overview")
    y -= 20

    c.setFont("Helvetica", 10)
    summary = analysis.get("summary", "No summary available")
    summary_lines = [summary[i:i+80] for i in range(0, len(summary), 80)]
    for line in summary_lines:
        if y < 100:
            add_page_footer()
            c.showPage()
            y = page_height - 50
        c.drawString(50, y, line)
        y -= 15
    y -= 20

    # Patents
    if y < 200:
        add_page_footer()
        c.showPage()
        y = page_height - 50

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Patents")
    y -= 20

    for patent in results:
        if y < 200:
            add_page_footer()
            c.showPage()
            y = page_height - 50

        c.setFont("Helvetica-Bold", 10)
        title = patent.get('title', 'Untitled Patent')
        title_lines = [title[i:i+80] for i in range(0, len(title), 80)]
        for line in title_lines:
            c.drawString(50, y, line)
            y -= 15

        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"ID: {patent.get('patent_id', 'N/A')}")
        y -= 15
        c.drawString(50, y, f"Inventors: {patent.get('inventors', 'N/A')}")
        y -= 15
        c.drawString(50, y, f"Filing Date: {patent.get('filing_date', 'N/A')}")
        y -= 20

        abstract = patent.get('abstract', 'No abstract available')
        abstract_lines = [abstract[i:i+80] for i in range(0, len(abstract), 80)]
        for line in abstract_lines:
            if y < 100:
                add_page_footer()
                c.showPage()
                y = page_height - 50
            c.drawString(50, y, line)
            y -= 15
        y -= 20

    # Add footer to the last page
    add_page_footer()
    c.save()
    buffer.seek(0)
    return buffer

def render_search_section(results):
    """Render the modernized search results section."""
    # Display results count separately to ensure proper rendering
    results_count = len(results) if results else 0
    st.markdown("""
        <style>
        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 2rem 0 1rem;
        }
        .results-title {
            font-size: 2rem;
            font-weight: 600;
            color: #202124;
            margin-bottom: 1.5rem;
        }
        .filter-container {
            display: flex;
            gap: 1rem;
            align-items: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create columns for the header: title and filters
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown(
            f'<div class="results-title">Search Results ({results_count})</div>',
            unsafe_allow_html=True
        )

    with col2:
        with st.expander("🔍 Filter Results"):
            # Year range filter
            min_year = min([p.get('publication_year', 2025) for p in results]) if results else 2000
            max_year = max([p.get('publication_year', 2025) for p in results]) if results else 2025

            year_range = st.slider(
                "Publication Year",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year)
            )

            # Citations range filter
            max_citations = max([p.get('cited_by_count', 0) for p in results]) if results else 100
            citation_range = st.slider(
                "Citations",
                min_value=0,
                max_value=max_citations,
                value=(0, max_citations)
            )

            # Similarity score filter
            similarity_range = st.slider(
                "Similarity Score",
                min_value=0.0,
                max_value=1.0,
                value=(0.0, 1.0),
                step=0.01,
                help="Filter papers based on their relevance to your search query"
            )

    with col3:
        with st.expander("📊 Sort By"):
            sort_option = st.selectbox(
                "Sort papers by",
                options=["Similarity Score", "Citations", "Publication Year"],
                index=0,
                label_visibility="collapsed"
            )

    # Filter results based on selected ranges
    filtered_results = [
        paper for paper in results
        if (paper.get('publication_year', 0) >= year_range[0] and 
            paper.get('publication_year', 0) <= year_range[1] and
            paper.get('cited_by_count', 0) >= citation_range[0] and
            paper.get('cited_by_count', 0) <= citation_range[1] and
            paper.get('similarity_score', 0) >= similarity_range[0] and
            paper.get('similarity_score', 0) <= similarity_range[1])
    ]

    # Sort filtered results based on selected option
    if sort_option == "Similarity Score":
        filtered_results.sort(key=lambda x: (-x.get('similarity_score', 0)))
    elif sort_option == "Citations":
        filtered_results.sort(key=lambda x: (-x.get('cited_by_count', 0)))
    else:  # Publication Year
        filtered_results.sort(key=lambda x: (-x.get('publication_year', 0)))

    # Modern paper cards style
    st.markdown("""
        <style>
        .paper-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            transition: all 0.2s ease;
        }
        .paper-card:hover {
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        }
        .paper-title {
            font-size: 1.1rem;
            font-weight: 500;
            color: #202124;
            margin-bottom: 0.5rem;
        }
        .paper-authors {
            font-size: 0.9rem;
            color: #5f6368;
            margin-bottom: 0.5rem;
        }
        .paper-citation {
            font-size: 0.9rem;
            color: #5f6368;
            margin-bottom: 1rem;
        }
        .paper-abstract {
            font-size: 0.95rem;
            color: #202124;
            line-height: 1.5;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .paper-metrics {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
            font-size: 0.9rem;
            color: #5f6368;
        }
        .paper-link {
            color: #1a73e8;
            text-decoration: none;
        }
        .paper-link:hover {
            text-decoration: underline;
        }
        .info-icon {
            cursor: pointer;
            color: #5f6368;
            font-size: 0.9rem;
            margin-left: 4px;
            position: relative;
            display: inline-block;
        }
        .info-tooltip {
            visibility: hidden;
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            bottom: 100%;
            background: white;
            border: 1px solid #ddd;
            padding: 8px 12px;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            width: 300px;
            z-index: 1000;
            margin-bottom: 8px;
            text-align: left;
            white-space: normal;
        }
        .info-icon:hover .info-tooltip {
            visibility: visible;
        }
        .copy-button {
            background: #ffffff;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 2px 8px;
            font-size: 0.8em;
            color: #666;
            cursor: pointer;
            margin-left: 8px;
        }
        .copy-button:hover {
            background: #f5f5f5;
            border-color: #999;
        }
        </style>
        <script>
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                console.log('Copying to clipboard was successful!');
            }, function(err) {
                console.error('Could not copy text: ', err);
            });
        }
        </script>
    """, unsafe_allow_html=True)

    # Display filtered papers
    for paper in filtered_results:
        # Get authors from authorships
        authors = []
        for authorship in paper.get('authorships', []):
            if 'author' in authorship and 'display_name' in authorship['author']:
                authors.append(authorship['author']['display_name'])
        authors_str = ', '.join(authors) if authors else 'Unknown Authors'

        # Get abstract with proper fallback
        abstract = paper.get('abstract')
        if not abstract or abstract.lower() == 'none' or abstract.strip() == '':
            abstract = """No abstract is available for this publication. 
            You can access more information about this research by clicking the 'View Paper' link below."""

        similarity = paper.get('similarity_score', 0)

        st.markdown(f"""
            <div class="paper-card">
                <div class="paper-title">{paper.get('title', 'Untitled')}</div>
                <div class="paper-authors">Authors: {authors_str}</div>
                <div class="paper-citation">{format_citation(paper)}</div>
                <div class="paper-abstract">{abstract}</div>
                <div class="paper-metrics">
                    <span>
                        Similarity Score: {similarity:.2f}
                        <div class="info-icon">ℹ️
                            <div class="info-tooltip">
                                The Similarity Score (0-1) indicates how well this paper matches your search query.
                                A higher score means the paper is more relevant to your search terms.
                                The score considers both title (70%) and abstract (30%) matches.
                            </div>
                        </div>
                    </span>
                    <span>Citations: {paper.get('cited_by_count', 0)}</span>
                    {f'<a href="{paper["url"]}" class="paper-link" target="_blank">View Paper</a>' if paper.get("url") and paper["url"] is not None else ""}
                </div>
            </div>
        """, unsafe_allow_html=True)

def render_patent_results(results, analysis):
    """Render patent search results with export functionality."""
    # Initialize sort option in session state if not exists
    if 'patent_sort_option' not in st.session_state:
        st.session_state.patent_sort_option = "Date (Newest)"

    # Create columns for the header and sort dropdown
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader(f"Document Results({len(results)})")

    with col2:
        # Use session state to maintain sort selection
        st.session_state.patent_sort_option = st.selectbox(
            "Sort By",
            options=["Date (Newest)", "Date (Oldest)"],
            key="patent_sort_dropdown",
            label_visibility="collapsed",
            index=["Date (Newest)", "Date (Oldest)"].index(st.session_state.patent_sort_option)
        )

    # Sort results based on selection
    sorted_results = list(results)  # Create a copy to avoid modifying original
    if st.session_state.patent_sort_option == "Date (Newest)":
        sorted_results.sort(key=lambda x: x.get('filing_date', ''), reverse=True)
    elif st.session_state.patent_sort_option == "Date (Oldest)":
        sorted_results.sort(key=lambda x: x.get('filing_date', ''))

    # Display patents
    for patent in sorted_results:
        with st.expander(f"📄 {patent.get('title', 'Untitled Patent')}"):
            st.write("**ID:**")
            st.code(patent.get('patent_id', 'N/A'), language='text')  # This makes the ID easily selectable and adds a copy button

            st.markdown(f"""
            **Inventors:** {patent.get('inventors', 'N/A')}  
            **Filing Date:** {patent.get('filing_date', 'N/A')}

            {patent.get('abstract', 'No abstract available')}

            {f"[View Details]({patent['url']})" if patent.get('url') else ''}
            """)

def render_analysis_section(analysis):
    """Render the AI analysis section."""
    # Header with export button
    col1, col2 = st.columns([2, 1])
    with col1:
        st.header("AI Analysis")
    with col2:
        st.download_button(
            label="📑 Export Analysis as PDF",
            data=generate_pdf_report([], analysis),
            file_name="research_analysis.pdf",
            mime="application/pdf",
            key="pdf_download"
        )

    # Summary
    st.subheader("Research Summary")
    st.write(analysis.get("summary", "No summary available"))

    # Trends
    st.subheader("Research Trends")
    trends = analysis.get("trends", {})
    col1, col2 = st.columns(2)
    with col1:
        st.write("Emerging Topics")
        for topic in trends.get("emerging_topics", []):
            st.write(f"• {topic}")
    with col2:
        st.write("Declining Topics")
        for topic in trends.get("declining_topics", []):
            st.write(f"• {topic}")

    # Research Gaps
    if analysis.get("opportunities"):
        st.subheader("Opportunities")
        for opportunity in analysis.get("opportunities", []):
            st.write(f"• {opportunity}")

    # Competition Analysis
    if analysis.get("competition"):
        st.subheader("Competition Analysis")
        st.write(analysis.get("competition", "No competition analysis available"))

    # Keyword Suggestions
    if analysis.get("keywords"):
        st.subheader("Keyword Suggestions")
        st.write("Consider using these keywords to refine your search:")
        keywords = analysis.get("keywords", [])
        if keywords:
            cols = st.columns(3)
            for i, keyword in enumerate(keywords):
                cols[i % 3].write(f"• {keyword}")

    # Complexity Assessment
    if analysis.get("complexity"):
        st.subheader("Complexity Assessment")
        complexity = analysis.get("complexity", {})
        score = complexity.get("complexity_score", 0)
        st.progress(score / 10)
        st.write(f"Complexity Score: {score}/10")
        st.write(complexity.get("explanation", "No explanation available"))

def handle_pdf_export(results, analysis):
    """This function is now deprecated as the export functionality has been moved to render_search_section"""
    pass

def render_combined_results(research_results, patent_results, combined_analysis):
    """Render enhanced combined analysis of research and patent results."""
    st.header("Comprehensive Analysis")

    # Summary
    st.subheader("Overview")
    st.write(combined_analysis.get("comprehensive_summary", "No summary available"))

    # Key Findings with Impact Scores
    st.subheader("Key Findings")
    findings = combined_analysis.get("key_findings", [])
    for finding in findings:
        with st.expander(f"🔍 Finding (Impact Score: {finding.get('impact_score', 'N/A')}/10)"):
            st.write(finding.get('finding', ''))
            st.write("**Evidence:**", finding.get('evidence', ''))

    # Research-Patent Alignment
    st.subheader("Research & Patent Alignment")
    alignment = combined_analysis.get("research_patent_alignment", {})
    st.write(alignment.get("overview", "No alignment analysis available"))

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Gaps:**")
        for gap in alignment.get("gaps", []):
            st.markdown(f"• {gap}")
    with col2:
        st.write("**Opportunities:**")
        for opp in alignment.get("opportunities", []):
            st.markdown(f"• {opp}")

    # Technology Assessment
    st.subheader("Technology Assessment")
    tech_assessment = combined_analysis.get("technology_assessment", {})
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Technology Readiness", f"{tech_assessment.get('readiness_score', 0)}/10")
        st.write("**Maturity Level:**", tech_assessment.get("maturity_level", "Unknown"))
    with col2:
        st.write("**Development Stages:**")
        for stage in tech_assessment.get("development_stages", []):
            st.markdown(f"• {stage}")

    # Innovation Opportunities
    st.subheader("Innovation Opportunities")
    for opp in combined_analysis.get("innovation_opportunities", []):
        with st.expander(f"💡 {opp.get('opportunity', 'Opportunity')} ({opp.get('potential_impact', 'N/A')} impact)"):
            st.write(f"**Implementation Timeline:** {opp.get('implementation_timeline', 'N/A')}")
            st.write(f"**Required Resources:** {opp.get('required_resources', 'N/A')}")

    # Risk Analysis
    st.subheader("Risk Analysis")
    risks = combined_analysis.get("risk_analysis", {})
    tab1, tab2, tab3 = st.tabs(["Technical Risks", "Market Risks", "Mitigation Strategies"])

    with tab1:
        for risk in risks.get("technical_risks", []):
            st.markdown(f"• {risk}")
    with tab2:
        for risk in risks.get("market_risks", []):
            st.markdown(f"• {risk}")
    with tab3:
        for strategy in risks.get("mitigation_strategies", []):
            st.markdown(f"• {strategy}")

    # Investment Recommendations
    st.subheader("Investment Recommendations")
    for rec in combined_analysis.get("investment_recommendations", []):
        with st.expander(f"💰 {rec.get('area', 'Investment Area')} (ROI: {rec.get('potential_roi', 'N/A')})"):
            st.write(f"**Timeframe:** {rec.get('timeframe', 'N/A')}")
            st.write(f"**Required Investment:** {rec.get('required_investment', 'N/A')}")

    # Future Directions
    st.subheader("Future Directions")
    for direction in combined_analysis.get("future_directions", []):
        with st.expander(f"🔮 {direction.get('direction', 'Direction')} (Probability: {direction.get('probability', 'N/A')}/10)"):
            st.write(f"**Impact:** {direction.get('impact', 'N/A')}")
            st.write(f"**Timeline:** {direction.get('timeline', 'N/A')}")

    # Collaboration Opportunities
    st.subheader("Collaboration Opportunities")
    for collab in combined_analysis.get("collaboration_opportunities", []):
        with st.expander(f"🤝 {collab.get('type', 'Collaboration')}"):
            st.write("**Potential Partners:**")
            for partner in collab.get("potential_partners", []):
                st.markdown(f"• {partner}")
            st.write("**Expected Benefits:**")
            for benefit in collab.get("expected_benefits", []):
                st.markdown(f"• {benefit}")

    # Industry Implications
    st.subheader("Industry Implications")
    implications = combined_analysis.get("industry_implications", {})

    st.write("**Affected Sectors:**")
    cols = st.columns(3)
    sectors = implications.get("affected_sectors", [])
    for i, sector in enumerate(sectors):
        cols[i % 3].markdown(f"• {sector}")

    st.write("**Impact Analysis:**")
    for impact in implications.get("impact_analysis", []):
        st.markdown(f"• {impact}")

    st.write("**Adaptation Strategies:**")
    for strategy in implications.get("adaptation_strategies", []):
        st.markdown(f"• {strategy}")

    # Statistics
    st.subheader("Document Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Research Papers", len(research_results))
    with col2:
        st.metric("Documents", len(patent_results))
    with col3:
        total_documents = len(research_results) + len(patent_results)
        st.metric("Total Documents", total_documents)

    if st.session_state.get('patent_results'):
        patent_tab, analysis_tab = st.tabs(["Documents", "AI Analysis"])

        with patent_tab:
            render_patent_results(st.session_state.patent_results, st.session_state.patent_analysis)

        with analysis_tab:
            if st.session_state.get('patent_analysis'):
                render_analysis_section(st.session_state.patent_analysis)