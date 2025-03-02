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
    st.title("Research & Innovation Synthesis")

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Prepare data for analysis
    synthesis_data = {
        "research": [],
        "patents": [],
        "funding": [],
        "selected_modules": list(selected_stages)
    }

    # Only include data for selected stages
    if "research" in selected_stages and research_data:
        synthesis_data["research"] = [{
            "title": r.get("title", ""),
            "abstract": r.get("abstract", ""),
            "year": r.get("publication_year", ""),
            "authors": [a.get("author", {}).get("display_name", "") for a in r.get("authorships", [])]
        } for r in research_data]

    if "patents" in selected_stages and patent_data:
        synthesis_data["patents"] = [{
            "title": p.get("title", ""),
            "abstract": p.get("abstract", ""),
            "filing_date": p.get("filing_date", ""),
            "inventors": p.get("inventors", "")
        } for p in patent_data]

    if "funding" in selected_stages and funding_data:
        synthesis_data["funding"] = funding_data

    try:
        # Create analysis prompt
        analysis_prompt = f"""You are an expert research analyst. Based on the provided data, generate a comprehensive synthesis report 
        analyzing {', '.join(selected_stages)} information.

        The data includes:
        Research papers: {len(synthesis_data['research'])} documents
        Patents: {len(synthesis_data['patents'])} documents
        Funding opportunities: {len(synthesis_data['funding'])} records

        Please provide a detailed analysis with the following structure:
        1. Summarize key findings across all selected areas
        2. Identify major trends and patterns
        3. Highlight opportunities and risks
        4. Provide actionable recommendations

        Format your response as a JSON object with this exact structure:
        {{
            "funding_analysis": {{
                "summary": "Detailed funding landscape analysis...",
                "trends": ["Specific trend 1", "Specific trend 2"],
                "risks": ["Clear risk 1", "Clear risk 2"],
                "recommendations": ["Actionable recommendation 1", "Actionable recommendation 2"],
                "opportunities": ["Specific opportunity 1", "Specific opportunity 2"]
            }},
            "research_analysis": {{
                "summary": "Comprehensive research findings overview...",
                "trends": ["Research trend 1", "Research trend 2"]
            }},
            "network_analysis": {{
                "key_players": ["Major player 1", "Major player 2"],
                "networks": ["Network insight 1", "Network insight 2"]
            }},
            "patents_analysis": {{
                "summary": "Patent landscape overview...",
                "trends": ["Patent trend 1", "Patent trend 2"],
                "opportunities": ["Innovation opportunity 1", "Innovation opportunity 2"],
                "competition": "Competitive landscape analysis"
            }}
        }}"""

        # Show the game while analysis is running
        game_placeholder = st.empty()
        with game_placeholder:
            render_waiting_game()

        # Get AI analysis
        with st.spinner("Generating comprehensive synthesis report..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "system",
                    "content": analysis_prompt
                }, {
                    "role": "user",
                    "content": json.dumps(synthesis_data)
                }],
                response_format={"type": "json_object"},
                temperature=0.7
            )

            analysis = json.loads(response.choices[0].message.content)

        # Clear the game after analysis is complete
        game_placeholder.empty()

        # Display Analysis Results
        st.header("Funding Analysis")
        with st.expander("Detailed Summary", expanded=True):
            funding_summary = analysis.get('funding_analysis', {}).get('summary', 'No summaryavailable')
            st.markdown(funding_summary)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Key Trends")
                trends = analysis.get('funding_analysis', {}).get('trends', [])
                for trend in trends:
                    st.write(f"• {trend}")

            with col2:
                st.subheader("Risk Factors")
                risks = analysis.get('funding_analysis', {}).get('risks', [])
                for risk in risks:
                    st.write(f"• {risk}")

            st.subheader("Recommendations")
            recs = analysis.get('funding_analysis', {}).get('recommendations', [])
            for rec in recs:
                st.write(f"• {rec}")

            st.subheader("Opportunities")
            opps = analysis.get('funding_analysis', {}).get('opportunities', [])
            for opp in opps:
                st.write(f"• {opp}")

        st.header("Research Analysis")
        with st.expander("Research Insights", expanded=True):
            research_summary = analysis.get('research_analysis', {}).get('summary', 'No summary available')
            st.markdown(research_summary)

            st.subheader("Research Trends")
            trends = analysis.get('research_analysis', {}).get('trends', [])
            for trend in trends:
                st.write(f"• {trend}")

        st.header("Network Analysis")
        with st.expander("Collaboration Network", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Key Players")
                players = analysis.get('network_analysis', {}).get('key_players', [])
                for player in players:
                    st.write(f"• {player}")

            with col2:
                st.subheader("Influential Networks")
                networks = analysis.get('network_analysis', {}).get('networks', [])
                for network in networks:
                    st.write(f"• {network}")

        st.header("Patents Analysis")
        with st.expander("Patent Insights", expanded=True):
            patent_summary = analysis.get('patents_analysis', {}).get('summary', 'No summary available')
            st.markdown(patent_summary)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Patent Trends")
                trends = analysis.get('patents_analysis', {}).get('trends', [])
                for trend in trends:
                    st.write(f"• {trend}")

            with col2:
                st.subheader("Innovation Opportunities")
                opps = analysis.get('patents_analysis', {}).get('opportunities', [])
                for opp in opps:
                    st.write(f"• {opp}")

            st.subheader("Competitive Analysis")
            competition = analysis.get('patents_analysis', {}).get('competition', 'No competition analysis available')
            st.markdown(competition)

        # Export Button
        st.download_button(
            label="Export Complete Synthesis Report",
            data=generate_synthesis_pdf_report(analysis),
            file_name="research_innovation_synthesis.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"An error occurred during synthesis: {str(e)}")

def render_waiting_game():
    """Render the game while waiting for analysis."""
    game_html = """
    <div class="init">
        <div class="center1">
            <h1>WE NEED YOU!</h1>
            <p>Click on each square to clean sea. You must hurry or 
the sea will be polluted.</p>
            <p class="floating bold">START GAME</p>
        </div>
    </div>
    <div class="won">
        <div class="center">
            <h1>YOU WON!</h1>
            <p class="floating replay bold">save the World again</p>
        </div>
    </div>
    <div class="init hidden"><h1 class="center">INCREASED VELOCITY!</h1></div>
    <div class="container">
        <div class="game"></div>
    </div>
    """

    game_css = """
    /* {
        border: 1px solid #888;
    }*/

    @import url('https://fonts.googleapis.com/css?family=Roboto');

    :root {
        --green:  	#0067a5;
        --red: #ff9292;
        --dim: 62px;
    }

    body {
        margin: 0;
        padding: 0;
        height: 100vh;
        background-color: #007aa5;
    }

    h1, h2 {
        font-family: 'Roboto', sans-serif;
        font-weight: bold;
        color: #333;
        margin: 10px;
    }

    h1 {
        font-size: 60px;
    }

    h2 {
        font-size: 37px;
    }

    p {
        font-family: 'Roboto', sans-serif;
        font-size: 23px;
        font-weight: 100;
        color: #333; 
        margin: 10px;
    }

    .bold {
      font-weight: 900;
    }

    .center {
        position: relative;
        top: 20%;
        margin: 0;
    }

    .center1 {
        position: relative;
        margin: 30px;
    }

    .container {
        height: 100%;
        position: relative;
    }

    .game {
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        margin: auto;
        width: 540px;
        height: 650px;
        border-radius: 9px;
        background-color: #333;
        padding: 5px;
    }

    .box {
        height: 100px;
        width: 100px;
        float: left;
        margin: 0;
        padding: 0px;
        text-align: center;
        border-radius: 9px;
        border: 4px solid #333;
        background-color: #b4cadf;
        background-position: center;
        background-size: 70%;
        background-repeat: no-repeat;
    }

    .green {
        background-color: var(--green);
        animation-name: getIn;
        animation-duration: .3s;
        animation-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }

    .tree {
        background-image: url('https://img.icons8.com/?size=100&id=On7Klul3EITI&format=png');
    }

    .red {
        background-color: var(--red);
        animation-name: getIn1;
        animation-duration: .3s;
        animation-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }

    .factory {
        background-image: url('https://img.icons8.com/?size=100&id=Gfo2-kRuGKUt&format=png');
    }

    .won, .init {
        z-index: 999;
        position: fixed;
        left: 0;
        right: 0;
        margin: auto;
        text-align: center;
        border: 8px solid #333;
        border-radius: 7px;
    }

    .won {
        background-color: var(--green);
        top: 100%;
        width: 600px;
        height: 300px;
    }

    .init {
        background-color: var(--red);
        top: 30%;
        width: 600px;
        height: 300px;
    }

    .floating {
        position: relative;
        animation-name: floating;
        animation-iteration-count: infinite;
        animation-duration: 1.5s;
        animation-timing-function: ease-in-out;
        cursor: pointer;
        text-decoration: underline;
        text-decoration-color: #333;
        margin-top: 30px;
    }

    .levelUp {
      animation: levelUp 2.5s ease-in-out;
      animation-delay: 2s;
    }

    .hidden {
      visibility: hidden;
    }

    @keyframes won {
        from {top: 100%; transform: rotate(180deg);}
        to   {top: 30%; transform: rotate(0deg);}    
    }

    @keyframes start {
        from   {top: 30%; transform: rotate(0deg);}    
        to {top: 100%; transform: rotate(180deg);}
    }

    @keyframes floating {
        0% {top: 0px; transform: rotate(0deg);}
        25% {top: 5px; transform: rotate(3deg);}
        50% {top: -5px; transform: rotate(-3deg);}
        100%   {top: 0px; transform: rotate(0deg);}  
    }

    @keyframes getIn {
        from {background-size: 0%;}
        to   {background-size: 70%;}
    }

    @keyframes getIn1 {
        from {background-size: 0%;}
        to   {background-size: 70%;}
    }

    @keyframes levelUp {
        0% {opacity: 0; visibility: visible;}
        50% {opacity: 1;}
        100%   {opacity: 0; visibility: hidden;}  
    }

    @media (max-width: 500px) {
        h1 {
            font-size: 37px;
        }

        .game {
            width: 331px;
            height: 396px;
        }

        .box {
            width: var(--dim);
            height: var(--dim);
            border: 2.1px solid #333;
        }

        .won, .init {
            width: 300px;
            height: 400px;
        }

        .init {
            top: 10%;
        }
    }
    """

    game_js = """
    <script>
    const game = document.querySelector('.game');
    var arrFactory = [];
    var arrTree = [];
    var newFactory;
    var interval = 800;

    function createGame() {
        for (let i = 0; i < 30; i++) {
            let a = document.querySelector('.game');
            let b = document.createElement('div');
            b.classList.add('box');
            b.setAttribute('data-value', i);
            a.appendChild(b);   
        }
    }

    function replay() {
        var replay = document.querySelector('.replay');
        replay.addEventListener('click', function() {
            box.forEach(function(box) {
                box.classList.remove('green');
                box.classList.remove('tree');
            });
            document.querySelector('.hidden').classList.add('levelUp')
            let bang = document.querySelector('.won');
            newFactory = setInterval(randomFactory, 600);
            bang.style.animation = 'start .6s ease-in-out';
            bang.style.top = '100%';
        });
    }

    function addTree(e) {
        let c = e.target;

        if(arrTree.indexOf(c.dataset.value) == -1) {
            arrTree.push(c.dataset.value);
            if(arrTree.length == 30) {
                clearInterval(newFactory);

                document.querySelector('.hidden').classList.remove('levelUp');
                let bang = document.querySelector('.won');
                bang.style.animation = 'won .6s ease-in-out';
                bang.style.top = '30%';
                replay();
            }
        } 

        if(arrFactory.indexOf(c.dataset.value) != -1) {
            arrFactory.splice(arrFactory.indexOf(c.dataset.value) ,1);
        }
        c.classList.remove('red');
        c.classList.remove('factory');
        c.classList.add('green');
        c.classList.add('tree');
    }

    function randomFactory() {
        let e = Math.random() * 30;
        let g = Math.floor(e);

        if(arrFactory.indexOf(box[g].dataset.value) == -1) {
            arrFactory.push(box[g].dataset.value);
            box[g].classList.add('red');
            box[g].classList.remove('green');
            box[g].classList.add('factory');
            if(arrFactory.length == 30) {
                clearInterval(newFactory);
            }
        } 

        if(arrTree.indexOf(box[g].dataset.value) != -1) {
            arrTree.splice(arrTree.indexOf(box[g].dataset.value), 1);
        }
    }

    // Initialize game when document is ready
    document.addEventListener('DOMContentLoaded', function() {
        createGame();
        var box = document.querySelectorAll('.box');
        var start = document.querySelector('.floating');

        start.addEventListener('click', function() {
            let init = document.querySelector('.init');
            init.style.animation = 'start .5s ease-in';
            init.style.top = '100%';
            newFactory = setInterval(randomFactory, interval);
        });

        box.forEach(function(box) {
            box.addEventListener('click', addTree);
        });
    });
    </script>
    """

    # Combine HTML, CSS and JavaScript in a container div
    st.markdown(
        f"""
        <style>
        {game_css}
        </style>
        <div id="game-container" style="height: 100vh;">
        {game_html}
        {game_js}
        </div>
        """,
        unsafe_allow_html=True
    )