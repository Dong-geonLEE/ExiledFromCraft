############################################################
#S---????   S: Start                0  1  2  3  4  5  6  7
#-X-X????   X: 금지                  8  9  10 11 12 13 14 15
#---X????   ?: Random state         16 17 18 19 20 21 22 23
#X---????   #: Outer                24 25 26 27 28 29 30 31
#????????                           32 33 34 35 36 37 38 39
#????????                           40 41 42 43 44 45 46 47
#????????                           48 49 50 51 52 53 54 55
#????????                           56 57 58 59 60 61 62 63
#############################################################

import random as rd

from pprint import pprint

"""
LEFT: -1
DOWN: +8
RIGHT: +1
UP: -8
"""

left_wall = [0, 8, 16, 24, 32, 40, 48, 56]
down_wall = [56, 57, 58, 59, 60, 61, 62, 63]
right_wall = [7, 15, 23, 31, 39, 47, 55, 63]
up_wall = [0, 1, 2, 3, 4, 5, 6, 7]

def get_transition_tuple(Grid, next_state, left_next, right_next):
    if Grid[next_state][0] == 'X':
        next = (0.33333, next_state, -1.0, True)

    else: next = (0.33333, next_state, 0.0, False)

    if Grid[left_next][0] == 'X':
        left = (0.33333, left_next, -1.0, True)

    else: left = (0.33333, left_next, 0.0, False)

    if Grid[right_next][0] == 'X':
        right = (0.33333, right_next, -1.0, True)

    else: right = (0.33333, right_next, 0.0, False)

    return [next, left, right]

def make_transition(Grid: dict, state: int):
    if Grid[state][0] in ['X', 'G']:
        T_tup = [(1.0, state, 0, True)]
        Grid[state][1][0] = T_tup
        Grid[state][1][1] = T_tup
        Grid[state][1][2] = T_tup
        Grid[state][1][3] = T_tup

    else:
        # LEFT
        if state == 0:
            next_state = state
            left_next = state + 8
            right_next = state

        elif state == 56:
            next_state = state
            left_next = state
            right_next = state - 8

        elif state in left_wall:
            next_state = state
            left_next = state + 8
            right_next = state - 8

        elif state in up_wall:
            next_state = state - 1
            left_next = state + 8
            right_next = state

        elif state in down_wall:
            next_state = state - 1
            left_next = state
            right_next = state - 8

        else:
            next_state = state - 1
            left_next = state + 8
            right_next = state - 8

        Grid[state][1][0] = get_transition_tuple(Grid, next_state, left_next, right_next)

        # DOWN

        if state == 63:
            next_state = state
            left_next = state - 1
            right_next = state

        elif state == 56:
            next_state = state
            left_next = state
            right_next = state + 1

        elif state in down_wall:
            next_state = state
            left_next = state - 1
            right_next = state - 1

        elif state in left_wall:
            next_state = state + 8
            left_next = state
            right_next = state + 1

        elif state in right_wall:
            next_state = state + 8
            left_next = state - 1
            right_next = state

        else:
            next_state = state + 8
            left_next = state - 1
            right_next = state + 1

        Grid[state][1][1] = get_transition_tuple(Grid, next_state, left_next, right_next)

        # RIGHT

        if state == 7:
            next_state = state
            left_next = state
            right_next = state + 8

        elif state == 63:
            next_state = state
            left_next = state - 8
            right_next = state

        elif state in right_wall:
            next_state = state
            left_next = state - 8
            right_next = state + 8

        elif state in up_wall:
            next_state = state + 1
            left_next = state
            right_next = state + 8

        elif state in down_wall:
            next_state = state + 1
            left_next = state - 8
            right_next = state

        else:
            next_state = state + 1
            left_next = state - 8
            right_next = state + 8

        Grid[state][1][2] = get_transition_tuple(Grid, next_state, left_next, right_next)

        # UP

        if state == 7:
            next_state = state
            left_next = state - 1
            right_next = state

        elif state == 0:
            next_state = state
            left_next = state
            right_next = state + 1

        elif state in up_wall:
            next_state = state
            left_next = state - 1
            right_next = state + 1

        elif state in left_wall:
            next_state = state - 8
            left_next = state
            right_next = state + 1

        elif state in right_wall:
            next_state = state - 8
            left_next = state - 1
            right_next = state

        else:
            next_state = state - 8
            left_next = state - 1
            right_next = state + 1

        Grid[state][1][3] = get_transition_tuple(Grid, next_state, left_next, right_next)

def creaft_8x8_frozen_lake_grid():
    FrozenLakeGrid8x8_Basic = {}

    for i in range(64):
        FrozenLakeGrid8x8_Basic[i] = ('state', {})

    FrozenLakeGrid8x8_Basic[0] = ('S', {})
    FrozenLakeGrid8x8_Basic[1] = ('-', {})
    FrozenLakeGrid8x8_Basic[2] = ('-', {})
    FrozenLakeGrid8x8_Basic[3] = ('-', {})
    FrozenLakeGrid8x8_Basic[8] = ('-', {})
    FrozenLakeGrid8x8_Basic[9] = ('X', {})
    FrozenLakeGrid8x8_Basic[10] = ('-', {})
    FrozenLakeGrid8x8_Basic[11] = ('X', {})
    FrozenLakeGrid8x8_Basic[16] = ('-', {})
    FrozenLakeGrid8x8_Basic[17] = ('-', {})
    FrozenLakeGrid8x8_Basic[18] = ('-', {})
    FrozenLakeGrid8x8_Basic[19] = ('X', {})
    FrozenLakeGrid8x8_Basic[24] = ('X', {})
    FrozenLakeGrid8x8_Basic[25] = ('-', {})
    FrozenLakeGrid8x8_Basic[26] = ('-', {})
    FrozenLakeGrid8x8_Basic[27] = ('-', {})

    sector1 = [4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23, 28, 29, 30, 31]
    sector2 = [32, 33, 34, 35, 40, 41, 42, 43, 48, 49, 50, 51, 56, 57, 58, 59]
    sector3 = [36, 37, 38, 39, 44, 45, 46, 47, 52, 53, 54, 55, 60, 61, 62, 63]

    goal = rd.choice(sector3)

    FrozenLakeGrid8x8_Basic[goal] = ('G', {})

    sector3.remove(goal)

    num_X = 5

    for s in [sector1, sector2, sector3]:
        holes = rd.choices(population=s, k=num_X)

        for h in holes:
            FrozenLakeGrid8x8_Basic[h] = ('X', {})

    for i in FrozenLakeGrid8x8_Basic:
        if FrozenLakeGrid8x8_Basic[i][0] == 'state':
            FrozenLakeGrid8x8_Basic[i] = ('-', {})

    for i in range(64):
        make_transition(FrozenLakeGrid8x8_Basic, state=i)

    map = ''

    for i in FrozenLakeGrid8x8_Basic:
        map = map + FrozenLakeGrid8x8_Basic[i][0]
        if i in right_wall:
            map += '\n'

    return FrozenLakeGrid8x8_Basic, goal, map



_, _, _ = creaft_8x8_frozen_lake_grid()