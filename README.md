# Probabilistic Poker Bot

Simple outline:
1. `evaluator.py` – wraps Treys (or any other C‐based evaluator) to get hand strength.
2. `simulator.py` – runs Monte Carlo simulations to estimate win probability.
3. `bot.py`   – high‐level decision logic (EV calculations, fold/call/raise).
4. `utils.py`  – helper routines (e.g., deck shuffling, card parsing).

## Quickstart

```bash
cd poker_bot
pip install -r requirements.txt
python bot.py
