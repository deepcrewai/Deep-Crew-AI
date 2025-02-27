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
    metrics = calculate_metrics(results)

    # Modern metrics cards
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
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    metrics_data = [
        {"label": "Total Papers", "value": metrics["total_papers"]},
        {"label": "Total Citations", "value": metrics["total_citations"]},
        {"label": "Average Year", "value": metrics["avg_year"]},
        {"label": "Average Citations", "value": metrics["avg_citations"]}
    ]

    for col, metric in zip([col1, col2, col3, col4], metrics_data):
        with col:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{metric['value']}</div>
                    <div class="metric-label">{metric['label']}</div>
                </div>
            """, unsafe_allow_html=True)

    # Modern results header with export button
    st.markdown("""
        <style>
        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 2rem 0 1rem;
        }
        .results-title {
            font-size: 1.5rem;
            font-weight: 500;
            color: #202124;
        }
        .export-button {
            background-color: #1a73e8;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 24px;
            text-decoration: none;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }
        .export-button:hover {
            background-color: #1557b0;
            box-shadow: 0 1px 6px rgba(32,33,36,.28);
        }
        </style>
        <div class="results-header">
            <div class="results-title">Search Results</div>
        </div>
    """, unsafe_allow_html=True)

    # Export button
    if 'pdf_generated' not in st.session_state:
        st.session_state.pdf_generated = False

    st.download_button(
        label="📑 Export Results as PDF",
        data=generate_pdf_report(results, st.session_state.analysis),
        file_name="research_report.pdf",
        mime="application/pdf",
        key="pdf_download",
        use_container_width=False
    )

    # Modern paper cards
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
        </style>
    """, unsafe_allow_html=True)

    for paper in results:
        similarity = paper.get('similarity_score', 0)
        st.markdown(f"""
            <div class="paper-card">
                <div class="paper-title">{paper.get('title', 'Untitled')}</div>
                <div class="paper-citation">{format_citation(paper)}</div>
                <div class="paper-abstract">{paper.get('abstract', 'No abstract available')}</div>
                <div class="paper-metrics">
                    <span>Similarity: {similarity:.2f}</span>
                    <span>Citations: {paper.get('cited_by_count', 0)}</span>
                    {'<a href="' + paper['url'] + '" class="paper-link" target="_blank">View Paper</a>' if paper.get('url') else ''}
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
        st.metric("Patents", len(patent_results))
    with col3:
        total_documents = len(research_results) + len(patent_results)
        st.metric("Total Documents", total_documents)

def render_accessibility_menu():
    """Render the accessibility menu using Streamlit native components."""
    with st.sidebar:
        st.markdown("### 🌐 Erişilebilirlik Araçları")

        # High Contrast Mode
        if st.toggle("🔳 Yüksek Kontrast (Alt+H)", value=st.session_state.get('high_contrast', False), key='high_contrast'):
            st.markdown("""
                <style>
                    body, .main-container, .stApp, [data-testid="stSidebar"] {
                        background-color: black !important;
                        color: white !important;
                    }
                    .stButton button, .stSelectbox, .stTextInput input {
                        background-color: white !important;
                        color: black !important;
                        border: 1px solid white !important;
                    }
                    .stMarkdown, .stText, .logo-title, .main-header, .subtitle {
                        color: white !important;
                    }
                    [data-testid="stSidebarNav"] {
                        background-color: black !important;
                    }
                </style>
            """, unsafe_allow_html=True)

        # Negative Contrast
        if st.toggle("🌙 Negatif Kontrast (Alt+N)", value=st.session_state.get('negative_contrast', False), key='negative_contrast'):
            st.markdown("""
                <style>
                    .stApp, body {
                        filter: invert(100%) !important;
                        background-color: white !important;
                    }
                    img, [data-testid="stImage"] {
                        filter: invert(100%) !important;
                    }
                    .stMarkdown a {
                        color: #0000EE !important;
                    }
                </style>
            """, unsafe_allow_html=True)

        # Screen Reader
        if st.toggle("🔊 Ekran Okuyucu (Alt+S)", value=st.session_state.get('screen_reader', False), key='screen_reader'):
            # Ekran okuyucu kullanım kılavuzu
            st.info("""
                ℹ️ **Ekran Okuyucu Kullanım Kılavuzu**

                1. **Otomatik Okuma**: 
                   - Bir öğeye tıkladığınızda veya Tab tuşu ile üzerine geldiğinizde otomatik olarak okunur

                2. **Manuel Okuma**: 
                   - Herhangi bir öğeyi seçin ve `Alt + S` tuşlarına basın
                   - Seçili öğenin içeriği sesli okunacaktır

                3. **Gezinme**:
                   - `Tab` tuşu: Sonraki öğeye geç
                   - `Shift + Tab`: Önceki öğeye geç
                   - `Alt + →`: Sonraki öğeye hızlı geçiş
                   - `Alt + ←`: Önceki öğeye hızlı geçiş

                4. **İpucu**: 
                   - Ekran okuyucu aktif olduğunda "Ekran okuyucu aktif" sesi duyacaksınız
                   - Her bir öğe üzerine geldiğinizde içeriği otomatik okunacaktır
            """)

            st.components.v1.html("""
                <div id="screenReaderContainer"></div>
                <script>
                    // Initialize speech synthesis
                    if ('speechSynthesis' in window) {
                        const synth = window.speechSynthesis;
                        let speaking = false;

                        // Initialize voices
                        let voices = [];
                        function loadVoices() {
                            voices = synth.getVoices();
                            const turkishVoice = voices.find(voice => voice.lang.includes('tr'));
                            if (turkishVoice) {
                                console.log('Turkish voice found:', turkishVoice.name);
                            }
                        }

                        synth.onvoiceschanged = loadVoices;
                        loadVoices();

                        // Speak function
                        function speak(text) {
                            if (!text || typeof text !== 'string') return;

                            // Cancel previous speech
                            if (speaking) {
                                synth.cancel();
                            }

                            // Create utterance
                            const utterance = new SpeechSynthesisUtterance(text);

                            // Try to set Turkish voice
                            const turkishVoice = voices.find(voice => voice.lang.includes('tr'));
                            if (turkishVoice) {
                                utterance.voice = turkishVoice;
                            }

                            utterance.lang = 'tr-TR';
                            utterance.rate = 1;
                            utterance.pitch = 1;
                            utterance.volume = 1;

                            // Speech events
                            utterance.onstart = () => { speaking = true; };
                            utterance.onend = () => { speaking = false; };
                            utterance.onerror = (e) => { 
                                speaking = false;
                                console.error('Speech error:', e);
                            };

                            // Speak
                            synth.speak(utterance);
                            console.log('Speaking:', text);
                        }

                        // Function to handle element text
                        function getElementText(element) {
                            return element.getAttribute('aria-label') || 
                                   element.title ||
                                   element.textContent ||
                                   element.value ||
                                   element.placeholder;
                        }

                        // Focus handler
                        function handleFocus(event) {
                            const element = event.target;
                            const text = getElementText(element);
                            if (text && text.trim()) {
                                speak(text.trim());
                            }
                        }

                        // Add event listeners
                        document.addEventListener('focusin', handleFocus);

                        // Manual trigger with Alt+S
                        document.addEventListener('keydown', (e) => {
                            if (e.altKey && e.key.toLowerCase() === 's') {
                                const element = document.activeElement;
                                const text = getElementText(element);
                                if (text && text.trim()) {
                                    speak(text.trim());
                                }
                            }
                        });

                        // Observer for dynamic content
                        const observer = new MutationObserver((mutations) => {
                            mutations.forEach((mutation) => {
                                if (mutation.type === 'childList') {
                                    mutation.addedNodes.forEach((node) => {
                                        if (node.nodeType === 1 && // Element node
                                            (node.getAttribute('data-testid') || 
                                             node.getAttribute('aria-label'))) {
                                            const text = getElementText(node);
                                            if (text && text.trim()) {
                                                speak(text.trim());
                                            }
                                        }
                                    });
                                }
                            });
                        });

                        // Start observing
                        observer.observe(document.body, {
                            childList: true,
                            subtree: true,
                            attributes: true,
                            attributeFilter: ['aria-label', 'value']
                        });

                        // Test speech on load
                        speak("Ekran okuyucu aktif");
                    } else {
                        console.warn('Speech Synthesis API is not supported');
                        document.getElementById('screenReaderContainer').textContent = 
                            'Bu tarayıcıda ekran okuyucu desteklenmiyor.';
                    }
                </script>
            """, height=1)

        # Keyboard Shortcuts Info
        with st.expander("⌨️ Klavye Kısayolları"):
            st.markdown("""
                - **Alt + H**: Yüksek Kontrast
                - **Alt + N**: Negatif Kontrast
                - **Alt + S**: Ekran Okuyucu
                - **Alt + R**: Sıfırla
                - **Alt + →**: Sonraki Eleman
                - **Alt + ←**: Önceki Eleman
                - **Space**: Seçili Elemanı Etkinleştir
            """)

        # Reset Button
        if st.button("🔄 Sıfırla (Alt+R)"):
            for key in ['high_contrast', 'negative_contrast', 'screen_reader']:
                st.session_state[key] = False
            st.rerun()