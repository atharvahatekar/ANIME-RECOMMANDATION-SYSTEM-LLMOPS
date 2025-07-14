import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv
import re

st.set_page_config(
    page_title="Anime Recommendation System",
    page_icon=":sparkles:",
    layout="wide",
    initial_sidebar_state="expanded"
    )

st.markdown("""
<style>
    /* Dark theme colors */
    :root {
        --background-color: #121212;
        --text-color: #E0E0E0;
        --accent-color: #BB86FC;
        --secondary-accent: #03DAC6;
        --highlight-color: #CF6679;
    }
    
    /* Main background */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--accent-color) !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
    }
    
    /* Input styling */
    div[data-baseweb="input"] input {
        font-size: 20px;
        background-color: #1E1E1E !important;
        border-color: var(--accent-color) !important;
        color: white !important;
        border-radius: 8px;
        text-align: center;
    }
    
    /* Center all text elements by default */
    .stTextInput, .stMarkdown {
        text-align: center;
    }
    
    /* Card styling for recommendations */
    .anime-card {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border-left: 5px solid var(--accent-color);
        text-align: center;
    }
    
    .anime-title {
        color: var(--accent-color);
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
        text-align: center;
    }
    
    .anime-summary {
        color: var(--text-color);
        font-size: 16px;
        margin-bottom: 10px;
        text-align: center;
    }
    
    .anime-reason {
        color: var(--secondary-accent);
        font-size: 16px;
        font-style: italic;
        text-align: center;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: var(--accent-color) !important;
    }
</style>
""", unsafe_allow_html=True)

load_dotenv()

@st.cache_resource
def init_pipeline():
    return AnimeRecommendationPipeline()

pipeline = init_pipeline()

st.title("✨ Anime Recommendation System ✨")

st.markdown('<h3 style="opacity: 0.8;">Discover your next favorite anime</h3>', unsafe_allow_html=True)

query = st.text_input("", placeholder="eg: action and adventure anime with strong female protagonists")

def parse_recommendations(response):
    anime_blocks = []
    if '|' in response:
        table_rows = [row.strip() for row in response.split('\n') if row.strip().startswith('|')]
        if len(table_rows) >= 3:  
            for row in table_rows[2:]:  
                cells = [cell.strip() for cell in row.split('|')[1:-1]]  
                if len(cells) >= 3:
                    anime_blocks.append({
                        'title': cells[0],
                        'summary': cells[1],
                        'reason': cells[2]
                    })
    
    if not anime_blocks:
        pattern = r"(\d+\.?\s*)(.*?)(?=\d+\.|\Z)"
        matches = re.findall(pattern, response, re.DOTALL)
        
        for match in matches:
            content = match[1].strip()
            title_match = re.search(r"([^:]+):", content)
            
            if title_match:
                title = title_match.group(1).strip()
                remaining = content[title_match.end():].strip()
                
                parts = remaining.split("Why it matches:", 1)
                if len(parts) == 2:
                    summary = parts[0].strip()
                    reason = parts[1].strip()
                    anime_blocks.append({
                        'title': title,
                        'summary': summary,
                        'reason': reason
                    })
    
    return anime_blocks

if query:
    with st.spinner("Finding the perfect anime for you..."):
        response = pipeline.run(query)

    if response:
        st.markdown("### 🌟 Recommended Anime For You:")
        
        recommendations = parse_recommendations(response)
        
        if recommendations:
            col1, col2, col3 = st.columns(3)
            cols = [col1, col2, col3]
            
            for i, anime in enumerate(recommendations):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="anime-card">
                        <div class="anime-title">{anime['title']}</div>
                        <div class="anime-summary"><b>Summary:</b> {anime['summary']}</div>
                        <div class="anime-reason"><b>Why it matches:</b> {anime['reason']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; border-left: 5px solid #BB86FC; text-align: center;">
                {}
            </div>
            """.format(response.replace('\n', '<br>')), unsafe_allow_html=True)
    else:
        st.error("No recommendations found. Please try a different query.")

st.markdown("""
<div style="text-align: center; margin-top: 30px; opacity: 0.7;">
    Made with ❤️ -By  <a href="https://www.linkedin.com/in/atharvahatekar/" target="_blank" style="color: var(--accent-color); text-decoration: none; font-weight: bold;"> Atharva Hatekar</a>
</div>
""", unsafe_allow_html=True)