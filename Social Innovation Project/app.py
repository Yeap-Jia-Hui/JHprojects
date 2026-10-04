import streamlit as st

from puzzles import MENU_COPY, PUZZLES


st.set_page_config(page_title="Two Minds, One Puzzle", page_icon="🧩", layout="centered")

st.markdown("""
<style>
:root { --ink:#202838; --muted:#667085; --paper:#f7f8fb; --line:#e6e9ef; --accent:#4658a8; }
.stApp { background:var(--paper); color:var(--ink); font-family:system-ui,sans-serif; }
[data-testid="stHeader"] { background:transparent; }
h1,h2,h3 { font-family:system-ui,sans-serif !important; letter-spacing:-.035em; color:var(--ink); }
.hero { text-align:center; padding:2.5rem 0 1.6rem; }
.hero h1 { font-size:clamp(2.25rem,6vw,3.35rem); margin-bottom:.35rem; }
.hero .sub { font-size:1.12rem; color:var(--accent); font-weight:700; }
.hero .desc { color:var(--muted); margin-top:.75rem; }
.eyebrow { text-transform:uppercase; letter-spacing:.12em; font-size:.72rem; color:var(--accent); font-weight:700; }
.card { border:1px solid var(--line); border-radius:18px; background:white; padding:1.35rem 1.45rem; min-height:174px; box-shadow:0 5px 18px #26334d08; }
.card .icon { font-size:1.6rem; }
.card h3 { font-size:1.15rem; margin:.45rem 0; }
.card p { color:var(--muted); min-height:48px; font-size:.94rem; }
.clue { border:1px solid var(--line); background:#fff; border-radius:14px; padding:1rem 1.1rem; min-height:108px; }
.clue strong { display:block; color:var(--accent); margin-bottom:.35rem; }
.social { color:var(--muted); font-size:.9rem; padding:.45rem 0 1rem; }
div.stButton > button { border-radius:11px; font-weight:700; min-height:2.7rem; }
.stButton>button[kind="primary"] { background:var(--accent); border-color:var(--accent); }
section[data-testid="stSidebar"] { background:#fff; border-right:1px solid var(--line); }
@media(max-width:640px) { .hero { padding-top:1.5rem; } .card { min-height:unset; } }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"
for key in PUZZLES:
    st.session_state.setdefault(f"solved_{key}", False)
    st.session_state.setdefault(f"revealed_{key}", False)
    st.session_state.setdefault(f"hint_{key}", 0)


def go(page):
    st.session_state.page = page


def reset(key):
    st.session_state[f"solved_{key}"] = False
    st.session_state[f"revealed_{key}"] = False
    st.session_state[f"hint_{key}"] = 0
    st.session_state[f"answer_{key}"] = ""


with st.sidebar:
    st.markdown("### 🧩 Two Minds")
    st.caption("Choose a puzzle to play together.")
    if st.button("⌂  Puzzle Menu", use_container_width=True):
        go("home")
    st.divider()
    for key, puzzle in PUZZLES.items():
        if st.button(f"{puzzle['emoji']}  {puzzle['title']}", key=f"nav_{key}", use_container_width=True):
            go(key)
    st.divider()
    st.caption("No order, scores, or rush. Just solve together.")


page = st.session_state.page
if page not in PUZZLES:
    st.markdown('<div class="hero"><div class="eyebrow">A little table for two</div><h1>Two Minds, One Puzzle</h1><div class="sub">Work together. Think differently. Solve it.</div><div class="desc">Pick a puzzle, sit down together, and see if you can figure it out.</div></div>', unsafe_allow_html=True)
    cols = st.columns(3, gap="medium")
    for (key, puzzle), col in zip(PUZZLES.items(), cols):
        with col:
            st.markdown(f"<div class='card'><div class='icon'>{puzzle['emoji']}</div><h3>{puzzle['title']}</h3><p>{MENU_COPY[key]}</p></div>", unsafe_allow_html=True)
            if st.button("Start Puzzle →", key=f"start_{key}", type="primary", use_container_width=True):
                go(key)
    st.markdown("<p class='social' style='text-align:center;margin-top:1.6rem'>Take turns sharing what you notice. What does your partner see that you don’t?</p>", unsafe_allow_html=True)
else:
    p = PUZZLES[page]
    st.markdown(f"<div class='eyebrow'>{p['emoji']} &nbsp; puzzle table</div><h1>{p['title']}</h1><p style='color:#667085'>{p['tagline']}</p>", unsafe_allow_html=True)
    if st.session_state[f"solved_{page}"] or st.session_state[f"revealed_{page}"]:
        st.success("✓ Solved! Nice work." if st.session_state[f"solved_{page}"] else "Answer revealed")
        st.markdown(f"**Answer:** {p['answer'].title()}  \n{p['explanation']}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Puzzle Menu", use_container_width=True):
                go("home")
        with col2:
            if st.button("Try Another Puzzle →", type="primary", use_container_width=True):
                go("home")
        if st.button("Reset this puzzle", use_container_width=True):
            reset(page)
            st.rerun()
    else:
        st.markdown(f"{p['instructions']}")
        if page == "modular":
            cols = st.columns(2, gap="medium")
            for (title, clue), col in zip(p["clues"], cols * 2):
                with col:
                    st.markdown(f"<div class='clue'><strong>{title}</strong>{clue}</div>", unsafe_allow_html=True)
        elif page == "visual":
            st.image(p["image"], use_container_width=True)
        else:
            st.info(f"**Scenario**\n\n{p['scenario']}")
            st.markdown("### What happened?")
        st.markdown("<div class='social'>Discuss your ideas before submitting. What does your partner notice that you don’t?</div>", unsafe_allow_html=True)
        with st.form(f"answer_form_{page}"):
            st.text_input("What is the answer?", key=f"answer_{page}", placeholder="Talk it through, then enter your answer")
            submitted = st.form_submit_button("Submit Answer", type="primary", use_container_width=True)
        if submitted:
            answer = st.session_state.get(f"answer_{page}", "").strip().lower()
            accepted = {item.lower() for item in p["accepted_answers"]}
            if answer in accepted:
                st.session_state[f"solved_{page}"] = True
                st.rerun()
            elif answer:
                st.error("Not quite. Compare your clues and give it another try.")
            else:
                st.warning("Enter an answer when you’re ready.")
        hint_col, reveal_col, reset_col = st.columns(3)
        with hint_col:
            if st.button("💡 Hint", use_container_width=True):
                current = st.session_state[f"hint_{page}"]
                if current < len(p["hints"]):
                    st.session_state[f"hint_{page}"] = current + 1
                st.rerun()
        with reveal_col:
            if st.button("Reveal Answer", use_container_width=True):
                st.session_state[f"revealed_{page}"] = True
                st.rerun()
        with reset_col:
            if st.button("Reset Puzzle", use_container_width=True):
                reset(page)
                st.rerun()
        shown = st.session_state[f"hint_{page}"]
        for i, hint in enumerate(p["hints"][:shown], start=1):
            st.info(f"Hint {i}: {hint}")
