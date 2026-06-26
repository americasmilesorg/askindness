# import json
# import os
# import streamlit as st
# from PIL import Image
# import random
# import base64
# import io
# from openai import OpenAI

# def show_footer():
#     st.markdown("""
#     <style>
#     .footer {
#         position: fixed;
#         left: 0;
#         bottom: 0;
#         width: 100%;
#         background-color: #f9f9f9;
#         color: #555;
#         text-align: center;
#         padding: 10px 0;
#         font-size: 13px;
#         border-top: 1px solid #e0e0e0;
#         z-index: 100;
#     }
#     .footer a {
#         color: #0066cc;
#         text-decoration: none;
#         font-weight: 500;
#     }
#     .footer a:hover {
#         text-decoration: underline;
#     }
#     </style>

#     <div class="footer">
#         © 2026 America Smiles. All rights reserved |
#         Contact us:
#         <a href="mailto:westportsmiles.org@gmail.com">
#             westportsmiles.org@gmail.com
#         </a>
#     </div>
#     """, unsafe_allow_html=True)

# # ================== ENV & OPENAI ==================
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# # ================== PAGE STATE ==================
# if "page" not in st.session_state:
#     st.session_state.page = "app"

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
#     st.session_state.username = ""

# # ================== USERS ==================
# USERS_FILE = "users.json"

# def load_users():
#     if os.path.exists(USERS_FILE):
#         with open(USERS_FILE, "r") as f:
#             return json.load(f)
#     return {}

# def save_users(users):
#     with open(USERS_FILE, "w") as f:
#         json.dump(users, f, indent=4)

# # ================== AI FUNCTIONS (MERGED) ==================
# def image_to_base64(image: Image.Image) -> str:
#     buf = io.BytesIO()
#     image.save(buf, format="PNG")
#     return base64.b64encode(buf.getvalue()).decode()

# def detect_object(image: Image.Image) -> str:
#     img64 = image_to_base64(image)

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": "Identify the main object. Only 1-3 words."},
#                 {
#                     "type": "image_url",
#                     "image_url": {"url": f"data:image/png;base64,{img64}"}
#                 }
#             ]
#         }],
#         temperature=0.2
#     )
#     return response.choices[0].message.content.strip()

# def kindness_ideas(object_name: str) -> str:
#     prompt = f"""
# You are helping a local community improve social interaction.
# The object identified is: {object_name}

# Generate 3–5 meaningful ideas for being kind when using this object.
# They must be kind, nice, and easy for kids to understand.
# """

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.8
#     )

#     return response.choices[0].message.content.strip()


# # ================= CHANGE PASSWORD PAGE =================


# if st.session_state.page == "change_password":

#     st.title("🔐 Change Password")

#     current_pwd = st.text_input("Current Password", type="password")
#     new_pwd = st.text_input("New Password", type="password")
#     confirm_pwd = st.text_input("Confirm New Password", type="password")

#     users = load_users()
#     username = st.session_state.username

#     if st.button("Update Password"):
#         if users.get(username) != current_pwd:
#             st.error("Current password is incorrect")
#         elif new_pwd != confirm_pwd:
#             st.error("New passwords do not match")
#         elif len(new_pwd) < 4:
#             st.error("Password should be at least 4 characters")
#         else:
#             users[username] = new_pwd
#             save_users(users)
#             st.success("Password updated successfully 🎉")

#     if st.button("⬅ Back to App"):
#         st.session_state.page = "app"
#         st.rerun()
#     show_footer()
#     st.stop()
# # ================= APP PAGE =================
# if st.session_state.page == "app":

#     # ---------- SESSION STATE INIT ----------
#     if "image" not in st.session_state:
#         st.session_state.image = None

#     if "input_source" not in st.session_state:
#         st.session_state.input_source = None  # "upload" or "camera"

#     # ---------- SIDEBAR ----------
#     st.sidebar.write("👋 Welcome!")

#     # ---------- HEADER ----------
#     col_logo, col_title = st.columns([1, 5])

#     with col_logo:
#         st.image("kindness_logo.png", width=80)

#     with col_title:
#         st.markdown("## America Smiles 😊")

#     st.info(random.choice([
#         "Say I love you to a loved one.",
#         "Smile at a stranger.",
#         "Give a friend a compliment.",
#         "Approach things with a positive attitude."
#     ]))

#     st.markdown("Upload or take a photo of an object")

#     # ---------- INPUT MODE ----------
#     mode = st.radio("Choose image source", ["Upload", "Camera"])

#     # ---------- IMAGE INPUT ----------
#     if mode == "Upload":
#         uploaded = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])

#         if uploaded:
#             st.session_state.image = Image.open(uploaded)
#             st.session_state.input_source = "upload"

#             # ✅ Only show image manually for upload
#             st.image(st.session_state.image, caption="Your Image", use_container_width=True)

#     else:
#         cam = st.camera_input("Take a photo")

#         if cam:
#             st.session_state.image = Image.open(cam)
#             st.session_state.input_source = "camera"
#             # ❌ Do NOT call st.image() → camera already shows preview

#     # ---------- PROCESS ----------
#     if st.session_state.image is not None:
#         if st.button("Kindness Starts Here"):
#             with st.spinner("Thinking kindly..."):
#                 obj = detect_object(st.session_state.image)
#                 ideas = kindness_ideas(obj)

#             st.subheader(f"🧠 Object: {obj}")
#             st.subheader("🌟 Kindness Ideas")

#             for idea in ideas.split("\n"):
#                 if idea.strip():
#                     st.write("•", idea)

#             # ✅ Reset after processing
#             st.session_state.image = None
#             st.session_state.input_source = None

#     # ---------- CLEAR BUTTON ----------
#     if st.session_state.image is not None:
#         if st.button("🗑 Clear Image"):
#             st.session_state.image = None
#             st.session_state.input_source = None
#             st.rerun()

#     show_footer()
#     st.stop()    

