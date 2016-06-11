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
        self.zero_element = 4

    def get_possible_moves(self):
        zero_index = self.board_list.index(self.zero_element)
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
            zero_index = self.board_list.index(self.zero_element)
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

    def __eq__(self, other):
        if not isinstance(other, board):
            return False
        for i, j in zip(self.board_list, other.board_list):
            if i == 8 and j == 0 or i == 0 and j == 8:
                continue
            elif i != j:
                return False

        return True

    def __str__(self):
        str_board = map(str, self.board_list)
        return '{}\n{}\n{}'.format(', '.join(str_board[:3]), ', '.join(str_board[3:6]), ', '.join(str_board[6:9]))


def find_possible_result(start_board=None):
    state_list = []
    if start_board is None:
        start_board = board()
    start_state = (start_board.get_heuristic(), start_board, [])
    heapq.heappush(state_list, start_state)
    explored_set = set()
    explored_set.add(start_board)
    while state_list:
        frontier = heapq.heappop(state_list)
        possible_moves = frontier[1].get_possible_moves()
        for action in possible_moves:
            new_board = frontier[1].generate_new_state(action)
            if new_board in explored_set:
                continue
            else:
                explored_set.add(new_board)
            new_path = frontier[2][:]
            new_path.append(action)
            if new_board.get_heuristic() <= 1:
                print len(explored_set)
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


def find_possible_result_bfs():
    state_list = []
    state_board = board()
    start_state = (state_board, [])
    explore_state = set()
    explore_state.add(state_board)
    state_list.append(start_state)
    while state_list:
        frontier = state_list.pop(0)
        possible_actions = frontier[0].get_possible_moves()
        for action in possible_actions:
            new_board = frontier[0].generate_new_state(action)
            if new_board in explore_state:
                continue
            else:
                explore_state.add(new_board)
            new_path = frontier[1][:]
            new_path.append(action)
            if new_board.get_heuristic() < 1:
                return new_path
            new_state = (new_board, new_path)
            state_list.append(new_state)


if __name__ == '__main__':
    actions = find_possible_result()
    i = board()
    print i
    for action in actions:
        print 'actions:', action
        i = i.generate_new_state(action)
        print i
        print
