# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  The game initially looked straightforward, with instructions to guess a number between 1 and 100. I noticed that the hints pointed in the wrong direction: when I guessed 5 against a secret of 40, the game told me to go lower instead of higher. The game also accepted decimal input instead of rejecting it as an invalid whole-number guess. Clicking New Game did not appear to fully reset the game. I also sometimes needed to click Submit Guess twice, although I had not yet confirmed the cause.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input / Trigger | Expected Behavior | Actual Behavior | Console Error / Output | Suspected Code Location |
|-----------------|-------------------|-----------------|------------------------|-------------------------|
| Guess 5 with secret 40 | Hint says “Go HIGHER!” | Hint says “Go LOWER!” | No console error; incorrect hint displayed | app.py: check_guess() |
| Enter 1.2 | Reject decimal input with an error | Accepts the input; code converts it to 1 | Hint displayed instead of a validation error | app.py: parse_guess(), int(float(raw)) |
| Click New Game after [describe game state] | Reset status, attempts, score, and history | [Describe exactly what remained unchanged] | [Exact displayed message, or “None”] | app.py: if new_game block |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  I used ChatGPT to review app.py and logic_utils.py, explain potential bugs, and suggest fixes and tests.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  ChatGPT correctly identified that the hints in check_guess() were reversed. I verified this by reviewing the code: when guess > secret, it returns “Go HIGHER!” even though the player should guess lower, and the opposite branch incorrectly says “Go LOWER!”
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
  I rejected ChatGPT’s proposed win-scoring change because the intended reward rules had not been confirmed. I kept the existing formula and verified in the code that it remained unchanged while I focused on the comparison repair.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  I checked whether the updated comparison logic matched the expected behavior: high guesses should suggest going lower, low guesses should suggest going higher, and matching guesses should win.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  The high-guess test calls check_guess(60, 50) and checks that it returns "Go HIGHER!” and “Go LOWER!”. After running pytest, I recorded the test to confirm whether the corrected function behaved as expected.
- Did AI help you design or understand any tests? How?
  ChatGPT helped design tests for high, low, and winning guesses. It also explained that check_guess() returns an outcome and a message, so checking both values is necessary to catch the reversed-hint bug.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit? 
  Streamlit reruns the Python script from top to bottom when someone interacts with a widget, such as clicking a button. Ordinary variables can be recreated during each rerun, so the app needs a way to remember the game’s progress. st.session_state acts like a memory box that keeps values such as the secret number, attempts, score, and history between reruns. Starting a new game requires resetting those stored values so the previous game does not affect the next one.

---


## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  I want to keep writing focused tests that check both a function’s result and its message. This helps catch bugs like reversed hints that checking only the outcome would miss.
- What is one thing you would do differently next time you work with AI on a coding task?
  Next time, I would ask AI to fix one specific bug at a time and review every changed file before accepting the solution.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  This project showed me that AI-generated code can look reasonable while still containing logic errors. I need to understand its behavior and verify it with tests and manual checks instead of assuming it is correct.
