# Pydoku
There are 3 algorithms used here, Backtrack, Brute Force, and BnB. All three algorithm actually utilise backtracking but
the actual Backtrack algorithm uses the sudoku rules as the boundary function and only find first solution

Brute force in the other hand will try to iterate all possible valid sudoku grid. Once a valid sudoku is generated, it
will check if said valid sudoku match the problem. This is not efficient and will only give results for 2x2 sudoku. You
may need to wait for billion years to find solution of a 3x3 sudoku problem.

Branch and Bound will try to fill cell with least possible values first instead of getting next neighbor from current
cell. In theory this should give better speed from proposed backtrack algorithm. But each time it will get cell with
least possible values with O(n^m).

## License
This work is licensed under Creative Commons Attribution-ShareAlike 3.0 Unported License
https://creativecommons.org/licenses/by-sa/3.0/deed.en_US

Feel free to use and improve the code under the the license conditions.

## Credit:
Sudoku UI http://newcoder.io/gui/
The UI is based on the tutorial given here. There are some changes to accomodate 2x2 Sudoku and introduces solvers.


norvig