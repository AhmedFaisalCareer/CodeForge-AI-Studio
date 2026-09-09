# ⚡ CodeForge AI Studio

> **Turn your ideas into code using natural language.**

CodeForge AI Studio is an AI-powered, multilingual code generation platform built with **Python, Streamlit, and Google Gemini**.

Users can describe what they want to create in natural language—such as English, Urdu, Hindi, Arabic, Spanish, and more—and CodeForge generates complete, runnable code in a wide range of programming languages.

---

## ✨ Features

### 🤖 AI Code Generation

Describe your idea and let AI generate the code for you.

Examples:

* Create a website
* Create a browser game
* Create a calculator
* Create a chatbot
* Create a Python application
* Create a dashboard
* Create an automation script

### 🌍 Multilingual Support

You can communicate with CodeForge in multiple languages, including:

* 🇬🇧 English
* 🇵🇰 Urdu
* 🇮🇳 Hindi
* 🇸🇦 Arabic
* 🇪🇸 Spanish
* 🇫🇷 French
* 🇩🇪 German
* 🇨🇳 Chinese
* 🇯🇵 Japanese
* 🇰🇷 Korean
* 🇹🇷 Turkish
* 🇧🇩 Bengali
* 🇵🇰 Punjabi
* 🇮🇷 Persian
* 🇵🇹 Portuguese

---

## 💻 Supported Programming Languages

CodeForge supports many popular programming languages:

| Language   | Extension |
| ---------- | --------- |
| HTML       | `.html`   |
| CSS        | `.css`    |
| JavaScript | `.js`     |
| TypeScript | `.ts`     |
| Python     | `.py`     |
| C          | `.c`      |
| C++        | `.cpp`    |
| C#         | `.cs`     |
| Java       | `.java`   |
| PHP        | `.php`    |
| Ruby       | `.rb`     |
| Go         | `.go`     |
| Rust       | `.rs`     |
| Swift      | `.swift`  |
| Kotlin     | `.kt`     |
| SQL        | `.sql`    |
| Bash       | `.sh`     |
| Dart       | `.dart`   |

---

## 🛠️ Main Features

* ⚡ AI code generation
* 🌍 Multilingual prompts
* 🎮 Game generation
* 🌐 Website generation
* 🐍 Python application generation
* 🛠️ AI code debugger
* 🧠 AI code explanation
* 📁 Multi-file project builder
* 👁️ Live HTML preview
* 📥 Download generated code
* 📚 Generation history
* 🎯 Beginner to production-level code
* 🎨 Modern red-and-black interface
* ⚙️ Adjustable AI creativity
* 💬 Natural-language programming

---

## 🧠 How It Works

The process is simple:

```text
Your Idea
   ↓
Natural Language Prompt
   ↓
CodeForge AI
   ↓
Google Gemini
   ↓
Generated Code
   ↓
Preview / Explain / Debug / Download
```

---

## 🚀 Example

You can write:

```text
Create a playable 2D space shooting game in HTML.
The player should control a spaceship, shoot enemies,
collect points, have a health system, and use keyboard controls.
```

Select:

```text
Programming Language: HTML
```

CodeForge will generate a complete HTML project containing the required HTML, CSS, and JavaScript.

---

## 🌍 Multilingual Example

You can also write your request in Urdu:

```text
HTML میں ایک ایسا گیم بنائیں جس میں ایک spaceship ہو،
دشمن ہوں، score system ہو اور player keyboard سے spaceship
کو control کر سکے۔
```

CodeForge can understand the request and generate the requested code.

---

# 📁 Project Structure

```text
CodeForge-AI-Studio/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/CodeForge-AI-Studio.git
```

Move into the project directory:

```bash
cd CodeForge-AI-Studio
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Gemini API Key

CodeForge uses Google Gemini for AI-powered generation.

Create an API key and configure it as an environment variable.

### Windows PowerShell

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Then start the application.

---

# ▶️ Run the Application

Run:

```bash
streamlit run app.py
```

The application will open in your browser.

If it does not open automatically, Streamlit will provide a local address such as:

```text
http://localhost:8501
```

---

# ☁️ Deploy on Streamlit Community Cloud

You can deploy CodeForge online using Streamlit Community Cloud.

### Steps

1. Upload the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub account.
4. Select this repository.
5. Select `app.py` as the main file.
6. Add your secret:

```toml
GEMINI_API_KEY = "YOUR_API_KEY"
```

7. Deploy the application.

---

# 🔐 Security

Never upload your Gemini API key to GitHub.

Do **not** write your real API key directly inside:

```text
app.py
```

Instead, use environment variables or Streamlit Secrets.

A `.gitignore` file should contain:

```text
.env
venv/
__pycache__/
*.pyc
.streamlit/secrets.toml
```

---

# 🎯 Use Cases

CodeForge can be useful for:

* 👨‍💻 Developers
* 🎓 Students
* 🧑‍🏫 Teachers
* 🚀 Beginners learning programming
* 💡 Entrepreneurs
* 🛠️ Software prototyping
* 🌐 Web development
* 🎮 Game development
* 📊 Data applications
* 🤖 AI projects

---

# 🔮 Future Improvements

Possible future features include:

* 🔥 AI-powered code auto-completion
* 🧪 Automatic code testing
* 🐛 Advanced error detection
* 📦 ZIP project downloads
* 🗂️ Full project file management
* 🌐 Online deployment
* 💾 Cloud project storage
* 👥 User accounts
* 🤝 Team collaboration
* 🎨 AI UI designer
* 🧩 Plugin system
* 🖥️ Built-in code editor
* 📱 Mobile-friendly improvements
* 🔄 GitHub integration

---

# 🧰 Technology Stack

### Frontend

**Streamlit**

### Backend

**Python**

### AI

**Google Gemini**

### Web Technologies

**HTML + CSS + JavaScript**

---

# 📜 License

This project is intended for educational and development purposes.

You can add your preferred open-source license to the repository.

---

# ⭐ Support

If you like CodeForge AI Studio:

* ⭐ Star the repository
* 🍴 Fork the project
* 🐛 Report bugs
* 💡 Suggest new features
* 🚀 Contribute improvements

---

## ⚡ CodeForge AI Studio

**Describe it. Generate it. Build it.**

Made with ❤️ using **Python + Streamlit + Google Gemini AI**.
