# -*- coding: utf-8 -*-
"""
Created on Mon May 11 13:31:17 2020

@author: Daniel
"""
from collections import Counter

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
	valid_list = [0, 1, 2, 3,4, 5, 6, 7, 8]
	return True if Counter(puzzle_input) == Counter(valid_list) else False

#swaps tiles and returns new puzzle
def swap(puzzle, tile1, tile2):
	puzzle[tile1[0]][tile1[1]], puzzle[tile2[0]][tile2[1]] = puzzle[tile2[0]][tile2[1]], puzzle[tile1[0]][tile1[1]]
	return puzzle

#prints puzzle to console
def puzzle_printer(puzzle):
	for i in range(3):
		print(puzzle[i])