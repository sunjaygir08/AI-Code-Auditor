import streamlit as st
from google import genai
import os
import re

st.set_page_config(
    page_title="DevAI | Code Auditor",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- THEME-CSS ----------
st.markdown("""
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    .stButton>button {width: 100%; background-color: #2b5cff; color: white; border-radius: 8px; height: 3rem; font-weight: bold;}
    .stButton>button:hover {background-color: #1e4bd6; color: white;}

    /* Tabs styling — uses Streamlit's native theme variables, no hardcoded colors */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 18px;
        font-weight: 600;
        background-color: var(--secondary-background-color);
    }
    .stTabs [aria-selected="true"] {
        background-color: #2b5cff !important;
        color: white !important;
    }

    /* File uploader dropzone */
    [data-testid="stFileUploaderDropzone"] {
        border-radius: 10px;
        border: 1.5px dashed rgba(128, 128, 128, 0.4);
    }

    .sidebar-footer {
        font-size: 0.8rem;
        opacity: 0.6;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- MODEL OPTIONS ----------
MODEL_OPTIONS = [
    "gemini-3.5-flash",
    "gemini-3.1-pro",
    "gemini-3-flash",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
]

EXT_MAP = {
    "Python": ["py"],
    "Java": ["java"],
    "C++": ["cpp", "cc", "h", "hpp"],
    "JavaScript": ["js", "jsx"],
    "Go": ["go"],
    "Other": ["txt", "py", "java", "cpp", "js", "go", "rb", "ts", "c", "cs"],
}

# ---------- SIDEBAR: MODEL SELECTION ----------
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    model_choice = st.selectbox(
        "Select Gemini Model:",
        MODEL_OPTIONS,
        index=0,
        help="Pro models = deeper reasoning. Flash models = faster & cheaper."
    )
    st.markdown("---")
    st.markdown('<p class="sidebar-footer">DevAI Code Auditor v2.0</p>', unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("# DevAI: Static Code Auditor & Optimizer")
st.markdown("##### *An automated assistant to audit syntax, identify logical flaws, and optimize runtime complexity.*")
st.markdown("---")

# --------- API CONFIGURATION ----------
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.warning("⚠️ System Environment Alert: Please configure your GEMINI_API_KEY in secrets.toml.")
else:
    client = genai.Client(api_key=API_KEY)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📝 Code Input Console")
    language = st.selectbox("Select Source Language:", ["Python", "Java", "C++", "JavaScript", "Go", "Other"])

    uploaded_file = st.file_uploader(
        "📂 Drag & drop a code file here, or click to browse",
        type=EXT_MAP.get(language),
        help="Uploading a file auto-fills the code box below. You can still edit it manually."
    )

    if uploaded_file is not None and st.session_state.get("_last_uploaded_name") != uploaded_file.name:
        try:
            st.session_state["code_input_box"] = uploaded_file.read().decode("utf-8", errors="ignore")
            st.session_state["_last_uploaded_name"] = uploaded_file.name
        except Exception:
            st.warning("⚠️ Could not read file as text. Please paste code manually.")

    code_input = st.text_area(
        "Paste your code layout block here:",
        height=340,
        key="code_input_box",
        placeholder=f"# Write or paste your {language} implementation logic here..."
    )

    analyze_clicked = st.button("Execute Deep Code Audit")

with col2:
    st.markdown("### 📊 Audit & Analysis Report")

    if analyze_clicked:
        if code_input.strip() == "":
            st.error("❌ Execution Block Empty: Please input sample code structure first.")
        elif not API_KEY:
            st.error("❌ Connection Refused: API Authentication Token is missing.")
        else:
            with st.spinner(f"Analyzing code architecture via {model_choice}..."):
                try:
                    prompt_text = f"""
                    You are a minimalist code quality gate. Analyze this {language} snippet:

                    ```
                    {code_input}
                    ```

                    Provide the response in this exact compact format without any extra description, introduction, or code comments:

                    ### Fixed Code
                    (Provide only the completely fixed, clean code block here inside a code fence. Do not include any inline comments)

                    ### Quick Fix Notes
                    * **Main Issue:** (1 line summary of what was broken)
                    * **Fix Applied:** (1 line summary of what you changed)

                    ### Performance Metrics
                    * **Time Complexity:** (Provide metric like O(1) or O(N))
                    * **Space Complexity:** (Provide metric like O(1) or O(N))
                    * **Recommendation:** (1 short best-practice tip)
                    """

                    response = client.models.generate_content(
                        model=model_choice,
                        contents=prompt_text
                    )

                    st.session_state["last_response"] = response.text
                    st.session_state["last_model_used"] = model_choice

                except Exception as e:
                    st.error(f"Execution Error: {e}")

    if "last_response" in st.session_state:
        full_text = st.session_state["last_response"]

        if "### Quick Fix Notes" in full_text:
            fixed_part, notes_part = full_text.split("### Quick Fix Notes", 1)
            notes_part = "### Quick Fix Notes" + notes_part
        else:
            fixed_part, notes_part = full_text, ""

        st.success(f"✅ Code Audit Finished Successfully — Model: `{st.session_state.get('last_model_used', '')}`")

        tab1, tab2 = st.tabs(["Fixed Code", "Notes & Metrics"])

        with tab1:
            st.markdown(fixed_part)
            code_match = re.search(r"```(?:\w+)?\n(.*?)```", fixed_part, re.DOTALL)
            if code_match:
                ext = EXT_MAP.get(language, ["txt"])[0]
                st.download_button(
                    "⬇️ Download Fixed Code",
                    data=code_match.group(1),
                    file_name=f"fixed_code.{ext}",
                    mime="text/plain"
                )

        with tab2:
            st.markdown(notes_part)

    elif not analyze_clicked:
        st.info("Ready for Input: Paste your functional logic code blocks in the left panel and hit execute.")

st.markdown("---")