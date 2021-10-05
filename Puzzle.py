from collections import Counter
from copy import deepcopy

class Puzzle:
    def __init__(self, puzzle, moves=[]):
        self.puzzle = puzzle
        self.correct_puzzle = self._get_correct()
        self.soln_states = [deepcopy(self.puzzle)]
        self.moves = moves

    def _get_correct(self):
        return [
            [0,1,2],
            [3,4,5],
            [6,7,8]
        ]

    def get_puzzle_state(self):
        return self.puzzle

    def get_copy(self):
        return self.puzzle, self.moves

    #Checks if puzzle is solved
    def puzzle_check(self):
        return self.puzzle == self.correct_puzzle

    #inputs list, ensures values are 0-8 in some order
    @staticmethod
    def validate(puzzle_input):
        valid_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        return Counter(puzzle_input) == Counter(valid_list)
    
    def add_move(self, move):
        self.moves.append(move)
    
    @staticmethod
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
    def swap(self, tile1, tile2):
        self.puzzle[tile1[0]][tile1[1]], self.puzzle[tile2[0]][tile2[1]] = \
               self.puzzle[tile2[0]][tile2[1]], self.puzzle[tile1[0]][tile1[1]]

    #prints puzzle to console
    def puzzle_printer(self):
        for i in range(3):
            print(self.puzzle[i])

    #converts a solution of coordinate swaps into a list of individual puzzle states
    #that represent solution
    def state_maker(self):
        #set puzzle to initial state
        self.puzzle = deepcopy(self.soln_states[0])
        for step in self.moves:
            self.swap(step[0], step[1])
            self.soln_states.append(deepcopy(self.puzzle))
            
        return self.soln_states
