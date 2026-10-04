# Two Minds, One Puzzle

A small Streamlit puzzle host for two people sitting together. Each puzzle is independent; choose any activity from the menu or sidebar, and leave whenever you like.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Push this folder to GitHub, create an app on Streamlit Community Cloud, choose `app.py` as the entry point, and deploy. The only Python dependency is Streamlit.

## Edit or add puzzles

Puzzle text and answers live in `puzzles.py`, separate from layout and interaction code in `app.py`. Edit a puzzle's `title`, `instructions`, clue/scenario/image, `answer`, `accepted_answers`, `hints`, and `explanation` there. The three menu activities are generated from `PUZZLES`, so adding an activity starts with a new entry using the same fields. Add any custom display for its content to the `page == ...` rendering section in `app.py` and add a short menu description to `MENU_COPY`. Each entry key is also its independent session-state key; use a short unique key. Local artwork belongs in `assets/`.
