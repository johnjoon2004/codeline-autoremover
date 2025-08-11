import re
import streamlit as st


st.set_page_config(layout="wide")
st.title("Codelines Auto-Cleaner")
st.checkbox("Remove all comments", value=True, key="remove_comments")

# init session state
st.session_state.setdefault("input_code", "")
st.session_state.setdefault("output_code", "")

col1, col_btn, col2 = st.columns([7, 1, 7])
tb_height = 500


def clean_code(text: str, remove_comments: bool = True) -> str:
    if remove_comments:
        text = re.sub(r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\')', "", text, flags=re.DOTALL)

    lines = text.splitlines()
    cleaned = []

    for line in lines:
        # removing line-numbers
        line = re.sub(r"^\s*\d+\s", "", line)

        if remove_comments:
            # removing leading comments
            if line.strip().startswith("#"):
                continue

            # removing inline comments
            parts = re.split(r"(#)", line)
            if len(parts) >= 3:
                code_only = "".join(parts[: parts.index("#")])
                line = code_only.rstrip()

        cleaned.append(line)

    return "\n".join(cleaned)


def auto_clean():
    # input-output auto-synchronization
    # `ctrl + enter` enables cleaning
    st.session_state["output_code"] = clean_code(
        st.session_state["input_code"],
        remove_comments=st.session_state["remove_comments"],
    )


with col1:
    st.text_area(
        "Input Your 🤮 Code:",
        value=st.session_state["input_code"],
        height=tb_height,
        key="input_code",
        on_change=auto_clean,
    )

with col_btn:
    st.write("")
    st.write("")
    run_clean = st.button("🧹", use_container_width=True)

with col2:
    if run_clean:
        st.session_state["output_code"] = clean_code(
            st.session_state["input_code"],
            remove_comments=st.session_state["remove_comments"],
        )
    st.text_area(
        "Cleaned ✨ Code:",
        value=st.session_state["output_code"],
        height=tb_height,
    )
