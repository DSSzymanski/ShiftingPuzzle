"""
Main module to be run to start the program. If ran with 0 inputs from the command
line or ran as a program, it will show the GUI representation.

If ran with more than 1 input will run the command line form of the program.
This 1 input needs to be an input of 0-8 non-repeating.

    An input of 012345678 or 81427653 will work as they have all the numbers from
    zero to eight, while 012345670 or 81234543 will not as they have duplicate
    numbers.
"""

import sys
import console
from puzzle_gui import ShiftingPuzzleGUI

if __name__ == "__main__":
    if len(sys.argv) == 1:
        gui = ShiftingPuzzleGUI()
        gui.title("Shifting Puzzle Solver")
        gui.eval('tk::PlaceWindow . center')
        gui.mainloop()
    else:
        error = console.console_solve(sys.argv[1:])
        if error != console.COMPLETION:
            print(error)
