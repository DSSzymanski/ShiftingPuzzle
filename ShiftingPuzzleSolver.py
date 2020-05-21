# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 21:02:26 2020
@author: Daniel
"""
from tkinter import *
from tkinter import messagebox
import Console
from Puzzle import validate
import sys

ERROR_MSG = "Tiles must represent 0-8, not repeating. Tiles 0-2 represents the \
	top row, 3-5 the middle, and 6-8 the bottom row."

#change button text to tiles
def button_increment(button):
	num = button.cget('text')
	num += 1
	if num > 8: num = 0
	button.config(text=num)
	
def get_tile_text(tiles):
	return [tile.cget("text") for tile in tiles]

def solve(tiles):
	puzzle = get_tile_text(tiles)
	if validate(puzzle):
		return True
	messagebox.showerror(title="Input error", message=ERROR_MSG)
	
def gui_solve():
	#initialize GUI
	window = Tk()
	window.title("Shifting Puzzle Solver")
	
	f1 = Frame(width=400, height=400)
	#set up and initialize all tile buttons to 0
	tile_0_0 = Button(f1, text=0, padx=40, pady=20, command=lambda: button_increment(tile_0_0))
	tile_0_1 = Button(window, text=0, padx=40, pady=20, command=lambda: button_increment(tile_0_1))
	tile_0_2 = Button(window, text=0, padx=40, pady=20, command=lambda: button_increment(tile_0_2))
	tile_1_0 = Button(window, text=0, padx=40, pady=20, command=lambda: button_increment(tile_1_0))
	tile_1_1 = Button(window, text=0, padx=40, pady=20, command=lambda: button_increment(tile_1_1))
	tile_1_2 = Button(window, text=0, padx=40, pady=20, command=lambda: button_increment(tile_1_2))
	tile_2_0 = Button(window, text=0, padx=40, pady=20, command=lambda: button_increment(tile_2_0))
	tile_2_1 = Button(window, text=0, padx=40, pady=20, command=lambda: button_increment(tile_2_1))
	tile_2_2 = Button(window, text=0, padx=40, pady=20, command=lambda: button_increment(tile_2_2))
	tiles_list = [tile_0_0, tile_0_1, tile_0_2, tile_1_0, tile_1_1, tile_1_2, tile_2_0, tile_2_1, tile_2_2]
   
	tile_solve = Button(window, text="Solve", command=lambda: solve(tiles_list))
	
	#show all tiles
	tile_0_0.grid(row=0, column=0)
	tile_0_1.grid(row=0, column=1)
	tile_0_2.grid(row=0, column=2)
	tile_1_0.grid(row=1, column=0)
	tile_1_1.grid(row=1, column=1)
	tile_1_2.grid(row=1, column=2)
	tile_2_0.grid(row=2, column=0)
	tile_2_1.grid(row=2, column=1)
	tile_2_2.grid(row=2, column=2)
	tile_solve.grid(row=3, column=1)
	
	#run
	window.mainloop()

if __name__ == "__main__":
	if len(sys.argv) == 1: gui_solve()
	else: Console.console_solve(sys.argv[1:])