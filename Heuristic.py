# -*- coding: utf-8 -*-
"""
Created on Mon May 11 16:13:00 2020

@author: Daniel
"""

import Puzzle
from collections import deque
from copy import deepcopy

#puzzle solver based on heuristics
def heuristic(puzzle):
	#base case
	if Puzzle.puzzle_check(puzzle) == True: return []
	
	#initialize data structures
	moves = []
	queue = deque()
	queue.append((puzzle, [], get_heuristic(puzzle)))
	found_states = set()
	
	#used to weed out moves that result in a worst heuristic value
	curr_heuristic = get_heuristic(puzzle)
	
	while True:
		current = queue.popleft()
		puzzle, moves = current[0], current[1]
		
		#loop used to generate every move from every tile location
		for i in range(3):
			for j in range(3):
				#used to store potential moves for each tile
				p_moves = generate_moves(i,j)
				
				#Iterates over all valid moves generated for the tile
				for move in p_moves:
					#create new puzzle & move lists & completes move
					#and evaluates new heuristic
					new_puzzle = deepcopy(puzzle)
					new_moves = moves.copy()
					new_puzzle = Puzzle.swap(new_puzzle, [i, j], move)
					new_heuristic = get_heuristic(new_puzzle)
					
					"""
					Checks if heuristic is a good move and puzzle hasnt been
					seen yet. If so, updates and checks if puzzle is solved. If
					it is, returns, else adds to the queue and updates best
					heuristic
					"""
					if new_heuristic <= curr_heuristic and str(new_puzzle) not in found_states:
						found_states.add(str(new_puzzle))
						curr_heuristic = new_heuristic
						new_moves.append([[i, j], move])
						if Puzzle.puzzle_check(new_puzzle): return new_moves
						queue.append((new_puzzle, new_moves))


#Generates all moves from the tile location.
def generate_moves(x_cord, y_cord):
	moves = []
	
	#north
	if x_cord != 0: 
		moves.append([x_cord-1, y_cord])
	#south
	if x_cord != 2:
		moves.append([x_cord+1, y_cord])
	#east
	if y_cord != 2:
		moves.append([x_cord, y_cord+1])
	#west
	if y_cord != 0:
		moves.append([x_cord, y_cord-1])
	
	return moves
						
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

"""
Old brute force that was used to test
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
						new_puzzle = Puzzle.swap(new_puzzle, [i, j], move)
						new_moves.append([[i, j], move])
						if new_puzzle == CORRECT_PUZZLE: return new_moves
						queue.append((new_puzzle, new_moves))
"""