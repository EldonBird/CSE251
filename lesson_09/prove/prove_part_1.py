"""
Course: CSE 251
Lesson: L09 Prove Part 1
File:   prove_part_1.py
Author: <Add name here>

Purpose: Part 1 of prove 9, finding the path to the end of a maze using recursion.

Instructions:

- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.
- Complete any TODO comments.
"""

import math

from Cython.Compiler.Tests.Utils import restore_Options

from screen import Screen
from maze import Maze
import cv2
import sys

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
SLOW_SPEED = 100
FAST_SPEED = 2
speed = SLOW_SPEED

# TODO: Add any functions needed here.

def solve_path(maze):
    """ Solve the maze and return the path found between the start and end positions.
        The path is a list of positions, (x, y) """
    # TODO: Solve the maze recursively while tracking the correct path
    path = []

    (x, y) = maze.get_start_pos()
    return maze_recersion(maze, path, x, y)

    # Hint: You can create an inner function to do the recursion


def maze_recersion(maze, path, x, y):

    # we should be able to move as we only call moves if they are valid, but check anyways
    if maze.can_move_here(x, y):
        path.append((x, y))
        maze.move(x, y, 1234)
    else:
        return # basically double check just in case, but if it is problematic, just end...

    # if you are at the end, we are done and just return the path
    if maze.at_end(x, y):
        return path











def get_path(log, filename):
    """ Do not change this function """
    # 'Maze: Press "q" to quit, "1" slow drawing, "2" faster drawing, "p" to play again'
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    path = solve_path(maze)

    log.write(f'Drawing commands to solve = {screen.get_command_count()}')

    done = False
    while not done:
        if screen.play_commands(speed):
            key = cv2.waitKey(0)
            if key == ord('1'):
                speed = SLOW_SPEED
            elif key == ord('2'):
                speed = FAST_SPEED
            elif key == ord('q'):
                exit()
            elif key != ord('p'):
                done = True
        else:
            done = True

    return path


def find_paths(log):
    """ Do not change this function """

    files = (
        'very-small.bmp',
        'very-small-loops.bmp',
        'small.bmp',
        'small-loops.bmp',
        'small-odd.bmp',
        'small-open.bmp',
        'large.bmp',
        'large-loops.bmp',
        # 'large-squares.bmp',
        # 'large-open.bmp'
    )

    log.write('*' * 40)
    log.write('Part 1')
    for filename in files:
        filename = f'./mazes/{filename}'
        log.write()
        log.write(f'File: {filename}')
        path = get_path(log, filename)
        log.write(f'Found path has length     = {len(path)}')
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_paths(log)


if __name__ == "__main__":
    main()
