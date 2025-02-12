# AI-Powered Research Agent 🔬

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-00A36C.svg)](https://openai.com/blog/openai-api)

An advanced AI-powered academic research discovery platform that transforms how researchers explore, analyze, and collaborate on scientific literature.

## ✨ Features

- 🔍 **Semantic Search**: Advanced search capabilities powered by OpenAI
- 📊 **Dynamic Visualizations**: Interactive data visualizations using Plotly
- 🌐 **Multi-Language Support**: Research discovery across multiple languages
- 📑 **PDF Export**: Generate comprehensive research reports
- 📈 **Trend Analysis**: Identify emerging research trends
- 🤖 **AI Analysis**: Get AI-powered insights and recommendations
- 🔗 **OpenAlex Integration**: Access comprehensive research database

## 🚀 Prerequisites

Before you begin, ensure you have:

- Python 3.11 or higher installed
- An OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Git installed on your system
- Internet connection for API access

## 💻 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-powered-research-agent.git
cd ai-powered-research-agent
```

### 2. Install Required Python Packages
```bash
pip install streamlit openai plotly reportlab requests pandas trafilatura pypdf2 anthropic twilio
```

### 3. Configure Environment Variables
1. Create a `.env` file in the project root directory:
```bash
# For Windows
echo. > .env

# For Linux/macOS
touch .env
```

2. Add your OpenAI API key to the `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Configure Streamlit
1. Create a `.streamlit` directory:
```bash
mkdir .streamlit
```

2. Create and configure `.streamlit/config.toml`:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

## 🖥️ Usage

1. Start the application:
```bash
streamlit run main.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## 📝 Features Guide

### Search
- Enter your research query in the search box
- AI will generate optimized search keywords
- View results with relevance scores and citations

### Analysis
- Get AI-generated research summaries
- View emerging and declining research trends
- Identify potential research gaps
- Assess research complexity

### Export
- Generate PDF reports with analysis
- Export visualizations and data
- Save search results for later reference

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4o API
- OpenAlex for research data access
- Streamlit for the web framework
- All contributors and users of this project

## 📧 Contact

For questions and support, please open an issue in the GitHub repository.
