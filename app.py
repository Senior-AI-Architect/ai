import streamlit as st
import os
import requests
from langchain_openai import ChatOpenAI

# --- UI SETUP ---
st.set_page_config(
    page_title="Ai Arham Intelligence - Live 2026 Verified Search",
    page_icon="🌍",
    layout="wide"
)
st.markdown("""
    <style>
    .chatgpt-box { border-radius: 15px; background-color: #f9f9f9; border: 1px solid #e5e5e5; padding: 30px; line-height: 1.8; }
    .google-card { margin-bottom: 25px; padding: 10px; border-bottom: 1px solid #eee; }
    .source-link { color: #1a0dab; text-decoration: none; font-size: 20px; }
    .featured-snippet { background-color: #f1f3f4; border-radius: 8px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #4285f4; }
    .stButton>button { width: 100%; border-color:green; border-radius: 10px; background-color: #4285f4; color: white; height: 2em; }
    .stButton>button:hover { 
    background-color: #357abd !important; 
    color: white !important; 
}
    </style>
    """, unsafe_allow_html=True)

# API Keys from Secrets
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY")
SERPER_KEY = st.secrets.get("SERPER_API_KEY")

def get_live_google_data(query):
    try:
        url = "https://google.serper.dev/search"
        payload = {"q": query, "num": 12, "gl": "us", "hl": "en"}
        headers = {'X-API-KEY': SERPER_KEY, 'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        return None

st.title("🌎 Ai Arham Intelligence")
st.caption("🚀 Double the Depth, Triple the Truth – Your Verified 2026 Search Partner.")

# --- SEARCH FRONTEND ---
col_in, col_btn = st.columns([4, 1])
with col_in:
    query = st.text_input("Sawal Likhein:", placeholder="Ask Ai Arham Intelligence", label_visibility="collapsed")
with col_btn:
    search_clicked = st.button("Search")

# Main Logic
if (search_clicked or st.session_state.get('last_query') == query) and query:
    st.session_state.last_query = query # Save state
    
    if not OPENAI_KEY or not SERPER_KEY:
        st.error("API Keys missing!")
    else:
        with st.spinner("🔄 Searching live data and thinking..."):
            try:
                llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
                col1, col2 = st.columns([1.4, 2], gap="large")

                # LEFT SIDE (ChatGPT Multi-language)
                with col1:
                    st.subheader("🤖 ChatGPT Smart Brain")
                    chat_prompt = f"Act as ChatGPT. Answer '{query}' in the same language. Detailed, 500+ words, headings, emojis, analogy."
                    chat_res = llm.invoke(chat_prompt).content
                    st.markdown(f"<div class='chatgpt-box'>{chat_res}</div>", unsafe_allow_html=True)

                # RIGHT SIDE (Google Stream English)
                with col2:
                    st.subheader("📡 Google Live Results")
                    data = get_live_google_data(query)
                    if data and 'organic' in data:
                        # Snippet
                        snips = " ".join([r.get('snippet', '') for r in data['organic'][:3]])
                        summary = llm.invoke(f"Summary for '{query}' in English: {snips}").content
                        st.markdown(f"<div class='featured-snippet'><b>Quick Answer:</b><br>{summary}</div>", unsafe_allow_html=True)
                        
                        # Links
                        for res in data['organic'][:12]:
                            st.markdown(f"""<div class='google-card'>
                                <a class='source-link' href='{res['link']}' target='_blank'>{res['title']}</a><br>
                                <small style='color:green'>{res['link']}</small>
                                <p style='color:#4d5156;font-size:14px'>{res.get('snippet','')}</p>
                            </div>""", unsafe_allow_html=True)
                    else:
                        st.error("Google data fetch failed. Check API Key/Network.")
            except Exception as e:
                st.error(f"An error occurred: {e}")











