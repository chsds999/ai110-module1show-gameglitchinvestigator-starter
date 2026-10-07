import random

import streamlit as st

from logic_utils import check_guess


def get_range_for_difficulty(difficulty: str):
    """Return the inclusive number range for a difficulty."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 50),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """Parse a whole-number guess without truncating decimals."""
    if raw is None or not raw.strip():
        return False, None, "Enter a guess."

    # FIX: Used ChatGPT to reject decimals instead of truncating them.
    try:
        value = int(raw.strip())
    except ValueError:
        return False, None, "Enter a whole number."

    return True, value, None


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Deduct five points for wrong guesses or award a win bonus."""
    # FIX: Used ChatGPT to make penalties consistent for incorrect guesses.
    if outcome == "Win":
        points = max(10, 100 - 10 * attempt_number)
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score


def reset_game(difficulty: str):
    """Reset all game values using the selected difficulty."""
    low, high = get_range_for_difficulty(difficulty)

    # FIX: Used ChatGPT to reset the full state and respect difficulty.
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_message = None
    st.session_state.input_error = None
    st.session_state.celebrate = False
    st.session_state.guess_input = ""


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("A guessing game with repaired logic and game state.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

# FIX: Start a fresh game when difficulty changes.
if (
    "secret" not in st.session_state
    or st.session_state.get("difficulty") != difficulty
):
    reset_game(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# The callback runs before the next script execution.
st.sidebar.button(
    "New Game 🔁",
    on_click=reset_game,
    args=(difficulty,),
)

show_hint = st.sidebar.checkbox("Show hint", value=True)

st.subheader("Make a guess")

attempts_left = max(0, attempt_limit - st.session_state.attempts)

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempts_left}"
)
st.write(f"Score: {st.session_state.score}")

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

game_finished = st.session_state.status != "playing"

# FIX: Use a form to submit the input and button together.
with st.form("guess_form"):
    raw_guess = st.text_input(
        "Enter your guess:",
        key="guess_input",
        disabled=game_finished,
    )
    submit = st.form_submit_button(
        "Submit Guess 🚀",
        disabled=game_finished,
    )

if submit and not game_finished:
    ok, guess_int, error = parse_guess(raw_guess)

    st.session_state.input_error = None

    if not ok:
        st.session_state.input_error = error
    elif not low <= guess_int <= high:
        st.session_state.input_error = (
            f"Enter a number between {low} and {high}."
        )
    else:
        # FIX: Count only valid guesses within the selected range.
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIX: Used ChatGPT to keep comparisons numeric on every attempt.
        outcome, message = check_guess(
            guess_int,
            st.session_state.secret,
        )

        st.session_state.last_message = message
        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.session_state.celebrate = True
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"

    # FIX: Refresh counters while retaining feedback in session state.
    st.rerun()

if st.session_state.input_error:
    st.error(st.session_state.input_error)

if (
    show_hint
    and st.session_state.last_message
    and st.session_state.status == "playing"
):
    st.warning(st.session_state.last_message)

if st.session_state.status == "won":
    if st.session_state.celebrate:
        st.balloons()
        st.session_state.celebrate = False

    st.success(
        f"You won! The secret was {st.session_state.secret}. "
        f"Final score: {st.session_state.score}"
    )
    st.caption("Click New Game in the sidebar to play again.")

elif st.session_state.status == "lost":
    st.error(
        f"Out of attempts! The secret was {st.session_state.secret}. "
        f"Final score: {st.session_state.score}"
    )
    st.caption("Click New Game in the sidebar to try again.")

st.divider()
st.caption("Repaired with AI assistance and human review.")