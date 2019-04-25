#!/usr/bin/python

import pygame
import random

from Game import Game

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""



def convert_shape_format(shape):
    positions = []
    # finds current shape
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            # if 0 exists, add that to position
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        # fixes offset on screen so it can be displayed better
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    # converts above list: [[(0, 1)], [(2, 3)]] -> [(0, 1), (2, 3)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            # check if in grid
            if pos[1] > -1:
                return False
    return True


def valid_space2(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    # converts above list: [[(0, 1)], [(2, 3)]] -> [(0, 1), (2, 3)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            # check if in grid
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


# noinspection PyBroadException
def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        # checks if black squares on row
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            # gets every position in row
            for j in range(len(row)):
                try:
                    # removes color row from grid
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        # sorts list: [(0, 1), (0, 0)] -> [(0, 0), (0, 1)]
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            # everything above 'y' row will be moved down
            if y < ind:
                # shifts everything from above row to a new lower row
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)

    return inc


# noinspection PyBroadException
def clear_rows2(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        # checks if black squares on row
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            # gets every position in row
            for j in range(len(row)):
                try:
                    # removes color row from grid
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        # sorts list: [(0, 1), (0, 0)] -> [(0, 0), (0, 1)]
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            # everything above 'y' row will be moved down
            if y < ind:
                # shifts everything from above row to a new lower row
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)

    return inc





def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
