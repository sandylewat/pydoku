import math


class SudokuSolverBase(object):
    def name(self):
        raise NotImplementedError
    
    def __init__(self, puzzle):
        self.puzzle = []
        self.degree = int(math.sqrt(len(puzzle)))
        self.side = self.degree * self.degree
        self.column_check = [[True for i in range(self.side + 1)] for j in range(self.side)]
        self.row_check = [[True for i in range(self.side + 1)] for j in range(self.side)]
        self.box_check = [[True for i in range(self.side + 1)] for j in range(self.side)]
        self.init_puzzle(puzzle)

    def init_puzzle(self, puzzle):
        for i in range(self.side):
            self.puzzle.append([])
            for j in range(self.side):
                val = puzzle[i][j]
                self.puzzle[i].append(val)
                self.set_validity(i, j, val, False)

    def is_valid(self, i, j, val):
        return self.column_check[i][val] \
               and self.row_check[j][val] \
               and self.box_check[(i / self.degree) * self.degree + j / self.degree][val]

    def set_val(self, i, j, val):
        old_val = self.puzzle[i][j]
        self.set_validity(i, j, old_val, True)
        self.puzzle[i][j] = val
        self.set_validity(i, j, val, False)

    def set_validity(self, i, j, val, is_valid):
        self.column_check[i][val] = is_valid
        self.row_check[j][val] = is_valid
        self.box_check[(i / self.degree) * self.degree + j / self.degree][val] = is_valid

    def solve(self):
        raise NotImplementedError


class BruteForce(SudokuSolverBase):
    def name(self):
        return "BruteForce"
    
    def init_puzzle(self, puzzle):
        self.target = []
        self.puzzle = [[0 for i in range(self.side)] for i in range(self.side)]
        for i in range(self.side):
            self.target.append([])
            for j in range(self.side):
                self.target[i].append(puzzle[i][j])

    def solve(self):
        return self.__find_solution(0, 0), self.puzzle

    def __find_solution(self, i, j):
        ni = i
        nj = (j + 1) % self.side
        if nj == 0:
            ni = (i + 1) % self.side
        val = 1
        while val < self.side + 1:
            if self.is_valid(i, j, val):
                self.set_val(i, j, val)
                if (ni == 0 and nj == 0) or self.__find_solution(ni, nj):
                    # Solution Found
                    # No more empty cells
                    # or next recursion is True
                    if self.__match_target():
                        return True
                    self.set_val(i, j, 0)
                    return False
                else:
                    self.set_val(i, j, 0)
            val += 1
        if val > self.side:
            return False

    def __match_target(self):
        for i in range(self.side):
            for j in range(self.side):
                if self.target[i][j] != 0 and self.target[i][j] != self.puzzle[i][j]:
                    return False
        return True

    def find_all_solution(self, i, j, solution_array):
        ni = i
        nj = (j + 1) % self.side
        if nj == 0:
            ni = (i + 1) % self.side
        val = 1
        while val < self.side + 1:
            if self.is_valid(i, j, val):
                self.set_val(i, j, val)
                if (ni == 0 and nj == 0) or self.find_all_solution(ni, nj, solution_array):
                    # A Solution Found
                    # Save to array
                    solution_array.append([row[:] for row in self.puzzle])
                    # never acknowledge as solution
                    self.set_val(i, j, 0)
                    return False
                else:
                    self.set_val(i, j, 0)
            val += 1
        if val > self.side:
            return False


class Backtrack(SudokuSolverBase):
    def name(self):
        return "Backtrack"

    def solve(self):
        return self.__find_solution(0, 0), self.puzzle

    def __find_solution(self, i, j):
        ni = i
        nj = (j + 1) % self.side
        if nj == 0:
            ni = (i + 1) % self.side
        if self.puzzle[i][j] == 0:
            val = 1
            while val < self.side + 1:
                if self.is_valid(i, j, val):
                    self.set_val(i, j, val)
                    if (ni == 0 and nj == 0) or self.__find_solution(ni, nj):
                        # No more empty cells
                        # or next recursion is True
                        return True
                    else:
                        self.set_val(i, j, 0)
                val += 1
            if val > self.side:
                return False
        else:
            if ni == 0 and nj == 0:
                # No more empty cells, solution found
                return True
            return self.__find_solution(ni, nj)


class BranchAndBound(SudokuSolverBase):
    def name(self):
        return "Branch And Bound"

    def solve(self):
        return self.__find_solution(0, 0), self.puzzle

    def __get_next_cell(self):
        min = self.side + 1
        ni = self.side + 1
        nj = self.side + 1
        for i in range(self.side):
            for j in range(self.side):
                if self.puzzle[i][j] == 0:
                    num_possible_values = self.__count_possible_values(i, j)
                    if min > num_possible_values:
                        min = num_possible_values
                        ni = i
                        nj = j
        return ni, nj

    def __count_possible_values(self, i, j):
        counter = 0
        for k in range(1, self.side + 1):
            if self.column_check[i][k] \
                    and self.row_check[j][k] \
                    and self.box_check[(i / self.degree) * self.degree + j / self.degree]:
                counter += 1
        return counter

    def __get_possible_values(self, i, j):
        values = []
        for k in range(1, self.side + 1):
            if self.column_check[i][k] \
                    and self.row_check[j][k] \
                    and self.box_check[(i / self.degree) * self.degree + j / self.degree][k]:
                values.append(k)
        return values

    def __find_solution(self, i, j):
        if self.puzzle[i][j] == 0:
            possible_values = self.__get_possible_values(i, j)
            for val in possible_values:
                self.set_val(i, j, val)
                ni, nj = self.__get_next_cell()
                if (ni == self.side + 1 and nj == self.side + 1) or self.__find_solution(ni, nj):
                    # No more empty cells
                    # or next recursion is True
                    return True
                else:
                    self.set_val(i, j, 0)
            return False
        else:
            ni, nj = self.__get_next_cell()
            if ni == self.side + 1 and nj == self.side + 1:
                # No more empty cells, solution found
                return True
            return self.__find_solution(ni, nj)