#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: layton147
# Author: Mark Wang
# Date: 11/6/2016

from Layton003 import board, find_possible_result

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


class NewBoard(board):
    def __init__(self):
        board.__init__(self)
        self.board_list = [4, 6, 5, 0, 8, 3, 2, 1, 7]
        self.zero_element = 8

    def __eq__(self, other):
        if not isinstance(other, NewBoard):
            return False
        for i, j in zip(self.board_list, other.board_list):
            if i != j:
                return False

        return True

    def get_heuristic(self, state_board=None):
        if state_board is None:
            state_board = self.board_list
        h = 0
        for i, j in enumerate(state_board):
            if i != j:
                h += 1

        return h

    def generate_new_state(self, action):
        if action not in self.get_possible_moves():
            return self
        else:
            zero_index = self.board_list.index(self.zero_element)
            new_board = NewBoard()
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


if __name__ == '__main__':
    actions = find_possible_result(NewBoard())
    i = NewBoard()
    print i
    for action in actions:
        print 'actions:', action
        i = i.generate_new_state(action)
        print i
        print
