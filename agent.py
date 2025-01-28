from __future__ import annotations
from board import Board
from collections.abc import Callable


'''
Heuristics
'''
def MT(board: Board) -> int:
    # given a board state, returns the number of misplaced tiles.
    misplaced_tiles = 0
    for i in range(3):
        for j in range(3):
            if board.state[i,j] != (i*3) + j + 1:
                misplaced_tiles+=1
    return misplaced_tiles

def CB(board: Board) -> int:
    # returns the sum of city-block distance for each tile from its goal location
    goal_locations = {1:(0,0), 2:(0,1), 3:(0,2), 4:(1,0), 5:(1,1), 6:(1,2), 7:(2,0), 8:(2,1)}
    city_block_distance = 0
    for i in range(3):
        for j in range(3):
            if board.state[i,j] == 0: # if empty space continue
                continue
            city_block_distance += abs(i - goal_locations[board.state[i,j]][0]) + abs(j - goal_locations[board.state[i,j]][1]) # add dif in x and dif in y to city_block_distance sum
    return city_block_distance


def NA(board: Board) -> int:
    return 



'''
A* Search 
'''
def a_star_search(board: Board, heuristic: Callable[[Board], int]):
    return
