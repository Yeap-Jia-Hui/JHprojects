import base64
import os

import requests
import streamlit as st


@st.cache_data(ttl=300)
def fetch_vault_from_github():
    token = st.secrets["GITHUB_TOKEN"]
    repo = st.secrets["GITHUB_REPO"]
    headers = {"Authorization": f"token {token}"}
    url = f"https://api.github.com/repos/{repo}/git/trees/main?recursive=1"
    resp = requests.get(url, headers=headers, timeout=30)

    if resp.status_code != 200:
        message = resp.json().get("message", "Unknown error")
        return [], f"GitHub error {resp.status_code}: {message}"

    tree = resp.json().get("tree", [])
    md_files = [entry for entry in tree if entry["path"].endswith(".md")]
    notes = []

    for md_file in md_files:
        try:
            blob = requests.get(md_file["url"], headers=headers, timeout=30).json()
            content = base64.b64decode(blob["content"]).decode("utf-8", errors="ignore")
            notes.append(
                {
                    "name": os.path.basename(md_file["path"]),
                    "path": md_file["path"],
                    "content": content,
                }
            )
        except Exception:
            continue

    return notes, None
