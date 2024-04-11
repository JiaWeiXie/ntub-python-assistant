import os
import json

from pathlib import Path

import streamlit as st


ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
SETTINGS_FILE = Path("syssettings.json")

if "admin_authenticated" in st.session_state:
    is_authenticated = st.session_state.get("admin_authenticated", False)
else:
    is_authenticated = False
password = st.sidebar.text_input("請輸入管理員密碼", type="password")


if st.sidebar.button("登入") and password == ADMIN_PASSWORD:
    st.sidebar.success("登入成功")
    st.session_state["admin_authenticated"] = True
    is_authenticated = True

if not password or password != ADMIN_PASSWORD or not is_authenticated:
    st.error("請輸入正確的管理員密碼")
    st.stop()

enable_guest_vaildation = True
saved_geust_password = ""
if SETTINGS_FILE.exists():
    with SETTINGS_FILE.open("r", encoding="utf-8") as f:
        data = f.read()
        if data:
            settings = json.loads(data)
            enable_guest_vaildation = settings.get("enable_guest_vaildation", True)
            saved_geust_password = settings.get("guest_password", "")

st.title("系統設定")
geust_password = st.text_input("請設定訪客密碼", type="password")
enable_guest_vaildation = st.checkbox("啟用訪客密碼", value=enable_guest_vaildation)

if st.button("儲存設定"):
    with SETTINGS_FILE.open("w", encoding="utf-8") as f:
        data = json.dumps(
            {
                "guest_password": geust_password or saved_geust_password,
                "enable_guest_vaildation": enable_guest_vaildation,
            }
        )
        f.write(data)
    st.success("設定已儲存")
