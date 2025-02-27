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

def main():
    setup_page()

    # Accessibility Settings in Sidebar
    with st.sidebar:
        st.title("🌐 Erişilebilirlik")

        # Initialize session state for settings if not exists
        if 'accessibility_settings' not in st.session_state:
            st.session_state.accessibility_settings = {
                'high_contrast': False,
                'negative_contrast': False,
                'screen_reader': False,
                'keyboard_shortcuts': False
            }

        # High Contrast Mode
        high_contrast = st.toggle("🔳 Yüksek Kontrast (Alt+H)", 
            value=st.session_state.accessibility_settings['high_contrast'],
            help="Yüksek kontrast modunu etkinleştirmek için Alt+H tuşlarını kullanın")
        if high_contrast != st.session_state.accessibility_settings['high_contrast']:
            st.session_state.accessibility_settings['high_contrast'] = high_contrast
            st.rerun()

        # Negative Contrast
        negative_contrast = st.toggle("🌙 Negatif Kontrast (Alt+N)", 
            value=st.session_state.accessibility_settings['negative_contrast'],
            help="Negatif kontrast modunu etkinleştirmek için Alt+N tuşlarını kullanın")
        if negative_contrast != st.session_state.accessibility_settings['negative_contrast']:
            st.session_state.accessibility_settings['negative_contrast'] = negative_contrast
            st.rerun()

        # Screen Reader
        screen_reader = st.toggle("🔊 Ekran Okuyucu (Alt+S)", 
            value=st.session_state.accessibility_settings['screen_reader'],
            help="Ekran okuyucuyu etkinleştirmek için Alt+S tuşlarını kullanın")
        if screen_reader != st.session_state.accessibility_settings['screen_reader']:
            st.session_state.accessibility_settings['screen_reader'] = screen_reader
            st.rerun()

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
            st.session_state.accessibility_settings = {
                'high_contrast': False,
                'negative_contrast': False,
                'screen_reader': False,
                'keyboard_shortcuts': False
            }
            st.rerun()

    # Apply accessibility styles and scripts
    styles = []
    scripts = []

    if st.session_state.accessibility_settings['high_contrast']:
        styles.append("""
            .stApp, body, [data-testid="stSidebar"] {
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
        """)

    if st.session_state.accessibility_settings['negative_contrast']:
        styles.append("""
            .stApp {
                filter: invert(100%) !important;
            }
            img, [data-testid="stImage"] {
                filter: invert(100%) !important;
            }
        """)

    if st.session_state.accessibility_settings['screen_reader']:
        scripts.append("""
            function speak(text) {
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'tr-TR';
                window.speechSynthesis.speak(utterance);
            }

            document.addEventListener('keydown', function(e) {
                if (e.altKey && e.key === 's') {
                    const focusedElement = document.activeElement;
                    if (focusedElement) {
                        speak(focusedElement.textContent || focusedElement.value || 'Seçili element');
                    }
                }
            });
        """)

    # Keyboard navigation script
    scripts.append("""
        document.addEventListener('keydown', function(e) {
            if (e.altKey) {
                switch(e.key) {
                    case 'h':
                        document.querySelector('[data-testid="stToggleButton"][aria-label*="Yüksek Kontrast"]').click();
                        break;
                    case 'n':
                        document.querySelector('[data-testid="stToggleButton"][aria-label*="Negatif Kontrast"]').click();
                        break;
                    case 's':
                        document.querySelector('[data-testid="stToggleButton"][aria-label*="Ekran Okuyucu"]').click();
                        break;
                    case 'r':
                        document.querySelector('button:contains("🔄 Sıfırla")').click();
                        break;
                    case 'ArrowRight':
                        navigateElements('next');
                        break;
                    case 'ArrowLeft':
                        navigateElements('prev');
                        break;
                }
            }
        });

        function navigateElements(direction) {
            const focusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
            const elements = Array.from(document.querySelectorAll(focusableElements));
            const currentElement = document.activeElement;
            const currentIndex = elements.indexOf(currentElement);
            let nextIndex;

            if (direction === 'next') {
                nextIndex = currentIndex + 1 >= elements.length ? 0 : currentIndex + 1;
            } else {
                nextIndex = currentIndex - 1 < 0 ? elements.length - 1 : currentIndex - 1;
            }

            elements[nextIndex].focus();
        }
    """)

    # Apply all styles and scripts
    if styles:
        st.markdown(f"""
            <style>
                {' '.join(styles)}
            </style>
        """, unsafe_allow_html=True)

    if scripts:
        st.markdown(f"""
            <script>
                {' '.join(scripts)}
            </script>
        """, unsafe_allow_html=True)

    # Main Content
    st.markdown("""
        <div class="main-container">
            <div class="logo-title">DEEP CREW</div>
            <h1 class="main-header">Research & Innovation Hub</h1>
            <p class="subtitle">
                Discover insights, analyze patents, and explore funding opportunities with AI-powered research tools
            </p>
        </div>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;500;600;700&display=swap');

            .main-container {
                max-width: 800px;
                margin: 3rem auto;
                text-align: center;
                font-family: 'Inter', sans-serif;
            }

            .logo-title {
                font-size: 2.75rem;
                font-weight: 700;
                padding: 1.25rem 0px 1rem;
                font-family: "Source Sans Pro", sans-serif;
                color: black;
            }

            .main-header {
                font-size: 2.5rem;
                font-weight: 500;
                color: #202124;
                margin: 1rem 0;
                font-family: 'Inter', sans-serif;
            }

            .subtitle {
                font-size: 1.1rem;
                color: #5f6368;
                margin-bottom: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # Search input with modern styling
    search_query = st.text_input(
        "",
        placeholder="Enter your research topic...",
        help="Type your research query here",
        label_visibility="collapsed"
    )

    # Initialize session state for selected stages
    if 'selected_stages' not in st.session_state:
        st.session_state.selected_stages = set()

    # Create stage buttons using columns for horizontal layout
    col1, col2, col3, col4, col5 = st.columns(5)

    stages = {
        'research': 'Research',
        'patents': 'Patents',
        'funding': 'Funding',
        'network': 'Network',
        'compliance': 'Compliance'
    }

    columns = [col1, col2, col3, col4, col5]

    for idx, (stage_key, label) in enumerate(stages.items()):
        with columns[idx]:
            is_selected = stage_key in st.session_state.selected_stages
            if st.button(
                label,
                key=f"btn_{stage_key}",
                help=f"Click to select {label}",
                use_container_width=True,
                type="secondary" if is_selected else "primary"
            ):
                if stage_key in st.session_state.selected_stages:
                    st.session_state.selected_stages.remove(stage_key)
                else:
                    st.session_state.selected_stages.add(stage_key)
                st.rerun()

    selected_stages = list(st.session_state.selected_stages)

    if search_query:
        if not selected_stages:
            st.warning("Please select at least one research stage to proceed.")
            return

        # Only add Results tab if more than one stage is selected
        if len(selected_stages) > 1:
            selected_stages.append("results")

        # Create tabs with modern styling
        tabs = st.tabs([stage.capitalize() for stage in selected_stages])

        for idx, tab in enumerate(tabs):
            with tab:
                if selected_stages[idx] == "research":
                    with st.spinner("🔍 Analyzing..."):
                        openalex_client = OpenAlexClient()
                        ai_analyzer = AIAnalyzer()

                        if search_query != st.session_state.get('last_query', ''):
                            keywords = ai_analyzer.generate_search_keywords(search_query)
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
                    with st.spinner("🔍 Searching patents..."):
                        patent_client = PatentSearchClient()
                        if search_query != st.session_state.get('last_query', '') or st.session_state.get('patent_results') is None:
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

                elif selected_stages[idx] == "results":
                    render_combined_results(
                        st.session_state.get('search_results') or [],
                        st.session_state.get('patent_results') or [],
                        st.session_state.combined_analysis if 'combined_analysis' in st.session_state else None
                    )

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