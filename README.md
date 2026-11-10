# 🤖 Multi-Agent Research System

An AI-powered research automation system built with **Python, LangChain, Groq, and Tavily**. It uses AI agents and web search capabilities to research topics, gather relevant information, and generate research outputs through an automated pipeline.

## 🚀 Overview

The Multi-Agent Research System is designed to automate the research process by combining Large Language Models (LLMs), web search tools, and agent-based workflows.

Instead of manually searching multiple websites and collecting information, users can provide a research topic and let the AI-powered pipeline handle the research process.

## ✨ Key Features

- **AI-Powered Research:** Uses LLMs to understand and process research topics.
- **Multi-Agent Architecture:** Organizes research tasks into specialized agent workflows.
- **Real-Time Web Search:** Integrates Tavily to retrieve relevant web information.
- **LLM Integration:** Uses Groq-powered language models for AI processing.
- **Automated Pipeline:** Executes research tasks through a structured workflow.
- **Dynamic Topic Input:** Research different topics without modifying the source code.
- **Python-Based:** Modular and extensible backend implementation.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| LangChain | Agent orchestration and LLM integration |
| Groq | LLM inference |
| Tavily | Web search and information retrieval |
| Requests | HTTP requests |
| BeautifulSoup | Web content extraction |
| Python-dotenv | Environment variable management |

## 🏗️ System Workflow

The research pipeline follows these general stages:

1. **Topic Input:** User enters a research topic.
2. **Web Research:** Tavily searches the web for relevant information.
3. **Information Processing:** AI agents process the retrieved information.
4. **Research Generation:** The LLM helps generate the research output.

## 📁 Project Structure

```text
MULTI---AGENT-Research-System/
│
├── pipeline.py          # Main research pipeline
├── tools.py             # Custom research and web search tools
├── requirements.txt     # Project dependencies
├── .env                 # API credentials (not committed)
├── .env.example         # Environment variable template
├── .gitignore           # Git ignored files
└── README.md            # Project documentation
```

*Note: Adjust the file tree to match your actual project files.*

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Hussain7276/MULTI---AGENT-Research-System.git
```

### 2. Navigate to the Project

```bash
cd MULTI---AGENT-Research-System
```

### 3. Create a Virtual Environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Get your API credentials:

- [Groq Console](https://console.groq.com/)
- [Tavily](https://tavily.com/)

**Important:** Never share or commit your `.env` file or API credentials.

### 6. Run the Application

```bash
python pipeline.py
```

Enter your research topic when prompted to start the research pipeline.

## 🔐 Environment Security

Sensitive credentials are managed through environment variables using `python-dotenv`.

The following files and directories should not be committed:

- `.env`
- `venv/`
- `__pycache__/`
- Python cache files

## 🎯 Project Goals

This project explores the practical implementation of:

- Multi-agent AI systems
- LLM-powered automation
- Agent orchestration with LangChain
- Web search integration
- Automated information retrieval
- Python backend development

## 🔮 Future Improvements

- Add specialized research, analysis, and writing agents.
- Generate downloadable PDF research reports.
- Add source citations and reference tracking.
- Implement a web-based user interface.
- Add persistent research history.
- Introduce parallel agent execution.

## 👨‍💻 Author

**Muhammad Hussain Raza**

- GitHub: [@Hussain7276](https://github.com/Hussain7276)
- LinkedIn: [Muhammad Hussain Raza](https://www.linkedin.com/in/hussainraza7276/)

---

⭐ If you find this project interesting, consider giving it a star!
