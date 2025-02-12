git clone https://github.com/yourusername/ai-powered-research-agent.git
cd ai-powered-research-agent
```

### 2. Set Up Python Virtual Environment (Optional)
```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Python Packages
```bash
pip install streamlit openai plotly reportlab requests pandas trafilatura pypdf2 anthropic twilio
```

### 4. Configure Environment Variables
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

### 5. Configure Streamlit
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

4. The system will automatically:
   - Generate AI-optimized search keywords
   - Fetch relevant papers from OpenAlex
   - Provide AI-powered analysis
   - Enable PDF export of results

## Project Structure 📁

```
├── main.py                # Main application entry point
├── ai_analyzer.py         # AI analysis logic
├── api_client.py         # OpenAlex API client
├── components.py         # UI components
├── utils.py             # Utility functions
└── visualizations.py    # Data visualization components
```

## Troubleshooting 🔧

### Common Issues and Solutions

1. **ImportError: No module named 'streamlit'**
   ```bash
   pip install streamlit
   ```

2. **ModuleNotFoundError: No module named 'openai'**
   ```bash
   pip install openai
   ```

3. **API Key Error**
   - Verify `.env` file location
   - Check API key format
   - Ensure environment variables are properly loaded

4. **Port 5000 is already in use**
   ```bash
   # Modify port in .streamlit/config.toml
   port = 5001  # or any other available port
   ```

5. **PDF Generation Issues**
   - Ensure ReportLab is installed
   ```bash
   pip install reportlab
   ```
   - Verify required font files are present

### For Other Issues

- Visit the GitHub Issues page
- Share error messages and logs
- Include system details (OS, Python version)

## Contributing 🤝

1. Fork the project
2. Create a feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

## Updates and Maintenance 🔄

1. Keep your project up to date:
```bash
git pull origin main
pip install -r requirements.txt