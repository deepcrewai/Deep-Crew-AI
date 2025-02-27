import streamlit as st
import plotly.express as px
from utils import format_citation, calculate_metrics
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
from reportlab.lib.utils import ImageReader

def render_combined_results(research_results, patent_results, combined_analysis):
    """Render enhanced combined analysis with minimal and corporate design."""

    # Custom CSS for corporate styling
    st.markdown("""
        <style>
            /* Corporate color palette */
            :root {
                --primary-color: #2C3E50;
                --secondary-color: #34495E;
                --accent-color: #3498DB;
                --text-color: #2C3E50;
                --light-bg: #F7F9FC;
                --border-color: #E5E9F2;
            }

            /* Card styling */
            .corporate-card {
                background: white;
                border: 1px solid var(--border-color);
                border-radius: 8px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }

            /* Section headers */
            .section-header {
                color: var(--primary-color);
                font-size: 1.25rem;
                font-weight: 600;
                margin: 2rem 0 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid var(--accent-color);
            }

            /* Metric cards */
            .metric-container {
                background: var(--light-bg);
                padding: 1rem;
                border-radius: 8px;
                text-align: center;
            }

            .metric-value {
                font-size: 1.5rem;
                font-weight: 600;
                color: var(--accent-color);
            }

            .metric-label {
                font-size: 0.875rem;
                color: var(--text-color);
                margin-top: 0.25rem;
            }

            /* List items */
            .corporate-list-item {
                padding: 0.5rem 0;
                border-bottom: 1px solid var(--border-color);
            }

            /* Expandable sections */
            .corporate-expander {
                border: 1px solid var(--border-color);
                border-radius: 8px;
                margin: 0.5rem 0;
            }

            /* Icons */
            .icon {
                margin-right: 0.5rem;
                color: var(--accent-color);
            }
        </style>
    """, unsafe_allow_html=True)

    # Main header
    st.markdown('<h1 class="section-header">Comprehensive Analysis</h1>', unsafe_allow_html=True)

    # Summary section with corporate card
    with st.container():
        st.markdown('<div class="corporate-card">', unsafe_allow_html=True)
        st.markdown("### Key Insights")
        st.write(combined_analysis.get("comprehensive_summary", "No summary available"))
        st.markdown('</div>', unsafe_allow_html=True)

    # Key metrics in a grid
    col1, col2, col3 = st.columns(3)
    metrics = [
        {"label": "Research Papers", "value": len(research_results), "icon": "📄"},
        {"label": "Patents", "value": len(patent_results), "icon": "📋"},
        {"label": "Analysis Score", "value": "A+", "icon": "📊"}
    ]

    for col, metric in zip([col1, col2, col3], metrics):
        with col:
            st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-value">{metric['icon']} {metric['value']}</div>
                    <div class="metric-label">{metric['label']}</div>
                </div>
            """, unsafe_allow_html=True)

    # Key findings section
    st.markdown('<h2 class="section-header">🔍 Key Findings</h2>', unsafe_allow_html=True)
    findings = combined_analysis.get("key_findings", [])
    for finding in findings:
        with st.expander(f"Finding (Impact: {finding.get('impact_score', 'N/A')}/10)"):
            st.markdown(f"""
                <div class="corporate-card">
                    <p><strong>Analysis:</strong> {finding.get('finding', '')}</p>
                    <p><strong>Evidence:</strong> {finding.get('evidence', '')}</p>
                </div>
            """, unsafe_allow_html=True)

    # Technology Assessment
    st.markdown('<h2 class="section-header">💻 Technology Assessment</h2>', unsafe_allow_html=True)
    tech_assessment = combined_analysis.get("technology_assessment", {})

    with st.container():
        st.markdown('<div class="corporate-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Technology Readiness", f"{tech_assessment.get('readiness_score', 0)}/10")
            st.write("**Maturity Level:**", tech_assessment.get("maturity_level", "Unknown"))
        with col2:
            st.write("**Development Stages:**")
            stages = tech_assessment.get("development_stages", [])
            funding_reqs = tech_assessment.get("funding_requirements", [])
            for stage, req in zip(stages, funding_reqs):
                st.markdown(f"""
                    <div class="corporate-list-item">
                        <span class="icon">▹</span> {stage}<br/>
                        <small><em>Funding: {req}</em></small>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Market and Investment Analysis
    st.markdown('<h2 class="section-header">📈 Market & Investment Analysis</h2>', unsafe_allow_html=True)

    # Display market gaps in a grid
    gaps = combined_analysis.get("market_research_gaps", [])
    for gap in gaps:
        st.markdown(f"""
            <div class="corporate-card">
                <h4>{gap.get('gap', '')}</h4>
                <p><strong>Market Potential:</strong> {gap.get('market_potential', 0)}/10</p>
                <p><strong>Recommended Approach:</strong> {gap.get('recommended_approach', '')}</p>
                <p><strong>Funding Availability:</strong> {gap.get('funding_availability', 'N/A')}</p>
            </div>
        """, unsafe_allow_html=True)

    # Future Directions with visual indicators
    st.markdown('<h2 class="section-header">🔮 Future Directions</h2>', unsafe_allow_html=True)

    directions = combined_analysis.get("future_directions", [])
    for direction in directions:
        prob = direction.get('probability', 0)
        with st.expander(f"Direction (Probability: {prob}/10)"):
            st.markdown(f"""
                <div class="corporate-card">
                    <p><strong>Direction:</strong> {direction.get('direction', '')}</p>
                    <p><strong>Impact:</strong> {direction.get('impact', '')}</p>
                    <p><strong>Timeline:</strong> {direction.get('timeline', '')}</p>
                    <p><strong>Funding Potential:</strong> {direction.get('funding_potential', '')}</p>
                </div>
            """, unsafe_allow_html=True)

    # Risk Analysis with modern tabs
    st.markdown('<h2 class="section-header">⚠️ Risk Analysis</h2>', unsafe_allow_html=True)

    risks = combined_analysis.get("risk_analysis", {})
    tab1, tab2, tab3, tab4 = st.tabs(["Technical", "Market", "Funding", "Mitigation"])

    with tab1:
        for risk in risks.get("technical_risks", []):
            st.markdown(f'<div class="corporate-list-item">● {risk}</div>', unsafe_allow_html=True)
    with tab2:
        for risk in risks.get("market_risks", []):
            st.markdown(f'<div class="corporate-list-item">● {risk}</div>', unsafe_allow_html=True)
    with tab3:
        for risk in risks.get("funding_risks", []):
            st.markdown(f'<div class="corporate-list-item">● {risk}</div>', unsafe_allow_html=True)
    with tab4:
        for strategy in risks.get("mitigation_strategies", []):
            st.markdown(f'<div class="corporate-list-item">● {strategy}</div>', unsafe_allow_html=True)

    # Bottom statistics bar
    st.markdown('<h2 class="section-header">📊 Analysis Statistics</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Documents", len(research_results) + len(patent_results))
    with col2:
        st.metric("Analysis Depth", "Comprehensive")
    with col3:
        st.metric("Confidence Score", "95%")


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
    """Render the modernized search results section with detailed paper information."""
    metrics = calculate_metrics(results)

    st.markdown("""
        <style>
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            text-align: center;
            transition: all 0.2s ease;
        }
        .metric-card:hover {
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: 600;
            color: #1a73e8;
            margin: 0.5rem 0;
        }
        .metric-label {
            font-size: 0.9rem;
            color: #5f6368;
        }
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
            font-size: 1.2rem;
            font-weight: 500;
            color: #202124;
            margin-bottom: 0.5rem;
        }
        .paper-section {
            margin: 1rem 0;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .paper-section-title {
            font-weight: 500;
            color: #1a73e8;
            margin-bottom: 0.5rem;
        }
        .paper-metadata {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            margin: 0.5rem 0;
        }
        .metadata-item {
            background: #e8f0fe;
            padding: 0.25rem 0.75rem;
            border-radius: 16px;
            font-size: 0.9rem;
            color: #1967d2;
        }
        .author-list {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin: 0.5rem 0;
        }
        .author-item {
            background: #f1f3f4;
            padding: 0.25rem 0.75rem;
            border-radius: 16px;
            font-size: 0.9rem;
            color: #202124;
        }
        .concepts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 0.5rem;
            margin: 0.5rem 0;
        }
        .concept-item {
            background: #e6f4ea;
            padding: 0.25rem 0.75rem;
            border-radius: 16px;
            font-size: 0.9rem;
            color: #137333;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Metrics display
    col1, col2, col3, col4 = st.columns(4)
    metrics_data = [
        {"label": "Toplam Makale", "value": metrics["total_papers"]},
        {"label": "Toplam Atıf", "value": metrics["total_citations"]},
        {"label": "Ortalama Yıl", "value": metrics["avg_year"]},
        {"label": "Ortalama Atıf", "value": metrics["avg_citations"]}
    ]

    for col, metric in zip([col1, col2, col3, col4], metrics_data):
        with col:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{metric['value']}</div>
                    <div class="metric-label">{metric['label']}</div>
                </div>
            """, unsafe_allow_html=True)

    # Results header
    st.markdown("""
        <div style="margin: 2rem 0 1rem">
            <h2 style="color: #202124; font-size: 1.5rem; font-weight: 500;">Araştırma Sonuçları</h2>
        </div>
    """, unsafe_allow_html=True)

    # Export button
    if 'pdf_generated' not in st.session_state:
        st.session_state.pdf_generated = False

    st.download_button(
        label="📑 PDF Olarak İndir",
        data=generate_pdf_report(results, st.session_state.analysis),
        file_name="research_report.pdf",
        mime="application/pdf",
        key="pdf_download",
        use_container_width=False
    )

    # Display detailed paper information with corrected data handling
    for paper in results:
        # Extract author information correctly
        authors = []
        institutions = []

        for authorship in paper.get('authorships', []):
            if authorship.get('author'):
                authors.append(authorship['author'].get('display_name', 'Anonim'))
            if authorship.get('institutions'):
                for inst in authorship['institutions']:
                    if inst.get('display_name'):
                        institutions.append(inst['display_name'])

        # Remove duplicates from institutions
        institutions = list(set(institutions))

        # Extract concepts properly
        concepts = [concept.get('display_name', '') for concept in paper.get('concepts', []) if concept.get('display_name')]

        venue = paper.get('host_venue', {})

        st.markdown(f"""
            <div class="paper-card">
                <!-- 1. Makale Temel Bilgileri -->
                <div class="paper-title">{paper.get('title', 'Başlıksız')}</div>
                <div class="paper-section">
                    <div class="paper-section-title">Temel Bilgiler</div>
                    <div class="paper-metadata">
                        <span class="metadata-item">📅 {paper.get('publication_year', 'N/A')}</span>
                        <span class="metadata-item">🔍 DOI: {paper.get('doi', 'N/A')}</span>
                        <span class="metadata-item">📖 {paper.get('type', 'Makale')}</span>
                    </div>
                    <p style="margin-top: 1rem;">{paper.get('abstract', 'Özet bulunmamaktadır.')}</p>
                </div>

                <!-- 2. Yazar Bilgileri -->
                <div class="paper-section">
                    <div class="paper-section-title">Yazarlar ve Kurumlar</div>
                    <div class="author-list">
                        {' '.join([f'<span class="author-item">👤 {author}</span>' for author in authors])}
                    </div>
                    <div class="paper-metadata">
                        {' '.join([f'<span class="metadata-item">🏛️ {inst}</span>' for inst in institutions])}
                    </div>
                </div>

                <!-- 3. Bibliyometrik Veriler -->
                <div class="paper-section">
                    <div class="paper-section-title">Etki Metrikleri</div>
                    <div class="paper-metadata">
                        <span class="metadata-item">📊 Atıf Sayısı: {paper.get('cited_by_count', 0)}</span>
                        <span class="metadata-item">🔄 Referans Sayısı: {len(paper.get('referenced_works', []))}</span>
                        <span class="metadata-item">📈 Etki Puanı: {paper.get('counts_by_year', [{'year': 0, 'cited_by_count': 0}])[0].get('cited_by_count', 0)}</span>
                    </div>
                </div>

                <!-- 4. Dergi/Yayın Bilgileri -->
                <div class="paper-section">
                    <div class="paper-section-title">Yayın Detayları</div>
                    <div class="paper-metadata">
                        <span class="metadata-item">📰 {venue.get('display_name', 'N/A')}</span>
                        <span class="metadata-item">🔖 ISSN: {venue.get('issn_l', 'N/A')}</span>
                        <span class="metadata-item">📘 Yayıncı: {venue.get('publisher', 'N/A')}</span>
                    </div>
                </div>

                <!-- 5. Araştırma Alanları -->
                <div class="paper-section">
                    <div class="paper-section-title">Konu Başlıkları ve Alanlar</div>
                    <div class="concepts-grid">
                        {' '.join([f'<span class="concept-item">{concept}</span>' for concept in concepts])}
                    </div>
                </div>

                <!-- Bağlantılar -->
                <div style="margin-top: 1rem; text-align: right;">
                    <a href="{paper.get('doi', '#')}" target="_blank" 
                       style="color: #1a73e8; text-decoration: none; font-weight: 500;">
                        Makaleyi Görüntüle →
                    </a>
                </div>
            </div>
        """, unsafe_allow_html=True)

def render_patent_results(results, analysis):
    """Render patent search results with export functionality."""
    # Display metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Patents", len(results))
    with col2:
        st.metric("Inventors", len(set([p['inventors'] for p in results])))

    # Display results header with export button
    col1, col2 = st.columns([2, 3])
    with col1:
        st.subheader("Patent Results")
    with col2:
        # Right-align the button using a container and custom CSS
        button_container = st.container()
        with button_container:
            st.markdown(
                """
                <style>
                div[data-testid="stDownloadButton"] {
                    display: flex;
                    justify-content: flex-end;
                }
                </style>
                """, 
                unsafe_allow_html=True
            )
            if 'patent_pdf_generated' not in st.session_state:
                st.session_state.patent_pdf_generated = False

            st.download_button(
                label="📑 Export Results as PDF",
                data=generate_patent_pdf_report(results, analysis),
                file_name="patent_report.pdf",
                mime="application/pdf",
                key="patent_pdf_download"
            )
            st.session_state.patent_pdf_generated = False

    # Display patents
    for patent in results:
        with st.expander(f"📄 {patent.get('title', 'Untitled Patent')}"):
            st.markdown(f"""
            **ID:** {patent.get('patent_id', 'N/A')}  
            **Inventors:** {patent.get('inventors', 'N/A')}  
            **Filing Date:** {patent.get('filing_date', 'N/A')}

            {patent.get('abstract', 'No abstract available')}

            {f"[View Details]({patent['url']})" if patent.get('url') else ''}
            """)

def render_analysis_section(analysis):
    """Render the AI analysis section."""
    st.header("AI Analysis")

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
    st.subheader("Research Gaps")
    for gap in analysis.get("gaps", []):
        st.write(f"• {gap}")

    # Keyword Suggestions
    st.subheader("Keyword Suggestions")
    st.write("Consider using these keywords to refine your search:")
    keywords = analysis.get("keywords", [])
    if keywords:
        cols = st.columns(3)
        for i, keyword in enumerate(keywords):
            cols[i % 3].write(f"• {keyword}")

    # Complexity Assessment
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
    """Render enhanced combined analysis of research, patent and funding results."""
    st.header("Comprehensive Analysis")

    # Summary
    st.subheader("Overview")
    st.write(combined_analysis.get("comprehensive_summary", "Nosummary available"))

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

    # Funding Landscape Analysis
    st.subheader("Funding Landscape")
    funding = combined_analysis.get("funding_landscape", {})

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Opportunities", funding.get("total_opportunities", "N/A"))
    with col2:
        st.metric("Available Funding", funding.get("total_available_funding", "N/A"))
    with col3:
        st.metric("Key Funders", len(funding.get("key_funders", [])))

    st.write("**Funding Trends:**")
    for trend in funding.get("funding_trends", []):
        st.markdown(f"• {trend}")

    st.write("**Research Alignment:**")
    st.write(funding.get("alignment_with_research", "No alignment analysis available"))

    st.write("**Recommended Funding Approaches:**")
    for approach in funding.get("recommended_approaches", []):
        st.markdown(f"• {approach}")

    # Technology Assessment
    st.subheader("Technology Assessment")
    tech_assessment = combined_analysis.get("technology_assessment", {})
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Technology Readiness", f"{tech_assessment.get('readiness_score', 0)}/10")
        st.write("**Maturity Level:**", tech_assessment.get("maturity_level", "Unknown"))
    with col2:
        st.write("**Development & Funding Stages:**")
        stages = tech_assessment.get("development_stages", [])
        funding_reqs = tech_assessment.get("funding_requirements", [])
        for stage, req in zip(stages, funding_reqs):
            st.markdown(f"• {stage}")
            st.markdown(f"  *Funding: {req}*")

    # Innovation Opportunities with Funding
    st.subheader("Innovation Opportunities")
    for opp in combined_analysis.get("innovation_opportunities", []):
        with st.expander(f"💡 {opp.get('opportunity', 'Opportunity')} ({opp.get('potential_impact', 'N/A')} impact)"):
            st.write(f"**Implementation Timeline:** {opp.get('implementation_timeline', 'N/A')}")
            st.write(f"**Required Resources:** {opp.get('required_resources', 'N/A')}")
            st.write(f"**Potential Funding Sources:** {opp.get('potential_funding', 'N/A')}")

    # Risk Analysis including Funding Risks
    st.subheader("Risk Analysis")
    risks = combined_analysis.get("risk_analysis", {})
    tab1, tab2, tab3, tab4 = st.tabs(["Technical Risks", "Market Risks", "Funding Risks", "Mitigation Strategies"])

    with tab1:
        for risk in risks.get("technical_risks", []):
            st.markdown(f"• {risk}")
    with tab2:
        for risk in risks.get("market_risks", []):
            st.markdown(f"• {risk}")
    with tab3:
        for risk in risks.get("funding_risks", []):
            st.markdown(f"• {risk}")
    with tab4:
        for strategy in risks.get("mitigation_strategies", []):
            st.markdown(f"• {strategy}")

    # Investment Recommendations with Funding Sources
    st.subheader("Investment Recommendations")
    for rec in combined_analysis.get("investment_recommendations", []):
        with st.expander(f"💰 {rec.get('area', 'Investment Area')} (ROI: {rec.get('potential_roi', 'N/A')})"):
            st.write(f"**Timeframe:** {rec.get('timeframe', 'N/A')}")
            st.write(f"**Required Investment:** {rec.get('required_investment', 'N/A')}")
            st.write("**Potential Funding Sources:**")
            for source in rec.get("funding_sources", []):
                st.markdown(f"• {source}")

    # Future Directions with Funding Potential
    st.subheader("Future Directions")
    for direction in combined_analysis.get("future_directions", []):
        with st.expander(f"🔮 {direction.get('direction', 'Direction')} (Probability: {direction.get('probability', 'N/A')}/10)"):
            st.write(f"**Impact:** {direction.get('impact', 'N/A')}")
            st.write(f"**Timeline:** {direction.get('timeline', 'N/A')}")
            st.write(f"**Funding Potential:** {direction.get('funding_potential', 'N/A')}")

    # Collaboration Opportunities with Funding
    st.subheader("Collaboration Opportunities")
    for collab in combined_analysis.get("collaboration_opportunities", []):
        with st.expander(f"🤝 {collab.get('type', 'Collaboration')}"):
            st.write("**Potential Partners:**")
            for partner in collab.get("potential_partners", []):
                st.markdown(f"• {partner}")
            st.write("**Expected Benefits:**")
            for benefit in collab.get("expected_benefits", []):
                st.markdown(f"• {benefit}")
            st.write("**Funding Opportunities:**")
            for funding in collab.get("funding_opportunities", []):
                st.markdown(f"• {funding}")

    # Industry Implications with Sector-Specific Funding
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

    st.write("**Sector-Specific Funding:**")
    for funding in implications.get("sector_specific_funding", []):
        st.markdown(f"• {funding}")

    st.write("**Adaptation Strategies:**")
    for strategy in implications.get("adaptation_strategies", []):
        st.markdown(f"• {strategy}")

    # Statistics
    st.subheader("Document Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Research Papers", len(research_results))
    with col2:
        st.metric("Patents", len(patent_results))
    with col3:
        total_documents = len(research_results) + len(patent_results)
        st.metric("Total Documents", total_documents)