
# ChemE Bot - Chemical Engineering AI Assistant

An intelligent chatbot specifically designed for chemical engineering students and professionals, powered by Google's Gemini AI with real-time web search capabilities.

## 🌟 Features

### Core Capabilities
- **Process Design & Optimization**: Get help with reactor design, separation processes, and optimization strategies
- **Unit Operations**: Detailed explanations and calculations for distillation, absorption, extraction, and more
- **Thermodynamics & Kinetics**: Phase equilibria, reaction kinetics, and thermodynamic calculations
- **Transport Phenomena**: Heat, mass, and momentum transfer concepts and calculations
- **Safety & HAZOP**: Safety protocols, risk assessment, and hazard analysis
- **Equipment Design**: Sizing and selection of chemical engineering equipment
- **Current Information**: Real-time access to latest industry standards and research

### AI-Powered Features
- **Contextual Understanding**: Recognizes chemical engineering terminology and concepts
- **Question Classification**: Automatically categorizes questions (theory, calculations, safety, design)
- **Web-Enhanced Responses**: Incorporates current information from reliable sources
- **Safety Prioritization**: Emphasizes safety considerations in all responses
- **Source Citations**: Provides references for information when available

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Streamlit account (for cloud deployment)
- Google Gemini API key

### Local Installation

1. **Clone the repository:**

cd ChemE_Bot

	1. Install dependencies:

pip install -r requirements.txt

	1. Set up API key:


		* Create .streamlit/secrets.toml file
		* Add your Gemini API key:
GEMINI_API_KEY = "your-gemini-api-key-here"

	2. Run the application:


streamlit run app.py

	1. Open your browser:

		* Navigate to http://localhost:8501
		* Start asking chemical engineering questions!

Cloud Deployment (Streamlit Cloud)
	1. Fork this repository to your GitHub account

	2. Deploy on Streamlit Cloud:


		* Go to share.streamlit.io
		* Connect your GitHub account
		* Select this repository
		* Choose app.py as the main file
	3. Add API key in Streamlit Cloud:


		* Go to your app settings
		* Navigate to "Secrets"
		* Add:
GEMINI_API_KEY = "your-gemini-api-key-here"

	4. Your bot is live! 🎉


🔧 Configuration
Environment Variables
	* GEMINI_API_KEY: Required - Your Google Gemini API key

App Settings
	* Web Search: Toggle to include/exclude web search in responses
	* Show Sources: Display source citations for responses
	* Question Types: Automatic categorization (theory, calculation, safety, design)

📚 Usage Examples
Basic Questions
"What is distillation?"
"Explain the difference between CSTR and PFR reactors"
"How does a heat exchanger work?"

Calculations
"Calculate the number of theoretical plates for benzene-toluene separation"
"How do I size a reactor for first-order reaction?"
"What's the heat duty for this heat exchanger?"

Safety Queries
"What are the safety considerations for working with benzene?"
"How do I conduct a HAZOP analysis?"
"What PPE is required for handling acids?"

Design Questions
"How do I design a distillation column?"
"What type of reactor is best for exothermic reactions?"
"How do I select a pump for my process?"

🏗️ Project Structure
ChemE_Bot/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore rules
│
└── src/                     # Core application code
    ├── __init__.py          # Package initializer
    ├── bot_engine.py        # Core AI logic with Gemini API
    ├── search_engine.py     # Web search functionality
    ├── utils.py             # Helper functions
    └── prompts.py           # Chemical engineering prompts

🔐 Security & Privacy
	* API Keys: Never commit API keys to version control
	* Local Development: Use .streamlit/secrets.toml (add to .gitignore)
	* Cloud Deployment: Use Streamlit Cloud's secrets management
	* Data Privacy: No conversation data is stored permanently
	* Safe Content: Content filtering enabled for safety

🧪 Testing
Local Testing
# Run the app locally
streamlit run app.py

# Test individual components in Python
python -c "from src.bot_engine import ChemEBot; bot = ChemEBot('your-api-key'); print(bot.ask('What is distillation?'))"

Using Jupyter Notebook
Create test notebooks to validate components:

# Test API connection
from src.bot_engine import ChemEBot
bot = ChemEBot("your-api-key")
response = bot.ask("What is a chemical reactor?")
print(response)

🛠️ Development
Adding New Features
	1. Extend prompts: Modify src/prompts.py for new question types
	2. Add utilities: Extend src/utils.py for new helper functions
	3. Enhance search: Improve src/search_engine.py for better web search
	4. UI improvements: Modify app.py for interface changes

Code Structure
	* Modular Design: Each component has specific responsibilities
	* Error Handling: Comprehensive error handling throughout
	* Type Hints: Python type hints for better code quality
	* Documentation: Detailed docstrings for all functions

🤝 Contributing
	1. Fork the repository
	2. Create a feature branch: git checkout -b feature-name
	3. Make changes and test thoroughly
	4. Commit changes: git commit -m "Add feature description"
	5. Push to branch: git push origin feature-name
	6. Create Pull Request

Contribution Guidelines
	* Follow existing code style and structure
	* Add appropriate tests for new features
	* Update documentation for any changes
	* Ensure all tests pass before submitting PR

📊 Features Roadmap
Current Version (v1.0)
	* ✅ Basic Q&A functionality
	* ✅ Web search integration
	* ✅ Chemical engineering specialization
	* ✅ Safety prioritization
	* ✅ Source citations

Planned Features (v2.0)
	* 🔄 Calculation engine integration
	* 🔄 Process diagram interpretation
	* 🔄 Multi-language support
	* 🔄 Advanced visualization
	* 🔄 Integration with simulation software

🐛 Known Issues & Limitations
Current Limitations
	* Web search limited to basic scraping (no premium APIs)
	* Calculation engine not yet integrated
	* Limited to text-based responses (no images/diagrams)
	* Response time depends on web search complexity

Workarounds
	* For complex calculations, ask for step-by-step methodology
	* For visual content, request descriptions and references
	* For faster responses, disable web search for basic questions

📞 Support & Contact
Getting Help
	* Issues: Open a GitHub issue for bugs or feature requests
	* Discussions: Use GitHub Discussions for questions
	* Documentation: Check this README and inline code comments

Troubleshooting
	* API Key Issues: Verify your Gemini API key is valid and has quota
	* Installation Problems: Ensure Python 3.8+ and all dependencies installed
	* Performance Issues: Try disabling web search for faster responses

📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

🙏 Acknowledgments
	* Google Gemini AI: For providing the core AI capabilities
	* Streamlit: For the excellent web app framework
	* Chemical Engineering Community: For inspiration and domain expertise
	* Open Source Libraries: beautifulsoup4, requests, and other dependencies

📈 Version History
v1.0.0 (Current)
	* Initial release with core functionality
	* Gemini AI integration
	* Web search capabilities
	* Chemical engineering specialization
	* Streamlit web interface

----

Built with ❤️ for the Chemical Engineering Community

Have questions or suggestions? Feel free to open an issue or contribute to the project!
```