import json
import os
import streamlit as st
from PIL import Image
import base64
import io
from openai import OpenAI
import urllib.parse
import requests
import streamlit.components.v1 as components


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
        margin: 0 6px;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>

    <div class="footer">
        © 2026 America Smiles. All rights reserved |
        <a href="?page=legal">Legal Disclaimer</a> |
        Contact us:
        <a href="mailto:info@americasmiles.org">
            info@americasmiles.org
        </a>
    </div>
    """, unsafe_allow_html=True)

# ================== ENV & OPENAI ==================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# ================== PAGE STATE ==================
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
# ================== URL QUERY PARAMETER SYNC ==================
if "page" in st.query_params:
    st.session_state.page = st.query_params["page"]
# ================== ICON HELPER ==================
# All brand icons embedded as inline SVG data URIs — no external requests needed

ICONS = {
    "amazon":      "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiByeD0iMTIiIGZpbGw9IiNGRjk5MDAiLz48dGV4dCB4PSIzMiIgeT0iMzYiIGZvbnQtZmFtaWx5PSJBcmlhbCBCbGFjayxzYW5zLXNlcmlmIiBmb250LXNpemU9IjEzIiBmb250LXdlaWdodD0iOTAwIiBmaWxsPSIjMTExIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5hbWF6b248L3RleHQ+PHBhdGggZD0iTTE2IDQyIFEzMiA1MCA0OCA0MiIgc3Ryb2tlPSIjMTExIiBzdHJva2Utd2lkdGg9IjIuNSIgZmlsbD0ibm9uZSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+PHBvbHlnb24gcG9pbnRzPSI0NiwzOSA1MCw0MiA0Nyw0NSIgZmlsbD0iIzExMSIvPjwvc3ZnPg==",
    "etsy":        "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiByeD0iMTIiIGZpbGw9IiNGNDU4MDAiLz48dGV4dCB4PSIzMiIgeT0iNDQiIGZvbnQtZmFtaWx5PSJHZW9yZ2lhLHNlcmlmIiBmb250LXNpemU9IjM0IiBmb250LXdlaWdodD0iNzAwIiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+ZXRzeTwvdGV4dD48L3N2Zz4=",
    "walmart":     "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiByeD0iMTIiIGZpbGw9IiMwMDcxQ0UiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgzMiwyOCkiPjxjaXJjbGUgcj0iNCIgZmlsbD0iI0ZGQzIyMCIvPjxsaW5lIHgxPSIwIiB5MT0iLTEwIiB4Mj0iMCIgeTI9Ii02IiBzdHJva2U9IiNGRkMyMjAiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+PGxpbmUgeDE9IjAiIHkxPSI2IiB4Mj0iMCIgeTI9IjEwIiBzdHJva2U9IiNGRkMyMjAiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+PGxpbmUgeDE9Ii0xMCIgeTE9IjAiIHgyPSItNiIgeTI9IjAiIHN0cm9rZT0iI0ZGQzIyMCIgc3Ryb2tlLXdpZHRoPSIzIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz48bGluZSB4MT0iNiIgeTE9IjAiIHgyPSIxMCIgeTI9IjAiIHN0cm9rZT0iI0ZGQzIyMCIgc3Ryb2tlLXdpZHRoPSIzIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz48bGluZSB4MT0iLTciIHkxPSItNyIgeDI9Ii00LjUiIHkyPSItNC41IiBzdHJva2U9IiNGRkMyMjAiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+PGxpbmUgeDE9IjQuNSIgeTE9IjQuNSIgeDI9IjciIHkyPSI3IiBzdHJva2U9IiNGRkMyMjAiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+PGxpbmUgeDE9IjciIHkxPSItNyIgeDI9IjQuNSIgeTI9Ii00LjUiIHN0cm9rZT0iI0ZGQzIyMCIgc3Ryb2tlLXdpZHRoPSIzIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz48bGluZSB4MT0iLTQuNSIgeTE9IjQuNSIgeDI9Ii03IiB5Mj0iNyIgc3Ryb2tlPSIjRkZDMjIwIiBzdHJva2Utd2lkdGg9IjMiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPjwvZz48dGV4dCB4PSIzMiIgeT0iNTAiIGZvbnQtZmFtaWx5PSJBcmlhbCxzYW5zLXNlcmlmIiBmb250LXNpemU9IjkiIGZvbnQtd2VpZ2h0PSI3MDAiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj53YWxtYXJ0PC90ZXh0Pjwvc3ZnPg==",
    "whatsapp":    "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiByeD0iMzIiIGZpbGw9IiMyNUQzNjYiLz48cGF0aCBkPSJNMzIgMTFDMjAuNCAxMSAxMSAyMC40IDExIDMyYzAgMy44IDEgNy40IDIuOCAxMC41TDExIDUzbDEwLjgtMi44QTIxIDIxIDAgMCAwIDMyIDUzYzExLjYgMCAyMS05LjQgMjEtMjFTNDMuNiAxMSAzMiAxMXptMTAuNyAyOC44Yy0uNCAxLjItMi42IDIuMy0zLjYgMi41LS45LjEtMiAuMS0zLjMtLjMtLjktLjMtMi4xLS43LTMuNi0xLjQtNi4zLTIuNy0xMC40LTkuMS0xMC43LTkuNS0uMy0uNC0yLjYtMy41LTIuNi02LjYgMC0zLjIgMS42LTQuNyAyLjItNS4zLjYtLjYgMS4zLS44IDEuNy0uOC40IDAgLjkgMCAxLjIuMDEuNC4wMS45IDAgMS40IDEuMS41IDEuMSAxLjggNC4zIDIgNC42LjIuMy4zLjcuMDYgMS4xLS4yLjQtLjMuNy0uNjUgMS4wNi0uMzQuMzctLjY3Ljg0LS45IDEuMDYtLjMuMy0uNjQuNjUtLjI3IDEuMy4zNy42NCAxLjY1IDIuNzMgMy41NSA0LjQzIDIuNDQgMi4xNyA0LjUgMi44NSA1LjE1IDMuMTYuNjUuMyAxLjAyLjI3IDEuNC0uMTcuMzctLjQ0IDEuNi0xLjg2IDIuMDItMi41LjQzLS42NS44Ni0uNTQgMS40My0uMzIuNTguMjMgMy42OCAxLjc0IDQuMzIgMi4wNS42My4zIDEuMDYuNDcgMS4yLjc0LjE3LjI3LjE3IDEuNDktLjI3IDIuN3oiIGZpbGw9IndoaXRlIi8+PC9zdmc+",
    "facebook":    "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiByeD0iMTIiIGZpbGw9IiMxODc3RjIiLz48cGF0aCBkPSJNNDIgMzJoLTd2LTRjMC0xLjcgMS4xLTIuMSAyLTIuMWg1VjE5aC03Yy02IDAtOSA0LTkgOXY0aC01djhoNXYxOGg5VjM5aDZsMS03eiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=",
    "telegram":    "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiByeD0iMzIiIGZpbGw9IiMyMjlFRDkiLz48cGF0aCBkPSJNNDcgMTdMMTAgMzEuNWMtMi41IDEtMi41IDIuNC0uNCAzbDkuMyAyLjkgMjEuNS0xMy42YzEtLjYgMS45LS4zIDEuMi40TDI1IDM3LjVsLS43IDkuNWMxIDAgMS40LS40IDEuOS0xbDQuOC00LjYgOS42IDdjMS43IDEgMyAuNSAzLjQtMS42bDYuMS0yOC43Yy43LTIuNi0uOS0zLjgtNS4xLTMuMXoiIGZpbGw9IndoaXRlIi8+PC9zdmc+",
    "twitter_x":   "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiByeD0iMTIiIGZpbGw9IiMwMDAiLz48cGF0aCBkPSJNMzYgMjkuM0w0OS41IDEzaC0zTDM0LjYgMjcuMyAyNS41IDEzSDE0bDE0IDIwTDE0IDUxaDNsMTIuMi0xNC4yTDM5LjUgNTFINTFMMzYgMjkuM3ptLTQuMyA1bC0xLjQtMi0xMS4yLTE2SDI0bDkgMTIuOCAxLjQgMkw0NiA0N2gtNC44TDMxLjcgMzQuM3oiIGZpbGw9IndoaXRlIi8+PC9zdmc+",
    "googlemeet":  "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiByeD0iMTIiIGZpbGw9IndoaXRlIiBzdHJva2U9IiNlMGUwZTAiIHN0cm9rZS13aWR0aD0iMiIvPjxyZWN0IHg9IjgiIHk9IjE4IiB3aWR0aD0iMzIiIGhlaWdodD0iMjgiIHJ4PSI1IiBmaWxsPSIjMDA4MzJEIi8+PHBhdGggZD0iTTQwIDI2bDE2LTEwdjMyTDQwIDM4VjI2eiIgZmlsbD0iIzAwQUM0NyIvPjxjaXJjbGUgY3g9IjI0IiBjeT0iMzIiIHI9IjciIGZpbGw9IndoaXRlIi8+PGNpcmNsZSBjeD0iMjQiIGN5PSIzMiIgcj0iNCIgZmlsbD0iIzAwODMyRCIvPjwvc3ZnPg==",
    "zoom":        "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiByeD0iMTIiIGZpbGw9IiMyRDhDRkYiLz48cGF0aCBkPSJNOCAyMmE0IDQgMCAwIDEgNC00aDI2YTQgNCAwIDAgMSA0IDR2MjBhNCA0IDAgMCAxLTQgNEgxMmE0IDQgMCAwIDEtNC00VjIyeiIgZmlsbD0id2hpdGUiLz48cGF0aCBkPSJNNDIgMjdsMTQtOXYyOEw0MiAzN1YyN3oiIGZpbGw9IndoaXRlIi8+PC9zdmc+",
    "teams":       "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiByeD0iMTIiIGZpbGw9IiM2MjY0QTciLz48Y2lyY2xlIGN4PSI0MCIgY3k9IjE5IiByPSI3IiBmaWxsPSJ3aGl0ZSIgb3BhY2l0eT0iLjkiLz48cmVjdCB4PSIzMyIgeT0iMjgiIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNCIgcng9IjQiIGZpbGw9IndoaXRlIiBvcGFjaXR5PSIuOSIvPjxjaXJjbGUgY3g9IjIyIiBjeT0iMjIiIHI9IjkiIGZpbGw9IndoaXRlIi8+PHJlY3QgeD0iMTEiIHk9IjMzIiB3aWR0aD0iMjIiIGhlaWdodD0iMTYiIHJ4PSI1IiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==",
    "facetime":    "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiByeD0iMTQiIGZpbGw9IiMzNEM3NTkiLz48cmVjdCB4PSI3IiB5PSIxOCIgd2lkdGg9IjMyIiBoZWlnaHQ9IjI4IiByeD0iNiIgZmlsbD0id2hpdGUiLz48cG9seWdvbiBwb2ludHM9IjM5LDI2IDU3LDE4IDU3LDQ2IDM5LDM4IiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==",
    "google":      "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiByeD0iMTIiIGZpbGw9IndoaXRlIiBzdHJva2U9IiNkZGQiIHN0cm9rZS13aWR0aD0iMiIvPjxwYXRoIGQ9Ik0zMiAxNmMtOC44IDAtMTYgNy4yLTE2IDE2czcuMiAxNiAxNiAxNmM4IDAgMTQuNy01LjYgMTUuNy0xM0gzMnYtNWgxOS44Yy4xLjkuMiAxLjcuMiAyLjUgMCAxMC41LTcuMiAxOS41LTIwIDIxLTEwLjMgMS4yLTIwLTUuMy0yMi41LTE1LjQtMi42LTEwLjMgMy40LTIwLjggMTMuMy0yNC41IDYuOC0yLjUgMTQuMy0xLjMgMjAgM2wtNCA0Yy0zLjgtMi43LTguNS0zLjUtMTMtMi4zLTcgMi0xMS41IDktMTAgMTYuNSAxLjMgNi41IDcgMTEuMiAxMy41IDExLjIgNS44IDAgMTAuOC0zIDEzLjItNy41SDMydi01eiIgZmlsbD0iIzQyODVGNCIvPjxwYXRoIGQ9Ik0xNiAzMmMwLTMuMyAxLTYuMyAyLjYtOC45bC00LjEtNEExNS45IDE1LjkgMCAwIDAgMTYgMzJ6IiBmaWxsPSIjMzRBODUzIi8+PHBhdGggZD0iTTMyIDE2Yy0yLjcgMC01LjIuNy03LjQgMS45bDQuMiA0LjFBMTAuNSAxMC41IDAgMCAxIDMyIDIxLjV6IiBmaWxsPSIjRkJCQzA0Ii8+PHBhdGggZD0iTTE4LjYgMjMuMWwtNC4xLTRBMTYgMTYgMCAwIDAgMTYgMzJsMC4xLTFjMC0yLjkuOC01LjYgMi41LTcuOXoiIGZpbGw9IiNFQTQzMzUiLz48L3N2Zz4=",
    "gmail":       "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiByeD0iMTIiIGZpbGw9IndoaXRlIiBzdHJva2U9IiNkZGQiIHN0cm9rZS13aWR0aD0iMiIvPjxwYXRoIGQ9Ik04IDE4aDQ4djI4SDhWMTh6IiBmaWxsPSIjZjJmMmYyIi8+PHBhdGggZD0iTTggMThsMjQgMTggMjQtMThIMnoiIGZpbGw9IiNFQTQzMzUiLz48cGF0aCBkPSJNOCAxOHYyOGg0OFYxOEwzMiAzNiA4IDE4eiIgZmlsbD0ibm9uZSIvPjxwb2x5bGluZSBwb2ludHM9IjgsMTggMzIsMzYgNTYsMTgiIGZpbGw9Im5vbmUiIHN0cm9rZT0iI0VBNDMzNSIgc3Ryb2tlLXdpZHRoPSIzIi8+PC9zdmc+",
}

def icon_btn(url, bg, icon_key, label, text_color="white", small=False):
    """Renders a branded icon+label button as an HTML link."""
    pad  = "7px 8px" if small else "10px 8px"
    fsize = "11px"   if small else "13px"
    logo_url = ICONS.get(icon_key, "")
    return (
        f'<a href="{url}" target="_blank" style="text-decoration:none;display:block">'
        f'<div style="display:flex;align-items:center;justify-content:center;gap:6px;'
        f'background:{bg};border-radius:10px;padding:{pad};cursor:pointer;'
        f'box-shadow:0 2px 5px rgba(0,0,0,0.15);">'
        f'<img src="{logo_url}" style="height:20px;width:20px;object-fit:contain;flex-shrink:0"/>'
        f'<span style="color:{text_color};font-weight:700;font-size:{fsize};white-space:nowrap">{label}</span>'
        f'</div></a>'
    )

# ================== AI FUNCTIONS ==================
def image_to_base64(image: Image.Image) -> str:
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def is_inappropriate_image(image: Image.Image) -> bool:
    img64 = image_to_base64(image)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analyze this image carefully. Does this image contain any of the following restricted categories:\n"
                            "1. Nudity, private body parts, or explicit sexual content.\n"
                            "2. Illegal drugs, illicit substances, or drug consumption tools (paraphernalia).\n"
                            "3. Alcohol, whiskey bottles, beer glasses, or bar/nightclub settings.\n"
                            "4. Weapons (guns, knives), active violence, blood, or gore.\n"
                            "5. Hate symbols, extremist imagery, or highly offensive gestures.\n"
                            "6. Written text containing profanity, swear words, insults, bullying, or mean/unfriendly messages.\n\n"
                            "Reply with exactly 'YES' if it contains ANY of these 6 categories, "
                            "or exactly 'NO' if it is completely safe, friendly, and clean for children."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{img64}"}
                    }
                ]
            }],
            temperature=0.0
        )
        verdict = response.choices[0].message.content.strip().upper()
        return "YES" in verdict
    except Exception:
        return True

def detect_object(image: Image.Image) -> str:
    img64 = image_to_base64(image)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "Identify the main object. Only 1-3 words."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img64}"}}
            ]
        }],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def kindness_ideas(object_name: str) -> str:
    prompt = f"""
