"""
Module puzzle contains the class that holds the data and performs the operations
for the shifting puzzle. Inside the class are 2 static methods used for validating
and converting lists of 9 ints into puzzle objects.

Classes:
    Puzzle:
        Constructor:
            Puzzle(list[int])

        Attributes:
            puzzle : list[list[int]]
            soln_states: list[puzzles]
            moves : list[list[int]]
            correct_puzzle list[list[int]]

        Methods:
            get_puzzle_state() -> list[list[int]]
            puzzle_check() -> boolean
            static validate(list[int]) -> boolean
            add_move(list[list[int]]) -> none
            puzzle_converter(list[str) -> none
            swap(list[list[int]], list[list[int]]) -> none
            static puzzle_printer(list[list[int]]) -> none
            get_soln_states() -> list[list[list[int]]]
"""
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass, field

@dataclass(order=True)
class Puzzle:
    """
    The Puzzle class is used to store the data and manipulate puzzle states.

    Usage
    -----
    Possible puzzle states can be validated by calling the static method validate,
    eg. validate([0,1,2,3,4,5,6,7,8]). It will work while populated with 9 ints
    or 9 strs that are the unique numbers 0-8 in some order.

    Once the input has been validated, you can create the class by calling
    Puzzle(arg) with the input from validate as arg.

    The main methods for manipulating the puzzles are swap() and add_move().
    Swap takes in 2 x,y coordinate ints in a list to swap the values at both
    locations. add_move() adds the 2 x,y coordinates used in the swap functions
    as a list and adds to the moves attr.

    e.g. calling swap([0,1], [1,0]) will switch the values of puzzle.puzzle at
    positions (0,1) and (1,0).

    e.g. calling add_move([[0,1], [1,0]]) adds the move.

    Attributes
    ----------
    puzzle : list[list[int]]
        current state of the puzzle
    soln_states : list[list[list[int]]]
        list of puzzle states representing optimal solution. Filled when
        get_soln_states() is called.
    moves : list[list[list[int]]]
        list of moves taken to get to current puzzle state. A move is 2 list of
        x, y coordinate value pairs.
    correct_puzzle : list[list[int]]
        puzzle state representing the end/solved state to compare the current
        state to.

    Methods
    -------
    get_puzzle_state() -> list[list[int]]:
        returns the current puzzle state.
    puzzle_check() -> boolean:
        returns a boolean if the current puzzle state equals the completed puzzle
        state.
    static validate(list[int] puzzle_input) -> boolean:
        returns a boolean if the puzzle_input is a valid shifting puzzle combination.
        Requires [0-8] or ['0'-'8'] uniquely in some order.
    add_move(list[list[int]] move) -> none:
        adds a move to the moves attr.
    puzzle_converter(list[str) -> none:
        converts puzzle_input from validate() into a valid 2d 3x3 shifting puzzle
        and sets self.puzzle to the valid puzzle.
    swap(list[list[int]] tile1, list[list[int]] tile2) -> none:
        swaps the values of the puzzle attr at the x,y location at tile1 with the
        x,y location attile2.
    static puzzle_printer(list[list[int]] puzzle) -> none:
        prints the inputted puzzle state to console.
    get_soln_states() -> list[list[list[int]]]:
        takes initial puzzle and applies all the moves in the moves attr. recording
        the states along the way and returns a list of the puzzle states needed
        to solve the puzzle.
    """
    puzzle: list=field(compare=False)

    def __init__(self, puzzle):
        self.puzzle = []
        self.puzzle_converter(puzzle)
        self.soln_states = [deepcopy(self.puzzle)]
        self.moves = []
        self.correct_puzzle =  [
                                    [1,2,3],
                                    [4,5,6],
                                    [7,8,0]
                                ]

    def get_puzzle_state(self):
        """
        Gets the current state of the puzzle.

        Returns
        -------
        List[List[int]]
            Returns 2d list representing current puzzle state.

        """
        return self.puzzle

    def get_zero_pos(self):
        """
        Gets the position of 0 in the current puzzle state.

        Returns
        -------
        list
            list containing the x,y positioning of 0.

        """
        for idx, valx in enumerate(self.puzzle):
            for idy, valy in enumerate(valx):
                if valy == 0:
                    return [idx, idy]

    def puzzle_check(self):
        """
        Compares current puzzle state to completed state to determine if the
        puzzle is solved.

        Returns
        -------
        Boolean
            Returns a boolean if the puzzle is completed.

        """
        return self.puzzle == self.correct_puzzle

    @staticmethod
    def validate(puzzle_input):
        """
        Examines an input list to determine if the list represents a valid
        shifting puzzle (ensures values are 0-8 uniquely in some order). Function
        static bc it's called BEFORE a puzzle object is created.

        Parameters
        ----------
        puzzle_input : list[str]
            List of strs representing ints for a possible shifting puzzle object.

        Returns
        -------
        Boolean
            Returns a boolean if input list is a valid shifting puzzle.

        """
        valid_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        return Counter(puzzle_input) == Counter(valid_list)

    def add_move(self, move):
        """
        Appends move to stored list of moves. Move consists of 2 lists of x,y
        coordinates to indicate which tiles are being swapped.

        Parameters
        ----------
        move : list[list[int]]
            List of lists representing a move.

        Returns
        -------
        None.

        """
        self.moves.append(move)

    def puzzle_converter(self, args):
        """
        Converts a list of strings into a 2d, 3x3 puzzle of ints and sets it to
        puzzle.puzzle.

        Parameters
        ----------
        args : List[str]
            List of strs representing ints for a valid shifting puzzle object.

        Returns
        -------
        None.

        """
        puzzle = []
        row = []
        for value in args:
            row.append(int(value))
            if len(row) == 3:
                puzzle.append(row)
                row = []
        self.puzzle = puzzle

    def swap(self, tile1, tile2):
        """
        Swaps the positioning of 2 x,y coords in the 2d puzzle.

        Parameters
        ----------
        tile1 : list[int]
            list of ints representing a single x,y coordinate.
        tile2 : list[int]
            list of ints representing a single x,y coordinate.

        Returns
        -------
        None.

        """
        self.puzzle[tile1[0]][tile1[1]], self.puzzle[tile2[0]][tile2[1]] = \
               self.puzzle[tile2[0]][tile2[1]], self.puzzle[tile1[0]][tile1[1]]

    @staticmethod
    def puzzle_printer(puzzle):
        """
        Prints the current puzzle to console

        Returns
        -------
        None.

        """
        for i in range(3):
            print(puzzle[i])

    def get_soln_states(self):
        """
        Converts the initial puzzle using the stored list of moves to create
        and return a list of puzzle states representing a solution.

        Returns
        -------
        List[List[List[int]]]
            Returns a list of puzzle states.

        """
        self.puzzle = deepcopy(self.soln_states[0])
        for step in self.moves:
            self.swap(step[0], step[1])
            self.soln_states.append(deepcopy(self.puzzle))

        return self.soln_states
