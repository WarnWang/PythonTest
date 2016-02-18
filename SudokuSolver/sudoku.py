#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: sudoku
# Author: warn
# Date: 18/2/2016 15:41

import copy
import pprint


class Sudoku(object):
    def __init__(self, input_matrix):
        self.matrix = copy.deepcopy(input_matrix)
        self.ceil_domain = None
        self.format_matrix()
        self.get_ceil_domain()

    def get_ceil_domain(self):
        result = False
        if self.ceil_domain is None:
            self.ceil_domain = [[] for i in range(9)]

        check_list = []

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] is None:
                    self.ceil_domain[i].append(range(1, 10))
                    check_list.append((i, j))
                else:
                    self.ceil_domain[i].append([])

        while check_list:
            check_position = check_list.pop()
            if self.format_position(check_position):
                result = True
                for i in range(len(self.matrix)):
                    for j in range(len(self.matrix[j])):
                        if self.matrix[i][j] is None and (i, j) not in check_list:
                            check_list.append((i, j))

        return result

    def format_position(self, position):
        x = position[0]
        y = position[1]
        result = False
        row_range = range(9)
        row_range.remove(x)
        for i in row_range:
            if self.matrix[i][y] in self.ceil_domain[x][y]:
                self.ceil_domain[x][y].remove(self.matrix[i][y])
                result = True

        line_range = range(9)
        line_range.remove(y)
        for j in line_range:
            if self.matrix[x][j] in self.ceil_domain[x][y]:
                self.ceil_domain[x][y].remove(self.matrix[x][j])
                result = True

        grid_x = x / 3 * 3
        grid_y = y / 3 * 3
        for i in range(9):
            temp_x = grid_x + i % 3
            temp_y = grid_y + i / 3
            if temp_x == x and temp_y == y:
                continue

            if self.matrix[temp_x][temp_y] in self.ceil_domain[x][y]:
                self.ceil_domain[x][y].remove(self.matrix[temp_x][temp_y])
                result = True

        if result and len(self.ceil_domain[x][y]) == 1:
            self.matrix[x][y] = self.ceil_domain[x][y].pop()

        return result

    def format_matrix(self):
        for i in self.matrix:
            for j in range(len(i)):
                if i[j] is None or i[j] not in range(1, 10):
                    i[j] = None

    def display_board(self):
        for i in self.matrix:
            s = ""
            for j in i:
                if j is None:
                    s = "%s\t0" % s
                else:
                    s = "%s\t%s" % (s, j)

            print s

    def count(self):
        result = 0
        for i in self.matrix:
            for j in i:
                if isinstance(j, int) and j in range(1, 10):
                    result += 1

        return result

    def grid_formulation(self):
        result = False
        for i in range(9):
            result |= self.check_grid(i)

        return result

    def check_grid(self, grid_index):
        result = False
        start_x = grid_index / 3 * 3
        start_y = grid_index % 3 * 3
        number_list = [[] for i in range(9)]
        for i in range(9):
            temp_x = start_x + i / 3
            temp_y = start_y + i % 3
            if self.matrix[temp_x][temp_y] is None:
                for j in self.ceil_domain[temp_x][temp_y]:
                    number_list[j - 1].append((temp_x, temp_y))

        for i in range(len(number_list)):
            if len(number_list[i]) == 1:
                position = number_list[i].pop()
                self.matrix[position[0]][position[1]] = i + 1
                self.ceil_domain[position[0]][position[1]] = []
                result = True
        return result

    def solver(self, keep_on=False):
        self.display_board()
        temp = True
        while temp:
            temp = self.grid_formulation() | self.get_ceil_domain()
            print self.count()
            if self.count() == 81:
                break

        self.display_board()
        if self.count() != 81 and keep_on:
            for i in range(9):
                for j in range(9):
                    if len(self.ceil_domain[i][j]) > 1:
                        for k in self.ceil_domain[i][j]:
                            temp_matrix = copy.deepcopy(self.matrix)
                            temp_matrix[i][j] = k
                            new_solver = Sudoku(temp_matrix)
                            new_solver.solver()
                            if new_solver.count() == 81:
                                self.matrix = copy.deepcopy(new_solver.matrix)
                                self.display_board()
                                return


if __name__ == "__main__":
    input_matrix = [[1, 0, 0, 0, 0, 0, 8, 0, 0],
                    [0, 4, 0, 0, 8, 0, 0, 0, 0],
                    [0, 0, 9, 0, 5, 0, 0, 6, 0],
                    [0, 0, 0, 0, 0, 4, 0, 2, 0],
                    [0, 0, 3, 0, 0, 0, 0, 0, 4],
                    [0, 1, 0, 0, 0, 8, 5, 0, 0],
                    [0, 0, 8, 0, 0, 1, 6, 0, 3],
                    [2, 0, 6, 0, 0, 0, 9, 0, 0],
                    [7, 0, 0, 9, 0, 0, 0, 0, 5]]
    test = Sudoku(input_matrix)
    test.display_board()
    # pprint.pprint(test.ceil_domain)
    print test.count()
    print ""

    test.solver(True)
    print test.count()
    test.display_board()
