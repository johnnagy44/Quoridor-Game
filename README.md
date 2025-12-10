# Quoridor Game

A Python implementation of the Quoridor board game using PyQt6 for the graphical user interface.

## Description

Quoridor is a strategic board game where players race to be the first to reach the opposite side of the board while placing walls to block opponents. This implementation features a modern neon-themed UI and supports both human and AI players.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

### Method 1: Using Virtual Environment (Recommended)

1. **Clone or navigate to the project directory:**

   ```
   cd Quoridor-Game
   ```

2. **Create a virtual environment:**

   - On Windows:
     ```
     python -m venv venv
     ```
   - On macOS/Linux:
     ```
     python3 -m venv venv
     ```

3. **Activate the virtual environment:**

   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

### Method 2: Without Virtual Environment

1. **Navigate to the project directory:**

   ```
   cd Quoridor-Game
   ```

2. **Install the required dependencies globally:**
   ```
   pip install -r requirements.txt
   ```
   > **Note:** Installing packages globally may require administrator privileges and can potentially conflict with other Python projects. Using a virtual environment is recommended.

## Running the Application

1. **Ensure you're in the project directory:**

   ```
   cd Quoridor-Game
   ```

2. **If using virtual environment, activate it (if not already activated):**

   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. **Run the application:**
   ```
   python main.py
   ```

The Quoridor game window should open, allowing you to start playing or access the settings menu.

## Features

- Neon-themed graphical user interface
- Support for human vs human gameplay
- AI player integration (configurable in settings)
- Wall placement mechanics
- Undo functionality
- Customizable board size (default 9x9)

## Project Structure

- `main.py`: Application entry point
- `game/`: Core game logic (board, players, rules, pathfinding)
- `ui/`: User interface components (PyQt6 widgets)
- `ai/`: AI player implementation
- `tests/`: Unit tests
- `requirements.txt`: Python dependencies

## Contributing

Feel free to submit issues and pull requests to improve the game.

## License

This project is open-source.
