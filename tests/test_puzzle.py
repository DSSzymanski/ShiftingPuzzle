import unittest
import random
from puzzle import Puzzle

class TestPuzzleValidate(unittest.TestCase):
    def test_valid_input(self):
        valid_input = [0,1,2,3,4,5,6,7,8]
        self.assertTrue(Puzzle.validate(valid_input))
        for _ in range(5):
            random.shuffle(valid_input)
            self.assertTrue(Puzzle.validate(valid_input))

    def test_invalid_duplicate_inputs(self):
        self.assertFalse(Puzzle.validate([1,1,2,3,4,5,6,7,8]))
        
    def test_invalid_too_many_inputs(self):
        self.assertFalse(Puzzle.validate([x for x in range(10)]))
    
    def test_invalid_too_few_inputs(self):
        self.assertFalse(Puzzle.validate([x for x in range(8)]))
    
    def test_invalid_empty_input(self):
        self.assertFalse(Puzzle.validate([]))

class TestPuzzleCreation(unittest.TestCase):
    def setUp(self):
        self.before = [x for x in range(9)]
        self.puzzle = Puzzle(self.before)
        self.converted = [
            [0,1,2],
            [3,4,5],
            [6,7,8]
        ]
    
    def test_correct_conversion(self):
        self.assertEqual(self.puzzle.puzzle, self.converted)
        
    def test_incorrect_conversion(self):
        self.assertNotEqual(self.puzzle.puzzle, self.before)
        
    def test_soln_state_init(self):
        self.assertIsNotNone(self.puzzle.soln_states)
        self.assertEqual(self.puzzle.puzzle, self.puzzle.soln_states[0])
        self.assertEqual(len(self.puzzle.soln_states), 1)

class TestPuzzleComparison(unittest.TestCase):
    def setUp(self):
        self.puzzle1 = Puzzle([x for x in range(9)])
        self.puzzle2 = Puzzle([x for x in range(9)])
        self.move = [[0,0],[1,1]]

    def test_equal_moves(self):
        self.assertFalse(self.puzzle1 < self.puzzle2)
        
    def test_against_more_moves(self):
        self.puzzle2.add_move(self.move)
        self.assertTrue(self.puzzle1 < self.puzzle2)
        
    def test_against_less_moves(self):
        self.puzzle1.add_move(self.move)
        self.assertFalse(self.puzzle1 < self.puzzle2)

class TestPuzzlePuzzleCheck(unittest.TestCase): 
    def test_completed_state(self):
        puzzle = Puzzle([1,2,3,4,5,6,7,8,0])
        self.assertTrue(puzzle.puzzle_check())
        
    def test_incomplete_state(self):
        puzzle_input = [x for x in range(9)]
        for _ in range(10):
            while puzzle_input == [1,2,3,4,5,6,7,8,0]:
                random.shuffle(puzzle_input)
            puzzle = Puzzle(puzzle_input)
            self.assertFalse(puzzle.puzzle_check())


if __name__ == '__main__':
    unittest.main()
