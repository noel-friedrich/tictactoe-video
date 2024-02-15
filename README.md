# TicTacToe Video  
> This is the repository for the source code used to make [a YouTube video](https://www.youtube.com/watch?v=_3MtmD9EyM0&t=26s).

## Table of contents
* [About](#about)
* [How to use](#how-to-use)
* [Code Structure](#code-structure)
* [Status](#status)

## About
I made a YouTube video which you could play a game of Tic Tac Toe against. You make moves by going to specified times in the video,
where you're told what the new game state is. My code generates all Tic Tac Toe games, finds the best moves and then
generates the frames for the video to be combined into a video later.

## Code Structure

The video generation happens when you execute `main.py`. The TicTacToe board logic is entirely contained
in `board.py` while `board_generator.py` cares about counter moves and board ordering and `main.py` creates the images and saves them
to `outputs/boards/...` which you can then combine into a video using ffmpeg or similar tools.

## Status
The project is finished and the video is published on YouTube! Try beating me at the game there :)