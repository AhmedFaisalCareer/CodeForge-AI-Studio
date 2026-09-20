# ⚡ CodeForge AI Studio

**CodeForge AI Studio** is a multilingual AI coding assistant built with **Python, Streamlit, and Google Gemini**.

It allows users to describe what they want to build in natural language and generate complete source code. It also includes an AI debugger, code explanation, HTML preview, multi-file project generation, downloads, and generation history.

---

## 🚀 Live Demo

**Streamlit App:**
`[YOUR-STREAMLIT-APP-LINK](https://codeforge-ai-studio-ij6nyvexybgmjfza4fyqui.streamlit.app/)`

Replace the placeholder above with your deployed Streamlit URL.

---

## ✨ Features

### 🤖 AI Code Generator

Describe your idea and CodeForge generates complete runnable code.

Examples:

* Websites
* Browser games
* Calculators
* Chatbots
* Dashboards
* Login pages
* Python applications
* Scripts
* And more

---

### 🌍 Multilingual Coding

Users can write their requests in multiple languages:

* English
* Urdu
* Hindi
* Arabic
* Spanish
* French
* German
* Chinese
* Japanese
* Korean
* Turkish
* Portuguese
* Bengali
* Punjabi
* Persian

---

### 💻 Multiple Programming Languages

CodeForge supports:

* HTML
* CSS
* JavaScript
* TypeScript
* Python
* C
* C++
* C#
* Java
* PHP
* Ruby
* Go
* Rust
* Swift
* Kotlin
* SQL
* Bash
* Dart

---

### 🐛 AI Code Debugger

Paste your broken code and error message.

CodeForge analyzes the problem and generates a corrected version of the complete source code.

---

### 🧠 AI Code Explanation

Generated code can be explained by AI.

The explanation can cover:

* What the program does
* Main components
* Variables
* Functions
* How the program works
* Programming concepts
* Customization
* Dependencies
* Possible improvements

---

### 👁️ HTML Live Preview

CodeForge includes an HTML preview workspace.

Users can preview generated HTML directly inside the application.

> Only preview HTML code that you trust.

---

### 📁 Multi-File Project Builder

Describe a complete project and CodeForge can generate multiple project files.

For example:

```text
portfolio/
├── index.html
├── style.css
└── script.js
```

The generated files can be viewed and downloaded individually.

---

### 📥 Code Downloads

Generated code can be downloaded directly from the application.

The filename is automatically selected based on the programming language.

Examples:

```text
index.html
style.css
script.js
generated_code.py
generated_code.cpp
generated_code.java
```

---

### 📚 Generation History

CodeForge stores recent generated projects during the current application session.

Users can:

* View previous requests
* View generated code
* Load previous code
* Clear generation history

The application keeps the latest 20 generations.

---

## ⚙️ AI Settings

The sidebar provides several AI controls.

### Code Complexity

Choose between:

* Beginner
* Intermediate
* Advanced
* Production

### Creativity

Adjust the AI creativity level from:

```text
0.0 → 1.0
```

### Comments

Users can choose whether the generated code should include useful comments.

---

## 🧰 Supported Frameworks

CodeForge provides options for several frameworks and technologies:

* None
* Streamlit
* React
* Next.js
* Flask
* Django
* FastAPI
* Node.js
* Express.js
* Bootstrap
* Tailwind CSS
* Pygame

---

## 🏗️ Technology Stack

| Technology          | Purpose                          |
| ------------------- | -------------------------------- |
| Python              | Application logic                |
| Streamlit           | Web application interface        |
| Google Gemini       | AI code generation               |
| Google GenAI SDK    | Gemini API integration           |
| Regular Expressions | Code cleanup and JSON processing |
| JSON                | Multi-file project processing    |

---

## 📂 Project Structure

The project contains:

```text
CodeForge-AI-Studio/
│
├── app.py
├── requirements.txt
└── README.md
```

### `app.py`

Contains the complete Streamlit application, AI functions, interface, styling, code generation, debugging, project builder, preview, and history.

### `requirements.txt`

Contains the Python packages required to run the application.

### `README.md`

Project documentation and setup instructions.

---

## 🔑 Gemini API Key Setup

CodeForge uses a Gemini API key.

### Streamlit Cloud

Add the following secret:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

Do not publish your real API key in GitHub or inside your source code.

### Windows Local Environment

You can also configure:

```text
GEMINI_API_KEY
```

as a Windows environment variable.

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone YOUR-GITHUB-REPOSITORY-URL
```

### 2. Open the project

```bash
cd CodeForge-AI-Studio
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your Gemini API key

Set `GEMINI_API_KEY` in your environment or Streamlit secrets.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📝 Example Prompts

### Website

```text
Create a modern responsive portfolio website for a Python developer.
```

### Game

```text
Create a playable browser game using HTML, CSS and JavaScript.
```

### Python

```text
Create a Python program that manages student records.
```

### Dashboard

```text
Create a modern analytics dashboard with charts and statistics.
```

### Debugging

Paste your code and error:

```text
NameError: name 'total' is not defined
```

CodeForge will generate a corrected version.

---

## 🔄 How CodeForge Works

```text
User Idea
   ↓
Natural Language Request
   ↓
CodeForge AI
   ↓
Google Gemini
   ↓
Generated Code
   ↓
Preview / Explain / Download
```

For multi-file projects:

```text
Project Description
        ↓
   Google Gemini
        ↓
     JSON Data
        ↓
   Project Files
        ↓
 View / Download Files
```

---

## 🛡️ Error Handling

CodeForge includes handling for common Gemini API problems such as:

* Missing API key
* Missing Google GenAI package
* API rate limits
* Temporary service errors
* Empty responses
* Invalid multi-file JSON responses

The application also retries temporary API errors automatically.

---

## 🎯 Project Goals

CodeForge AI Studio was designed to make programming more accessible.

Instead of starting with programming syntax, users can start with an idea:

```text
"I want to build a website for my business."
```

CodeForge turns that idea into source code using AI.

---

## 🔮 Possible Future Improvements

Future versions could include:

* User accounts
* Cloud project storage
* GitHub integration
* More AI models
* Code execution sandbox
* More framework templates
* ZIP project downloads
* File editor
* Syntax validation
* AI-powered code optimization
* AI test generation
* Project deployment tools
* Collaborative projects

---

## 👨‍💻 Developer

**Ahmed Faisal**

Interested in:

* Python
* Streamlit
* AI Applications
* Automation
* Web Applications
* Software Development

---

## ⭐ Support the Project

If you find CodeForge AI Studio useful:

* ⭐ Star the GitHub repository
* 🐛 Report bugs
* 💡 Suggest features
* 🔀 Contribute improvements

---

## ⚡ CodeForge AI Studio

**Describe it. Generate it. Build it.**