You are helping a local community improve social interaction.
The object identified is: {object_name}

Generate 3-5 meaningful ideas for being kind when using this object. No number less points.
They must be kind, nice, and easy to understand.
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

def expand_kindness_idea(idea: str) -> str:
    prompt = f"""
Explain this kindness idea in a simple and fun way:
"{idea}"

Give a short explanation in 4 points.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def get_kindness_action_options(idea: str, zipcode: str) -> dict:
    prompt = f"""
You are a helpful kindness assistant for the Westport Smiles community project.

Kindness idea: "{idea}"
User ZIP code: {zipcode}

Return a JSON object with exactly these keys:
{{
  "online_option": "A specific product or website where someone can purchase or find this online (e.g. Amazon, Etsy, etc.) with a brief description"
}}

Return ONLY valid JSON. No extra text, no markdown fences.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    raw = response.choices[0].message.content.strip()
    try:
        return json.loads(raw)
    except Exception:
        return {"online_option": "Search for this item on Amazon or Etsy."}

def build_share_message(idea: str, more_info: str) -> str:
    """Build a warm share message: friendly greeting paragraph + the 4 points listed below."""
    prompt = f"""
You are helping someone share a kindness idea with a close friend in a warm, cheerful, and friendly way.

Kindness idea: "{idea}"

The 4 explanation points from More Info:
{more_info}

Write the message in TWO clearly separated parts:

PART 1 — A warm, friendly greeting paragraph (2-3 sentences, NO numbered lists or bullet points):
- Start EXACTLY with:
  "Hi! I want to share a kindness idea with you 💖"

- Write 2-4 short conversational sentences.
- Make it feel warm, personal, encouraging, and emotionally uplifting.
- Sound like a caring friend texting another friend.
- Briefly explain why this kindness idea feels meaningful, fun, helpful, or heartwarming.
- Use natural language and a positive tone.
- You may include emojis naturally.
- DO NOT use bullet points or numbered lists in this section.
- DO NOT sound formal, robotic, motivational-speaker-like, or AI-generated.

PART 2 — The 4 points, each on its own line, keeping the original wording from the explanation above but without bold markdown (**):
1. point 1
2. point 2
3. point 3
4. point 4

End with a new line: "Would love to try this with you! 💖"

Return ONLY the message, no extra labels or formatting.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def build_meetup_invite(idea: str) -> str:
    """Generate a short, friendly meetup invite message based on the idea."""
    prompt = f"""
