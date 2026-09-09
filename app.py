import streamlit as st
import re
import json
import os
import time
import random
from datetime import datetime


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
# GEMINI IMPORT
# ============================================================

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


# ============================================================
# CUSTOM CSS — RED + BLACK THEME
# ============================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #ffffff;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* ============================================================
   SIDEBAR
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

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.30) !important;
}

section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    color: #ffe5e5 !important;
}

/* ============================================================
   MAIN TEXT
   ============================================================ */

h1, h2, h3, h4, h5, h6 {
    color: #111111 !important;
}

p {
    color: #222222;
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
}

.feature-card p {
    color: #555555 !important;
}

/* ============================================================
   BUTTONS
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
   SELECTBOX
   ============================================================ */

div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #111111 !important;
    border-color: #cccccc !important;
}

/* ============================================================
   DOWNLOAD BUTTON
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
   EXPANDERS
   ============================================================ */

[data-testid="stExpander"] {
    border: 1px solid #eeeeee !important;
    border-radius: 12px !important;
}

.streamlit-expanderHeader {
    color: #111111 !important;
}

/* ============================================================
   CODE
   ============================================================ */

pre {
    border-radius: 14px !important;
}

/* ============================================================
   DIVIDERS
   ============================================================ */

hr {
    border: none !important;
    border-top: 2px solid #eeeeee !important;
    margin: 25px 0;
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
""",
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "history": [],
    "generated_code": "",
    "generated_language": "HTML",
    "generated_filename": "index.html",
    "explanation": "",
    "project_files": {},
    "total_generations": 0,
    "quick_request": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# SUPPORTED LANGUAGES
# ============================================================

LANGUAGES = {
    "HTML": "html",
    "CSS": "css",
    "JavaScript": "js",
    "TypeScript": "ts",
    "Python": "py",
    "C": "c",
    "C++": "cpp",
    "C#": "cs",
    "Java": "java",
    "PHP": "php",
    "Ruby": "rb",
    "Go": "go",
    "Rust": "rs",
    "Swift": "swift",
    "Kotlin": "kt",
    "SQL": "sql",
    "Bash": "sh",
    "Dart": "dart"
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


FRAMEWORKS = [
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


# ============================================================
# API KEY
# ============================================================

def get_api_key():

    # Streamlit Cloud Secrets
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    # Windows / local environment
    return os.getenv("GEMINI_API_KEY", "")


# ============================================================
# CLEAN GENERATED CODE
# ============================================================

def clean_code(text):

    if not text:
        return ""

    text = text.strip()

    text = re.sub(
        r"^```[a-zA-Z0-9_+#\-]*\s*",
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
# FILENAME
# ============================================================

def get_filename(language):

    extension = LANGUAGES.get(language, "txt")

    if language == "HTML":
        return "index.html"

    if language == "CSS":
        return "style.css"

    if language == "JavaScript":
        return "script.js"

    if language == "TypeScript":
        return "script.ts"

    return f"generated_code.{extension}"


# ============================================================
# GEMINI REQUEST WITH RETRY + FALLBACK
# ============================================================

def call_gemini(
    prompt,
    temperature=0.6,
    max_output_tokens=12000
):

    api_key = get_api_key()

    if not api_key:
        return None, "API_KEY_MISSING"

    if not GEMINI_AVAILABLE:
        return None, "GEMINI_PACKAGE_MISSING"

    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        return None, f"CLIENT_ERROR: {e}"

    # Primary model first, fallback second
    models = [
        "gemini-3-flash-preview",
    
    ]

    last_error = None

    for model in models:

        for attempt in range(4):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=max_output_tokens
                    )
                )

                if response and response.text:

                    return response.text, None

                last_error = "EMPTY_RESPONSE"

            except Exception as e:

                error_text = str(e)
                last_error = error_text

                temporary_error = any(
                    x in error_text.upper()
                    for x in [
                        "503",
                        "UNAVAILABLE",
                        "429",
                        "RESOURCE_EXHAUSTED",
                        "500",
                        "INTERNAL"
                    ]
                )

                if temporary_error:

                    # Exponential backoff:
                    # approximately 2, 4, 8, 16 seconds
                    wait_time = (
                        2 ** attempt
                        + random.uniform(0.5, 1.5)
                    )

                    time.sleep(wait_time)

                    continue

                # Don't retry permanent errors
                break

    return None, last_error


# ============================================================
# GENERATE CODE
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

    comment_instruction = (
        "Include useful comments."
        if include_comments
        else "Use minimal comments."
    )

    framework_instruction = (
        framework
        if framework != "None"
        else "No external framework is required."
    )

    prompt = f"""
You are CodeForge AI, an expert software engineer,
programming teacher and multilingual coding assistant.

USER REQUEST:
{request}

PROGRAMMING LANGUAGE:
{language}

USER LANGUAGE:
{response_language}

CODE LEVEL:
{complexity}

FRAMEWORK:
{framework_instruction}

COMMENTS:
{comment_instruction}

CREATIVITY:
{creativity}

Your task is to create complete, functional,
high-quality and runnable code.

IMPORTANT RULES:

1. Return ONLY the source code.
2. Do NOT use markdown code fences.
3. Do NOT add an explanation before the code.
4. Do NOT add an explanation after the code.
5. Do NOT leave TODO placeholders.
6. Make the program actually functional.
7. Use modern best practices.
8. Handle reasonable errors.
9. Never expose API keys, passwords or secrets.
10. If HTML is requested, create a complete HTML document.
11. HTML projects may include CSS and JavaScript in the same file.
12. If the user asks for a game, make it playable.
13. If the user asks for a website, make it responsive.
14. If the user asks for a UI, make it visually polished.
15. Respect the requested programming language.
16. Use the user's natural language for visible UI text when appropriate.

Generate the final code now.
"""

    return call_gemini(
        prompt,
        temperature=float(creativity),
        max_output_tokens=12000
    )


# ============================================================
# EXPLAIN CODE
# ============================================================

def explain_code(
    code,
    language,
    response_language
):

    prompt = f"""
You are an expert programming teacher.

Explain this {language} code.

Respond in {response_language}.

Explain:

1. What the program does
2. Main components
3. Important variables
4. Important functions
5. How the program works
6. Important programming concepts
7. How the user can customize it
8. Dependencies
9. Possible improvements

Keep the explanation clear and educational.

CODE:

{code}
"""

    return call_gemini(
        prompt,
        temperature=0.3,
        max_output_tokens=5000
    )


# ============================================================
# DEBUG CODE
# ============================================================

def debug_code(
    code,
    language,
    error_message,
    response_language
):

    prompt = f"""
You are an expert software debugger.

PROGRAMMING LANGUAGE:
{language}

USER LANGUAGE:
{response_language}

ERROR:
{error_message}

CODE:
{code}

Find and fix the problems.

Return ONLY the complete corrected source code.

Rules:

1. No markdown fences.
2. No explanation.
3. No TODO placeholders.
4. Preserve the original purpose.
5. Improve error handling where useful.
6. Return complete runnable code.
"""

    return call_gemini(
        prompt,
        temperature=0.2,
        max_output_tokens=12000
    )


# ============================================================
# MULTI-FILE PROJECT
# ============================================================

def generate_project(
    request,
    response_language
):

    prompt = f"""
You are a senior full-stack developer.

Create a complete multi-file project.

USER REQUEST:
{request}

USER LANGUAGE:
{response_language}

Return ONLY valid JSON.

Required format:

{{
    "files": {{
        "filename.ext": "complete file content",
        "another.ext": "complete file content"
    }}
}}

Rules:

1. Return valid JSON only.
2. Do not use markdown.
3. Do not include explanations.
4. Include only necessary files.
5. Every file must be complete.
6. Make the project functional.
7. Escape JSON characters correctly.
8. Never include API keys or secrets.
9. Use modern coding practices.
"""

    result, error = call_gemini(
        prompt,
        temperature=0.7,
        max_output_tokens=16000
    )

    if error:
        return {}, error

    try:

        raw = result.strip()

        raw = re.sub(
            r"^```json\s*",
            "",
            raw,
            flags=re.IGNORECASE
        )

        raw = re.sub(
            r"^```\s*",
            "",
            raw
        )

        raw = re.sub(
            r"\s*```$",
            "",
            raw
        )

        data = json.loads(raw)

        files = data.get("files", {})

        if isinstance(files, dict):
            return files, None

        return {}, "Invalid project structure."

    except Exception as e:

        return {}, f"PROJECT_JSON_ERROR: {e}"


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
        min_value=0.0,
        max_value=1.0,
        value=0.65,
        step=0.05
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
    st.caption("Python • Streamlit • Gemini")


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">

<h1>⚡ CodeForge AI Studio</h1>

<p>
Turn your ideas into real computer programs using natural language.
Ask in English, Urdu, Hindi, Arabic, Spanish and many other languages.
</p>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# GENERATOR PAGE
# ============================================================

if page == "🏠 Generator":

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
<div class="feature-card">

<h3>🤖 AI Generation</h3>

<p>
Describe your idea and receive complete runnable code.
</p>

</div>
""",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
<div class="feature-card">

<h3>🌍 Multilingual</h3>

<p>
Write your request in English, Urdu, Hindi and more.
</p>

</div>
""",
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
<div class="feature-card">

<h3>🚀 Any Project</h3>

<p>
Create games, websites, tools, dashboards and applications.
</p>

</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("## ✨ Create Something")

    left, right = st.columns([2, 1])

    with left:

        request = st.text_area(
            "Describe what you want to build",
            value=st.session_state.quick_request,
            height=190,
            placeholder=(
                "Example:\n\n"
                "Create a 2D space shooting game with a spaceship, "
                "enemies, score, health system and keyboard controls. "
                "Make it in HTML."
            )
        )

    with right:

        language = st.selectbox(
            "Programming language",
            list(LANGUAGES.keys())
        )

        response_language = st.selectbox(
            "Your language",
            USER_LANGUAGES
        )

        framework = st.selectbox(
            "Framework / technology",
            FRAMEWORKS
        )

    st.markdown("### 💡 Quick Ideas")

    ideas = [
        ("🎮", "Browser Game"),
        ("🌐", "Portfolio"),
        ("🧮", "Calculator"),
        ("🤖", "Chatbot"),
        ("📊", "Dashboard"),
        ("🔐", "Login Page")
    ]

    idea_columns = st.columns(6)

    quick_requests = [
        "Create a playable browser game using HTML, CSS and JavaScript.",
        "Create a modern responsive developer portfolio website.",
        "Create a beautiful scientific calculator.",
        "Create a modern chatbot interface.",
        "Create a modern analytics dashboard.",
        "Create a modern responsive login page."
    ]

    for i, (icon, name) in enumerate(ideas):

        with idea_columns[i]:

            if st.button(
                f"{icon} {name}",
                use_container_width=True,
                key=f"quick_{i}"
            ):

                st.session_state.quick_request = quick_requests[i]

                st.rerun()

    st.markdown("")

    generate = st.button(
        "⚡ Generate Code",
        type="primary",
        use_container_width=True
    )

    if generate:

        if not request.strip():

            st.warning(
                "Please describe what you want to build."
            )

        else:

            with st.spinner(
                "🧠 CodeForge is generating your code..."
            ):

                result, error = generate_code(
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
                        "❌ GEMINI_API_KEY was not found."
                    )

                    st.info(
                        "Add GEMINI_API_KEY to Streamlit Secrets "
                        "or your Windows environment variables."
                    )

                elif error == "GEMINI_PACKAGE_MISSING":

                    st.error(
                        "❌ google-genai is not installed."
                    )

                    st.code(
                        "pip install -U google-genai"
                    )

                elif (
                    "503" in str(error)
                    or "UNAVAILABLE" in str(error).upper()
                ):

                    st.error(
                        "⚠️ Gemini is currently experiencing "
                        "high demand."
                    )

                    st.info(
                        "CodeForge already attempted automatic retries "
                        "and a fallback model. Please wait a little "
                        "and try again."
                    )

                elif (
                    "429" in str(error)
                    or "RESOURCE_EXHAUSTED" in str(error).upper()
                ):

                    st.error(
                        "⚠️ API rate limit reached."
                    )

                    st.info(
                        "Please wait before making another request."
                    )

                else:

                    st.error(
                        f"❌ Generation failed:\n\n{error}"
                    )

            else:

                code = clean_code(result)

                st.session_state.generated_code = code

                st.session_state.generated_language = language

                st.session_state.generated_filename = (
                    get_filename(language)
                )

                st.session_state.explanation = ""

                st.session_state.total_generations += 1

                history_item = {
                    "time": datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    ),
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

                st.success(
                    "✅ Code generated successfully!"
                )

    # ========================================================
    # GENERATED CODE
    # ========================================================

    if st.session_state.generated_code:

        st.markdown("---")

        st.markdown("## 💻 Generated Code")

        code = st.session_state.generated_code

        current_language = (
            st.session_state.generated_language
        )

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

                with st.spinner(
                    "🧠 Creating explanation..."
                ):

                    explanation, explanation_error = (
                        explain_code(
                            code,
                            current_language,
                            response_language
                        )
                    )

                if explanation_error:

                    st.error(
                        f"Explanation failed: {explanation_error}"
                    )

                else:

                    st.session_state.explanation = (
                        explanation
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
        "Paste your code and error message. "
        "CodeForge will analyze and repair it."
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

    debug_response_language = st.selectbox(
        "Response language",
        USER_LANGUAGES,
        key="debug_response_language"
    )

    if st.button(
        "🐛 Fix My Code",
        type="primary",
        use_container_width=True
    ):

        if not debug_code_input.strip():

            st.warning(
                "Please paste your code first."
            )

        else:

            with st.spinner(
                "🔎 Analyzing and fixing your code..."
            ):

                fixed, error = debug_code(
                    debug_code_input,
                    debug_language,
                    error_message,
                    debug_response_language
                )

            if error:

                st.error(
                    f"❌ Debugging failed:\n\n{error}"
                )

            else:

                fixed_code = clean_code(fixed)

                st.success(
                    "✅ Corrected code generated!"
                )

                st.code(
                    fixed_code,
                    language=debug_language.lower()
                )

                st.download_button(
                    "📥 Download Fixed Code",
                    fixed_code,
                    file_name=(
                        f"fixed."
                        f"{LANGUAGES[debug_language]}"
                    ),
                    mime="text/plain",
                    use_container_width=True
                )


# ============================================================
# HTML PREVIEW
# ============================================================

elif page == "👁️ Preview":

    st.markdown("## 👁️ Live HTML Preview")

    st.info(
        "This preview is intended for HTML projects. "
        "Only preview code you trust."
    )

    if st.session_state.generated_code:

        if (
            st.session_state.generated_language
            == "HTML"
        ):

            html_code = st.session_state.generated_code

        else:

            html_code = st.text_area(
                "Paste HTML",
                height=350
            )

    else:

        html_code = st.text_area(
            "Paste HTML",
            height=400,
            placeholder=(
                "<!DOCTYPE html>\n"
                "<html>\n"
                "<body>\n"
                "...\n"
                "</body>\n"
                "</html>"
            )
        )

    if html_code.strip():

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
        "Describe a complete project and CodeForge will "
        "generate the required files."
    )

    project_request = st.text_area(
        "Describe your project",
        height=180,
        placeholder=(
            "Example:\n"
            "Create a modern portfolio website with "
            "Home, About, Projects and Contact sections."
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

            st.warning(
                "Please describe your project first."
            )

        else:

            with st.spinner(
                "🏗️ Building project files..."
            ):

                files, error = generate_project(
                    project_request,
                    project_language
                )

            if error:

                st.error(
                    f"❌ Project generation failed:\n\n{error}"
                )

            else:

                st.session_state.project_files = files

                st.success(
                    f"✅ Created {len(files)} project files!"
                )

    if st.session_state.project_files:

        st.markdown("### 📦 Generated Files")

        for filename, content in (
            st.session_state.project_files.items()
        ):

            with st.expander(
                f"📄 {filename}",
                expanded=True
            ):

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
                    data=content,
                    file_name=filename,
                    mime="text/plain",
                    key=f"file_{filename}"
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

            short_request = (
                item["request"][:70]
                .replace("\n", " ")
            )

            with st.expander(
                f"{index + 1}. "
                f"{item['language']} — "
                f"{short_request}"
            ):

                st.caption(
                    item["time"]
                )

                st.write(
                    item["request"]
                )

                st.code(
                    item["code"],
                    language=item["language"].lower()
                )

                if st.button(
                    "Load Code",
                    key=f"load_history_{index}"
                ):

                    st.session_state.generated_code = (
                        item["code"]
                    )

                    st.session_state.generated_language = (
                        item["language"]
                    )

                    st.session_state.generated_filename = (
                        get_filename(item["language"])
                    )

                    st.success(
                        "✅ Code loaded into the workspace."
                    )


# ============================================================
# ABOUT
# ============================================================

elif page == "ℹ️ About":

    st.markdown("## ⚡ About CodeForge AI Studio")

    st.markdown(
        """
### 🚀 What is CodeForge?

CodeForge AI Studio is a multilingual AI programming
assistant that converts natural-language ideas into
working computer code.

### 🌍 Languages

Users can communicate with CodeForge in:

**English • Urdu • Hindi • Arabic • Spanish • French •
German • Chinese • Japanese • Korean • Turkish •
Portuguese • Bengali • Punjabi • Persian**

### 💻 Programming

CodeForge supports:

**Python • HTML • CSS • JavaScript • TypeScript • C •
C++ • C# • Java • PHP • Ruby • Go • Rust • Swift •
Kotlin • SQL • Bash • Dart**

### 🧰 Tools

- 🤖 AI Code Generator
- 🐛 AI Debugger
- 🧠 Code Explanation
- 📁 Multi-file Project Builder
- 👁️ HTML Preview
- 📥 Code Downloads
- 📚 Generation History

### 🛠️ Technology

**Python + Streamlit + Google Gemini**

### 🎯 Mission

Make programming easier by allowing people to explain
their ideas naturally instead of having to know every
programming syntax before they start.

---

## ⚡ Describe it. Generate it. Build it.
"""
    )

    st.markdown("---")

    st.success(
        "CodeForge AI Studio is ready to turn ideas into code."
    )
