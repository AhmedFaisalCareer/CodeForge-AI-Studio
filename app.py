import streamlit as st
import re
import json
import os
from datetime import datetime
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CodeForge AI Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# OPTIONAL GEMINI IMPORT
# ============================================================

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


# ============================================================
# CUSTOM CSS — RED & BLACK THEME
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ============================================================
   MAIN BACKGROUND
   ============================================================ */

.stApp {
    background: #ffffff;
}

.main {
    background: #ffffff;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* ============================================================
   SIDEBAR — RED
   ============================================================ */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #b30000 0%,
        #d00000 45%,
        #8f0000 100%
    ) !important;
}

section[data-testid="stSidebar"] > div {
    background: transparent !important;
}

/* Sidebar text */

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Sidebar radio buttons */

section[data-testid="stSidebar"] label {
    color: #ffffff !important;
    font-weight: 600;
}

/* Sidebar dividers */

section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.3) !important;
}

/* Sidebar metrics */

section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    color: #ffe5e5 !important;
}

/* ============================================================
   HERO
   ============================================================ */

.hero {
    padding: 35px;
    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            #fff5f5 0%,
            #ffffff 50%,
            #ffe9e9 100%
        );

    border: 2px solid #d00000;

    margin-bottom: 25px;

    box-shadow:
        0 10px 35px rgba(180,0,0,0.12);
}

.hero h1 {
    font-size: 46px;
    font-weight: 800;
    color: #111111 !important;
    margin-bottom: 8px;
}

.hero p {
    font-size: 18px;
    color: #333333 !important;
}

/* ============================================================
   MAIN HEADINGS — DARK BLACK
   ============================================================ */

h1, h2, h3, h4, h5, h6 {
    color: #111111 !important;
}

p, span, label, div {
    color: #222222;
}

/* Keep sidebar white */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div {
    color: #ffffff !important;
}

/* ============================================================
   FEATURE CARDS
   ============================================================ */

.feature-card {
    background: #ffffff;

    border: 1px solid #eeeeee;

    padding: 20px;

    border-radius: 18px;

    min-height: 150px;

    box-shadow:
        0 5px 20px rgba(0,0,0,0.07);

    transition: all 0.25s ease;
}

.feature-card:hover {
    transform: translateY(-4px);

    border-color: #d00000;

    box-shadow:
        0 10px 30px rgba(180,0,0,0.14);
}

.feature-card h3 {
    color: #111111 !important;
    margin-top: 0;
}

.feature-card p {
    color: #555555 !important;
}

/* ============================================================
   STAT CARDS
   ============================================================ */

.stat-card {
    padding: 18px;

    border-radius: 16px;

    background: #ffffff;

    border: 1px solid #eeeeee;

    text-align: center;

    box-shadow:
        0 5px 20px rgba(0,0,0,0.06);
}

.stat-number {
    font-size: 28px;
    font-weight: 800;
    color: #b00000 !important;
}

.stat-label {
    color: #555555 !important;
    font-size: 13px;
}

/* ============================================================
   BUTTONS — RED
   ============================================================ */

.stButton > button {
    border-radius: 10px;

    font-weight: 700;

    border: 1px solid #b00000;

    background: #d00000;

    color: #ffffff !important;

    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #a80000;

    border-color: #8f0000;

    color: #ffffff !important;

    transform: translateY(-1px);
}

/* Primary buttons */

.stButton > button[kind="primary"] {
    background: linear-gradient(
        135deg,
        #e00000,
        #a80000
    ) !important;

    color: #ffffff !important;

    border: none !important;

    box-shadow:
        0 5px 15px rgba(200,0,0,0.25);
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(
        135deg,
        #b00000,
        #850000
    ) !important;
}

/* ============================================================
   TEXT INPUTS
   ============================================================ */

.stTextInput input,
.stTextArea textarea {
    background: #ffffff !important;

    color: #111111 !important;

    border: 1px solid #cccccc !important;

    border-radius: 10px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border: 2px solid #d00000 !important;

    box-shadow:
        0 0 0 2px rgba(208,0,0,0.10) !important;
}

/* ============================================================
   SELECT BOX
   ============================================================ */

div[data-baseweb="select"] > div {
    background: #ffffff !important;

    color: #111111 !important;

    border-color: #cccccc !important;
}

