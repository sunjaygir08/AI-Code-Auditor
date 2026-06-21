import streamlit as st
from google.genai import client
import os

st.set_page_config(
    page_title="DevAI | Code Auditor", 
    page_icon="", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    .stButton>button {width: 100%; background-color: #2b5cff; color: white; border-radius: 8px; height: 3rem; font-weight: bold;}
    .stButton>button:hover {background-color: #1e4bd6; color: white;}
    </style>
""", unsafe_allow_html=True)

st.markdown("# DevAI: Static Code Auditor & Optimizer")
st.markdown("##### *An automated assistant to audit syntax, identify logical flaws, and optimize runtime complexity.*")
st.markdown("---")

if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.warning("⚠️ System Environment Alert: Please configure your GEMINI_API_KEY in secrets.toml.")
else:
    client = client(api_key=API_KEY)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📝 Code Input Console")
    language = st.selectbox("Select Source Language:", ["Python", "Java", "C++", "JavaScript", "Go", "Other"])
    
    code_input = st.text_area(
        "Paste your code layout block here:", 
        height=380, 
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
            with st.spinner("Analyzing code architecture via new Google GenAI SDK..."):
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
                        model="gemini-3.5-flash",
                        contents=prompt_text
                    )
                    
                    st.success("✅ Code Audit Finished Successfully.")
                    st.markdown(response.text)
                        
                except Exception as e:
                    st.error(f"Execution Error: {e}")
    else:
        st.info("💡 Ready for Input: Paste your functional logic code blocks in the left panel and hit execute.")