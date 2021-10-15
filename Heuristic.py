"""
Heuristic is the module that is in control of solving hte puzzles. The heuristic
model finds the optimal path to the solution using heuristics and breadth first
search to find the answer.

Usage
-----
With a valid puzzle object, call heuristic() with your puzzle as input. The
heuristic algorithm will search and return a puzzle with the optimal solution.
You can get a list containing the solution set of states by calling the returned
puzzle's get_soln_states() function.

Methods
------
heuristic(Puzzle puzzle) -> Puzzle:
    main function called to solve the shifting puzzle. returns a puzzle with
    completed steps stored inside.
_generate_moves(int x_cord, int y_cord) -> list[list[int]]:
    returns a list of valid moves from the position (x_cord, y_cord).
_get_tile_loc_dict() -> dict:
    returns a dict maping the correct numbers that are in position position (x,y).
_get_heuristic(Puzzle puzzle) -> int:
    returns the heuristic value indicating how close a state is to being complete.

"""
import queue as Q
from copy import deepcopy

def bfs_shift(puzzle, button=None):
    """
    Main function to run the shifting puzzle. Function takes in a Puzzle object
    and runs BFS on it's state to find the optimal solution. If no solution exists,
    function will run until it examines every possible state. Adds [-1] to puzzle
    moves if no solution exists.

    Parameters
    ----------
    puzzle : Puzzle
        initial puzzle configuration to begin searching.

    Returns
    -------
    Puzzle
        Returns puzzle with moves/solution state attributes filled.

    """
    #base case
    if puzzle.puzzle_check() is True:
        return puzzle

    #initialize data structures
    queue = Q.Queue()
    queue.put(puzzle)
    found_states = set(str(puzzle.get_puzzle_state()))
    #bfs for solution state
    while not queue.empty():
        puzzle = queue.get()
        zero = puzzle.get_zero_pos()
        moves = _generate_moves(zero[0], zero[1])
        for move in moves:
            if button:
                button['text'] = len(found_states)
            new_puzzle = deepcopy(puzzle)
            new_puzzle.swap(zero, move)

            #if state already seen, continue to next state
            if str(new_puzzle.get_puzzle_state()) in found_states:
                continue

            new_puzzle.add_move([zero, move])
            if new_puzzle.puzzle_check():
                return new_puzzle
            queue.put(new_puzzle)
            found_states.add(str(new_puzzle.get_puzzle_state()))
    puzzle.add_move([-1])
    return puzzle

def heuristic_swap(puzzle):
    """
    Heuristic takes in puzzle and uses a queue to find the shortest path through
    the puzzle by swapping any tiles. The puzzle is examined to find every
    possible move and a new puzzle is generated with each move. If the puzzle
    hasn't been seen yet, it adds the puzzle and it's heuristic value to the
    priority queue. Once a puzzle is found with a completed board, it is
    returned with the moves stored inside of it.

    Parameters
    ----------
    puzzle : Puzzle
        puzzle at current state (2d list of ints).

    Returns
    -------
    Puzzle
        Returns a puzzle that has been solved using heuristics.

    """
    #base case
    if puzzle.puzzle_check() is True:
        return puzzle

    #initialize data structures
    queue = Q.PriorityQueue()
    queue.put((0, puzzle))
    found_states = set()

    while True:
        _, puzzle_state = queue.get()

        #loop used to generate every move from every tile location
        for i in range(3):
            for j in range(3):
                #used to store potential moves for each tile
                p_moves = _generate_moves(i,j)

                #Iterates over all valid moves generated for the tile
                for move in p_moves:
                    #create new puzzle & move lists & completes move
                    #and evaluates new heuristic
                    new_puzzle = deepcopy(puzzle_state)
                    new_puzzle.swap([i, j], move)
                    new_heuristic = _get_heuristic(new_puzzle.get_puzzle_state())

                    if str(new_puzzle.get_puzzle_state()) in found_states:
                        continue
                    found_states.add(str(new_puzzle.get_puzzle_state()))
                    new_puzzle.add_move([[i, j], move])
                    if new_puzzle.puzzle_check():
                        return new_puzzle
                    queue.put((new_heuristic, new_puzzle))

def _generate_moves(x_cord, y_cord):
    """
    Generates all moves from x,y location.

    Parameters
    ----------
    x_cord : int
        int representing x coordinate in the puzzle grid.
    y_cord : int
        int representing x coordinate in the puzzle grid.

    Returns
    -------
    moves : list[list[int]]
        returns a list of coordinate ints of tiles that tile x_cord, y_cord can
        move to.

    """
    moves = []

    #north
    if x_cord != 0:
        moves.append([x_cord-1, y_cord])
    #south
    if x_cord != 2:
        moves.append([x_cord+1, y_cord])
    #east
    if y_cord != 2:
        moves.append([x_cord, y_cord+1])
    #west
    if y_cord != 0:
        moves.append([x_cord, y_cord-1])

    return moves

def _get_tile_loc_dict():
    """
    Method to get a lookup dictionary to find where a tile number should be by
    using a completed puzzle as a reference.
    0---1---2
    |   |   |
    3---4---5
    |   |   |
    6---7---8

    Parameters
    ----------
    None

    Returns
    -------
    tiles : dict[int] -> list[int]
        returns a lookup dict for where each tile should be.
    """
    tiles = {}
    tiles[1] = [0,0]
    tiles[2] = [0,1]
    tiles[3] = [0,2]
    tiles[4] = [1,0]
    tiles[5] = [1,1]
    tiles[6] = [1,2]
    tiles[7] = [2,0]
    tiles[8] = [2,1]
    tiles[0] = [2,2]

    return tiles

def _get_heuristic(puzzle):
    """
    Determines heuristic value of puzzle by adding up how far each tile in the
    puzzle is from it's proper position.

    Parameters
    ----------
    puzzle : list[list[int]] (state not puzzle class)
        puzzle at current state (2d list of ints).

    Returns
    -------
    h_sum : int
        returns heuristic for current puzzle state.
    """
    tile_dic = _get_tile_loc_dict()
    h_sum = 0
    for i in range(3):
        for j in range(3):
            proper = [i,j] #what should lie at (i,j)
            current = tile_dic[puzzle[i][j]] #what actually lies at (i,j)
            #add x and y distances of tile to proper to heuristic
            h_sum += abs(current[0] - proper[0]) + abs(current[1] - proper[1])
    return h_sum
