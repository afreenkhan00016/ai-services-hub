import streamlit as st

st.set_page_config(
    page_title="AI Services Hub",
    page_icon="✨",
    layout="wide"
)

st.title("✨ AI Services Hub")
st.write("Your free, local AI workspace powered by Ollama.")

st.info("Choose a service from the navigation menu.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("💬 AI Chatbot")
    st.write("Draft helpful answers for customers and clients.")

    st.subheader("⚙️ Business Automation")
    st.write("Create workflows, standard operating procedures, and reply templates.")

with col2:
    st.subheader("✍️ AI Content Creator")
    st.write("Create captions, story ideas, and content plans.")

    st.subheader("📢 Marketing Materials")
    st.write("Prepare promotional copy, poster text, and campaign ideas.")

st.divider()
st.subheader("🎬 AI Episode Video Studio")
st.write(
    "Plan cinematic drama episodes, scene prompts, trailers, and Shorts. "
    "Open the AI Episode Video Studio page from the navigation menu."
)

st.caption("Local AI model: Ollama Llama 3.2 3B | Software budget: ₹0")
