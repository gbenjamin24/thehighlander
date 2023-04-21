// frontend/src/components/GameCard.js
import React from 'react';
import { Card } from 'react-bootstrap';
import './GameCard.css';

const GameCard = ({ game, onClick }) => {
  const {
    home_team: { name: homeTeamName, logo_url: homeTeamLogo },
    away_team: { name: awayTeamName, logo_url: awayTeamLogo },
    date,
  } = game;

  const gameDate = new Date(date);
  const humanFriendlyDate = gameDate.toLocaleString('en-US', {
    weekday: 'short',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <Card className="game-card" onClick={onClick}>
      <Card.Body>
        <div className="team">
          <img src={homeTeamLogo} alt={homeTeamName} />
          <span>{homeTeamName}</span>
        </div>
        <div className="team">
          <img src={awayTeamLogo} alt={awayTeamName} />
          <span>{awayTeamName}</span>
        </div>
        <hr />
        <Card.Text>{humanFriendlyDate}</Card.Text>
      </Card.Body>
    </Card>
  );
};

export default GameCard;
