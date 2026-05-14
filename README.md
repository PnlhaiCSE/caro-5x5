# Caro AI 5x5

A web-based Gomoku (Caro) game where a player competes against an AI opponent on a **5x5 board**.  
The AI is implemented using the **Minimax algorithm with Alpha-Beta Pruning** and heuristic board evaluation.

The project follows a **frontend-backend architecture** and can be deployed using **Docker**.

---

# Project Structure

```text
CARO-AI
│
├── engine
│   ├── ai.py               # Core AI engine (minimax, alpha-beta pruning, evaluation)
│   ├── board.py            # Board size and win-checking logic
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│   ├── templates/
│   │   └── index.html      # Main game interface
│   └── static/
│       ├── script.js       # Frontend game logic + API calls
│       └── style.css       # UI styling
│
├── Dockerfile              # Docker build configuration 
├── .gitignore              # Files ignored by Git 
└── README.md               # Project documentation 
```
---

# Technologies Used
Python<br>
Flask<br>
JavaScript<br>
HTML<br>
CSS<br>
Docker

---

# Quick Start
```bash
git clone git@github.com:pnlhaiIT/caro-5x5.git
cd engine
docker compose up --build
```

Then open:
```text
http://localhost:5050
```
---

#  Author

Student project demonstrating classical Artificial Intelligence techniques.<br>
Base của repo caro 10x10.<br>
Phạm Nguyễn Long Hải

---
