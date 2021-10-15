"""
Puzzle GUI is the module that is completely in control of the visual elements
of the project. The main tkinter window is stored in the ShiftingPuzzleGui and
the main frame that is viewed is alternated between the other 2 classes, Puzzle
Frame and Soln Frame.

Puzzle Frame is in control of the view where the user can input their shifting
puzzle. It consists of 9 buttons representing tiles and 1 button to start the
algorithm. The algorithm itself is called from within the solve method when the
solve button is clicked and then it changes the frame to the SolnFrame after
getting the solution set.

Soln Frame is in control of viewing solution set that shows the optimal path from
the inputed puzzle frame to a completed puzzle frame. The frame consists of the
same 9 buttons showing the puzzle tiles, 2 arrow buttons to iterate forwards and
backwards through the solution set puzzle states, and a button to return to the
Puzzle Frame to input another puzzle.

Classes:
    ShiftingPuzzleGUI:
        Constructor:
            ShiftingPuzzleGUI()

        Attributes:
            box_size : int
            _frame : tkinter.frame

        Methods:
            get_puzzle_frame() -> none
            get_soln_frame(list[list[list[int]]]) -> none

    PuzzleFrame:
        Constructor:
            PuzzleFrame(self(tkinter.TK))

        Attributes:
            _tiles_list : list[tkinter.Button]
            shift_btn : tkinter.Button
            swap_btn : tkinter.Button

        Methods:
            _init_tiles() -> none
            _init_random_btn() -> tkinter.Button
            _randomize -> none
            _init_solve_btn() -> tkinter.Button
            _button_increment(tkinter.Button) -> none
            shift_solve() -> none
            swap_solve() -> none
            _get_tiles() -> list[str]

    SolnFrame:
        Attributes:
             _pointer : int
             _tiles_list : list[tkinter.Button]
             _soln_set : list[list[list[int]]]

        Methods:
            _init_tiles() -> none
            _init_btns() -> none
            _update_tiles() -> none
            _update_btns() -> none
            _update_text() -> none
            _update() -> none
            _forwards() -> none
            _backwards() -> none


Global Variables:
    BG_COLOR : str
        global string representing hex color; used for backgrounds.
    FONT_COLOR : str
        global string representing hex color; used for font/foregrounds.
    ERROR_MSG : str
        error message that is displayed when the _tiles_list buttons aren't 0-8
        non-repeating.
"""

import threading
import tkinter
import random
from math import floor
from tkinter import messagebox
from puzzle import Puzzle
import heuristic as H

BG_COLOR = '#181a19'
ERROR_MSG = "Tiles must represent 0-8, not repeating. Tiles 0-2 represents " +\
                         "the top row, 3-5 the middle, and 6-8 the bottom row."
FONT_COLOR = 'red'

