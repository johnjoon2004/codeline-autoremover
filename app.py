import re

import streamlit as st


remove_comments = st.checkbox("Remove all comments", value=True)

st.title("Codelines Auto-Cleaner ✨")

input_code = st.text_area("Input Your 🤮 Code Here:", height=300)


def clean_code(text: str, remove_comments: bool = True) -> str:
    lines = text.splitlines()
    cleaned = []

    for line in lines:
        line = re.sub(r"^\s*\d+\s", "", line)

        if remove_comments:
            if line.strip().startswith("#"):
                continue

            parts = re.split(r"(#)", line)
            if len(parts) >= 3:
                code_only = "".join(parts[: parts.index("#")])
                line = code_only.rstrip()

        cleaned.append(line)

    return "\n".join(cleaned)


if st.button("   🧹   "):
    output_code = clean_code(input_code, remove_comments=remove_comments)
    st.text_area("Result:", value=output_code, height=300)