/* ============================================================
   CODE BLOCK
   ============================================================ */

pre {
    border-radius: 14px !important;
}

/* ============================================================
   RED HORIZONTAL LINE
   ============================================================ */

hr {
    border: none !important;

    border-top: 2px solid #eeeeee !important;

    margin: 25px 0;
}

/* ============================================================
   SUCCESS BOX
   ============================================================ */

.success-box {
    padding: 15px;

    border-radius: 12px;

    background: #fff3f3;

    border: 1px solid #d00000;

    color: #700000;
}

/* ============================================================
   INFO BOX
   ============================================================ */

.info-box {
    padding: 15px;

    border-radius: 12px;

    background: #fff5f5;

    border: 1px solid #e00000;

    color: #333333;
}

/* ============================================================
   EXPANDERS
   ============================================================ */

.streamlit-expanderHeader {
    background: #fff5f5 !important;

    color: #111111 !important;

    border-radius: 10px;
}

/* ============================================================
   DOWNLOAD BUTTONS
   ============================================================ */

.stDownloadButton > button {
    background: #ffffff !important;

    color: #b00000 !important;

    border: 2px solid #b00000 !important;

    border-radius: 10px;

    font-weight: 700;
}

.stDownloadButton > button:hover {
    background: #b00000 !important;

    color: #ffffff !important;
}

/* ============================================================
   ALERTS
   ============================================================ */

[data-testid="stAlert"] {
    border-radius: 12px;
}

/* ============================================================
   SCROLLBAR
   ============================================================ */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
    background: #b00000;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #850000;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "generated_code" not in st.session_state:
    st.session_state.generated_code = ""

if "generated_language" not in st.session_state:
    st.session_state.generated_language = "HTML"

if "generated_filename" not in st.session_state:
    st.session_state.generated_filename = "index.html"

if "explanation" not in st.session_state:
    st.session_state.explanation = ""

if "project_files" not in st.session_state:
    st.session_state.project_files = {}

if "total_generations" not in st.session_state:
    st.session_state.total_generations = 0


# ============================================================
# LANGUAGE DATA
# ============================================================

LANGUAGES = {
    "HTML": {
        "extension": "html",
        "comment": "<!-- -->",
        "type": "web"
    },
    "CSS": {
        "extension": "css",
        "comment": "/* */",
        "type": "web"
    },
    "JavaScript": {
        "extension": "js",
        "comment": "//",
        "type": "web"
    },
    "TypeScript": {
        "extension": "ts",
        "comment": "//",
        "type": "web"
    },
    "Python": {
        "extension": "py",
        "comment": "#",
        "type": "general"
    },
    "C": {
        "extension": "c",
        "comment": "//",
        "type": "general"
    },
    "C++": {
        "extension": "cpp",
        "comment": "//",
        "type": "general"
    },
    "C#": {
        "extension": "cs",
        "comment": "//",
        "type": "general"
    },
    "Java": {
        "extension": "java",
        "comment": "//",
        "type": "general"
    },
    "PHP": {
        "extension": "php",
        "comment": "//",
        "type": "web"
    },
    "Ruby": {
        "extension": "rb",
        "comment": "#",
        "type": "general"
    },
    "Go": {
        "extension": "go",
        "comment": "//",
        "type": "general"
    },
    "Rust": {
        "extension": "rs",
        "comment": "//",
        "type": "general"
    },
    "Swift": {
        "extension": "swift",
        "comment": "//",
        "type": "general"
    },
    "Kotlin": {
        "extension": "kt",
        "comment": "//",
        "type": "general"
    },
    "SQL": {
        "extension": "sql",
        "comment": "--",
        "type": "database"
    },
    "Bash": {
        "extension": "sh",
        "comment": "#",
        "type": "shell"
    },
    "Dart": {
        "extension": "dart",
        "comment": "//",
        "type": "general"
    }
}


USER_LANGUAGES = [
    "English",
    "Urdu",
    "Hindi",
    "Arabic",
    "Spanish",
    "French",
    "German",
    "Chinese",
    "Japanese",
    "Korean",
    "Turkish",
    "Portuguese",
    "Bengali",
    "Punjabi",
    "Persian"
]


