"""
The console module is used to start the program as a command line program. Once
started, the program validates the input and either returns an error or runs the
program. If the input is ran, it will then print every state in the solution set
to the console along with time information.

Methods
-------
console_solve(list argv) -> str:
    validates input from command line, returns error if invalid input, runs program
    and prints to console.

Globals
-------
INVALID_INPUT_ERROR : str
    error to print to console if the input isn't 0-8 non-repeating.
TOO_MANY_INPUT_ERROR : str
    error to print if more than 1 input is given.
COMPLETION : str
    string to return if the program is successfully ran.
"""

from time import perf_counter
import heuristic as H
from puzzle import Puzzle

INVALID_INPUT_ERROR = "Invalid Input: input must be the numbers 0-8 non-repeating."
TOO_MANY_INPUT_ERROR = "Too many inputs detected. Program needs 1 string, but got "
COMPLETION = "Program completed."
def console_solve(argv):
    """
    console_solve is used to run the program in console form. The function takes
    the input and validates it, returning either an error message for too many
    inputs if there are more than 1 input in the list or an incorrect input if
    the input isn't 0-8 non-repeating. If the input was validated, the program
    creates a puzzle object and starts a timer. The program solves the puzzle
    then stops the timer. Once stopped, the solutions set will be printed to
    console with the final time, and finally returning the completion string.

    Parameters
    ----------
    argv : list
        list of inputs given through command prompt.

    Returns
    -------
    str
        Returns string representing error msg or completion msg.

    """
    if len(argv) > 1:
        return TOO_MANY_INPUT_ERROR + f"{len(argv)} inputs."
    puzzle_str = [int(i) for i in list(argv[0])]
    if not Puzzle.validate(puzzle_str):
        return print(INVALID_INPUT_ERROR)
    puzzle = Puzzle(puzzle_str)

    start_time = perf_counter()
    puzzle = H.heuristic(puzzle)
    soln_set = puzzle.get_soln_states()
    end_time = perf_counter()

    for idx, puzzle in enumerate(soln_set):
        if idx == 0:
            print("Initital State:")
        else:
            print(f"State: {idx}")
        Puzzle.puzzle_printer(puzzle)
        print()

    print(f"Total time: {round(end_time - start_time, 5)}s.")
    return COMPLETION