Write a short, warm meetup invitation message (2-3 sentences) for this kindness idea:
"{idea}"

The message should:
- Suggest a specific casual meetup (walk, video call, etc.) without specifying a time or place. 
- Mention the kindness idea naturally
- Be friendly and easy to copy-paste to a friend

Return ONLY the message, no extra text.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
# ================= LEGAL PAGE =================
if st.session_state.page == "legal":
    st.title("Legal Disclaimer & Technology Disclosure")
    st.markdown("""
### 🔬 Beta Platform & AI Usage
This website is currently in **Beta** and serves as an experimental platform for our mission.  
To help us build bridges and generate smiles more efficiently, we utilize various third-party artificial intelligence and web technologies, including tools provided by **OpenAI, Google, and Streamlit**.

---

### 🔍 Transparency & Independent Policy

#### 🧭 Independent Policies
We are an independent entity. Our organizational policies, mission, and content standards are **distinct** from those of our technology providers (including OpenAI, Google, and Streamlit).  
Your interaction with our site is governed by **our own terms**, not the terms of our software vendors.

#### ⚠️ Accuracy & Human Oversight
Although we use AI to assist in our work, our team strives to oversee and curate the content provided.  
AI-generated content can occasionally be **incorrect or incomplete**. Please verify any critical information independently before relying upon it.

#### 📘 Nature of Information
Content on this site is provided for **general informational purposes only** and does **not** constitute professional, legal, medical, or financial advice.

#### ⚖️ Limitation of Liability
By using this site, you acknowledge that you are using these tools at your own discretion and risk.  
**Westport Smiles and its affiliates are not liable** for any damages or losses resulting from your reliance on the information or services provided here.

---

### 💙 Our Commitment
We are using code to build bridges and spread positivity.  
We appreciate your patience and feedback as we continue to test and refine this technology to better serve our community.

---

### 🔗 Learn More
- OpenAI Usage Policies  
- Google AI Principles  
- Streamlit Terms of Service  
""")
    if st.button("⬅ Back to Home"):
        st.query_params.clear()
        st.session_state.page = "landing"
        st.rerun()
    show_footer()
    st.stop()
