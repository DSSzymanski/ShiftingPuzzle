# -*- coding: utf-8 -*-
"""
Created on Sat May 16 19:00:22 2020

@author: Daniel
"""
from time import perf_counter
import Heuristic as H
from Puzzle import puzzle_printer, swap, puzzle_converter

def console_solve(argv):
	puzzle = puzzle_converter(argv)

	start_time = perf_counter()
	ans = H.heuristic(puzzle)
	end_time = perf_counter()
	
	#printing answer
	puzzle_printer(puzzle)
	for a in ans:
		swap(puzzle, a[0], a[1])
		print("\n" + "Tile: " + str(puzzle[a[0][0]][a[0][1]]) + " -> " +\
		   str(puzzle[a[1][0]][a[1][1]]))
		print("Location: ", a[0], "->", a[1], "\n")
		print("State:")
		puzzle_printer(puzzle)
	print(f"\nSteps: {len(ans)}\nTime: {end_time - start_time}")
