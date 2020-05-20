# -*- coding: utf-8 -*-
"""
Created on Sat May 16 19:00:22 2020

@author: Daniel
"""
from time import perf_counter
import Heuristic as H
import Puzzle

def console_solve(argv):
	puzzle = split_input(argv)

	start_time = perf_counter()
	ans = H.heuristic(puzzle)
	end_time = perf_counter()
	
	#printing answer
	Puzzle.puzzle_printer(puzzle)
	for a in ans:
		Puzzle.swap(puzzle, a[0], a[1])
		print("\n" + "Tile: " + str(puzzle[a[0][0]][a[0][1]]) + " -> " +\
		   str(puzzle[a[1][0]][a[1][1]]))
		print("Location: ", a[0], "->", a[1], "\n")
		print("State:")
		Puzzle.puzzle_printer(puzzle)
	print(f"\nSteps: {len(ans)}\nTime: {end_time - start_time}")
	
def split_input(args):
	puzzle = []
	row = []
	for i in range(0, len(args)):
		row.append(int(args[i]))
		if len(row) == 3:
			puzzle.append(row)
			row = []
	return puzzle
