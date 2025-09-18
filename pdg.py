# prd_generator.py
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

# -------------------------------
# Load Environment Variables
# -------------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not set in .env file.")
else:
    genai.configure(api_key=API_KEY)

# -------------------------------
# Streamlit App UI
# -------------------------------
st.set_page_config(page_title="PRD Forge - AI PRD Generator", layout="wide")

st.title("📄 PRD Forge - AI PRD Generator")
st.write("Generate professional Product Requirements Documents (PRDs) from simple app ideas.")

# Sidebar for Settings
st.sidebar.header("⚙️ Settings")
app_type = st.sidebar.selectbox("Select App Type", ["Web App", "Mobile App", "Hybrid", "AI Tool", "IoT App"])
language = st.sidebar.selectbox("Output Language", ["English", "Hindi", "Telugu"])
export_format = st.sidebar.radio("Export Format", ["Markdown", "Text"])

# -------------------------------
# User Input
# -------------------------------
app_name = st.text_input("App Name", placeholder="e.g., PRD Forge")
app_idea = st.text_area("Describe your app idea", placeholder="Enter a short description of your app...")

generate_button = st.button("🚀 Generate PRD")

# -------------------------------
# AI Prompt
# -------------------------------
def generate_prd(app_name, app_idea, app_type, language):
    prompt = f"""
    Generate a **Product Requirements Document (PRD)** for the following idea:

    App Name: {app_name}
    App Type: {app_type}
    Description: {app_idea}

    Format the PRD into the following sections:
    1. Overview
    2. Essential Core Features
    3. Tech Stack
    4. Design Preferences
    5. All Screens/Pages
    6. App Menu and Navigation Structure
    7. User Flow
    8. Monetization Strategy
    9. Risks & Challenges
    10. Roadmap (MVP → Future Releases)

    Language: {language}
    Make the PRD clear, structured, and professional.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text if response else "⚠️ No response from Gemini."


# -------------------------------
# Generate & Display PRD
# -------------------------------
if generate_button:
    if not app_idea or not app_name:
        st.warning("⚠️ Please enter both App Name and Description.")
    else:
        with st.spinner("Generating PRD... ⏳"):
            prd_output = generate_prd(app_name, app_idea, app_type, language)

        st.subheader("📑 Generated PRD")
        st.markdown(prd_output)

        # -------------------------------
        # Export Option
        # -------------------------------
        file_name = f"{app_name.replace(' ', '_')}_PRD_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if export_format == "Markdown":
            file_content = prd_output.encode("utf-8")
            st.download_button("⬇️ Download PRD (Markdown)", data=file_content, file_name=f"{file_name}.md", mime="text/markdown")
        else:
            file_content = prd_output.encode("utf-8")
            st.download_button("⬇️ Download PRD (Text)", data=file_content, file_name=f"{file_name}.txt", mime="text/plain")
