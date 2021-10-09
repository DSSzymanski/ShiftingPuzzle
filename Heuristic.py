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
from collections import deque
from copy import deepcopy

def heuristic(puzzle):
    """
    Heuristic takes in puzzle and uses a queue to find the shortest path through
    the shifting puzzle. The puzzle is examined to find every possible move and
    a new puzzle is generated with each move and if it has a lower or equal
    heuristic value to the current best, adds it that puzzle to the queue. Once
    a puzzle is found with a completed board, it is returned with the moves stored
    inside of it.

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
    queue = deque()
    queue.append(puzzle)
    found_states = set()

    #used to weed out moves that result in a worst heuristic value
    curr_heuristic = _get_heuristic(puzzle.get_puzzle_state())

    while True:
        puzzle_state = queue.popleft()

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


                    #Checks if heuristic is a good move and puzzle hasnt been
                    #seen yet. If so, updates and checks if puzzle is solved. If
                    #it is, returns, else adds to the queue and updates best
                    #heuristic
                    if new_heuristic <= curr_heuristic and \
                        str(new_puzzle.get_puzzle_state()) not in found_states:
                        found_states.add(str(new_puzzle.get_puzzle_state()))
                        curr_heuristic = new_heuristic
                        new_puzzle.add_move([[i, j], move])
                        if new_puzzle.puzzle_check():
                            return new_puzzle
                        queue.append(new_puzzle)

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
    tiles[0] = [0,0]
    tiles[1] = [0,1]
    tiles[2] = [0,2]
    tiles[3] = [1,0]
    tiles[4] = [1,1]
    tiles[5] = [1,2]
    tiles[6] = [2,0]
    tiles[7] = [2,1]
    tiles[8] = [2,2]

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
