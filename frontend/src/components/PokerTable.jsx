import React, { useState } from 'react';
import './PokerTable.css';

const suits = ['S', 'H', 'D', 'C'];
const ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];

// For images (Deck of Cards API uses 0 for 10)
const getCardImageCode = (rank, suit) => {
  return (rank === '10' ? '0' : rank[0]) + suit;
};

const getCardUrl = (rank, suit) =>
  `https://deckofcardsapi.com/static/img/${getCardImageCode(rank, suit)}.png`;

// For backend (treys expects 'Ts', lowercase suit)
const getBackendCode = (rank, suit) => {
  const backendRank = rank === '10' ? 'T' : rank;
  return backendRank + suit.toLowerCase();
};

const PokerTable = () => {
  const [selectedCards, setSelectedCards] = useState([]); // stores {rank, suit}
  const [action, setAction] = useState('');
  const [winProb, setWinProb] = useState(null);

  const isSelected = (rank, suit) =>
    selectedCards.some(c => c.rank === rank && c.suit === suit);

  const handleCardClick = (rank, suit) => {
    const card = { rank, suit };
    const isAlreadySelected = isSelected(rank, suit);

    if (isAlreadySelected) {
      setSelectedCards(selectedCards.filter(c => !(c.rank === rank && c.suit === suit)));
    } else if (selectedCards.length < 7) {
      setSelectedCards([...selectedCards, card]);
    }
  };

  const resetSelection = () => {
    setSelectedCards([]);
    setAction('');
    setWinProb(null);
  };

  const getRecommendation = async () => {
    if (selectedCards.length !== 7) {
      alert('Please select exactly 2 hole cards and 5 community cards.');
      return;
    }

    const holeCards = selectedCards.slice(0, 2).map(c => getBackendCode(c.rank, c.suit));
    const communityCards = selectedCards.slice(2).map(c => getBackendCode(c.rank, c.suit));

    try {
      const res = await fetch('http://127.0.0.1:5000/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          holeCards: holeCards,              // 👈 use correct camelCase key
          communityCards: communityCards     // 👈 use correct camelCase key
        }),
      });

      const data = await res.json();

      if (data.error) {
        alert(data.error);
        return;
      }

      setAction(data.recommendation);
      setWinProb((data.winProbability * 100).toFixed(2));
    } catch (err) {
      console.error('Error fetching recommendation:', err);
      alert('An error occurred. See console for details.');
    }
  };

  return (
    <div className="poker-table">
      <div className="table-background">
        <div className="cards-on-table">
          {selectedCards.slice(2).map(({ rank, suit }) => (
            <img
              key={`comm-${rank}${suit}`}
              src={getCardUrl(rank, suit)}
              alt={`${rank}${suit}`}
              className="card"
            />
          ))}
        </div>
        <div className="hole-cards">
          {selectedCards.slice(0, 2).map(({ rank, suit }) => (
            <img
              key={`hole-${rank}${suit}`}
              src={getCardUrl(rank, suit)}
              alt={`${rank}${suit}`}
              className="card"
            />
          ))}
        </div>
        <div className="result">
          {action && <p><strong>Action:</strong> {action}</p>}
          {winProb !== null && <p><strong>Win Probability:</strong> {winProb}%</p>}
        </div>
      </div>

      <div className="deck-grid">
        {suits.map(suit =>
          ranks.map(rank => {
            const imageCode = getCardImageCode(rank, suit);
            const selected = isSelected(rank, suit);
            return (
              <img
                key={rank + suit}
                src={`https://deckofcardsapi.com/static/img/${imageCode}.png`}
                alt={`${rank}${suit}`}
                className={`card ${selected ? 'selected' : ''}`}
                onClick={() => handleCardClick(rank, suit)}
              />
            );
          })
        )}
      </div>

      <div className="buttons">
        <button className="reset" onClick={resetSelection}>Reset Selection</button>
        <button className="submit" onClick={getRecommendation}>Get Recommendation</button>
      </div>
    </div>
  );
};

export default PokerTable;
