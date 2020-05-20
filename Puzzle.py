# -*- coding: utf-8 -*-
"""
Created on Mon May 11 13:31:17 2020

@author: Daniel
"""
from collections import Counter
from copy import deepcopy

#Correct puzzle format
CORRECT_PUZZLE = [
	[0,1,2],
	[3,4,5],
	[6,7,8]
]

#Checks if puzzle is solved
def puzzle_check(puzzle):
	if puzzle == CORRECT_PUZZLE: return True
	return False

#inputs list, ensures values are 0-8 in some order
def validate(puzzle_input):
	valid_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
	return True if Counter(puzzle_input) == Counter(valid_list) else False

def puzzle_converter(args):
	puzzle = []
	row = []
	for i in range(0, len(args)):
		row.append(int(args[i]))
		if len(row) == 3:
			puzzle.append(row)
			row = []
	return puzzle

#swaps tiles and returns new puzzle
def swap(puzzle, tile1, tile2):
	puzzle[tile1[0]][tile1[1]], puzzle[tile2[0]][tile2[1]] = puzzle[tile2[0]][tile2[1]], puzzle[tile1[0]][tile1[1]]
	return puzzle

#prints puzzle to console
def puzzle_printer(puzzle):
	for i in range(3):
		print(puzzle[i])
	
#converts a solution of coordinate swaps into a list of individual puzzle states
#that represent solution
def state_maker(init_puzzle, solution):
	states = [init_puzzle]
	curr_puzzle = deepcopy(init_puzzle)
	for step in solution:
		curr_puzzle = deepcopy(curr_puzzle)
		swap(curr_puzzle, step[0], step[1])
		states.append(curr_puzzle)
	return states