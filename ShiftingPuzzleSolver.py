# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 21:02:26 2020
@author: Daniel
"""
from collections import deque
from time import perf_counter
from copy import deepcopy
from tkinter import *
import sys

CORRECT_PUZZLE = [
	[0,1,2],
	[3,4,5],
	[6,7,8]]

#puzzle solver based on heuristics
def heuristic(puzzle):
	global CORRECT_PUZZLE
	
	#base case
	if puzzle == CORRECT_PUZZLE: return []
	
	#initialize data structures
	moves = []
	queue = deque()
	queue.append((puzzle, [], get_heuristic(puzzle)))
	states = set()
	
	#used to weed out moves that result in a worst heuristic value
	best_heuristic = get_heuristic(puzzle)
	
	while True:
		current = queue.popleft()
		puzzle, moves = current[0], current[1]
		
		#loop used to generate every move from every tile location
		for i in range(3):
			for j in range(3):
				#used to store potential moves for each tile
				p_moves = [] 
				
				"""
				Generates all moves from the tile location. Built in validation
				to ensure all moves stay in the grid
				"""
				if i != 0: 
					north = [i-1, j]
					p_moves.append(north)
				if i != 2:
					south = [i+1, j]
					p_moves.append(south)
				if j != 2:
					east = [i, j+1]
					p_moves.append(east)
				if j != 0:
					west = [i, j-1]
					p_moves.append(west)
				
				
				#Iterates over all valid moves generated for the tile
				for move in p_moves:
					#create new puzzle & move lists & completes move
					#and evaluates new heuristic
					new_puzzle = deepcopy(puzzle)
					new_moves = moves.copy()
					new_puzzle = swap(new_puzzle, [i, j], move)
					new_heuristic = get_heuristic(new_puzzle)
					
					"""
					Checks if heuristic is a good move and puzzle hasnt been
					seen yet. If so, updates and checks if puzzle is solved. If
					it is, returns, else adds to the queue and updates best
					heuristic
					"""
					if new_heuristic <= best_heuristic and str(new_puzzle) not in states:
						states.add(str(new_puzzle))
						best_heuristic = new_heuristic
						new_moves.append([[i, j], move])
						if new_puzzle == CORRECT_PUZZLE: return new_moves
						queue.append((new_puzzle, new_moves))
					

#works for basic puzzles, memory n!
def brute_force(puzzle):
	global CORRECT_PUZZLE
	if puzzle == CORRECT_PUZZLE: return [] #basecase
	moves = []
	queue = deque()
	queue.append((puzzle, []))
	
	while True:
		current = queue.popleft()
		puzzle, moves = current[0], current[1]
		
		#iterate over grid
		for i in range(3):
			for j in range(3):
				#generate moves
				north = [i-1, j]
				south = [i+1, j]
				east = [i, j+1]
				west = [i, j-1]
				
				p_moves = [north, south, east, west] #potential moves
				
				for move in p_moves:
					#check if valid
					if move[0] < 3 and move[0] >= 0 and move[1] < 3 and move[1] >= 0:
						#generate move, check if solved, if not add to queue
						new_puzzle = deepcopy(puzzle)
						new_moves = moves.copy()
						new_puzzle = swap(new_puzzle, [i, j], move)
						new_moves.append([[i, j], move])
						if new_puzzle == CORRECT_PUZZLE: return new_moves
						queue.append((new_puzzle, new_moves))

#shows proper coordinates of tiles
def get_tile_loc_dict():
	"""
	0---1---2
	|   |   |
	3---4---5
	|   |   |
	6---7---8
	Moves where the first position moves to a lower position ie 8 -> 5 because
	that swap is already accounted for
	"""
	tiles = {}
	tiles[0] = [0,0]
	tiles[1] = [0,1]
	tiles[2] = [0,2]
	tiles[3] = [1,0]
	tiles[4] = [1,1]
	tiles[5] = [1,2]
	tiles[6] = [2,0]
	tiles[7] = [2,1]
	tiles[8] = [2,2]
	
	return tiles

"""
determines heuristic value of puzzle by adding up how far each tile in the 
puzzle is from it's proper position
"""
def get_heuristic(puzzle):
	tile_dic = get_tile_loc_dict()
	h_sum = 0
	for i in range(3):
		for j in range(3):
			current = [i,j]
			proper = tile_dic[puzzle[i][j]]
			h_sum += abs(current[0] - proper[0]) + abs(current[1] - proper[1])
	return h_sum

#swaps tiles and returns new puzzle
def swap(puzzle, tile1, tile2):
	puzzle[tile1[0]][tile1[1]], puzzle[tile2[0]][tile2[1]] = puzzle[tile2[0]][tile2[1]], puzzle[tile1[0]][tile1[1]]
	return puzzle

#prints puzzle to console
def puzzle_printer(puzzle):
	for i in range(3):
		print(puzzle[i])

def console_solve(argv):
	puzzle = []
	row = []
	for i in range(0, len(argv)):
		row.append(int(argv[i]))
		if len(row) == 3:
			puzzle.append(row)
			row = []
	
	start_time = perf_counter()
	ans = heuristic(puzzle)
	end_time = perf_counter()
	
	#printing answer
	puzzle_printer(puzzle)
	for a in ans:
		swap(puzzle, a[0], a[1])
		print("\n" + str(puzzle[a[0][0]][a[0][1]]) + " -> " +\
		   str(puzzle[a[1][0]][a[1][1]]))
		print(a[0], "->", a[1], "\n")
		puzzle_printer(puzzle)
	print(f"Steps: {len(ans)}\n Time: {end_time - start_time}")
	
#change button text to tiles
def button_increment(button):
	num = int(button.cget('text'))
	num += 1
	if num > 8: num = 0
	button.config(text=num)
	
def gui_solve():
	#initialize GUI
	window = Tk()
	window.title("Shifting Puzzle Solver")
	
	#set up and initialize all tile buttons to 0
	tile_0_0 = Button(window, text="0", padx=40, pady=20, command=lambda: button_increment(tile_0_0))
	tile_0_1 = Button(window, text="0", padx=40, pady=20, command=lambda: button_increment(tile_0_1))
	tile_0_2 = Button(window, text="0", padx=40, pady=20, command=lambda: button_increment(tile_0_2))
	tile_1_0 = Button(window, text="0", padx=40, pady=20, command=lambda: button_increment(tile_1_0))
	tile_1_1 = Button(window, text="0", padx=40, pady=20, command=lambda: button_increment(tile_1_1))
	tile_1_2 = Button(window, text="0", padx=40, pady=20, command=lambda: button_increment(tile_1_2))
	tile_2_0 = Button(window, text="0", padx=40, pady=20, command=lambda: button_increment(tile_2_0))
	tile_2_1 = Button(window, text="0", padx=40, pady=20, command=lambda: button_increment(tile_2_1))
	tile_2_2 = Button(window, text="0", padx=40, pady=20, command=lambda: button_increment(tile_2_2))
	
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
	
	#run
	window.mainloop()

if __name__ == "__main__":
	if len(sys.argv) == 1: gui_solve()
	else: console_solve(sys.argv[2:])
	