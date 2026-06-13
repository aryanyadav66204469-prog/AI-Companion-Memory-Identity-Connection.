import streamlit as st
import os
from dotenv import load_dotenv
import pyttsx3

from utils.storage import save_memory, load_memories
from utils.face_match import find_person


st.set_page_config(
    page_title="MemoryBridge",
    page_icon="🧠",
    layout="wide"
)

load_dotenv()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0F172A,#111827,#1E1B4B);
    color: white;
}
.main-title {
    text-align:center;
    font-size:60px;
    font-weight:bold;
}
.subtitle {
    text-align:center;
    color:#A78BFA;
    font-size:22px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='main-title'>🧠 MemoryBridge</div>
<div class='subtitle'>Reconnecting Memories Through AI</div>
<br>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "➕ Add Memory", "🔍 Recognize Person"]
)

if menu == "🏠 Home":
    st.write("Welcome to MemoryBridge")

elif menu == "➕ Add Memory":

    st.header("Add Memory")

    name = st.text_input("Name")
    relationship = st.text_input("Relationship")
    memory = st.text_area("Memory")

    photo = st.file_uploader("Upload Photo", type=["jpg","png","jpeg"], key="add_photo")

    if st.button("Save Memory"):

        if photo:
            image_path = f"images/{photo.name}"

            with open(image_path, "wb") as f:
                f.write(photo.getbuffer())

            save_memory({
                "name": name,
                "relationship": relationship,
                "memory": memory,
                "image": image_path
            })

            st.success("Memory Saved!")
            st.balloons()


elif menu == "🔍 Recognize Person":

    st.header("Recognize Person")

    st.subheader("Choose Input Method")
    option = st.radio("Select", ["Upload Image", "Use Camera"])

    person = None

    
    if option == "Use Camera":

        image = st.camera_input("Take a picture")

        if image:
            temp_path = "images/camera.jpg"

            with open(temp_path, "wb") as f:
                f.write(image.getbuffer())

            memories = load_memories()
            person = find_person(temp_path, memories)

    
    elif option == "Upload Image":

        uploaded = st.file_uploader(
            "Upload Face",
            type=["jpg", "png", "jpeg"],
            key="recognize_upload"
        )

        if uploaded:
            temp_path = f"images/{uploaded.name}"

            with open(temp_path, "wb") as f:
                f.write(uploaded.getbuffer())

            memories = load_memories()
            person = find_person(temp_path, memories)

    if person:

        st.success(f"Recognized: {person['name']}")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(person["image"], width=250)

        with col2:
            st.markdown(f"""
            ### 👤 {person['name']}
            ❤️ {person['relationship']}
            
            💭 {person['memory']}
            """)

        
        if st.button("🔊 Speak Memory"):

            speech = f"""
            This is {person['name']}.
            They are your {person['relationship']}.
            {person['memory']}
            """

            speak(speech)

        st.subheader("🤖 AI Assistant")

        if "chat" not in st.session_state:
            st.session_state.chat = []

        user_input = st.text_input("Ask about this person")

        if st.button("Send"):

            response = f"""
            This is {person['name']}.
            They are your {person['relationship']}.
            {person['memory']}
            """

            st.session_state.chat.append(("You", user_input))
            st.session_state.chat.append(("AI", response))

        for sender, msg in st.session_state.chat:
            if sender == "You":
                st.markdown(f"**🧑 You:** {msg}")
            else:
                st.markdown(f"**🤖 AI:** {msg}")

        
        st.info("🤖 AI Recall is under development")

    else:
        st.warning("No person detected yet")

st.markdown("<hr><center>Made with ❤️ | MemoryBridge</center>", unsafe_allow_html=True)