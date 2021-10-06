#import Console
from puzzle import Puzzle
import heuristic as H
import sys
import tkinter
from tkinter import messagebox
from math import floor

BG_COLOR = '#181a19'
FONT_COLOR = 'red'

class ShiftingPuzzleGUI(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.box_size = 50
        self.configure(background='black')
        self._frame = None
        self.get_puzzle_frame()

    #switch to frame for inputting puzzle
    def get_puzzle_frame(self):
        new_frame = PuzzleFrame(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    #switch to frame to view soln set
    def get_soln_frame(self, soln_set):
        """
        :param soln_set: list of puzzle states for solution
        """
        new_frame = SolnFrame(self, soln_set)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class PuzzleFrame(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self._tiles_list = [tkinter.Button] * 9
        self.configure(background=BG_COLOR)
        self._init_tiles()
        self.solve_btn = tkinter.Button(
              self,
              padx=self.master.box_size-20,
              text="Solve",
              bg=BG_COLOR,
              fg=FONT_COLOR,
              activebackground=BG_COLOR,
              activeforeground=FONT_COLOR,
              font=("Times New Roman", 16),
              command=lambda: self.solve())
        self.solve_btn.grid(row=3, column=1)
        self.grid_rowconfigure(3, minsize=50)
        self.ERROR_MSG = "Tiles must represent 0-8, not repeating. Tiles 0-2 represents the top row, 3-5 the middle, and 6-8 the bottom row."

    #sets up tiles in grid
    def _init_tiles(self):
        tile_size = 9
        row_len = 3
        for i in range(tile_size):
            self._tiles_list[i] = tkinter.Button(
              self,
              text=i,
              bg=BG_COLOR,
              activebackground=BG_COLOR,
              activeforeground=FONT_COLOR,
              fg=FONT_COLOR,
              padx=self.master.box_size,
              pady=self.master.box_size,
                font=("Times New Roman", 20),
              #index = i needed to maintain mapping to correct tile
              command=lambda index=i: self.button_increment(self._tiles_list[index])
            )
            self._tiles_list[i].grid(row=floor(i/row_len), column=i%row_len)

    #increments button values by 1, after 8 gets set to 0
    def button_increment(self, button):
        """
        :param button: button to have value incremented
        """
        num = button.cget('text')
        num += 1
        if num > 8:
            num = 0
        button.config(text=num)

    """
    Checks to see if tiles give a valid puzzle.
    If so, converts to puzzle and solves, changing to Solution Frame
    If not, gives an error popup and stays on curr frame
    """
    def solve(self):
        if Puzzle.validate(self.get_tiles()):
            puzzle = Puzzle(self.get_tiles())
            puzzle = H.heuristic(puzzle)
            soln_set = puzzle.get_soln_states()
            self.master.get_soln_frame(soln_set)
        else:
            messagebox.showerror(title="Input error", message=self.ERROR_MSG)

    #gets list of puzzle tiles
    def get_tiles(self):
        return [tile.cget("text") for tile in self._tiles_list]

#GUI for solution states
class SolnFrame(tkinter.Frame):
    def __init__(self, master, soln_set):
        """
        :param soln_set: list of puzzle states for solution
        """
        tkinter.Frame.__init__(self, master)
        self.configure(background=BG_COLOR)
        self._pointer = 0
        self._tiles_list = []
        self._soln_set = soln_set

        self._get_images()
        self._init_tiles()
        self._init_btns()
        self._update()

    #setup btn images
    def _get_images(self):
        forward_img_path = r"images/forward_arrow.png"
        backwards_img_path = r"images/backwards_arrow.png"
        self.forward_arrow = tkinter.PhotoImage(file=forward_img_path)
        self.backwards_arrow = tkinter.PhotoImage(file=backwards_img_path)

    #sets up tiles in grid
    def _init_tiles(self):
        col_len = 3
        row_len = 3
        for y in range(col_len):
            self._tiles_list.append([])
            for x in range(row_len):
                self._tiles_list[y].append(tkinter.Button(
                  self,
                  padx=self.master.box_size,
                  pady=self.master.box_size,
                  bg=BG_COLOR,
                  fg=FONT_COLOR,
                  activebackground=BG_COLOR,
                  activeforeground=FONT_COLOR,
                  font=("Times New Roman", 20),
                  ))
                self._tiles_list[y][x].grid(row=x, column=y)

    #initializes forwards, backwards buttons and adds them to grid
    #initializes button to go back to puzzle frame and adds to grid
    def _init_btns(self):
        self.forward = tkinter.Button(
            self,
            image=self.forward_arrow,
            bg=BG_COLOR,
            activebackground=BG_COLOR,
            command=lambda: self._forward())
        self.forward.grid(row=3, column=2)
        self.backwards = tkinter.Button(
            self,
            image=self.backwards_arrow,
            bg=BG_COLOR,
            activebackground=BG_COLOR,
            command=lambda: self._backwards())
        self.backwards.grid(row=3, column=0)
        self.grid_rowconfigure(3, minsize=50)

        self.to_puzzle = tkinter.Button(
                self,
                text="New Puzzle",
                bg=BG_COLOR,
                fg=FONT_COLOR,
                activebackground=BG_COLOR,
                activeforeground=FONT_COLOR,
                font=("Times New Roman", 16),
                command=lambda: self.master.get_puzzle_frame())
        self.to_puzzle.grid(row=4, column=1)

    """
    Maps tiles to new state after forward/backwards button is clicked
    or solution frame is initialized
    """
    def _update_tiles(self):
        for y in range(3):
            for x in range(3):
                self._tiles_list[y][x]["text"] = self._soln_set[self._pointer][x][y]

    """
    checks which state soln frame is in with pointer.
    Disables backwards btn @ state 0
    Disables forwards btn @ last state
    """
    def _update_btns(self):
        self.backwards["state"] = self.forward["state"] = tkinter.NORMAL
        if self._pointer == 0:
            self.backwards["state"] = tkinter.DISABLED
        if self._pointer == len(self._soln_set)-1:
            self.forward["state"] = tkinter.DISABLED

    #updates label for current step
    def _update_text(self):
        step_text = f"Step: {self._pointer + 1}/{len(self._soln_set)}"
        step_label =tkinter.Label(
            self,
            fg=FONT_COLOR,
            bg=BG_COLOR,
            text=step_text)
        step_label.grid(row=3, column=1)

    def _update(self):
        self._update_tiles()
        self._update_btns()
        self._update_text()

    #increments state pointer forward one state and updates tiles
    def _forward(self):
        self._pointer += 1
        self._update()

    #decrements state pointer backwards one state and updates tiles
    def _backwards(self):
        self._pointer -= 1
        self._update()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        gui = ShiftingPuzzleGUI()
        gui.title("Shifting Puzzle Solver")
        gui.eval('tk::PlaceWindow . center')
        gui.mainloop()
    #else: Console.console_solve(sys.argv[1:])