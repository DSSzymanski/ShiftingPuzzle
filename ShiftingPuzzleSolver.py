# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 21:02:26 2020
@author: Daniel
"""
import Console
import Puzzle
import Heuristic as H
import sys
import tkinter
from tkinter import messagebox
from math import floor

class ShiftingPuzzleGUI(tkinter.Tk):
	def __init__(self):
		tkinter.Tk.__init__(self)
		self._frame = None
		self.get_puzzle_frame()
	
	def get_puzzle_frame(self):
		new_frame = PuzzleFrame(self)
		if self._frame is not None: 
			self._frame.destroy()
		self._frame = new_frame
		self._frame.pack()
		
	def get_soln_frame(self, soln_set):
		new_frame = SolnFrame(self, soln_set)
		if self._frame is not None:
			self._frame.destroy()
		self._frame = new_frame
		self._frame.pack()
		
class PuzzleFrame(tkinter.Frame):
	def __init__(self, master):
		tkinter.Frame.__init__(self, master)
		self._tiles_list = []
		self._init_tiles()
		self.solve_btn = tkinter.Button(self, text="Solve", command=lambda: self.solve())
		self.solve_btn.grid(row=3, column=1)
		self.ERROR_MSG = "Tiles must represent 0-8, not repeating. Tiles 0-2 represents the top row, 3-5 the middle, and 6-8 the bottom row."
	
	#sets up tiles in grid
	def _init_tiles(self):
		tile_size = 9
		row_len = 3
		for i in range(tile_size):
			self._tiles_list.append(tkinter.Button(self, text=i, padx=40, pady=20))
			self._tiles_list[i].grid(row=floor(i/row_len), column=i%row_len)
		
	#increments button values by 1, after 8 gets set to 0
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
		puzzle = [8,1,2,3,4,5,6,7,0]
		if Puzzle.validate(puzzle):
			puzzle = Puzzle.puzzle_converter(puzzle)
			soln = H.heuristic(puzzle)
			soln_set = Puzzle.state_maker(puzzle, soln)
			self.master.get_soln_frame(soln_set)
		else:
			messagebox.showerror(title="Input error", message=self.ERROR_MSG)
	
	#gets list of puzzle tiles
	def get_tiles(self):
		return [tile.cget("text") for tile in self._tiles_list]
		
#GUI for solution states
class SolnFrame(tkinter.Frame):
	def __init__(self, master, soln_set):
		tkinter.Frame.__init__(self, master)
		self._pointer = 0
		self._tiles_list = []
		self._soln_set = soln_set
		
		self._get_images()
		self._init_tiles()
		self._init_btns()
		self._update_tiles()
		
	def _get_images(self):
		#setup btn images
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
				self._tiles_list[y].append(tkinter.Button(self, padx=40, pady=20, state=tkinter.DISABLED))
				self._tiles_list[y][x].grid(row=x, column=y)
				
	def _init_btns(self):
		self.forward = tkinter.Button(self, image=self.forward_arrow, command=lambda: self._forward())
		self.forward.grid(row=3, column=2)
		self.backwards = tkinter.Button(self, image=self.backwards_arrow, command=lambda: self._backwards())
		self.backwards.grid(row=3, column=0)
		self.grid_rowconfigure(3, minsize=50)
		
	def _update_tiles(self):
		for y in range(3):
			for x in range(3):
				self._tiles_list[y][x]["text"] = self._soln_set[self._pointer][x][y]
		self._update_btns()
	
	def _update_btns(self):
		self.backwards["state"] = self.forward["state"] = tkinter.NORMAL
		if self._pointer == 0:
			self.backwards["state"] = tkinter.DISABLED
		if self._pointer == len(self._soln_set)-1:
			self.forward["state"] = tkinter.DISABLED
	
	def _forward(self): 
		self._pointer += 1
		self._update_tiles()
	
	def _backwards(self):
		self._pointer -= 1
		self._update_tiles()

if __name__ == "__main__":
	if len(sys.argv) == 1: 
		gui = ShiftingPuzzleGUI()
		gui.mainloop()
	else: Console.console_solve(sys.argv[1:])