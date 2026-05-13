# Tic-Tac-Toe AI

A modern Python Flask Tic-Tac-Toe web game featuring a Minimax-powered AI opponent with alpha-beta pruning. The game runs in the browser, works on PC and mobile, and includes multiple difficulty levels, score tracking, smooth animations, and a clean responsive interface.

## Description

**Tic-Tac-Toe AI** is a Python Flask web application where players can play Tic-Tac-Toe against an AI opponent or another human player locally.

The AI uses the **Minimax algorithm** with **alpha-beta pruning** on hard difficulty, allowing it to calculate the best possible move and play optimally. The project also includes easier difficulty modes where the AI makes random or semi-random moves, making the game more playable for casual users.

The frontend is built with HTML, CSS, and JavaScript, while the backend handles AI move calculation through a Flask API route.

## Features

- Play against AI
- Play against another human locally
- Three AI difficulty levels:
  - Easy
  - Medium
  - Hard
- Hard difficulty uses Minimax AI
- Alpha-beta pruning for optimized AI decisions
- Score tracking for X, O, and draws
- Animated game board
- Win highlighting
- Confetti effect on player victory
- AI thinking indicator
- Responsive design for PC and mobile
- Flask backend API
- Clean dark-themed UI

## Built With

- Python
- Flask
- HTML
- CSS
- JavaScript
- Minimax Algorithm
- Alpha-Beta Pruning

## How It Works

The game board is stored as a 3x3 grid. When the player makes a move, the frontend sends the current board state to the Flask backend through the `/ai_move` API route.

The backend checks the selected difficulty and decides the AI move:

- **Easy:** chooses a random available move
- **Medium:** sometimes chooses a random move and sometimes plays smart
- **Hard:** uses the Minimax algorithm with alpha-beta pruning to find the best possible move

After the backend returns the chosen move, the frontend updates the board and checks for a win, draw, or next turn.

## AI Logic

The AI plays as **O**, while the player plays as **X**.

On hard mode, the AI evaluates all possible future game states using Minimax:

- Winning as O gives a positive score
- Winning as X gives a negative score
- A draw gives a neutral score
- Alpha-beta pruning skips unnecessary branches to improve performance

This makes the hard AI extremely difficult to beat.

## Installation

Clone the repository:

```bash
git clone https://github.com/Zzcyper/tic-tac-toe-ai.git
cd tic-tac-toe-ai
