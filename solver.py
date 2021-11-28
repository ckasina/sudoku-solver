from copy import deepcopy


class Puzzle:
    def __init__(self, grid):
        """Puzzle class, used to complete various functions of Sudoku incl. solving
        :param grid: 2-dimensional 9x9 list storing the numbers in the puzzle"""

        self._rows = 9
        self._cols = 9
        self._grid = grid

    def getGrid(self):
        """:return: Returns the puzzle as a 2-dimensional 9x9 list"""

        return self._grid

    def getRow(self, row):
        """:param row: Zero-based index of the row to be retrieved
        :return: Returns the specified row as a 1-dimensional list"""

        return self._grid[row]

    def getCol(self, col):
        """:param col: Zero-based index of the column to be retrieved
        :return: Returns the specified column as a 1-dimensional list"""

        return [self._grid[row][col] for row in range(self._rows)]

    def getBox(self, row, col):
        """:param row: Zero-based index of the row the cell is in
        :param col: Zero-based index of the column the cell is in
        :return: Returns all the cells of the box the cell is in as a 1-dimensional list"""

        startRow = (row // 3) * 3
        startCol = (col // 3) * 3

        return [
            self._grid[row][col]
            for row in range(startRow, startRow + 3)
            for col in range(startCol, startCol + 3)
        ]

    def getCell(self, row, col):
        """:param row: Zero-based index of the row of the cell
        :param col: Zero-based index of the column of the cell
        :return: Returns the specified cell"""

        return self._grid[row][col]

    def getEmptyCells(self):
        """:return: Returns a 1-dimensional list containing row,col tuples of empty cells in the puzzle"""

        return [
            (row, col)
            for col in range(self._cols)
            for row in range(self._rows)
            if self._grid[row][col] == 0
        ]

    def getNextEmpty(self):
        """:return: Returns a tuple with the row, col of the next empty cell in the puzzle"""

        indexes = self.getEmptyCells()
        if len(indexes) == 0:
            return None, None
        else:
            return indexes[0]

    def getCandidates(self, row, col):
        """:param row: Zero-based index of the row of the cell
        :param col: Zero-based index of the column of the cell
        :return: Returns the candidates of the specified cell as a 1-dimensional list"""

        return [num for num in range(1, 10) if not self.checkConflict(row, col, num)]

    def setCell(self, row, col, num):
        """:param row: Zero-based index of the row of the cell
        :param col: Zero-based index of the column of the cell
        :param num: The number to change the value of the specified cell to"""

        self._grid[row][col] = num

    def clearPuzzle(self):
        """Sets the value of each cell in the puzzle to 0"""

        for row in range(self._rows):
            for col in range(self._cols):
                self._grid[row][col] = 0

    def checkConflict(self, row, col, num):
        """Checks the box, row, and column of the specified cell for conflicts
        :param row: Zero-based index of the row of the cell
        :param col: Zero-based index of the column of the cell
        :param num: The number to check for conflicts with
        :return: Boolean value of whether there's conflicts"""

        def checkConflictBox(row, col, num):
            return num in self.getBox(row, col)

        def checkConflictRow(row, num):
            return num in self.getRow(row)

        def checkConflictCol(col, num):
            return num in self.getCol(col)

        return (
            checkConflictBox(row, col, num)
            or checkConflictRow(row, num)
            or checkConflictCol(col, num)
        )

    def solve(self):
        """Solves the puzzle using various methods specified below (for now just backtracking)"""

        newPuzzle = deepcopy(self)
        solvable = self.backtrack(newPuzzle)
        if solvable:
            self._grid = deepcopy(newPuzzle._grid)

        else:
            print("Could not be solved!")

    def backtrack(self, newPuzzle):
        """Recursive function that brute force attempts all the cells with valid numbers until solved
        :param newPuzzle: Puzzle object that is carried forward in the parameter each time backtrack is called whilst solving
        :return: Boolean value representing whether the puzzle was solved"""

        row, col = newPuzzle.getNextEmpty()
        if (row, col) == (None, None): 
            # if there's no more empty cells then the puzzle is solved
            return True

        for num in newPuzzle.getCandidates(row, col):
            # For each valid number that can be inputted into the current empty cell
            newPuzzle.setCell(row, col, num)

            # Continues recursively trying to solve the puzzle
            if newPuzzle.backtrack(newPuzzle): 
                return True
            else:
                # If the puzzle cannot be solved from inputting the number into the cell then
                # it clears it and tries the next number
                newPuzzle.setCell(row, col, 0) 

        return False

    def __str__(self):
        """:return: Returns this Puzzle class as a string with 9 rows of 9 numbers"""

        return "\n".join(
            [
                "".join([str(self.getCell(row, col)) for col in range(self._cols)])
                for row in range(self._rows)
            ]
        )


# Imports puzzle from a file with 9 rows of 9 numbers representing the puzzle where 0 is an empty cell
puzzle2D = []

with open("puzzle.txt", "r") as file:
    puzzle = file.read()
    puzzle2D = [[int(col) for col in row] for row in puzzle.split("\n")]


puzzleObj = Puzzle(puzzle2D)
puzzleObj.solve()
print(puzzleObj)