# ============================================================
# API KEY
# ============================================================

def get_api_key():

    # Streamlit Cloud secrets
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    # Local environment
    return os.getenv("GEMINI_API_KEY", "")


# ============================================================
# CLEAN AI RESPONSE
# ============================================================

def clean_code(text):

    if not text:
        return ""

    text = text.strip()

    # Remove markdown fences
    text = re.sub(
        r"^```[a-zA-Z0-9_+\-#]*\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


# ============================================================
# FILE EXTENSION
# ============================================================

def get_filename(language):

    data = LANGUAGES.get(language)

    if not data:
        return "generated_code.txt"

    return f"generated_code.{data['extension']}"


# ============================================================
# AI GENERATOR
# ============================================================

def generate_code(
    request,
    language,
    response_language,
    complexity,
    include_comments,
    framework,
    creativity
):

    api_key = get_api_key()

    if not api_key:
        return None, "API_KEY_MISSING"

    if not GEMINI_AVAILABLE:
        return None, "GEMINI_PACKAGE_MISSING"

    try:

        client = genai.Client(api_key=api_key)

        comment_instruction = (
            "Include helpful comments."
            if include_comments
            else "Keep comments minimal."
        )

        framework_instruction = (
            framework
            if framework != "None"
            else "Do not require an external framework unless absolutely necessary."
        )

        prompt = f"""
You are CodeForge AI, an expert software engineer and multilingual
programming assistant.

USER REQUEST:
{request}

PROGRAMMING LANGUAGE:
{language}

USER'S NATURAL LANGUAGE:
{response_language}

COMPLEXITY:
{complexity}

FRAMEWORK / TECHNOLOGY:
{framework_instruction}

COMMENTS:
{comment_instruction}

CREATIVITY:
{creativity}

TASK:

Create production-quality, complete, runnable code that directly solves
the user's request.

Important rules:

1. Return ONLY the source code.
2. Do NOT wrap the answer in markdown code fences.
3. Do NOT write explanations before or after the code.
4. Do not leave TODO placeholders.
5. Make the application functional.
6. Handle reasonable errors.
7. Use modern best practices.
8. If the requested language is HTML, create a complete HTML document.
9. If HTML is requested, CSS and JavaScript may be embedded inside the
   same HTML file when useful.
10. Make UI projects visually polished and responsive.
11. Respect the user's requested language for comments/text where possible.
12. Never expose API keys, passwords, tokens, or secrets.
13. If the user asks for a game, make it actually playable.
14. If the user asks for a website, make it interactive where appropriate.
15. Prefer self-contained code when possible.
"""

        temperature = float(creativity)

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=12000
            )
        )

        code = clean_code(response.text)

        if not code:
            return None, "EMPTY_RESPONSE"

        return code, None

    except Exception as e:
        return None, str(e)


# ============================================================
# EXPLANATION
# ============================================================

def explain_code(code, language, response_language):

    api_key = get_api_key()

    if not api_key or not GEMINI_AVAILABLE:
        return "AI explanation requires a configured Gemini API key."

    try:

        client = genai.Client(api_key=api_key)

        prompt = f"""
Explain the following {language} code clearly.

Respond in {response_language}.

Cover:

1. What the program does
2. Main components
3. Important functions
4. How the code works
5. Important concepts used
6. How the user can customize it
7. Any dependencies
8. Potential improvements

Keep the explanation educational and easy to understand.

CODE:

{code}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=5000
            )
        )

        return response.text

    except Exception as e:
        return f"Could not generate explanation: {e}"


# ============================================================
# DEBUG CODE
# ============================================================

def debug_code(code, language, error_message, response_language):

    api_key = get_api_key()

    if not api_key or not GEMINI_AVAILABLE:
        return None

    try:

        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an expert debugging assistant.

Programming language:
{language}

User language:
{response_language}

ERROR:
{error_message}

CODE:
{code}

Fix the code.

Return ONLY the complete corrected code.
Do not use markdown fences.
Do not provide explanations.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=12000
            )
        )

        return clean_code(response.text)

    except Exception:
        return None


# ============================================================
# PROJECT GENERATOR
# ============================================================

def generate_project(request, response_language):

    api_key = get_api_key()

    if not api_key or not GEMINI_AVAILABLE:
        return {}

    try:

        client = genai.Client(api_key=api_key)

        prompt = f"""
