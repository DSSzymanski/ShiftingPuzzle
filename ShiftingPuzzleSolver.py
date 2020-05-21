# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 21:02:26 2020
@author: Daniel
"""
import Console
from Puzzle import validate
import sys
import tkinter
from tkinter import messagebox

class ShiftingPuzzleGUI(tkinter.Tk):
	def __init__(self):
		tkinter.Tk.__init__(self)
		self._frame = None
		self.switch_frame(PuzzleFrame)
	
	def switch_frame(self, frame_class):
		new_frame = frame_class(self)
		if self._frame is not None: 
			self._frame.destroy()
		self._frame = new_frame
		self._frame.pack()
		
class PuzzleFrame(tkinter.Frame):
	def __init__(self, master):
		tkinter.Frame.__init__(self, master)
		self.tiles_list = []
		self._init_tiles()
		self.solve_btn = tkinter.Button(self, text="Solve", command=lambda: self.solve())
		self.solve_btn.grid(row=3, column=1)
		self.ERROR_MSG = "Tiles must represent 0-8, not repeating. Tiles 0-2 represents the top row, 3-5 the middle, and 6-8 the bottom row."
		
	def _init_tiles(self):
		self.tile_0_0 = tkinter.Button(self, text=0, padx=40, pady=20, command=lambda: self.button_increment(self.tile_0_0))
		self.tile_0_1 = tkinter.Button(self, text=0, padx=40, pady=20, command=lambda: self.button_increment(self.tile_0_1))
		self.tile_0_2 = tkinter.Button(self, text=0, padx=40, pady=20, command=lambda: self.button_increment(self.tile_0_2))
		self.tile_1_0 = tkinter.Button(self, text=0, padx=40, pady=20, command=lambda: self.button_increment(self.tile_1_0))
		self.tile_1_1 = tkinter.Button(self, text=0, padx=40, pady=20, command=lambda: self.button_increment(self.tile_1_1))
		self.tile_1_2 = tkinter.Button(self, text=0, padx=40, pady=20, command=lambda: self.button_increment(self.tile_1_2))
		self.tile_2_0 = tkinter.Button(self, text=0, padx=40, pady=20, command=lambda: self.button_increment(self.tile_2_0))
		self.tile_2_1 = tkinter.Button(self, text=0, padx=40, pady=20, command=lambda: self.button_increment(self.tile_2_1))
		self.tile_2_2 = tkinter.Button(self, text=0, padx=40, pady=20, command=lambda: self.button_increment(self.tile_2_2))

		self.tiles_list = [self.tile_0_0, self.tile_0_1, self.tile_0_2, \
					 self.tile_1_0, self.tile_1_1, self.tile_1_2, self.tile_2_0, \
					 self.tile_2_1, self.tile_2_2]
		#show all tiles
		self.tile_0_0.grid(row=0, column=0)
		self.tile_0_1.grid(row=0, column=1)
		self.tile_0_2.grid(row=0, column=2)
		self.tile_1_0.grid(row=1, column=0)
		self.tile_1_1.grid(row=1, column=1)
		self.tile_1_2.grid(row=1, column=2)
		self.tile_2_0.grid(row=2, column=0)
		self.tile_2_1.grid(row=2, column=1)
		self.tile_2_2.grid(row=2, column=2)
		
	#change button text to tiles
	def button_increment(self, button):
		num = button.cget('text')
		num += 1
		if num > 8: num = 0
		button.config(text=num)
	
	"""
	Checks to see if tiles give a valid puzzle.
	If so, converts to puzzle and solves, changing to Solution Frame
	If not, gives an error popup and stays on curr frame
	"""
	def solve(self):
		puzzle = self.get_tiles()
		if validate(puzzle):
			return True
		tkinter.messagebox.showerror(title="Input error", message=self.ERROR_MSG)
	
	#gets list of puzzle tiles
	def get_tiles(self):
		return [tile.cget("text") for tile in self.tiles_list]
		
class SolveFrame(tkinter.Frame):
	def __init__(self, master):
		tkinter.Frame.__init__(self, master)
		tkinter.Button(self, text="Go to puzzle", command=lambda: master.switch_frame(PuzzleFrame)).pack()

if __name__ == "__main__":
	if len(sys.argv) == 1: 
		gui = ShiftingPuzzleGUI()
		gui.mainloop()
	else: Console.console_solve(sys.argv[1:])