class ShiftingPuzzleGUI(tkinter.Tk):
    """
    Main class used to setup tkinter window and swap between different frames.
    Puzzle frame is used for setting up and running the shifting puzzle alg and
    is the initial frame displayed. Solution frame is the frame used for displaying
    the solution of puzzle states.

    Attributes
    ----------
    box_size : int
        used for padding sizing for gui button elements
    _frame : tkinter.frame
        currently displayed tkinter frame

    Methods
    -------
    get_puzzle_frame() -> none:
        sets main tkinter window to 'puzzle frame' for puzzle inputing.
    get_soln_frame(list[list[list[int]]] soln_set) -> none:
        sets maifn tkinter window to view inputed solution (puzzle states).

    """
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.box_size = 50
        self.configure(background='black')
        self._frame = None
        self.get_puzzle_frame()

    def get_puzzle_frame(self):
        """
        Makes tkinter window display puzzle frame which allows buttons to be
        incremented to setup shifting puzzle.

        Returns
        -------
        None.

        """
        new_frame = PuzzleFrame(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    #switch to frame to view soln set
    def get_soln_frame(self, soln_set):
        """
        Sets tkinter window to solution frame which allows viewing solutions
        to the inputed shifting puzzle.

        Parameters
        ----------
        soln_set : list[list[list[int]]]
            list of puzzle states for solution
        """
        new_frame = SolnFrame(self, soln_set)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class PuzzleFrame(tkinter.Frame): # pylint: disable=too-many-ancestors
    """
    Class for showing puzzle frame. Puzzle frame is the display that lets users
    set the shifting puzzle up and initiate the algorithm to solve the puzzle.
    To run a shifting puzzle, the buttons need to be displaying the numbers 0-8
    non-repeating. Frame includes 9 buttons representing the shifting puzzle tiles
    and 1 button to initate solving.

    Attributes
    ----------
    _tiles_list : list[tkinter.Button]
        list used to store the button objects which represent the puzzle tiles.
    shift_btn : tkinter.Button
        button used to initiate the bfs shifting algorithm used to find the
        solution set.
    swap_btn : tkinter.Button
        button used to initiate the heuristic swap algorithm used to find the
        solution set.

    Methods
    -------
    _init_tiles() -> none:
        initializes the tkinter.buttons used for the shifting puzzle tiles.
    _init_random_btn() -> tkinter.Button:
        button that randomizes tile buttons to a new puzzle state on click.
    _randomize() -> none:
        randomizes the tile buttons to a new puzzle.
    _init_solve_btn() -> tkinter.Button:
        initializes the solve button for starting the algorithm.
    _button_increment(tkinter.button button) -> none:
        increments input button text by 1.
    swap_solve() -> none:
        validates button tiles, runs main swap solving algorithm, and changes frame.
    shift_solve() -> none:
        validates button tiles, runs main shift solving algorithm, and changes frame.
    _get_tiles() -> list[str]:
        returns a list of strings from the tile button texts.
    """

    def __init__(self, master):
        """
        Parameters
        ----------
        master : tkinter.TK
            TK that calls frame.
        """
        tkinter.Frame.__init__(self, master)
        self._tiles_list = []
        self.configure(background=BG_COLOR)
        self._init_tiles()
        self.shift_btn = self._init_solve_btn('Shift', self.shift_solve)
        self.shift_btn.grid(row=3, column=0)
        self.swap_btn = self._init_solve_btn('Swap', self.swap_solve)
        self.swap_btn.grid(row=3, column=1)
        self.random_btn = self._init_random_btn()
        self.random_btn.grid(row=3, column=2)
        self.grid_rowconfigure(3, minsize=50)


    def _init_tiles(self):
        """
        Method used to initialize all the tkinter.buttons used for the shifting
        puzzle tiles. Sets buttons to increment upon click.

        Returns
        -------
        None.

        """
        tile_size = 9
        row_len = 3
        for i in range(tile_size):
            self._tiles_list.append(tkinter.Button(
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
              command=lambda index=i: PuzzleFrame._button_increment(self._tiles_list[index])
            ))
            self._tiles_list[i].grid(row=floor(i/row_len), column=i%row_len)

    def _init_random_btn(self):
        """
        Method used for initializing the swapping solve button. When clicked,
        the solve button starts the algorithm that's used to find the optimal
        solution states and later changes the main frame.

        Returns
        -------
        tkinter.Button
            returns a set-up button used for initiating the solving algorithm.

        """
        return tkinter.Button(
              self,
              padx=self.master.box_size-20,
              text="Random",
              bg=BG_COLOR,
              fg=FONT_COLOR,
              activebackground=BG_COLOR,
              activeforeground=FONT_COLOR,
              font=("Times New Roman", 12),
              command=self._randomize
         )

    def _randomize(self):
        """
        Function that generates a random valid puzzle and sets the button tiles
        to that puzzle

        Returns
        -------
        None.

        """
        nums = [0,1,2,3,4,5,6,7,8]
        random.shuffle(nums)
        for idx, tile in enumerate(self._tiles_list):
            tile['text'] = nums[idx]

    def _init_solve_btn(self, text, command):
        """
        Method used for randomizing the tile buttons to get a new puzzle combination.

        Returns
        -------
        tkinter.Button
            returns a set-up button used for generating a random puzzle.

        """
        return tkinter.Button(
              self,
              padx=self.master.box_size-20,
              text=text,
              bg=BG_COLOR,
              fg=FONT_COLOR,
              activebackground=BG_COLOR,
              activeforeground=FONT_COLOR,
              font=("Times New Roman", 12),
              command=threading.Thread(target=command, daemon=True).start
         )

    @staticmethod
    def _button_increment(button):
        """
        Increments button text by 1. Valid numbers are 0-8 and if the current
        number on the button is 8, sets the number to 0.

        Parameters
        ----------
        button : tkinter.Button
            input button to have text incremented by 1.

        Returns
        -------
        None.

        """
        num = button.cget('text')
        num += 1
        if num > 8:
            num = 0
        button.config(text=num)

    def shift_solve(self):
        """
        shift solve is the method called when the swap_button is clicked. Once clicked,
        makes sure that the buttons representing the shifting puzzle tiles are
        a valid puzzle. If they are, it initializes the solving algorithm
        and sets the resulting solution set as the input to change from a puzzle
        frame to a soln frame. If the tiles aren't validated, produces an error
        message box.

        Returns
        -------
        None.

        """
        self.swap_btn['state'] = 'disabled'
        self.shift_btn['state'] = 'disabled'
        self.shift_btn['text'] = 'Running'
        if Puzzle.validate(self._get_tiles()):
            puzzle = Puzzle(self._get_tiles())
            new_puzzle = H.bfs_shift(puzzle, self.random_btn)
            if not new_puzzle:
                messagebox.showerror(title="No solution", message="No solution found.")
                self.master.get_soln_frame(puzzle.get_soln_states())
            else:
                soln_set = new_puzzle.get_soln_states()
                self.master.get_soln_frame(soln_set)
        else:
            #input that's failed validation throws error messagebox
            messagebox.showerror(title="Input error", message=ERROR_MSG)
            self.swap_btn['state'] = 'normal'
            self.shift_btn['state'] = 'normal'

    def swap_solve(self):
        """
        swap solve is the method called when the swap_button is clicked. Once clicked,
        makes sure that the buttons representing the swapping puzzle tiles are
        a valid puzzle. If they are, it initializes the solving algorithm
        and sets the resulting solution set as the input to change from a puzzle
        frame to a soln frame. If the tiles aren't validated, produces an error
        message box.

        Returns
        -------
        None.

        """
        self.swap_btn['state'] = 'disabled'
        self.shift_btn['state'] = 'disabled'
        if Puzzle.validate(self._get_tiles()):
            puzzle = Puzzle(self._get_tiles())
            puzzle = H.heuristic_swap(puzzle)
            soln_set = puzzle.get_soln_states()
            self.master.get_soln_frame(soln_set)
        else:
            #input that's failed validation throws error messagebox
            messagebox.showerror(title="Input error", message=ERROR_MSG)
            self.swap_btn['state'] = 'normal'
            self.shift_btn['state'] = 'normal'

    def _get_tiles(self):
        """
        Returns a list of strings from the buttons representing the shifting puzzle
        tiles. Method used for input for initializing a new Puzzle object.

        Returns
        -------
        list[str]
            returns list of strings from the tile button texts.

        """
        return [tile.cget("text") for tile in self._tiles_list]

class SolnFrame(tkinter.Frame): # pylint: disable=too-many-ancestors
    """
    Class for showing solution frame. Solution frame shows the set of puzzle states
    leading to a solution to the shifting puzzle. Frame includes 9 buttons
    representing the shifting puzzle tiles, a button to go back to puzzle frame
    to start a new puzzle, and 2 buttons to go forwards and backwards between
    the solution set puzzle frames.

    Attributes
    ----------
    _pointer : int
        pointer used to show which puzzle frame is displayed.
    _tiles_list : list[tkinter.Button]
        list of buttons used to represent shifting puzzle tiles.
    _soln_set : list[list[list[int]]]
        list of puzzle frames representing optimal shifting puzzle solution.

    (3 below are initialized in init_btns)
    forward : tkinter.Button
        arrow button to go forwards in solution set frames.
    backwards : tkinter.Button
        arrow button to go backwards in solution set frames.
    to_puzzle : tkinter.Button
        button to go back to puzzle frame to do another puzzle.

    (images gotten through _get_images)
    forward_arrow : tkinter.PhotoImage
        arrow image for forward button
    backwards_arrow : tkinter.PhotoImage
        arrow image for backwards button

    Methods
    -------
    _init_tiles() ->  none:
        initializes buttons used to represent the shifting puzzle tiles.
    _init_btns() -> none:
        initializes the forward, backwards, and to_puzzle buttons that control
        the frame.
    _update_tiles() -> none:
        updates buttons representing tiles to the new puzzle state.
    _update_btns() -> none:
        disables buttons for first/last puzzle solution state.
    _update_text() -> none:
        updates the label text for solution state.
    _update() -> none:
        calls all update functions when a button is clicked.
    _forward() -> none:
        increments state pointer forward one state and updates tile buttons.
    _backwards() -> none:
        decrements state pointer backwards one state and updates tile buttons.

    """

    def __init__(self, master, soln_set):
        """
        Parameters
        ----------
        master : tkinter.TK
            TK that calls frame.
        soln_set : list[list[list[int]]]
            list of puzzle states for solution
        """
        tkinter.Frame.__init__(self, master)
        self.configure(background=BG_COLOR)
        self._pointer = 0
        self._tiles_list = []
        self._soln_set = soln_set

        self._init_tiles()
        self._init_btns()
        self._update()

    def _init_tiles(self):
        """
        Initializes the buttons used to represent the shifting puzzle tiles.
        Buttons are unclickable due to them representing the solution set and
        don't need to be changed.

        Returns
        -------
        None.

        """
        col_len = 3
        row_len = 3
        for col in range(col_len):
            self._tiles_list.append([])
            for row in range(row_len):
                self._tiles_list[col].append(tkinter.Button(
                  self,
                  padx=self.master.box_size,
                  pady=self.master.box_size,
                  bg=BG_COLOR,
                  fg=FONT_COLOR,
                  activebackground=BG_COLOR,
                  activeforeground=FONT_COLOR,
                  font=("Times New Roman", 20),
                  ))
                self._tiles_list[col][row].grid(row=row, column=col)

    def _init_btns(self):
        """
        Initializes the 3 buttons that control the SolnFrame. A forwards button
        moves the _tiles_list to display the next puzzle frame in the _soln_set.
        A backwards button moves the _tiles_list to display the previous puzzle
        frame in the _soln_set. A to_puzzle button that returns the main frame
        to PuzzleFrame.

        Returns
        -------
        None.

        """
        forward_img_path = r"images/forward_arrow.png"
        backwards_img_path = r"images/backwards_arrow.png"
        self.forwards_img = tkinter.PhotoImage(file=forward_img_path)
        self.backwards_img = tkinter.PhotoImage(file=backwards_img_path)
        #setup forward button
        self.forward = tkinter.Button(
            self,
            image=self.forwards_img,
            bg=BG_COLOR,
            activebackground=BG_COLOR,
            command=self._forward
        )
        self.forward.grid(row=3, column=2)

        #setup backwards button
        self.backwards = tkinter.Button(
            self,
            image=self.backwards_img,
            bg=BG_COLOR,
            activebackground=BG_COLOR,
            command=self._backwards
        )
        self.backwards.grid(row=3, column=0)
        self.grid_rowconfigure(3, minsize=50)

        #setup to_puzzle button
        self.to_puzzle = tkinter.Button(
                self,
                text="New Puzzle",
                bg=BG_COLOR,
                fg=FONT_COLOR,
                activebackground=BG_COLOR,
                activeforeground=FONT_COLOR,
                font=("Times New Roman", 16),
                command=self.master.get_puzzle_frame
        )
        self.to_puzzle.grid(row=4, column=1)

    def _update_tiles(self):
        """
        Maps tiles to new state after forward/backwards button is clicked
        or solution frame is initialized.

        Returns
        -------
        None.
        """
        for col in range(3):
            for row in range(3):
                self._tiles_list[col][row]["text"] = \
                    self._soln_set[self._pointer][row][col]

    def _update_btns(self):
        """
        Checks which state soln frame is in with pointer. Disables backwards btn
        at state 0 and disables forwards btn at last state.

        Returns
        -------
        None.
        """
        self.backwards["state"] = self.forward["state"] = tkinter.NORMAL
        if self._pointer == 0:
            self.backwards["state"] = tkinter.DISABLED
        if self._pointer == len(self._soln_set)-1:
            self.forward["state"] = tkinter.DISABLED

    def _update_text(self):
        """
        Updates the tkinter.label according to which number state in the solution
        set is being displayed.

        Returns
        -------
        None.

        """
        step_text = f"Step: {self._pointer + 1}/{len(self._soln_set)}"
        step_label =tkinter.Label(
            self,
            fg=FONT_COLOR,
            bg=BG_COLOR,
            text=step_text)
        step_label.grid(row=3, column=1)

    def _update(self):
        """
        Calls all the update functions when a button is clicked.

        Returns
        -------
        None.

        """
        self._update_tiles()
        self._update_btns()
        self._update_text()

    def _forward(self):
        """
        Increments state pointer forward one state and updates tile buttons.

        Returns
        -------
        None.

        """
        self._pointer += 1
        self._update()

    def _backwards(self):
        """
        Decrements state pointer backwards one state and updates tile buttons.

        Returns
        -------
        None.

        """
        self._pointer -= 1
        self._update()
