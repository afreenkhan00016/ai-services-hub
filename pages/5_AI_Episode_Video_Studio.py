import streamlit as st
import requests
from datetime import datetime
from pathlib import Path
import re

st.set_page_config(page_title="AI Episode Video Studio", page_icon="🎬", layout="wide")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output" / "episodes"
OUT.mkdir(parents=True, exist_ok=True)

st.title("🎬 AI Episode Video Studio")
st.write("Create cinematic drama scripts and production plans using your local Ollama model.")

MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/chat"

with st.sidebar:
    st.subheader("Studio settings")
    st.write("Model: llama3.2:3b")
    st.write("Cost: ₹0 for local script generation")
    st.caption("This tool creates text and prompts, not video footage.")

series = st.text_input("Series name", "The Hidden Truth")
genre = st.selectbox("Genre", ["Family drama", "Romance", "Mystery", "Thriller", "College drama", "Social drama"])
format_type = st.selectbox("Video type", ["Full episode (10+ minutes)", "YouTube Short", "Trailer"])
aspect = st.selectbox("Aspect ratio", ["16:9 cinematic", "9:16 vertical"])
visual_style = st.selectbox("Visual style", ["Realistic cinematic AI drama", "Moody cinematic realism", "Naturalistic television drama"])

idea = st.text_area(
    "Story idea",
    "A young woman discovers a family secret. When she confronts her mother, an unexpected visitor arrives with evidence that changes everything.",
    height=120
)
characters = st.text_area("Main characters", "Describe each character's age, appearance, personality, and relationships.")
continuity = st.text_area("Previous events (optional)", "")
requirements = st.text_area("Must-have moments or ending (optional)", "")

task = st.selectbox("What should the AI create?", [
    "Episode outline",
    "Full episode script draft",
    "Scene-by-scene production plan",
    "Cinematic visual prompts",
    "Trailer script",
    "YouTube Short script"
])
scene_count = st.slider("Scenes to plan (for scene plans/prompts)", 1, 8, 4)

guides = {
    "Episode outline": "Create a strong hook, act structure, character goals, conflict, turning points, emotional climax, and cliffhanger for a 10+ minute episode.",
    "Full episode script draft": "Write a screenplay draft intended for at least 10 minutes, with scene headings, action, natural dialogue, emotional beats, and an ending. Aim for 1300-1700 words if possible. If too long for one response, end at a complete scene and say where to continue.",
    "Scene-by-scene production plan": f"Create {scene_count} numbered scenes. For each give purpose, location, time, characters, action, shot type, camera movement, lighting, sound, transition, and continuity notes.",
    "Cinematic visual prompts": f"Create {scene_count} detailed prompts for realistic cinematic text-to-video or text-to-image generation. Include character appearance, wardrobe, setting, lighting, composition, camera movement, mood, aspect ratio, and a negative prompt. Do not claim footage has been generated.",
    "Trailer script": "Create a 30-60 second trailer with an opening hook, escalating shots, short dialogue or voice-over, music and sound cues, title-card suggestions, and a cliffhanger.",
    "YouTube Short script": "Create a 30-60 second vertical short with a hook in the first two seconds, concise shots, dialogue or voice-over, caption suggestions, sound cues, and a final hook."
}

if st.button("✨ Generate with Ollama", type="primary", use_container_width=True):
    if not idea.strip():
        st.error("Please enter a story idea.")
    else:
        prompt = f"""
You are a professional screenwriter and film production planner.
Create original fiction; do not copy an existing show or film.

Series: {series}
Genre: {genre}
Video type: {format_type}
Visual style: {visual_style}
Aspect ratio: {aspect}
Story idea: {idea}
Characters: {characters}
Previous events: {continuity}
Additional requirements: {requirements}
Task: {task}
Instructions: {guides[task]}

Be cinematic, practical, and specific. Maintain consistent character appearance.
Separate scene action, dialogue, camera, lighting, and sound where appropriate.
"""
        try:
            with st.spinner("Generating with your local model..."):
                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": MODEL,
                        "stream": False,
                        "messages": [
                            {"role": "system", "content": "You are a creative, careful cinematic writing assistant."},
                            {"role": "user", "content": prompt}
                        ],
                        "options": {"temperature": 0.8}
                    },
                    timeout=600
                )
                response.raise_for_status()
                st.session_state["draft"] = response.json()["message"]["content"]
                st.session_state["draft_title"] = series
                st.session_state["draft_task"] = task
        except requests.exceptions.ConnectionError:
            st.error("Ollama is not responding. Check that Ollama is running.")
        except requests.exceptions.Timeout:
            st.error("Generation took too long. Try an outline or fewer scenes.")
        except Exception as exc:
            st.error(f"Generation failed: {exc}")

if "draft" in st.session_state:
    st.subheader("Review your draft")
    edited = st.text_area("Edit the generated result", st.session_state["draft"], height=450)
    safe_series = re.sub(r"[^A-Za-z0-9_-]+", "_", st.session_state["draft_title"])
    safe_task = re.sub(r"[^A-Za-z0-9_-]+", "_", st.session_state["draft_task"])
    filename = f"{safe_series}_{safe_task}.txt"

    st.download_button("⬇️ Download draft", edited, file_name=filename, mime="text/plain", use_container_width=True)

    if st.button("Save draft in project folder"):
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = OUT / f"{stamp}_{filename}"
        target.write_text(edited, encoding="utf-8")
        st.success(f"Saved to {target}")

st.divider()
st.caption("To make a finished video, you still need footage, audio, and a video editor.")