Create a complete multi-file software project.

User request:
{request}

Response language:
{response_language}

Return ONLY valid JSON in this structure:

{{
    "files": {{
        "index.html": "file content",
        "style.css": "file content",
        "script.js": "file content"
    }}
}}

Rules:
- Only include files actually required.
- No markdown.
- No explanation.
- Escape JSON correctly.
- Make every file complete and functional.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=16000
            )
        )

        raw = response.text.strip()

        raw = re.sub(r"^```json", "", raw)
        raw = re.sub(r"^```", "", raw)
        raw = re.sub(r"```$", "", raw)

        return json.loads(raw.strip()).get("files", {})

    except Exception:
        return {}


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚡ CodeForge")

    st.caption("AI Multilingual Code Studio")

    st.divider()

    page = st.radio(
        "Workspace",
        [
            "🏠 Generator",
            "🛠️ Debugger",
            "👁️ Preview",
            "📁 Project Builder",
            "📚 History",
            "ℹ️ About"
        ]
    )

    st.divider()

    st.markdown("### ⚙️ AI Settings")

    complexity = st.select_slider(
        "Code complexity",
        options=[
            "Beginner",
            "Intermediate",
            "Advanced",
            "Production"
        ],
        value="Advanced"
    )

    creativity = st.slider(
        "Creativity",
        0.0,
        1.0,
        0.65,
        0.05
    )

    include_comments = st.checkbox(
        "Include comments",
        value=True
    )

    st.divider()

    st.markdown("### 📊 Statistics")

    st.metric(
        "Generations",
        st.session_state.total_generations
    )

    st.metric(
        "History",
        len(st.session_state.history)
    )

    st.divider()

    st.caption("CodeForge AI Studio")
    st.caption("Built with Python + Streamlit + Gemini")


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<h1>⚡ CodeForge AI Studio</h1>

<p>
Turn your ideas into real computer programs using natural language.
Ask in English, Urdu, Hindi or many other languages.
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# GENERATOR
# ============================================================

