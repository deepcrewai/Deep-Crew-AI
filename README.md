# DeepCrew AI - Patent Research Platform 🔬

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-00A36C.svg)](https://openai.com/blog/openai-api)

An advanced AI-powered patent search and innovation platform that combines technological research with interactive design and dynamic user engagement, featuring comprehensive accessibility and multilingual support.

## ✨ Key Features

- 🔍 **Advanced Patent Search**: Intelligent search across global patent databases
- 🤖 **AI Analysis**: Deep insights and trend analysis using GPT-4
- 📊 **Dynamic Visualizations**: Interactive data visualization with Plotly
- 💰 **Funding Analysis**: Track and analyze funding opportunities
- 🌐 **Multi-Language Support**: Research across multiple languages
- 📑 **Export Capabilities**: Generate comprehensive PDF reports
- 🔗 **Network Analysis**: Discover research collaborations and connections

## 🚀 Prerequisites

Before installation, ensure you have:

1. Python 3.11 or higher
2. Git
3. OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
4. Internet connection for API access

## 💻 Installation Guide

### Step 1: Clone the Repository
```bash
git clone https://github.com/deepcrewai/patent-research-platform.git
cd patent-research-platform
```

### Step 2: Install Dependencies
```bash
# Install required Python packages
pip install streamlit openai plotly reportlab pandas requests anthropic twilio trafilatura
```

### Step 3: Configure Environment
1. Create the `.streamlit` directory and configuration:
```bash
mkdir -p .streamlit
```

2. Create `.streamlit/config.toml`:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

### Step 4: Set Up API Keys
1. Create a `.env` file:
```bash
touch .env
```

2. Add your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 🖥️ Usage Guide

### Starting the Application
```bash
streamlit run main.py
```
The application will be available at `http://localhost:5000`

### Using the Platform

#### 1. Research Tab
- Enter your research query
- Filter results by year, citations, and relevance
- View detailed paper information with citations
- Export research findings as PDF

#### 2. Patent Analysis
- Search for patents using keywords
- View patent details including inventors and filing dates
- Analyze patent trends and opportunities
- Generate patent analysis reports

#### 3. Funding Analysis
- Discover funding opportunities
- Filter by region and deadline
- View success rates and requirements
- Get AI-powered funding recommendations

#### 4. Network Analysis
- Explore researcher networks
- View collaboration patterns
- Access researcher profiles with ORCID links
- Identify potential collaborators

#### 5. Export Features
- Generate comprehensive PDF reports
- Export visualization data
- Save search results
- Create custom analysis reports

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT-4
- **Data Visualization**: Plotly
- **PDF Generation**: ReportLab
- **API Integration**: OpenAlex, PQAI
- **Data Processing**: Pandas
- **Documentation**: GitBook

## 🔗 Links

- GitHub: [https://github.com/deepcrewai](https://github.com/deepcrewai)
- Documentation: [https://deepcrewai.gitbook.io/deepcrewai](https://deepcrewai.gitbook.io/deepcrewai)
- Twitter: [https://x.com/deepcrewai](https://x.com/deepcrewai)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API access
- Streamlit team for the web framework
- Our contributors and users

## 💡 Support

For questions and support:
- Check our [Documentation](https://deepcrewai.gitbook.io/deepcrewai)
- Open an issue on [GitHub](https://github.com/deepcrewai)
- Follow us on [X/Twitter](https://x.com/deepcrewai)