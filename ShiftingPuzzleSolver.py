# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 21:02:26 2020

@author: Daniel
"""

#def brute_force():

def get_moves_dict():
	"""
	0---1---2
	|   |   |
	3---4---5
	|   |   |
	6---7---8
	"""
	moves = {}
	moves[0] = [1,3]
	moves[1] = [0,2,4]
	moves[2] = [1,5]
	moves[3] = [0,4,6]
	moves[4] = [1,3,5,7]
	moves[5] = [2,4,8]
	moves[6] = [3,7]
	moves[7] = [4,6,8]
	moves[8] = [5,7]
	
	return moves
	
def swap(puzzle, tile_1, tile_2):
	puzzle[tile_1], puzzle[tile_2] = puzzle[tile_2], puzzle[tile_1]
	return puzzle