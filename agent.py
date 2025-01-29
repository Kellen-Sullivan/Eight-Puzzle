from __future__ import annotations
from board import Board
from collections.abc import Callable
import heapq
import itertools


'''
Heuristics
'''
def MT(board: Board) -> int:
    # given a board state, returns the number of misplaced tiles.
    misplaced_tiles = 0
    for i in range(3):
        for j in range(3):
            if board.state[i,j] == 0: # don't add a misplaced tile if its the empty tile
                continue
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
    h = 0   # initialize heuristic
    if heuristic is not None: # set h to heuristic value if not None
        h = heuristic(board)

    counter = itertools.count() # use this to make sure each value in heapq is unique, so board doesn't compare with board
    pq = [(h, 0, next(counter), board, "")] # (f:(dist total: h + g), g:(dist from start), board, path)

    curr = board
    path = None
    while not curr.goal_test(): # Also set max limit on time or nodes searched
        f, g, _, curr, path = heapq.heappop(pq)
        g + 1

        for b, move in curr.next_action_states():
            if heuristic is not None: # set h to heuristic value if not None
                h = heuristic(b)
            heapq.heappush(pq, (g + h, g, next(counter), b, path + " " + move + " "))

    return path.split()
