# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 21:06:26 2020

@author: Daniel
"""

import unittest
import ShiftingPuzzleSolver as SPS

class TestSwap(unittest.TestCase):
	test_puzzle = []
	for i in range(5):
		test_puzzle.append(i)
	
	def test_basic(self):
		valid_tile_1, valid_tile_2 = 2, 3
		test_puzzle = SPS.swap(TestSwap.test_puzzle, valid_tile_1, valid_tile_2)
		key = [0, 1, 3, 2, 4]
		self.assertEqual(test_puzzle, key)
		
	def test_input_tiles(self):
		valid_tile = 2
		invalid_tile_1 = -1 #out of range
		invalid_tile_2 = 6 #out of range
		invalid_tile_3 = 'why, hello there' #wrong input type
		test_tiles = [invalid_tile_1, invalid_tile_2, invalid_tile_3]
		for test in test_tiles:
			self.assertEqual(SPS.swap(self.test_puzzle, test, valid_tile), None)
			self.assertEqual(SPS.swap(self.test_puzzle, valid_tile, test), None)
		

if __name__ == '__main__':
	unittest.main()