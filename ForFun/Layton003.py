#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: Layton003
# Author: Mark Wang
# Date: 10/6/2016

import heapq

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


class board(object):
    def __init__(self):
        self.board_list = [0, 1, 2, 3, 7, 6, 5, 4, 8]

    def get_possible_moves(self):
        zero_index = self.board_list.index(4)
        possible_actions = [UP, DOWN, LEFT, RIGHT]
        if zero_index < 3:
            possible_actions.remove(DOWN)

        elif zero_index > 5:
            possible_actions.remove(UP)

        if zero_index % 3 == 0:
            possible_actions.remove(RIGHT)

        elif zero_index % 3 == 2:
            possible_actions.remove(LEFT)

        return possible_actions

    def get_heuristic(self, state_board=None):
        if state_board is None:
            state_board = self.board_list
        h = 0
        for i, j in enumerate(state_board):
            if i == 8 and j == 0 or i == 0 and j == 8:
                continue
            if i != j:
                h += 1

        return h

    def generate_new_state(self, action):
        if action not in self.get_possible_moves():
            return self
        else:
            zero_index = self.board_list.index(4)
            new_board = board()
            new_board_list = self.board_list[:]
            if action == UP:
                new_board_list[zero_index], new_board_list[zero_index + 3] = new_board_list[zero_index + 3], \
                                                                             new_board_list[zero_index]
            elif action == DOWN:
                new_board_list[zero_index], new_board_list[zero_index - 3] = new_board_list[zero_index - 3], \
                                                                             new_board_list[zero_index]
            elif action == RIGHT:
                new_board_list[zero_index], new_board_list[zero_index - 1] = new_board_list[zero_index - 1], \
                                                                             new_board_list[zero_index]
            else:

                new_board_list[zero_index], new_board_list[zero_index + 1] = new_board_list[zero_index + 1], \
                                                                             new_board_list[zero_index]
            new_board.board_list = new_board_list

            return new_board

    def __hash__(self):
        return str(self.board_list).__hash__()


def find_possible_result():
    state_list = []
    start_board = board()
    start_state = (start_board.get_heuristic(), start_board, [])
    heapq.heappush(state_list, start_state)
    while state_list:
        frontier = heapq.heappop(state_list)
        possible_moves = frontier[1].get_possible_moves()
        for action in possible_moves:
            new_board = frontier[1].generate_new_state(action)
            new_path = frontier[2][:]
            new_path.append(action)
            if new_board.get_heuristic() <= 0.1:
                return new_path
            new_state = (len(new_path) + new_board.get_heuristic(), new_board, new_path)
            heapq.heappush(state_list, new_state)


def find_possible_result_ucs():
    state_list = []
    start_board = board()
    start_state = (0, start_board, [])
    heapq.heappush(state_list, start_state)
    explored_state = set()
    explored_state.add(start_board)
    while state_list:
        frontier = heapq.heappop(state_list)
        possible_actions = frontier[1].get_possible_moves()
        for action in possible_actions:
            new_board = frontier[1].generate_new_state(action)
            if new_board in explored_state:
                continue
            else:
                explored_state.add(new_board)
            new_path = frontier[2][:]
            new_path.append(action)
            if new_board.get_heuristic() <= 0.1:
                return new_path
            new_state = (frontier[0] + 1, new_board, new_path)
            heapq.heappush(state_list, new_state)


if __name__ == '__main__':
    print find_possible_result_ucs()
