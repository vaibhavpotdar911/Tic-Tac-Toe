#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system

USER = -1
COMPUTER = +1
game_board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

def evaluate(state):
    if wins(state, COMPUTER):
        score = +1
    elif wins(state, USER):
        score = -1
    else:
        score = 0

    return score

def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False

def game_over(state):
    return wins(state, USER) or wins(state, COMPUTER)

def empty_cells(state):
    cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells

def valid_move(x, y):
    if [x, y] in empty_cells(game_board):
        return True
    else:
        return False

def set_move(x, y, player):
    if valid_move(x, y):
        game_board[x][y] = player
        return True
    else:
        return False

def minimax_algorithm(state, depth, player):
    if player == COMPUTER:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax_algorithm(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMPUTER:
            if score[2] > best[2]:
                best = score  # high value
        else:
            if score[2] < best[2]:
                best = score  # low value
    return best

def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')

def render(state, computer_choice, user_choice):
    chars = {
        -1: user_choice,
        +1: computer_choice,
        0: ' '
    }
    str_line = '---------'
    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'|{symbol}|', end='')
        print('\n' + str_line)

def ai_turn(computer_choice, user_choice):
    depth = len(empty_cells(game_board))
    if depth == 0 or game_over(game_board):
        return
    clean()
    print(f'Computer turn [{computer_choice}]')
    render(game_board, computer_choice, user_choice)
    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax_algorithm(game_board, depth, COMPUTER)
        x, y = move[0], move[1]
    set_move(x, y, COMPUTER)
    time.sleep(1)

def user_turn(computer_choice, user_choice):
    depth = len(empty_cells(game_board))
    if depth == 0 or game_over(game_board):
        return
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }
    clean()
    print(f'Users turn [{user_choice}]')
    render(game_board, computer_choice, user_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numbers from 1 to 9:'))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], USER)

            if not can_move:
                print('Incorrect move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Exiting! Bye.')
            exit()
        except (KeyError, ValueError):
            print('Incorrect move')

def main():
    clean()
    user_choice = ''
    computer_choice = ''
    first = ''
    while user_choice != 'O' and user_choice != 'X':
        try:
            print('')
            user_choice = input('Choose X or O \n Chosen: ').upper()

        except (EOFError, KeyboardInterrupt):
            print('Exiting! Bye.')
            exit()
        except (KeyError, ValueError):
            print('Incorrect choice')

    if user_choice == 'X':
        computer_choice = 'O'
    else:
        computer_choice = 'X'
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('Do you want to start first? Y/N?: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Exiting! Bye.')
            exit()
        except (KeyError, ValueError):
            print("Incorrect choice")

    while len(empty_cells(game_board)) > 0 and not game_over(game_board):
        if first == 'N':
            ai_turn(computer_choice, user_choice)
            first = ''
        user_turn(computer_choice, user_choice)
        ai_turn(computer_choice, user_choice)

    if wins(game_board, USER):
        clean()
        print(f'User turn [{user_choice}]')
        render(game_board, computer_choice, user_choice)
        print('User wins!')
    elif wins(game_board, COMPUTER):
        clean()
        print(f'Computer turn [{computer_choice}]')
        render(game_board, computer_choice, user_choice)
        print('Computer wins!')
    else:
        clean()
        render(game_board, computer_choice, user_choice)
        print('Game is DRAW')
    exit()

if __name__ == '__main__':
    main()