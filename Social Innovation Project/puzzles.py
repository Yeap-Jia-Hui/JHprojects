"""Puzzle content for Two Minds, One Puzzle.

Add new activities here; the Streamlit interface renders each puzzle using the
same fields so puzzle content stays separate from presentation logic.
"""

PUZZLES = {
    "modular": {
        "title": "Modular Puzzle",
        "emoji": "🧩",
        "tagline": "Four clues. One shared answer.",
        "instructions": "Each module gives you a number. Use the key **1 = A, 2 = B, … 26 = Z** to turn the four numbers into a word. Put the letters together in module order.",
        "clues": [
            ("Module A · Pattern", "3, 6, 9, __ — what number comes next?"),
            ("Module B · Text clue", "How many natural satellites does Earth have?"),
            ("Module C · Number clue", "What is 3 + 10?"),
            ("Module D · Number clue", "What is 4 × 4?"),
        ],
        "answer": "lamp",
        "accepted_answers": ["lamp"],
        "hints": ["Solve each card in order, then use the letter key in the instructions.", "The four numbers are 12, 1, 13, and 16."],
        "explanation": "The clues give 12, 1, 13, and 16. With 1 = A, those become L, A, M, P: **LAMP**.",
    },
    "visual": {
        "title": "Visual Riddle",
        "emoji": "👁️",
        "tagline": "Look closely. Let the picture do the talking.",
        "instructions": "Study the objects and how they fit together. Say what you notice to each other before you answer.",
        "image": "assets/visual_riddle.svg",
        "answer": "time flies",
        "accepted_answers": ["time flies", "time fly", "time flies by"],
        "hints": ["The clock and the insect each stand for a word.", "Read the clock's idea together with the winged insect."],
        "explanation": "The clock represents **time** and the winged insect is a **fly**. Together they say **time flies**.",
    },
    "lateral": {
        "title": "Lateral Thinking",
        "emoji": "💡",
        "tagline": "A small mystery with a hidden assumption.",
        "instructions": "Read the situation together. What assumption might you be making about the sound?",
        "scenario": "A person walks into a quiet room and asks for a glass of water. The person behind the counter suddenly rings a loud bell. The visitor smiles, says “That did it—thank you,” and leaves without any water. What happened?",
        "answer": "hiccups",
        "accepted_answers": ["hiccups", "had hiccups", "the hiccups", "they had hiccups", "a case of hiccups"],
        "hints": ["The visitor needed help with a bodily annoyance, not thirst.", "The loud surprise stopped a bout of hiccups."],
        "explanation": "The visitor had **hiccups** and asked for water to try to stop them. The sudden bell startled them, curing the hiccups, so they no longer needed the water.",
    },
}

MENU_COPY = {
    "modular": "Combine clues from different parts of the website to discover the answer.",
    "visual": "Look closely. The answer is hidden somewhere in the picture.",
    "lateral": "Challenge your assumptions and figure out what really happened.",
}
