# ♠️ Probabilistic Poker Bot

A full-stack Texas Hold'em poker assistant that uses Monte Carlo simulation to estimate your win probability and recommend actions (call or fold) based on your current hand and community cards.

## 🃏 Features

- Select **2 hole cards** and **5 community cards** via an interactive UI
- Backend powered by **Monte Carlo simulation** (10,000+ iterations)
- Instant calculation of:
  - Win probability (e.g., 73.42%)
  - Recommended action (call or fold)
- Card assets sourced from the [Deck of Cards API](https://deckofcardsapi.com/)
- Built with modern tech stack: **React + Flask**

---

## 🔧 Tech Stack

| Layer        | Tech                         |
|--------------|------------------------------|
| Frontend     | React, CSS, Vite             |
| Backend      | Flask, Python, Treys         |
| Simulation   | Custom Monte Carlo engine    |
| Utilities    | NumPy, TQDM, Treys Hand Eval |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/poker-bot.git
cd poker-bot
2. Backend Setup (Python)
bash
Copy
Edit
cd backend
pip install -r requirements.txt
python flask_app.py
Frontend Setup (React)
bash
Copy
Edit
cd frontend
npm install
npm run dev
🧠 How It Works
You select 7 cards total (2 hole + 5 community)

The frontend sends a POST request to /api/recommend

Backend uses a Monte Carlo simulator to:

Deal random opponent hands

Complete missing community cards (if any)

Evaluate all hands using Treys

Calculates:

Win %

Tie %

Expected Value (EV)

Returns a recommendation: call or fold

