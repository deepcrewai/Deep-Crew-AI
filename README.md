git clone https://github.com/yourusername/ai-powered-research-agent.git
cd ai-powered-research-agent
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