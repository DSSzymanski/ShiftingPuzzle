# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 21:02:26 2020
@author: Daniel
"""
from collections import deque
from time import perf_counter
from copy import deepcopy
import sys

CORRECT_PUZZLE = [
	[0,1,2],
	[3,4,5],
	[6,7,8]]

#works for basic puzzles, memory n!
def heuristic(puzzle):
	global CORRECT_PUZZLE
	
	if puzzle == CORRECT_PUZZLE: return [] #basecase
	
	moves = []
	queue = deque()
	queue.append((puzzle, [], get_heuristic(puzzle)))
	
	states = set()
	
	#used to weed out bad moves
	best_heuristic = get_heuristic(puzzle)
	
	while True:
		current = queue.popleft()
		puzzle, moves = current[0], current[1]
		
		#iterate over grid
		for i in range(3):
			for j in range(3):
				p_moves = [] #potential moves
				#generate moves
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
				
				for move in p_moves:
					#generate move, check if solved, if not add to queue
					new_puzzle = deepcopy(puzzle)
					new_moves = moves.copy()
					
					new_puzzle = swap(new_puzzle, [i, j], move)
					new_heuristic = get_heuristic(new_puzzle)
					
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
determines heuristic value of puzzle by adding up how far each tile is from 
it's proper position
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

#prints puzzle
def puzzle_printer(puzzle):
	for i in range(3):
		print(puzzle[i])

def main(argv):
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
	
if __name__ == "__main__":
	main(sys.argv[1:])