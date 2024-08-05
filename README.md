# Ethan's Wordle (Hard Edition)

### Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Technologies Used](#technologies-used)
6. [Challenges and Solutions](#challenges-and-solutions)
7. [Future Improvements](#future-improvements)
8. [Contact](#contact)

## 1. Introduction

**Ethan's Wordle (Hard Edition)** is a Python-based game inspired by the popular New York Times game 'Wordle'. This project, which started as a simple text-based game, evolved into a full-fledged GUI application using Tkinter and integrates API calls for enhanced functionality.

### Motivation

I created this project to challenge myself by replicating the logic of Wordle and expanding my skills in Python and GUI development. This project also helped me learn how to integrate APIs and handle errors effectively.

## 2. Features

- **Random Word Generation**: Utilizes the Random Word API to generate a new target word for each game.
- **Word Definition Display**: Provides the definition of the target word upon winning or losing, using the Merriam-Webster Dictionary API.
- **Error Handling for Invalid Inputs**: Checks if the user’s guess is a valid word and ensures it is exactly 5 characters long, providing feedback for invalid inputs.
- **On-Screen Keyboard**: Allows users to select letters via an on-screen keyboard and displays the selected letters in real-time.
- **Color-Coded Feedback**: Updates the background colors of the letters in the grid to indicate correct letters in the correct spot (green), correct letters in the wrong spot (yellow), and incorrect letters (grey).
- **Play Again or Exit Options**: Provides the option to play again or exit the game upon completion.

## 3. Installation

### Prerequisites

- Python 3.x installed on your machine

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/username/project-name.git
