import streamlit as st
import plotly.express as px
from utils import format_citation, calculate_metrics
from openai import OpenAI
import os
import json
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
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

def render_patent_results(results, analysis, context="standalone"):
    """Render patent search results with export functionality."""
    # Create columns for the header and sort dropdown
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader(f"Document Results({len(results)})")

    with col2:
        sort_option = st.selectbox(
            "Sort By",
            options=["Date (Newest)", "Date (Oldest)"],
            key=f"patent_sort_option_{context}",
            label_visibility="collapsed"
        )

    with col3:
        if analysis:  # Only show export button if we have analysis
            st.download_button(
                label="📑 Export Patent Analysis",
                data=generate_patent_pdf_report(results, analysis),
                file_name="patent_analysis.pdf",
                mime="application/pdf",
                key=f"patent_pdf_download_{context}"  # Make key unique based on context
            )

    # Sort results based on selection
    sorted_results = list(results)  # Create a copy to avoid modifying original
    if sort_option == "Date (Newest)":
        sorted_results.sort(key=lambda x: x.get('filing_date', ''), reverse=True)
    elif sort_option == "Date (Oldest)":
        sorted_results.sort(key=lambda x: x.get('filing_date', ''))

    # Display patents
    for patent in sorted_results:
        with st.expander(f"📄 {patent.get('title', 'Untitled Patent')}"):
            st.write("**ID:**")
            st.code(patent.get('patent_id', 'N/A'), language='text')

            st.markdown(f"""
            **Inventors:** {patent.get('inventors', 'N/A')}  
            **Filing Date:** {patent.get('filing_date', 'N/A')}

            {patent.get('abstract', 'No abstract available')}

            {f"[View Details]({patent['url']})" if patent.get('url') else ''}
            """)

