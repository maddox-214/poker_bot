
import tkinter as tk
from tkinter import ttk, messagebox
import threading

from treys import Card
from simulator import MonteCarloSimulator
from utils import parse_pretty_cards

class PokerBotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Probabilistic Poker Bot")
        self.geometry("400x300")

        # Hole cards input
        tk.Label(self, text="Hole Cards (e.g. As,Kd):").pack(pady=(10, 0))
        self.hole_entry = tk.Entry(self, width=20)
        self.hole_entry.pack()

        # Community cards input
        tk.Label(self, text="Community Cards (e.g. 2h,Jc,Ts):").pack(pady=(10, 0))
        self.community_entry = tk.Entry(self, width=20)
        self.community_entry.pack()

        # Number of Players
        tk.Label(self, text="Number of Players:").pack(pady=(10, 0))
        self.players_spin = tk.Spinbox(self, from_=2, to=10, width=5)
        self.players_spin.pack()

        # Simulation count
        tk.Label(self, text="Simulations:").pack(pady=(10, 0))
        self.sim_spin = tk.Spinbox(self, from_=1000, to=100000, increment=1000, width=7)
        self.sim_spin.pack()

        # Simulate button
        self.run_button = tk.Button(self, text="Simulate", command=self.start_simulation)
        self.run_button.pack(pady=(15, 0))

        # Indeterminate progress bar
        self.progress = ttk.Progressbar(self, mode="indeterminate")

        # Result label
        self.result_label = tk.Label(self, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=(15, 0))

    def start_simulation(self):
        hole_text = self.hole_entry.get().strip()
        community_text = self.community_entry.get().strip()
        players = int(self.players_spin.get())
        sims = int(self.sim_spin.get())

        if not hole_text:
            messagebox.showerror("Error", "Enter hole cards (e.g. As,Kd)")
            return

        # Split by comma and strip whitespace
        hole_list = [s.strip() for s in hole_text.split(",")]
        comm_list = [s.strip() for s in community_text.split(",")] if community_text else []

        try:
            hole_cards = parse_pretty_cards(hole_list)
            community_cards = parse_pretty_cards(comm_list) if comm_list else []
        except Exception as e:
            messagebox.showerror("Error", f"Invalid card format: {e}")
            return
        
        
        # Disable button & start progress bar
        self.run_button.config(state="disabled")
        self.result_label.config(text="")
        self.progress.pack(pady=(10, 0))
        self.progress.start()

        # Run simulation in background
        thread = threading.Thread(
            target=self.run_simulation,
            args=(hole_cards, community_cards, players, sims),
            daemon=True
        )
        thread.start()

    def run_simulation(self, hole_cards, community_cards, players, sims):
        sim = MonteCarloSimulator(n_players=players, n_simulations=sims)
        win_prob, tie_prob = sim.simulate_win_prob(hole_cards, community_cards)
        result_text = f"Win Probability: {win_prob:.3f}\nTie Probability: {tie_prob:.3f}"
        # Back to main thread to update UI
        self.after(0, lambda: self.show_result(result_text))

    def show_result(self, text):
        self.progress.stop()
        self.progress.pack_forget()
        self.result_label.config(text=text)
        self.run_button.config(state="normal")


if __name__ == "__main__":
    app = PokerBotGUI()
    app.mainloop()
