import json
import os
import streamlit as st
from PIL import Image
import random
import base64
import io
from openai import OpenAI

def show_footer():
    st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f9f9f9;
        color: #555;
        text-align: center;
        padding: 10px 0;
        font-size: 13px;
        border-top: 1px solid #e0e0e0;
        z-index: 100;
    }
    .footer a {
        color: #0066cc;
        text-decoration: none;
        font-weight: 500;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>

    <div class="footer">
        © 2026 America Smiles. All rights reserved |
        Contact us:
        <a href="mailto:westportsmiles.org@gmail.com">
            westportsmiles.org@gmail.com
        </a>
    </div>
    """, unsafe_allow_html=True)

# ================== ENV & OPENAI ==================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# ================== PAGE STATE ==================
if "page" not in st.session_state:
    st.session_state.page = "app"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# ================== USERS ==================
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ================== AI FUNCTIONS (MERGED) ==================
def image_to_base64(image: Image.Image) -> str:
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def detect_object(image: Image.Image) -> str:
    img64 = image_to_base64(image)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "Identify the main object. Only 1-3 words."},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{img64}"}
                }
            ]
        }],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def kindness_ideas(object_name: str) -> str:
    prompt = f"""
You are helping a local community improve social interaction.
The object identified is: {object_name}

Generate 3–5 meaningful ideas for being kind when using this object.
They must be kind, nice, and easy for kids to understand.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    return response.choices[0].message.content.strip()


# ================= CHANGE PASSWORD PAGE =================


if st.session_state.page == "change_password":

    st.title("🔐 Change Password")

    current_pwd = st.text_input("Current Password", type="password")
    new_pwd = st.text_input("New Password", type="password")
    confirm_pwd = st.text_input("Confirm New Password", type="password")

    users = load_users()
    username = st.session_state.username

    if st.button("Update Password"):
        if users.get(username) != current_pwd:
            st.error("Current password is incorrect")
        elif new_pwd != confirm_pwd:
            st.error("New passwords do not match")
        elif len(new_pwd) < 4:
            st.error("Password should be at least 4 characters")
        else:
            users[username] = new_pwd
            save_users(users)
            st.success("Password updated successfully 🎉")

    if st.button("⬅ Back to App"):
        st.session_state.page = "app"
        st.rerun()
    show_footer()
    st.stop()
# ================= APP PAGE =================
if st.session_state.page == "app":

    # ---------- SESSION STATE INIT ----------
    if "image" not in st.session_state:
        st.session_state.image = None

    if "input_source" not in st.session_state:
        st.session_state.input_source = None  # "upload" or "camera"

    # ---------- SIDEBAR ----------
    st.sidebar.write("👋 Welcome!")

    # ---------- HEADER ----------
    col_logo, col_title = st.columns([1, 5])

    with col_logo:
        st.image("kindness_logo.png", width=80)

    with col_title:
        st.markdown("## America Smiles 😊")

    st.info(random.choice([
        "Say I love you to a loved one.",
        "Smile at a stranger.",
        "Give a friend a compliment.",
        "Approach things with a positive attitude."
    ]))

    st.markdown("Upload or take a photo of an object")

    # ---------- INPUT MODE ----------
    mode = st.radio("Choose image source", ["Upload", "Camera"])

    # ---------- IMAGE INPUT ----------
    if mode == "Upload":
        uploaded = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])

        if uploaded:
            st.session_state.image = Image.open(uploaded)
            st.session_state.input_source = "upload"

            # ✅ Only show image manually for upload
            st.image(st.session_state.image, caption="Your Image", use_container_width=True)

    else:
        cam = st.camera_input("Take a photo")

        if cam:
            st.session_state.image = Image.open(cam)
            st.session_state.input_source = "camera"
            # ❌ Do NOT call st.image() → camera already shows preview

    # ---------- PROCESS ----------
    if st.session_state.image is not None:
        if st.button("Kindness Starts Here"):
            with st.spinner("Thinking kindly..."):
                obj = detect_object(st.session_state.image)
                ideas = kindness_ideas(obj)

            st.subheader(f"🧠 Object: {obj}")
            st.subheader("🌟 Kindness Ideas")

            for idea in ideas.split("\n"):
                if idea.strip():
                    st.write("•", idea)

            # ✅ Reset after processing
            st.session_state.image = None
            st.session_state.input_source = None

    # ---------- CLEAR BUTTON ----------
    if st.session_state.image is not None:
        if st.button("🗑 Clear Image"):
            st.session_state.image = None
            st.session_state.input_source = None
            st.rerun()

    show_footer()
    st.stop()    