# ================= APP PAGE (only page) =================

# ---------- SESSION STATE INIT ----------
for key, default in [
    ("image", None), ("input_source", None), ("is_blurred", False),
    ("expanded_ideas", {}), ("action_data", {}), ("action_view", {}),
    ("zipcode_input", {}), ("last_sub_action", {}),
    ("share_messages", {}), ("meetup_invites", {}),
    ("camera_active", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ---------- BACKGROUND COLORS ----------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #E8F4FD !important;
}
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stMainBlockContainer"],
[data-testid="stMain"],
.main,
section.main,
[data-testid="stToolbar"],
header[data-testid="stHeader"] {
    background-color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.write("👋 Welcome!")

st.sidebar.markdown("""
<style>
.step-card {
    background: #ffffff;
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 10px;
    border: 1px solid #e8e8e8;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    text-align: center;
}
.step-number {
    display: inline-block;
    width: 26px;
    height: 26px;
    border-radius: 50%;
    color: white;
    font-weight: 700;
    font-size: 13px;
    text-align: center;
    line-height: 26px;
    margin-bottom: 6px;
}
.step-title {
    font-size: 14px;
    font-weight: 700;
    color: #1a1a1a;
    margin: 4px 0 5px 0;
}
.step-desc {
    font-size: 12px;
    color: #555;
    line-height: 1.55;
    margin: 0;
}
</style>

<div class="step-card">
    <div class="step-number" style="background:#E8490F;">1</div>
    <div class="step-title">📷 Photo (Upload)</div>
    <p class="step-desc">Point your camera and take a photo of an everyday object — like a coffee mug, a stack of books, or even a random sandal! (or Upload a Photo)</p>
</div>

<div class="step-card">
    <div class="step-number" style="background:#7B2FBE;">2</div>
    <div class="step-title">✨ Discover</div>
    <p class="step-desc">The app will say "Kindness Starts Here," and our digital guide, <strong>Professor Juju</strong>, will give you fun, totally unique kindness ideas based on your photo.</p>
</div>

<div class="step-card">
    <div class="step-number" style="background:#0A8A5F;">3</div>
    <div class="step-title">🤝 Connect</div>
    <p class="step-desc">Pick your favorite idea, put your phone away, and bring that small act of kindness to life in your community.</p>
</div>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("kindness_logo.png", width=80)
with col_title:
    st.markdown("## America Smiles 😊")

daily_quotes = [
    "Smile at a stranger.",
    "Say I love you to a loved one.",
    "Give a friend a compliment.",
    "Approach things with a positive attitude.",
    "Hold the door open for someone.",
    "Send a thank you message today.",
    "Share your lunch with a coworker.",
    "Check in on a friend you haven't spoken to in a while.",
    "Tell someone what you appreciate about them.",
    "Speak kindly—to others and to yourself.",
    "Offer a genuine smile to brighten someone’s day.",
    "Believe in something good happening today.",
    "Show appreciation for the little things.",
    "Lift someone up with your word."
]

_quotes_js = json.dumps(daily_quotes)
components.html(f"""
<div id="insp" style="background:#e8f4fd;border-radius:10px;padding:12px 18px 10px 18px;
     border-left:4px solid #4a90d9;font-family:sans-serif;text-align:center;">
  <div style="font-size:11px;font-weight:700;color:#4a90d9;text-transform:uppercase;
              letter-spacing:1px;margin-bottom:6px;">🌟 Daily Inspiration</div>
  <div id="qt" style="font-size:15px;color:#222;font-style:italic;line-height:1.6;
       min-height:24px;"></div>
</div>
<script>
  var quotes = {_quotes_js};
  var idx = 0;
  function show() {{
    document.getElementById("qt").textContent = "“" + quotes[idx] + "”";
    idx = (idx + 1) % quotes.length;
  }}
  show();
  setInterval(show, 6000);
</script>
""", height=80)

st.markdown("### A Kindness Project : See an Object, Spark a Connection!")
st.write(
    "Join us—Lisette, Leonie, and Professor Juju—as we use AI to fight the loneliness epidemic "
    "by turning everyday objects into sparks for human connection. Our mission is to help everyone, "
    "from kids to seniors, break down barriers and \"Be Best\" through small acts of kindness that "
    "foster a healthier community. We invite you to explore our project, where we merge technology "
    "with real-world interaction to ensure no one has to feel like they are on a \"lonely island\" anymore."
)
st.write("Upload or take a photo of an object")
st.markdown("""
<style>
[data-testid="stFileUploaderDropzone"] {
    border: none !important;
    background: transparent !important;
    padding: 0 !important;
    min-height: unset !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] {
    display: none !important;
}
[data-testid="stFileUploader"] > label {
    display: none !important;
}
</style>
<p style='margin:0 0 4px 0;font-size:16px;font-weight:400;color:#222;'>Choose image source</p>
""", unsafe_allow_html=True)

# ---------- INPUT MODE ----------
cam_label = "📷 Close Camera" if st.session_state.camera_active else "📷 Camera"
if st.button(cam_label, use_container_width=False):
    st.session_state.camera_active = not st.session_state.camera_active
    st.rerun()

uploaded = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
if uploaded:
    if st.session_state.input_source != "upload":
        st.session_state.is_blurred = False
    st.session_state.image = Image.open(uploaded)
    st.session_state.input_source = "upload"
    st.session_state.camera_active = False

if st.session_state.image is not None and st.session_state.input_source == "upload":
    if st.session_state.is_blurred:
        st.markdown("<style>div[data-testid='stImage'] img { filter: blur(30px); }</style>", unsafe_allow_html=True)
        st.image(st.session_state.image, caption="⚠️ Content Hidden (Flagged)", use_container_width=True)
    else:
        st.image(st.session_state.image, caption="Your Image", use_container_width=True)

if st.session_state.camera_active:
    cam = st.camera_input("Take a photo", label_visibility="collapsed")
    if cam:
        if st.session_state.input_source != "camera":
            st.session_state.is_blurred = False
        st.session_state.image = Image.open(cam)
        st.session_state.input_source = "camera"
        if st.session_state.is_blurred:
            st.markdown("<style>div[data-testid='stCameraInput'] video { filter: blur(30px); }</style>", unsafe_allow_html=True)

# ---------- PROCESS ----------
if st.session_state.image is not None:
    if st.session_state.is_blurred:
        st.error("🚨 Processing halted: This image contains private or explicit content.")
    if not st.session_state.is_blurred:
        if st.button("Kindness Starts Here"):
            with st.spinner("Checking image safety..."):
                is_flagged = is_inappropriate_image(st.session_state.image)
            if is_flagged:
                st.session_state.is_blurred = True
                st.rerun()
            else:
                with st.spinner("Thinking kindly..."):
                    obj   = detect_object(st.session_state.image)
                    ideas = kindness_ideas(obj)
                st.session_state.object_name    = obj
                st.session_state.ideas_list     = [idea.strip() for idea in ideas.split("\n") if idea.strip()]
                st.session_state.expanded_ideas = {}
                st.session_state.action_data    = {}
                st.session_state.action_view    = {}
                st.session_state.zipcode_input  = {}
                st.session_state.last_sub_action= {}
                st.session_state.share_messages = {}
                st.session_state.meetup_invites = {}
                st.session_state.image          = None
                st.session_state.input_source   = None

# ---------- RESULTS ----------
if "ideas_list" in st.session_state and "object_name" in st.session_state:
    st.subheader(f" Object: {st.session_state.object_name}")
    st.subheader("🐾Kindness Ideas")

    for i, idea in enumerate(st.session_state.ideas_list):
        st.write(f"• {idea}")

        more_key   = f"more_{i}"
        action_key = f"action_{i}"

        # ---- MORE INFO + KINDNESS ACTION side by side (small buttons) ----
        col_more, col_action, col_empty = st.columns([1, 1, 2])
        with col_more:
            if st.button("🔍 More Info", key=f"btn_more_{i}", use_container_width=True):
                with st.spinner("Thinking more kindly..."):
                    extra = expand_kindness_idea(idea)
                    st.session_state.expanded_ideas[more_key] = extra
                with st.spinner("Preparing share message..."):
                    msg = build_share_message(idea, extra)
                    st.session_state.share_messages[action_key] = msg

        with col_action:
            if st.button("🤗 Kindness Action", key=f"btn_action_{i}", use_container_width=True):
                st.session_state.action_view[action_key] = (
                    None if st.session_state.action_view.get(action_key) == "menu" else "menu"
                )
                st.rerun()

        if more_key in st.session_state.expanded_ideas:
            st.info(st.session_state.expanded_ideas[more_key])

        # ---- ACTION PANEL ----
        if st.session_state.action_view.get(action_key):
            with st.container():
                st.markdown(
                    "<div style='background:#f0f8ff;border-radius:12px;padding:14px 16px 6px 16px;"
                    "border-left:4px solid #4a90d9;margin:8px 0 4px 0;'>"
                    "<strong>🤞 Choose your Kindness Action</strong></div>",
                    unsafe_allow_html=True
                )

                zipcode = st.text_input(
                    "📍 Enter your ZIP code to find local options",
                    key=f"zip_{i}", max_chars=10, placeholder="e.g. 06880"
                )
                st.session_state.zipcode_input[action_key] = zipcode
                st.markdown("""
                <style>
                div[data-testid="stHorizontalBlock"] button {
                    font-size: 11px !important;
                    padding: 4px 2px !important;
                    line-height: 1.2 !important;
                    white-space: nowrap !important;
                }
                </style>
                """, unsafe_allow_html=True)
                # Four action buttons side by side
                col_a, col_b, col_c, col_d = st.columns(4)
                with col_a:
                    buy_online  = st.button("🛒 purchase Online",   key=f"buy_online_{i}",  use_container_width=True)
                with col_b:
                    buy_offline = st.button("🏪 purchase Offline",  key=f"buy_offline_{i}", use_container_width=True)
                with col_c:
                    share_msg   = st.button("📤 Share kindness",     key=f"share_{i}",       use_container_width=True)
                with col_d:
                    meetup_btn  = st.button("📅 Schedule kindness",   key=f"meetup_{i}",      use_container_width=True)

                sub_action = None
                if buy_online:  sub_action = "online"
                elif buy_offline: sub_action = "offline"
                elif share_msg:   sub_action = "message"
                elif meetup_btn:  sub_action = "meetup"

                # Handle fetches
                if sub_action == "online":
                    entered_zip = st.session_state.zipcode_input.get(action_key, "").strip()
                    with st.spinner("Finding online options..."):
                        result = get_kindness_action_options(idea, entered_zip or "06880")
                        st.session_state.action_data[action_key] = result
                    st.session_state.last_sub_action[action_key] = sub_action

                elif sub_action == "offline":
                    entered_zip = st.session_state.zipcode_input.get(action_key, "").strip()
                    if not entered_zip:
                        st.warning("Please enter your ZIP code to find local stores.")
                        sub_action = None
                    else:
                        st.session_state.last_sub_action[action_key] = sub_action

                elif sub_action == "message":
                    more_text = st.session_state.expanded_ideas.get(more_key, "")
                    if not more_text:
                        st.warning("💡 Click **More Info** first, then share!")
                        sub_action = None
                    else:
                        if action_key not in st.session_state.share_messages:
                            with st.spinner("Crafting your share message..."):
                                msg = build_share_message(idea, more_text)
                                st.session_state.share_messages[action_key] = msg
                        st.session_state.last_sub_action[action_key] = sub_action

                elif sub_action == "meetup":
                    if action_key not in st.session_state.meetup_invites:
                        with st.spinner("Writing your meetup invite..."):
                            invite = build_meetup_invite(idea)
                            st.session_state.meetup_invites[action_key] = invite
                    st.session_state.last_sub_action[action_key] = sub_action

                active_sub  = sub_action or st.session_state.last_sub_action.get(action_key)
                entered_zip = st.session_state.zipcode_input.get(action_key, "").strip()

                # ---- SHOW RESULTS ----
                if active_sub:
                    st.markdown("---")

                    # PURCHASE ONLINE
                    if active_sub == "online" and action_key in st.session_state.action_data:
                        data = st.session_state.action_data[action_key]
                        st.success(f"🛒 **Online Option:** {data.get('online_option', '')}")
                        query       = urllib.parse.quote_plus(st.session_state.object_name or "")
                        amazon_url  = f"https://www.amazon.com/s?k={query}"
                        etsy_url    = f"https://www.etsy.com/search?q={query}"
                        walmart_url = f"https://www.walmart.com/search?q={query}"
                        google_url  = f"https://www.google.com/search?tbm=shop&q={query}"
                        c1, c2, c3, c4 = st.columns(4)
                        with c1:
                            st.markdown(icon_btn(amazon_url,  "#FF9900", "amazon",  "Amazon",      "#111", small=True), unsafe_allow_html=True)
                        with c2:
                            st.markdown(icon_btn(etsy_url,    "#F45800", "etsy",    "Etsy",         small=True),        unsafe_allow_html=True)
                        with c3:
                            st.markdown(icon_btn(walmart_url, "#0071CE", "walmart", "Walmart",      small=True),        unsafe_allow_html=True)
                        with c4:
                            st.markdown(icon_btn(google_url,  "#ffffff", "google",  "Google Shop", "#3c4043", small=True), unsafe_allow_html=True)

                    # PURCHASE OFFLINE
                    elif active_sub == "offline":
                        if not entered_zip:
                            st.warning("Please enter your ZIP code to find local stores.")
                        else:
                            query    = urllib.parse.quote_plus(f"{st.session_state.object_name} store near {entered_zip}")
                            maps_url = f"https://www.google.com/maps/search/?api=1&query={query}"
                            st.link_button("🗺️ Open Google Maps — stores near " + entered_zip, maps_url)

                    # SHARE — friendly message + social buttons
                    elif active_sub == "message":
                        share_text = st.session_state.share_messages.get(action_key, "")
                        if share_text:
                            b64_text = base64.b64encode(share_text.encode("utf-8")).decode("ascii")
                            copy_id2 = f"copy_share_{i}"
                            lines = share_text.split('\n')
                            total_lines = sum(max(1, -(-len(line) // 75)) for line in lines)  # ceiling division
                            card_h = total_lines * 24 + 60  # 24px per line + padding

                            components.html(f"""
                            <style>
                            html, body {{ margin: 0; padding: 0; overflow: hidden; }}
                            </style>
                            <div style='background:#e3f2fd;border-radius:10px;
                                        padding:12px 14px 14px 14px;border-left:4px solid #1877F2;
                                        position:relative;font-family:sans-serif;box-sizing:border-box;
                                        width:100%;'>
                            <div style='font-size:12px;color:#555;margin-bottom:6px;font-weight:600;'>
                                💌 share kindness:
                            </div>
                            <div style='font-size:13px;color:#222;line-height:1.8;
                                white-space:pre-wrap;padding-right:90px;'>{share_text}</div>
                            <button id='{copy_id2}'
                                onclick="(function(){{
                                var b64='{b64_text}';
                                var txt=atob(b64);
                                var ta=document.createElement('textarea');
                                ta.value=decodeURIComponent(escape(txt));
                                ta.style.cssText='position:fixed;left:-9999px;top:-9999px;';
                                document.body.appendChild(ta);
                                ta.select();
                                document.execCommand('copy');
                                document.body.removeChild(ta);
                                var b=document.getElementById('{copy_id2}');
                                b.textContent='✅ Copied!';
                                b.style.background='#43a047';
                                setTimeout(function(){{b.textContent='📋 Copy';b.style.background='#1877F2';}},2000);
                                }})()"
                                style='position:absolute;top:10px;right:10px;background:#1877F2;
                                    border:none;border-radius:6px;color:white;font-size:12px;
                                    font-weight:600;padding:6px 12px;cursor:pointer;'>
                                📋 Copy
                            </button>
                            </div>
                            """, height=card_h, scrolling=False)
                            st.markdown("<div style='font-size:12px;color:#666;margin-bottom:6px;'>Or send directly via:</div>", unsafe_allow_html=True)
                            encoded      = urllib.parse.quote(share_text)
                            subject      = urllib.parse.quote("A Kindness Idea for You 💖")
                            whatsapp_url = f"https://wa.me/?text={encoded}"
                            facebook_url = f"https://www.facebook.com/sharer/sharer.php?u=https://westportsmiles.org&quote={encoded}"
                            telegram_url = f"https://t.me/share/url?url=https://westportsmiles.org&text={encoded}"
                            twitter_url  = f"https://twitter.com/intent/tweet?text={encoded}"
                            gmail_url    = f"https://mail.google.com/mail/?view=cm&fs=1&su={subject}&body={encoded}"
                            cw, cf, ct, cx, cg = st.columns(5)
                            with cw:
                                st.markdown(icon_btn(whatsapp_url, "#25D366", "whatsapp",  "WhatsApp"),    unsafe_allow_html=True)
                            with cf:
                                st.markdown(icon_btn(facebook_url, "#1877F2", "facebook",  "Facebook"),    unsafe_allow_html=True)
                            with ct:
                                st.markdown(icon_btn(telegram_url, "#229ED9", "telegram",  "Telegram"),    unsafe_allow_html=True)
                            with cx:
                                st.markdown(icon_btn(twitter_url,  "#000000", "twitter_x", "X (Twitter)"), unsafe_allow_html=True)
                            with cg:
                                st.markdown(icon_btn(gmail_url,    "#ffffff", "gmail",      "Gmail", "#3c4043", small=True), unsafe_allow_html=True)

                    # SCHEDULE A MEET — invite message + app buttons (small, single row)
                    elif active_sub == "meetup":
                        invite_text = st.session_state.meetup_invites.get(action_key, "")
                        if invite_text:
                            b64_inv  = base64.b64encode(invite_text.encode("utf-8")).decode("ascii")
                            copy_id3 = f"copy_meet_{i}"
                            est_lines3 = sum(max(1, len(line)//55 + 1) for line in invite_text.split('\n'))
                            card_h3    = max(120, est_lines3 * 22 + 80)
                            components.html(f"""
                            <div id='card_{copy_id3}' style='background:#e8f5e9;border-radius:10px;padding:12px 14px 14px 14px;
                                        border-left:4px solid #34A853;position:relative;
                                        font-family:sans-serif;box-sizing:border-box;'>
                              <div style='font-size:12px;color:#555;margin-bottom:6px;font-weight:600;'>
                                📅 Kindness schedule invite:
                              </div>
                              <div style='font-size:13px;color:#222;line-height:1.6;
                                   white-space:pre-wrap;padding-right:80px;'>{invite_text}</div>
                              <button id='{copy_id3}'
                                onclick="(function(){{
                                  var b64='{b64_inv}';
                                  var txt=atob(b64);
                                  var ta=document.createElement('textarea');
                                  ta.value=decodeURIComponent(escape(txt));
                                  ta.style.cssText='position:fixed;left:-9999px;top:-9999px;';
                                  document.body.appendChild(ta);
                                  ta.select();
                                  document.execCommand('copy');
                                  document.body.removeChild(ta);
                                  var b=document.getElementById('{copy_id3}');
                                  b.textContent='✅ Copied!';
                                  b.style.background='#2e7d32';
                                  setTimeout(function(){{b.textContent='📋 Copy';b.style.background='#34A853';}},2000);
                                }})()"
                                style='position:absolute;top:10px;right:10px;background:#34A853;
                                       border:none;border-radius:6px;color:white;font-size:12px;
                                       font-weight:600;padding:6px 12px;cursor:pointer;'>
                                📋 Copy
                              </button>
                            </div>
                            <script>
                              var el = document.getElementById('card_{copy_id3}');
                              if (el) {{
                                var h = el.scrollHeight + 8;
                                window.frameElement.style.height = h + 'px';
                              }}
                            </script>
                            """, height=card_h3, scrolling=False)
                            st.markdown("<div style='font-size:12px;color:#666;margin:2px 0 6px;'>Open your preferred app to schedule:</div>", unsafe_allow_html=True)

                        meet_url  = "https://meet.google.com/new"
                        zoom_url  = "https://zoom.us/meeting/schedule"
                        teams_url = "https://teams.microsoft.com/l/meeting/new"
                        facetime_url = "facetime://"
                        wa_call_url  = "https://wa.me/"

                        cg, cz, ct2, cf2, cw2 = st.columns(5)
                        with cg:
                            st.markdown(icon_btn(meet_url,     "#ffffff", "googlemeet", "Meet",    "#3c4043", small=True), unsafe_allow_html=True)
                        with cz:
                            st.markdown(icon_btn(zoom_url,     "#2D8CFF", "zoom",       "Zoom",    small=True),            unsafe_allow_html=True)
                        with ct2:
                            st.markdown(icon_btn(teams_url,    "#6264A7", "teams",      "Teams",   small=True),            unsafe_allow_html=True)
                        with cf2:
                            st.markdown(icon_btn(facetime_url, "#34C759", "facetime",   "FaceTime",small=True),            unsafe_allow_html=True)
                        with cw2:
                            st.markdown(icon_btn(wa_call_url,  "#25D366", "whatsapp",   "WhatsApp",small=True),            unsafe_allow_html=True)

        st.markdown("---")

# ---------- CLEAR BUTTON ----------
if st.session_state.image is not None:
    if st.button("🗑 Clear Image"):
        st.session_state.image        = None
        st.session_state.input_source = None
        st.session_state.is_blurred   = False
        st.rerun()

show_footer()