def render_analysis_section(analysis, section_type="research"):
    """Render the AI analysis section."""
    # Header with export button
    col1, col2 = st.columns([2, 1])
    with col1:
        st.header("AI Analysis")
    with col2:
        st.download_button(
            label="📑 Export Analysis as PDF",
            data=generate_pdf_report(
                st.session_state.get('search_results' if section_type.startswith("research") else 'patent_results', []),
                analysis
            ),
            file_name=f"{section_type}_analysis.pdf",
            mime="application/pdf",
            key=f"{section_type}_analysis_pdf_download"  # Make key unique based on section type
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

def handle_pdf_export(results, analysis):
    """This function is now deprecated as the export functionality has been moved to render_search_section"""
    pass

def render_network_section(research_results):
    """Render network section showing author ORCID links."""
    st.header("Collaboration Network")

    # Check if Research is selected in session state
    selected_stages = st.session_state.get('selected_stages', set())
    if 'research' not in selected_stages:
        st.info("Please select the Research tab first to view author networks.")
        return

    if not research_results:
        st.info("Please perform a search in the Research tab first.")
        return

    # Add custom HTML/CSS for links
    st.markdown("""
        <style>
        .orcid-link {
            color: #1a73e8;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            padding: 4px 8px;
            border-radius: 4px;
            background: #f8f9fa;
            margin: 4px 0;
        }
        .orcid-link:hover {
            background: #e8f0fe;
        }
        </style>
    """, unsafe_allow_html=True)

    # Tüm yazarları topla
    authors = {}
    for paper in research_results:
        for authorship in paper.get('authorships', []):
            author = authorship.get('author', {})
            author_name = author.get('display_name')
            if author_name and author_name not in authors:
                authors[author_name] = {
                    'orcid': author.get('orcid'),
                    'papers': []
                }
            if author_name:
                authors[author_name]['papers'].append(paper.get('title'))

    # Yazarları göster
    for author_name, data in authors.items():
        with st.expander(f"👤 {author_name}"):
            if data['orcid']:
                orcid_url = f"https://orcid.org/{data['orcid']}"
                # Use custom HTML for the link
                st.markdown(
                    f'<a href="{orcid_url}" class="orcid-link" target="_blank" rel="noopener noreferrer">'
                    f'🔗 ORCID: {data["orcid"]}</a>',
                    unsafe_allow_html=True
                )
            else:
                st.write("🚫 No ORCID ID found")

            st.write("📚 Documents:")
            for paper in data['papers']:
                st.write(f"- {paper}")

def generate_synthesis_pdf_report(analysis):
    """Generate a PDF report for the synthesis analysis."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    page_width, page_height = letter

    def add_page_footer():
        c.setFont("Helvetica", 10)
        c.drawString(50, 30, datetime.now().strftime('%Y-%m-%d'))
        c.setFillColorRGB(0, 0, 1)
        c.drawString(page_width - 150, 30, "deep-crew.ai")

    # Add logo
    logo = ImageReader("attached_assets/deep-crew.jpg")
    c.drawImage(logo, page_width - 250, page_height - 100, width=200, preserveAspectRatio=True)

    y = page_height - 150

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, y, "Research & Innovation Synthesis Report")
    y -= 40

    sections = [
        # 1. Funding Analysis
        ("Funding Analysis", [
            ("Summary", [analysis.get('funding_analysis', {}).get('summary', '')]),
            ("Key Trends", analysis.get('funding_analysis', {}).get('trends', [])),
            ("Risk Factors", analysis.get('funding_analysis', {}).get('risks', [])),
            ("Recommendations", analysis.get('funding_analysis', {}).get('recommendations', [])),
            ("Opportunities", analysis.get('funding_analysis', {}).get('opportunities', []))
        ]),
        # 2. Research Analysis
        ("Research Analysis", [
            ("Summary", [analysis.get('research_analysis', {}).get('summary', '')]),
            ("Research Trends", analysis.get('research_analysis', {}).get('trends', []))
        ]),
        # 3. Network Analysis
        ("Network Analysis", [
            ("Key Players", analysis.get('network_analysis', {}).get('key_players', [])),
            ("Influential Networks", analysis.get('network_analysis', {}).get('networks', []))
        ]),
        # 4. Patents Analysis
        ("Patents Analysis", [
            ("Summary", [analysis.get('patents_analysis', {}).get('summary', '')]),
            ("Patent Trends", analysis.get('patents_analysis', {}).get('trends', [])),
            ("Innovation Opportunities", analysis.get('patents_analysis', {}).get('opportunities', [])),
            ("Competition Analysis", [analysis.get('patents_analysis', {}).get('competition', '')])
        ])
    ]

    for section_title, subsections in sections:
        if y < 100:
            add_page_footer()
            c.showPage()
            y = page_height - 50

        # Section Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, section_title)
        y -= 30

        # Subsections
        for subsection_title, items in subsections:
            if y < 100:
                add_page_footer()
                c.showPage()
                y = page_height - 50

            c.setFont("Helvetica-Bold", 12)
            c.drawString(70, y, subsection_title)
            y -= 20

            c.setFont("Helvetica", 10)
            for item in items:
                if not item:  # Skip empty items
                    continue

                if y < 100:
                    add_page_footer()
                    c.showPage()
                    y = page_height - 50

                # Wrap text to fit page width
                wrapped_text = [item[i:i+80] for i in range(0, len(item), 80)]
                for line in wrapped_text:
                    c.drawString(90, y, f"• {line}")
                    y -= 15
                y -= 5

        y -= 20  # Extra space between sections

    add_page_footer()
    c.save()
    buffer.seek(0)
    return buffer

def render_synthesis_section(research_data, patent_data, funding_data, selected_stages):
    """Render the synthesis section that combines and analyzes data from multiple modules."""
    st.title("🔄 Research & Innovation Synthesis")

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Prepare data for analysis
    synthesis_data = {
        "research": [{"title": r.get("title"), "abstract": r.get("abstract"), 
                     "year": r.get("publication_year")} for r in research_data] if "research" in selected_stages else [],
        "patents": [{"title": p.get("title"), "abstract": p.get("abstract"),
                    "filing_date": p.get("filing_date")} for p in patent_data] if "patents" in selected_stages else [],
        "funding": funding_data if "funding" in selected_stages else [],
        "selected_modules": list(selected_stages)
    }

    try:
        # Create analysis prompt based on the provided template
        analysis_prompt = """As an AI research analyst, provide a comprehensive synthesis report with the following structure:

        1. Funding Analysis
        - Detailed Summary: Overview of key funding sources and investment trends
        - Key Trends: Emerging patterns in financing and technological shifts
        - Risk Factors: Financial, regulatory, and market risks
        - Recommendations: Strategic funding suggestions
        - Opportunities: Available grants and funding programs

        2. Research Analysis
        - Research Summary: Major findings and breakthroughs
        - Research Trends: Evolution of research focus areas

        3. Network Analysis
        - Key Players: Organizations and researchers
        - Influential Networks: Partnerships and industry alliances

        4. Patents Analysis
        - Summary: Key patents defining the landscape
        - Trends: Patent filing patterns
        - Opportunities: Innovation potential areas
        - Competition: Comparative analysis

        Data to analyze: {data}

        Return in JSON format:
        {{
            "funding_analysis": {{
                "summary": "string",
                "trends": ["string"],
                "risks": ["string"],
                "recommendations": ["string"],
                "opportunities": ["string"]
            }},
            "research_analysis": {{
                "summary": "string",
                "trends": ["string"]
            }},
            "network_analysis": {{
                "key_players": ["string"],
                "networks": ["string"]
            }},
            "patents_analysis": {{
                "summary": "string",
                "trends": ["string"],
                "opportunities": ["string"],
                "competition": "string"
            }}
        }}""".format(data=json.dumps(synthesis_data))

        # Get AI analysis
        with st.spinner("🤖 Generating comprehensive synthesis report..."):
            response = client.chat.completions.create(
                model="gpt-4o",  # Latest model as of May 13, 2024
                messages=[{
                    "role": "system",
                    "content": analysis_prompt
                }],
                response_format={"type": "json_object"}
            )

            analysis = json.loads(response.choices[0].message.content)

        # Display Analysis Results with Modern UI

        # 1. Funding Analysis Section
        st.header("💰 Funding Analysis")

        with st.expander("📊 Detailed Summary", expanded=True):
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
                {analysis.get('funding_analysis', {}).get('summary', 'No summary available')}
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📈 Key Trends")
                for trend in analysis.get('funding_analysis', {}).get('trends', []):
                    st.markdown(f"• {trend}")

            with col2:
                st.subheader("⚠️ Risk Factors")
                for risk in analysis.get('funding_analysis', {}).get('risks', []):
                    st.markdown(f"• {risk}")

            st.subheader("💡 Recommendations")
            for rec in analysis.get('funding_analysis', {}).get('recommendations', []):
                st.markdown(f"• {rec}")

            st.subheader("🎯 Opportunities")
            for opp in analysis.get('funding_analysis', {}).get('opportunities', []):
                st.markdown(f"• {opp}")

        # 2. Research Analysis Section
        st.header("🔬 Research Analysis")

        with st.expander("📚 Research Insights", expanded=True):
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
                {analysis.get('research_analysis', {}).get('summary', 'No summary available')}
            </div>
            """, unsafe_allow_html=True)

            st.subheader("📊 Research Trends")
            for trend in analysis.get('research_analysis', {}).get('trends', []):
                st.markdown(f"• {trend}")

        # 3. Network Analysis Section
        st.header("🌐 Network Analysis")

        with st.expander("🤝 Collaboration Network", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("👥 Key Players")
                for player in analysis.get('network_analysis', {}).get('key_players', []):
                    st.markdown(f"• {player}")

            with col2:
                st.subheader("🔗 Influential Networks")
                for network in analysis.get('network_analysis', {}).get('networks', []):
                    st.markdown(f"• {network}")

        # 4. Patents Analysis Section
        st.header("📋 Patents Analysis")

        with st.expander("🔍 Patent Insights", expanded=True):
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
                {analysis.get('patents_analysis', {}).get('summary', 'No summary available')}
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📈 Patent Trends")
                for trend in analysis.get('patents_analysis', {}).get('trends', []):
                    st.markdown(f"• {trend}")

            with col2:
                st.subheader("💡 Innovation Opportunities")
                for opp in analysis.get('patents_analysis', {}).get('opportunities', []):
                    st.markdown(f"• {opp}")

            st.subheader("🏢 Competitive Analysis")
            st.markdown(analysis.get('patents_analysis', {}).get('competition', 'No competition analysis available'))

        # Export Button
        st.download_button(
            label="📥 Export Complete Synthesis Report",
            data=generate_synthesis_pdf_report(analysis),
            file_name="research_innovation_synthesis.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"An error occurred during synthesis: {str(e)}")