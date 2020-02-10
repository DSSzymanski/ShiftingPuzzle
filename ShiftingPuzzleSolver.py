# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 21:02:26 2020
@author: Daniel
"""
from collections import deque

CORRECT_PUZZLE = [1,2,3,4,5,6,7,8,9]

def brute_force(puzzle):
	global CORRECT_PUZZLE
	if puzzle == CORRECT_PUZZLE: return [] #basecase
	move_dict = get_moves_dict()
	queue = deque()
	queue.append((puzzle, []))
	
	while True:
		current = queue.popleft()
		puzzle, moves = current[0], current[1]
		for i in range(9):
			for j in move_dict[i]:
				new_moves = moves.copy()
				new_moves.append((i,j))
				new_puzzle = puzzle.copy()
				new_puzzle = swap(new_puzzle, i, j)
				if new_puzzle == CORRECT_PUZZLE: return new_moves
				queue.append((new_puzzle, new_moves))

def get_moves_dict():
	"""
	0---1---2
	|   |   |
	3---4---5
	|   |   |
	6---7---8
	Moves where the first position moves to a lower position ie 8 -> 5 because
	that swap is already accounted for
	"""
	moves = {}
	moves[0] = [1,3]
	moves[1] = [2,4]
	moves[2] = [5]
	moves[3] = [4,6]
	moves[4] = [3,5,7]
	moves[5] = [8]
	moves[6] = [7]
	moves[7] = [8]
	moves[8] = []
	
	return moves
	
def swap(puzzle, tile_1, tile_2):
	puzzle[tile_1], puzzle[tile_2] = puzzle[tile_2], puzzle[tile_1]
	return puzzle

