# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 21:06:26 2020

@author: Daniel
"""

import unittest
import ShiftingPuzzleSolver as SPS
5
class TestSwap(unittest.TestCase):
	test_puzzle = []
	for i in range(5):
		test_puzzle.append(i)
	
	def test_basic(self):
		valid_tile_1, valid_tile_2 = 2, 3
		test_puzzle = SPS.swap(TestSwap.test_puzzle, valid_tile_1, valid_tile_2)
		key = [0, 1, 3, 2, 4]
		self.assertEqual(test_puzzle, key)
		
	"""
	def test_input_tiles(self):
		valid_tile = 2
		invalid_tile_1 = -1 #out of range
		invalid_tile_2 = 6 #out of range
		invalid_tile_3 = 'why, hello there' #wrong input type
		test_tiles = [invalid_tile_1, invalid_tile_2, invalid_tile_3]
		for test in test_tiles:
			self.assertEqual(SPS.swap(self.test_puzzle, test, valid_tile), None)
			self.assertEqual(SPS.swap(self.test_puzzle, valid_tile, test), None)
	"""
	
class TestBruteForce(unittest.TestCase):
	def test_puzzles(self):
		#TP# = TestPuzzle(number), AP# = AnswerPuzzle(number)
		TP1 = [1,2,3,4,5,6,7,8,9] #should return []
		AP1 = []
		TP2 = [2,1,3,4,5,6,7,8,9] #tests 1 swap in same row
		AP2 = [(0,1)]
		TP3 = [2,1,3,5,4,6,8,7,9] #tests 1 swap in row for all rows
		AP3 = [(0,1),(3,4),(6,7)]
		TP4 = [4,2,3,1,5,6,7,8,9] #tests horizontal swap
		AP4 = [(0,3)]
		tests = [TP1, TP2, TP3, TP4]
		answers = [AP1, AP2, AP3, AP4]
		for i in range(len(tests)):
			self.assertEqual(SPS.brute_force(tests[i]), answers[i])	

if __name__ == '__main__':
	unittest.main()