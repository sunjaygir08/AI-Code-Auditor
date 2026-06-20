# ⚡ DevAI: Static Code Auditor & Optimizer

DevAI is a minimalist, high-performance static code analysis dashboard built with **Streamlit** and powered by the modern **Google GenAI SDK (`gemini-3.5-flash`)**. It instantly audits source code layouts, catches syntax or logical bugs, evaluates complexity metrics, and generates optimized runtime code patches.

## 🚀 Key Features
- **Multi-Language Pipeline:** Seamlessly parses Python, Java, C++, JavaScript, and Go structures.
- **Production-Ready UI:** Responsive dual-column console layout optimizing user code input vs real-time audit logs.
- **Ultra-Crisp Diagnostics:** Strips away verbose explanations to deliver clean, comment-free refactored code block templates.
- **Automated Metrics:** Direct diagnostic output for Time/Space Complexities (O(1), O(N), etc.) and best-practice gates.

---

## 🛠️ Quick Setup & Installation

### 1. Initialize Environment
Clone this repository to your workstation, open your terminal, and install the required engineering stacks:
pip install streamlit google-genai

2. Configure Environment Secrets
Create a secure local directory file structure at .streamlit/secrets.toml in your root workspace and map your Google AI Studio API key token:

Ini, TOML
GEMINI_API_KEY = "AIzaSyYourActualAPIKeyHere..."

3. Deploy the Application Locally
Launch the reactive automation pipeline server via the terminal:

streamlit run app.py


📂 Project Architecture Layout
Plaintext
├── .streamlit/
│   └── secrets.toml      # Local encrypted environment authentication key
├── .venv/                # Isolated python virtual runtime environment (Git Ignored)
├── app.py                # Core Streamlit dashboard rendering application script
├── README.md             # Developer setup configuration & pipeline manual
└── .gitignore            # Version control tracking exclusions layout rules