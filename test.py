import time
import math
from sudoku_solver import BruteForce, Backtrack, BranchAndBound

PROBLEM_SETS = ["easy50.txt", "hardest.txt"]


class Util(object):
    @staticmethod
    def read_file(file_name, sep='\n'):
        return file(file_name).read().strip().split(sep)

    @staticmethod
    def array_to_puzzle(string_array):
        length = len(string_array)
        side = int(math.sqrt(length))
        if length != side*side and side in [4, 81]:
            raise Exception("String should have exact length of 4 or 81")
        puzzle = []
        for i in range(side):
            puzzle.append([])
            for j in range(side):
                char = string_array[i*side+j]
                if char not in "0123456789":
                    raise Exception("Invalid character " + char + " at (" + `i` + ", " + `j` + ")")
                puzzle[i].append(int(char))
        return puzzle


if __name__ == '__main__':
    solvers = ["Backtrack", "BranchAndBound"]

    for file_name in PROBLEM_SETS:
        with open('%s' % file_name, 'r') as sets:
            str_set = sets.read().strip().split('\n')
            puzzle_set = []
            for str_puzzle in str_set:
                puzzle_set.append(Util.array_to_puzzle(str_puzzle))
            for solver in solvers:
                length = len(puzzle_set)
                time_records = []
                total_time = 0
                for puzzle in puzzle_set:
                    duration = time.clock()
                    sudoku_solver_instance = globals()[solver](puzzle)
                    sudoku_solver_instance.solve()
                    duration = time.clock() - duration
                    time_records.append(duration)
                    total_time += duration
                average = float(total_time/length)

                output_file = open(solver + " " + file_name, "w")
                output_file.write("average = " + `average` + '\n')
                for time_record in time_records:
                    output_file.write(`time_record` + '\n')
                output_file.close()





