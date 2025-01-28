# 8-Puzzle Game

A Python-based interactive 8-puzzle game with AI solver capabilities, built using Pygame.

## Overview
The 8-puzzle game is a sliding puzzle consisting of a 3x3 grid with numbered tiles (1–8) and one empty space. The objective is to rearrange the tiles to match the goal state by sliding tiles into the empty space.

This program provides both a manual mode where users can solve the puzzle themselves and an AI mode where the puzzle is solved using the A* algorithm.

## Features
- **Interactive Gameplay**: Use arrow keys to move tiles manually.
- **Shuffle Functionality**: Press `S` to randomize the puzzle.
- **AI Solver**: Press `Space` to solve the puzzle using A* search with a Manhattan distance heuristic.
- **Timer**: Displays the time taken for the AI to solve the puzzle.
- **Animations**: Smooth tile transitions for a visually appealing experience.
- **Time Limit**: AI solver stops if it exceeds the maximum allowed time (60 seconds).

## Prerequisites
- Python 3.x
- Pygame library

## Controls
- **Arrow Keys**: Move tiles manually.
- **S**: Shuffle the puzzle.
- **Spacebar**: Solve the puzzle using AI.

## How It Works
1. **Grid Creation**: The grid is initialized as a 3x3 matrix with a random arrangement of tiles.
2. **Tile Movement**: The empty space can be moved up, down, left, or right, swapping positions with adjacent tiles.
3. **AI Solver**: The A* algorithm finds the shortest path to the goal state:
   - **Heuristic**: Manhattan distance is used to estimate the cost of reaching the goal.
   - **Priority Queue**: States are explored based on their combined cost (steps taken + heuristic value).
4. **Animations**: Smooth visual transitions enhance user experience.
