# AI-Powered Academic Literature Analysis 🎓

An advanced academic literature discovery tool powered by OpenAlex API and AI technologies, designed to provide precise and comprehensive research exploration.

## Features 🌟

- 🔍 OpenAI-enhanced search with multi-keyword extraction
- 📄 Customizable PDF export with branding options
- 🌐 Multi-language support
- 📊 Interactive Streamlit interface
- 🔄 Dynamic search, filtering, and export mechanisms

## Prerequisites 📋

Before you begin, ensure you have:
- Python 3.11 or later
- OpenAI API key
- Basic understanding of terminal/command line operations

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/yourusername/academic-literature-analysis.git
cd academic-literature-analysis
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory and add:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

4. Configure Streamlit:
Create a `.streamlit` directory and add `config.toml`:
```bash
mkdir .streamlit
```

Add the following to `.streamlit/config.toml`:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

## Usage 🖥️

1. Start the application:
```bash
streamlit run main.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Enter your research query in the search box.

4. The system will:
   - Generate optimized search keywords using AI
   - Fetch relevant papers from OpenAlex
   - Provide AI-powered analysis
   - Allow PDF export of results

## Project Structure 📁

```
├── main.py                 # Main application entry point
├── ai_analyzer.py          # AI analysis logic
├── api_client.py           # OpenAlex API client
├── components.py           # UI components
├── utils.py               # Utility functions
└── visualizations.py      # Data visualization components
```

## Features in Detail 🔎

### AI-Enhanced Search
- Automatically extracts 4 focused keywords from your query
- Uses OpenAI's GPT-4o model for intelligent keyword generation
- Ranks results based on relevance and citation metrics

### PDF Export
- Generates professional PDF reports
- Includes AI analysis and research trends
- Custom branding options
- Citation formatting

### Analysis Features
- Research trend identification
- Gap analysis in current research
- Complexity assessment
- Keyword optimization suggestions

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 👏

- OpenAlex API for providing academic paper data
- OpenAI for AI capabilities
- Streamlit for the web interface framework

## Support 💡

For support, please open an issue in the GitHub repository or contact the maintainers.
