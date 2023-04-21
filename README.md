# The Highlander

The Highlander is a web app that lets users bet on basketball games. It uses Flask as the backend and React with React-Bootstrap for the frontend. Users can browse upcoming games, and the app will suggest a team to bet on.

## Features

- Browse upcoming basketball games in a modern, horizontally-scrollable interface.
- Click on a game to get a suggested team to bet on.
- Clear and minimal design.

## Installation

To run/develop on the Highlander locally, follow these steps:

1. Clone the repository:

```
bash
git clone https://github.com/gbenjamin24/thehighlander.git
cd thehighlander
```

2. Setup the backend
```
./setup_venv.sh
```

3. Set up the frontend:
```
cd frontend
npm install
```

4. Create an .env file in the thehighlander directory

5. The app is currently configured to run on port 2121 with
```
docker-compose build
docker-compose up -d
```