if page == "🏠 Generator":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>🤖 AI Generation</h3>
        <p>Describe your idea and receive complete runnable code.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
        <h3>🌍 Multilingual</h3>
        <p>Write your request in English, Urdu, Hindi and more.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
        <h3>🚀 Any Project</h3>
        <p>Games, websites, tools, automation, apps and more.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## ✨ Create Something")

    left, right = st.columns([2, 1])

    with left:

        request = st.text_area(
            "Describe what you want to build",
            height=190,
            placeholder=(
                "Example:\n"
                "Create a 2D space shooting game with a spaceship, "
                "enemies, score, health system and keyboard controls. "
                "Make it in HTML, CSS and JavaScript."
            )
        )

    with right:

        language = st.selectbox(
            "Programming language",
            list(LANGUAGES.keys()),
            index=0
        )

        response_language = st.selectbox(
            "Your language",
            USER_LANGUAGES,
            index=0
        )

        framework_options = [
            "None",
            "Streamlit",
            "React",
            "Next.js",
            "Flask",
            "Django",
            "FastAPI",
            "Node.js",
            "Express.js",
            "Bootstrap",
            "Tailwind CSS",
            "Pygame"
        ]

        framework = st.selectbox(
            "Framework / technology",
            framework_options
        )

    st.markdown("### 💡 Quick Ideas")

    ideas = [
        "🎮 Create a browser game",
        "🌐 Create a modern portfolio",
        "🧮 Create a calculator",
        "🤖 Create an AI chatbot",
        "📊 Create a dashboard",
        "🔐 Create a login page"
    ]

    idea_cols = st.columns(6)

    for i, idea in enumerate(ideas):

        with idea_cols[i]:

            if st.button(
                idea,
                use_container_width=True,
                key=f"idea_{i}"
            ):

                idea_requests = {
                    0: "Create a playable browser game using HTML, CSS and JavaScript.",
                    1: "Create a modern responsive developer portfolio website.",
                    2: "Create a beautiful scientific calculator.",
                    3: "Create a chatbot interface.",
                    4: "Create a modern analytics dashboard.",
                    5: "Create a modern responsive login page."
                }

                st.session_state.quick_request = idea_requests[i]

    if "quick_request" in st.session_state:
        request = st.session_state.quick_request

    st.markdown("")

    generate = st.button(
        "⚡ Generate Code",
        type="primary",
        use_container_width=True
    )

    if generate:

        if not request.strip():

            st.warning("Please describe what you want to build.")

        else:

            with st.spinner("🧠 CodeForge is writing your code..."):

                code, error = generate_code(
                    request=request,
                    language=language,
                    response_language=response_language,
                    complexity=complexity,
                    include_comments=include_comments,
                    framework=framework,
                    creativity=creativity
                )

            if error:

                if error == "API_KEY_MISSING":

                    st.error(
                        "Gemini API key not found. Add GEMINI_API_KEY "
                        "to Streamlit Secrets or your environment."
                    )

                elif error == "GEMINI_PACKAGE_MISSING":

                    st.error(
                        "Gemini package is missing. Install "
                        "`google-genai`."
                    )

                else:

                    st.error(f"Generation failed: {error}")

            else:

                st.session_state.generated_code = code
                st.session_state.generated_language = language
                st.session_state.generated_filename = get_filename(language)
                st.session_state.total_generations += 1

                history_item = {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "request": request,
                    "language": language,
                    "code": code
                }

                st.session_state.history.insert(
                    0,
                    history_item
                )

                st.session_state.history = (
                    st.session_state.history[:20]
                )

                st.success("✅ Code generated successfully!")

    if st.session_state.generated_code:

        st.markdown("---")

        st.markdown("## 💻 Generated Code")

        code = st.session_state.generated_code
        current_language = st.session_state.generated_language

        st.code(
            code,
            language=current_language.lower()
        )

        download_col, explain_col = st.columns(2)

        with download_col:

            st.download_button(
                "📥 Download Code",
                data=code,
                file_name=st.session_state.generated_filename,
                mime="text/plain",
                use_container_width=True
            )

        with explain_col:

            if st.button(
                "🧠 Explain Code",
                use_container_width=True
            ):

                with st.spinner("Explaining..."):

                    st.session_state.explanation = explain_code(
                        code,
                        current_language,
                        response_language
                    )

        if st.session_state.explanation:

            st.markdown("## 📖 AI Explanation")

            st.markdown(
                st.session_state.explanation
            )


# ============================================================
# DEBUGGER
# ============================================================

elif page == "🛠️ Debugger":

    st.markdown("## 🛠️ AI Code Debugger")

    st.write(
        "Paste broken code and the error message. "
        "CodeForge will try to repair it."
    )

    debug_language = st.selectbox(
        "Programming language",
        list(LANGUAGES.keys()),
        key="debug_language"
    )

    debug_code_input = st.text_area(
        "Broken code",
        height=350,
        placeholder="Paste your code here..."
    )

    error_message = st.text_area(
        "Error message",
        height=130,
        placeholder="Paste the error message here..."
    )

    debug_language_response = st.selectbox(
        "Explanation language",
        USER_LANGUAGES,
        key="debug_response_language"
    )

    if st.button(
        "🐛 Fix My Code",
        type="primary",
        use_container_width=True
    ):

        if not debug_code_input.strip():

            st.warning("Paste some code first.")

        else:

            with st.spinner("🔎 Analyzing code..."):

                fixed = debug_code(
                    debug_code_input,
                    debug_language,
                    error_message,
                    debug_language_response
                )

            if fixed:

                st.success("✅ A corrected version was generated.")

                st.code(
                    fixed,
                    language=debug_language.lower()
                )

                st.download_button(
                    "📥 Download Fixed Code",
                    fixed,
                    file_name=f"fixed.{LANGUAGES[debug_language]['extension']}",
                    mime="text/plain",
                    use_container_width=True
                )

            else:

                st.error(
                    "Could not debug the code. Check your API configuration."
                )


# ============================================================
# HTML PREVIEW
# ============================================================

