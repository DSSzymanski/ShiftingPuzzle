import console
import sys
from puzzle_gui import ShiftingPuzzleGUI

if __name__ == "__main__":
    if len(sys.argv) == 1:
        gui = ShiftingPuzzleGUI()
        gui.title("Shifting Puzzle Solver")
        gui.eval('tk::PlaceWindow . center')
        gui.mainloop()
    else:
        console.console_solve(sys.argv[1:])
