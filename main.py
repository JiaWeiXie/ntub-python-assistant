import os
import time
import json

from pathlib import Path

import streamlit as st
import tiktoken
from openai import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.environ.get("OPENAI_ASSISTANT_ID")
ROLES = {
    "user": "你",
    "assistant": "助理",
}
SETTINGS_FILE = Path("syssettings.json")


if "is_authenticated" in st.session_state:
    is_authenticated = st.session_state.get("is_authenticated", False)
else:
    is_authenticated = False

enable_guest_vaildation = True
saved_geust_password = ""
if SETTINGS_FILE.exists():
    with SETTINGS_FILE.open(encoding="utf-8") as f:
        data = f.read()
        if data:
            settings = json.loads(data)
            enable_guest_vaildation = settings.get("enable_guest_vaildation", True)
            saved_geust_password = settings.get("guest_password", "")

if enable_guest_vaildation and not is_authenticated:
    geust_password = st.sidebar.text_input("請輸入訪客密碼", type="password")
    if st.sidebar.button("登入") and geust_password == saved_geust_password:
        st.sidebar.success("登入成功")
        st.session_state["is_authenticated"] = True
    else:
        st.error("請輸入正確的訪客密碼")
        st.stop()


if OPENAI_API_KEY is None:
    st.error("請設定 OpenAI API Key")

if OPENAI_ASSISTANT_ID is None:
    st.error("請設定 OpenAI Assistant ID")

client = OpenAI(api_key=OPENAI_API_KEY)


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model("gpt-4")
    num_tokens = len(encoding.encode(string))
    return num_tokens


question = st.text_area("請輸入你的問題")


newchat_block, button_block = st.columns([0.8, 0.2])
is_submit = False
thread_id = None

with newchat_block:
    if st.button("開始新的對話"):
        thread = client.beta.threads.create()
        st.session_state["thread_id"] = thread.id
        st.toast("已開始新的對話，請輸入你的問題")

with button_block:
    is_submit = st.button("送出問題")

if is_submit:
    if "thread_id" not in st.session_state:
        st.toast("請先開始新的對話")
        st.rerun()

    if not st.session_state["thread_id"]:
        st.toast("請先開始新的對話")
        st.rerun()

    thread_id = st.session_state["thread_id"]

    st.metric("字詞數", num_tokens_from_string(question))
    st.toast("已送出問題")
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=question,
    )
    with st.spinner("等待助理回覆"):
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=OPENAI_ASSISTANT_ID,
        )
        while run.status in ["queued", "in_progress"]:
            st.toast(run.status)
            time.sleep(3)
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            messages.data.reverse()
            for message in messages.data:
                with st.chat_message(ROLES[message.role]):
                    for content in message.content:
                        if content.type == "text":
                            st.markdown(content.text.value)
        else:
            st.error("助理暫時無法回覆")
            st.write(run.status)
            if run.last_error:
                st.markdown(f"錯誤代碼: `{run.last_error.message}`")
                st.write("錯誤訊息:")
                st.write(run.last_error.message)
