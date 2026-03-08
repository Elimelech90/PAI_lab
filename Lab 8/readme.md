# HAHA.EXE — Random Joke App
## Lab 7 Task 1 | Programming for Artificial Intelligence

---

## Overview
A Flask web app that fetches random jokes from the **JokeAPI** (free, no key required).

## Features
- 7 joke categories: Any, Programming, Misc, Dark, Pun, Spooky, Christmas
- Two-part jokes with a hidden punchline reveal button
- Emoji reactions (😂 🙄 💀) with live counters
- Session stats: jokes told, laughs, last category
- Copy joke to clipboard
- Spacebar shortcut to get next joke
- Safe-mode enabled (no NSFW content)

## API Used
**JokeAPI v2** — https://v2.jokeapi.dev  
Free, no API key required.

### Flask Routes
| Route | Method | Description |
|---|---|---|
| `/` | GET | Renders the main page |
| `/api/joke` | GET | Random joke (Any category) |
| `/api/joke/<category>` | GET | Joke from specific category |
| `/api/joke/<category>/<type>` | GET | Joke by category + type (single/twopart) |

## Setup

```bash
pip install -r requirements.txt
python app.py
# Open: http://localhost:5000
```

## Project Structure
```
joke_app/
├── app.py              # Flask backend + API integration
├── requirements.txt
├── templates/
│   └── index.html      # Full frontend (HTML/CSS/JS)
└── README.md
```