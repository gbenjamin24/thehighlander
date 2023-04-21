import { useState } from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import Slider from 'react-slick';
import GameCard from './components/GameCard';
import { fetchWeeklyBasketballGames, suggestTeam } from './api';
import './App.css';

function App() {
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState(null);

  const handleStartBetting = async () => {
    const fetchedGames = await fetchWeeklyBasketballGames();
    setGames(fetchedGames);
    setSelectedGame(null);
    window.scrollTo({ bottom: 0, behavior: 'smooth' });
  };

  const handleGameCardClick = async (game) => {
    const suggestedTeam = await suggestTeam(game);
    setSelectedGame({ ...game, suggestedTeam });
    window.scrollTo({ bottom: 0, behavior: 'smooth' });
  };

  // Slider settings
  const sliderSettings = {
    dots: false,
    infinite: true,
    speed: 500,
    slidesToShow: 6,
    swipeToSlide: true,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 3,
          infinite: true,
        },
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
        },
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        },
      },
    ],
  };

  return (
    <div className="App">
      <Container fluid className="bg-dark text-white min-vh-100 d-flex flex-column justify-content-center">
        <Row className="justify-content-center mb-4">
          <Col xs={12} md={8} className="text-center">
            <h1>Welcome to The Highlander</h1>
            <h2>Let's Gamble</h2>
          </Col>
        </Row>
        <Row className="justify-content-center">
          <Col xs={12} md={4} className="text-center">
            <Button variant="outline-light" size="lg" onClick={handleStartBetting}>
              Start Betting
            </Button>
          </Col>
        </Row>
        {games.length > 0 && (
          <Row className="justify-content-center">
            <Col xs={12}>
              <div className="game-cards-container">
                <Slider {...sliderSettings}>
                  {games.map((game, index) => (
                    <GameCard key={index} game={game} onClick={() => handleGameCardClick(game)} />
                  ))}
                </Slider>
              </div>
            </Col>
          </Row>
        )}
        {selectedGame && (
          <Row className="justify-content-center mb-4">
            <Col xs={12} md={8} className="text-center">
              <h3>{selectedGame.suggestedTeam}</h3>
            </Col>
          </Row>
        )}
      </Container>
    </div>
  );
}

export default App;