elif page == "👁️ Preview":

    st.markdown("## 👁️ Live HTML Preview")

    st.info(
        "This preview works with generated HTML. "
        "Only preview code you trust."
    )

    html_code = st.session_state.generated_code

    if not html_code:

        html_code = st.text_area(
            "Paste HTML",
            height=400,
            placeholder="Paste your HTML here..."
        )

    else:

        st.text_area(
            "Current HTML",
            value=html_code,
            height=250,
            key="preview_source"
        )

    if html_code:

        st.markdown("### 🌐 Preview")

        st.components.v1.html(
            html_code,
            height=650,
            scrolling=True
        )


# ============================================================
# PROJECT BUILDER
# ============================================================

elif page == "📁 Project Builder":

    st.markdown("## 📁 AI Multi-File Project Builder")

    st.write(
        "Describe a complete project and CodeForge can generate "
        "multiple files."
    )

    project_request = st.text_area(
        "Describe your project",
        height=180,
        placeholder=(
            "Example: Create a modern portfolio website with "
            "home, about, projects and contact sections."
        )
    )

    project_language = st.selectbox(
        "Response language",
        USER_LANGUAGES,
        key="project_language"
    )

    if st.button(
        "🚀 Build Project",
        type="primary",
        use_container_width=True
    ):

        if not project_request.strip():

            st.warning("Describe your project first.")

        else:

            with st.spinner("🏗️ Building project files..."):

                files = generate_project(
                    project_request,
                    project_language
                )

            if files:

                st.session_state.project_files = files

                st.success(
                    f"Created {len(files)} project files."
                )

            else:

                st.error(
                    "Project generation failed. "
                    "Check your Gemini API key."
                )

    if st.session_state.project_files:

        st.markdown("### 📦 Generated Files")

        for filename, content in st.session_state.project_files.items():

            with st.expander(f"📄 {filename}", expanded=True):

                st.code(
                    content,
                    language=(
                        filename.split(".")[-1]
                        if "." in filename
                        else "text"
                    )
                )

                st.download_button(
                    f"📥 Download {filename}",
                    content,
                    file_name=filename,
                    mime="text/plain",
                    key=f"download_{filename}"
                )


# ============================================================
# HISTORY
# ============================================================

elif page == "📚 History":

    st.markdown("## 📚 Generation History")

    if not st.session_state.history:

        st.info(
            "Your generated projects will appear here."
        )

    else:

        if st.button(
            "🗑️ Clear History",
            use_container_width=True
        ):

            st.session_state.history = []

            st.rerun()

        for index, item in enumerate(
            st.session_state.history
        ):

            with st.expander(
                f"{index + 1}. {item['language']} — "
                f"{item['request'][:70]}..."
            ):

                st.caption(item["time"])

                st.write(
                    item["request"]
                )

                st.code(
                    item["code"],
                    language=item["language"].lower()
                )

                if st.button(
                    "Load Code",
                    key=f"load_{index}"
                ):

                    st.session_state.generated_code = item["code"]

                    st.session_state.generated_language = (
                        item["language"]
                    )

                    st.session_state.generated_filename = (
                        get_filename(item["language"])
                    )

                    st.success("Loaded into workspace.")


# ============================================================
# ABOUT
# ============================================================

elif page == "ℹ️ About":

    st.markdown("## ⚡ About CodeForge AI Studio")

    st.markdown("""
    **CodeForge AI Studio** is an AI-powered multilingual programming
    assistant built with Python and Streamlit.

    ### 🎯 What can it do?

    - Generate computer programs from natural language
    - Generate websites
    - Create browser games
    - Generate Python applications
    - Explain existing code
    - Debug code
    - Build multi-file projects
    - Preview HTML
    - Download generated files

    ### 🌍 Natural-language support

    You can communicate with the AI in many languages, including:

    **English • Urdu • Hindi • Arabic • Spanish • French • German •
    Chinese • Japanese • Korean • Turkish • Bengali • Punjabi**

    ### 💻 Programming languages

    CodeForge supports many popular programming languages such as:

    **Python • HTML • CSS • JavaScript • TypeScript • C • C++ • C# •
    Java • PHP • Ruby • Go • Rust • Swift • Kotlin • SQL • Bash • Dart**

    ### 🧠 Technology

    - Python
    - Streamlit
    - Google Gemini
    - HTML
    - CSS
    - JavaScript

    """)

    st.markdown("---")

    st.markdown(
        "### 🚀 Turn an idea into code."
    )
