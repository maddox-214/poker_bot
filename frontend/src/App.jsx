import React, { useState } from "react";

const CARD_IMAGE_URL = (code) => `https://deckofcardsapi.com/static/img/${code}.png`;
const BACKEND_URL = "http://localhost:5000/api/recommend"; // adjust if needed

const suits = ["S", "H", "D", "C"];
const ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K"];
const fullDeck = ranks.flatMap((rank) => suits.map((suit) => `${rank}${suit}`));

const App = () => {
  const [selectedCards, setSelectedCards] = useState([]);
  const [recommendation, setRecommendation] = useState("");
  const [error, setError] = useState("");

  const toggleCardSelection = (code) => {
    setSelectedCards((prev) =>
      prev.includes(code) ? prev.filter((c) => c !== code) : [...prev, code].slice(0, 7)
    );
  };

  const resetSelection = () => {
    setSelectedCards([]);
    setRecommendation("");
    setError("");
  };

  const getRecommendation = async () => {
    if (selectedCards.length < 2 || selectedCards.length > 7) {
      setError("Please select 2 hole cards and up to 5 community cards.");
      setRecommendation("");
      return;
    }

    const payload = {
      hole_cards: selectedCards.slice(0, 2),
      community_cards: selectedCards.slice(2)
    };

    try {
      const response = await fetch(BACKEND_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error("Backend error");

      const data = await response.json();
      setRecommendation(`${data.recommendation} (Win %: ${data.win_percentage}%)`);
      setError("");
    } catch (err) {
      setError("Failed to fetch recommendation.");
      setRecommendation("");
    }
  };

  return (
    <div className="min-h-screen bg-green-900 flex flex-col items-center justify-center p-6">
      {/* Selected Cards Display */}
      <div className="mb-8">
        <div className="flex justify-center space-x-2 mb-2">
          {selectedCards.slice(2).map((code) => (
            <img key={code} src={CARD_IMAGE_URL(code)} alt={code} className="w-16 h-24" />
          ))}
        </div>
        <div className="flex justify-center space-x-2">
          {selectedCards.slice(0, 2).map((code) => (
            <img key={code} src={CARD_IMAGE_URL(code)} alt={code} className="w-16 h-24" />
          ))}
        </div>
      </div>

      {/* Card Grid */}
      <div className="bg-green-800 rounded-lg p-4 grid grid-cols-13 gap-2">
        {fullDeck.map((code) => (
          <img
            key={code}
            src={CARD_IMAGE_URL(code)}
            alt={code}
            className={`w-12 h-18 border-2 rounded-sm cursor-pointer transition-transform hover:scale-105 ${selectedCards.includes(code) ? "opacity-50 border-red-500" : "border-transparent"}`}
            onClick={() => toggleCardSelection(code)}
          />
        ))}
      </div>

      {/* Controls */}
      <div className="mt-4 flex flex-col items-center space-y-2">
        <button onClick={resetSelection} className="bg-red-600 text-white px-4 py-2 rounded">
          Reset Selection
        </button>
        <button onClick={getRecommendation} className="bg-blue-600 text-white px-6 py-2 rounded">
          Get Recommendation
        </button>
        {recommendation && (
          <p className="text-white mt-2 text-lg">{recommendation}</p>
        )}
        {error && <p className="text-red-400 mt-2">{error}</p>}
      </div>
    </div>
  );
};

export default App;
