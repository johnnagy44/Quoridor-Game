# Quoridor Game

A Python implementation of the **Quoridor** board game using PyQt6 for the graphical user interface. Features a modern neon-themed UI, support for human vs AI gameplay, and strategic board mechanics.

## 📋 Table of Contents

- [Game Description](#game-description)
- [Screenshots](#screenshots)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Game Controls](#game-controls)
- [Features](#features)
- [Demo Video](#demo-video)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## 🎮 Game Description

Quoridor is a strategic board game where two players race to reach the opposite side of a 9×9 grid while placing walls to block their opponent's path.

### Objective

- **Player 1 (Cyan):** Start at the bottom center and reach the top row
- **Player 2 (Magenta):** Start at the top center and reach the bottom row
- First player to reach the opposite side wins!

### Core Mechanics

**Player Movement:**

- Move your pawn one square in any cardinal direction (up, down, left, right)
- Jump over adjacent opponents (if you can move through)
- Move diagonally around blocked opponents

**Wall Placement:**

- Each player starts with 10 walls
- Walls span two adjacent cells (horizontal or vertical)
- Walls cannot overlap
- Walls cannot completely block a player's path to their goal
- Place walls strategically to slow down your opponent

**Turn Structure:**

- Players alternate turns
- Each turn: move your pawn OR place a wall
- The game continues until one player reaches their goal

## 📸 Screenshots

### Main Menu

<img src="ui/assets/screenshots/main_menu.png" width="600" alt="Main Menu">

_The welcoming main menu with options for New Game, How to Play, Settings, and Exit_

### Game Setup

<img src="ui/assets/screenshots/setup_screen.png" width="600" alt="Setup Screen">

_Configure players, AI difficulty, board size, and time limits before starting_

### Active Gameplay

<img src="ui/assets/screenshots/gameplay.png" width="600" alt="Gameplay Board">

_Neon-themed game board with player positions, available walls, and turn indicator_

### Game Over Screen

<img src="ui/assets/screenshots/victory_screen.png" width="600" alt="Victory Screen">

_Celebration screen when a player reaches the opposite side_

## 📦 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🔧 Installation

### Method 1: Using Virtual Environment (Recommended)

1. **Clone or navigate to the project directory:**

   ```bash
   cd Quoridor-Game
   ```

2. **Create a virtual environment:**

   - On Windows:
     ```bash
     python -m venv venv
     ```
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     ```

3. **Activate the virtual environment:**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Method 2: Without Virtual Environment

1. **Navigate to the project directory:**

   ```bash
   cd Quoridor-Game
   ```

2. **Install the required dependencies globally:**
   ```bash
   pip install -r requirements.txt
   ```
   > **Note:** Installing packages globally may require administrator privileges and can potentially conflict with other Python projects. Using a virtual environment is recommended.

## 🚀 Running the Application

1. **Ensure you're in the project directory:**

   ```bash
   cd Quoridor-Game
   ```

2. **If using virtual environment, activate it (if not already activated):**

   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. **Run the application:**
   ```bash
   python main.py
   ```

The Quoridor game window should open, displaying the main menu.

## 🎮 Game Controls

### Main Menu

- **New Game**: Click to configure and start a new game
- **How to Play**: View detailed rules and strategy tips
- **Settings**: Customize game preferences and default settings
- **Exit**: Close the application

### Game Setup Screen

- **Player Names**: Enter custom names for both players
- **AI Opponent**: Toggle to enable/disable AI player for Player 2
- **AI Difficulty**: Select from Easy, Medium, or Hard difficulty levels
- **Board Size**: Choose from 9×9, 11×11, or 13×13 grids
- **Time Limit**: Set optional time limit per move (0 for unlimited)
- **Start Game**: Begin the match with selected settings

### During Gameplay

**Pawn Movement:**

- **Left Click** on an empty cell to move your pawn there
- Your pawn can only move to legally adjacent squares
- Valid moves are highlighted on hover

**Wall Placement:**

- **Right Click** near the grid lines between cells to preview wall placement
- Wall previews appear in semi-transparent pink
- Release to place the wall if it's valid
- Invalid placements flash red and are rejected

**Game Actions:**

- **Reset**: Clear the board and start a new game with same settings
- **Menu**: Return to the main menu (ends current game)

### Turn Indicator

- **Bottom Bar** displays whose turn it is
- Player colors: Cyan (Player 1) and Magenta (Player 2)
- AI players show "thinking..." status during move calculation

### Player Info Cards

- **Left/Right sides** show player names and remaining walls
- **Current goal** displayed for reference
- Updates in real-time as walls are placed

## ✨ Features

- **Neon-Themed UI**: Modern cyan and magenta neon aesthetic
- **Human vs Human**: Play with another person locally
- **Human vs AI**: Challenge the computer with three difficulty levels:
  - Easy: Shallow 1-level minimax search
  - Medium: 2-level minimax search
  - Hard: 3-level minimax search with alpha-beta pruning
- **Responsive Board**: Dynamically scales to window size
- **Wall Validation**: Ensures no player is completely blocked from their goal
- **Customizable Games**: Adjust board size, player names, and time limits
- **Settings Panel**: Save preferences for sound, move hints, and animations
- **How to Play**: In-game guide with rules and strategy tips
- **Real-time Feedback**: Wall placement preview and invalid move indicators

## 🎥 Demo Video

[Watch the Quoridor Game Demo](https://youtube.com/path-to-demo)
_See the game in action with AI vs human gameplay_


## 📁 Project Structure

```
Quoridor-Game/
├── main.py                 # Application entry point
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── game/                  # Core game logic
│   ├── board.py          # Board state and wall management
│   ├── game_state.py     # Game state and move validation
│   ├── player.py         # Player class definition
│   ├── rules.py          # Game rules and legal moves
│   └── pathfinding.py    # BFS pathfinding for wall validation
├── ai/                    # AI player implementation
│   └── ai.py            # Minimax algorithm with alpha-beta pruning
├── ui/                    # User interface components
│   ├── main_window.py    # Main window container
│   ├── main_menu.py      # Main menu screen
│   ├── setup_window.py   # Game setup screen
│   ├── game_window.py    # Main gameplay screen
│   ├── board_widget.py   # Interactive game board
│   ├── settings_window.py # Settings panel
│   ├── how_to_play_window.py # Rules and help screen
│   └── assets/           # Images, fonts, and stylesheets
│       ├── quoridor_neon.qss      # Neon theme stylesheet
│       ├── background.jpg         # UI background image
│       ├── fonts/                 # Custom fonts
│       └── icons/                 # Button icons
└── tests/                 # Unit tests
    └── test_board.py     # Board logic tests
```

## 🎯 Game Rules Summary

1. **Setup**: Place pawns at opposite centers, each player gets 10 walls
2. **Turn**: Player either moves pawn one square OR places one wall
3. **Movement**: Pawn moves to adjacent empty square (with jump rules)
4. **Walls**: Block adjacent cells; cannot completely trap a player
5. **Win**: First to reach opposite side of board wins

## 🤝 Contributing

Feel free to submit issues and pull requests to improve the game. Contributions are welcome!

## 📄 License

This project is open-source and available under the MIT License.
