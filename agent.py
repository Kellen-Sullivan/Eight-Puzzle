from __future__ import annotations
from board import Board
from collections.abc import Callable
import heapq
import itertools

MAX_NODES_SEARCHED = 50000

'''
Heuristics
'''
def MT(board: Board) -> int:
    # given a board state, returns the number of misplaced tiles.
    misplaced_tiles = 0
    for i in range(3):
        for j in range(3):
            if board.state[i,j] != 0 and board.state[i,j] != (i*3) + j + 1:
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
    goal_locations = {1:(0,0), 2:(0,1), 3:(0,2), 4:(1,0), 5:(1,1), 6:(1,2), 7:(2,0), 8:(2,1)}
    city_block_distance = 0
    
    empty = (None, None)
    # Find empty location
    for i in range(3):
        for j in range(3):
            if board.state[i,j] == 0: # if empty space continue
                empty = (i, j)
                continue
    
    dists_from_empty = [False for _ in range(5)]
    for i in range(3):
        for j in range(3):
            if board.state[i,j] == 0: # if empty space continue
                continue
            city_block_distance += abs(i - goal_locations[board.state[i,j]][0]) + abs(j - goal_locations[board.state[i,j]][1]) # add dif in x and dif in y to city_block_distance sum

            moveable_positions = []
            #check and add moveable x position
            if i > goal_locations[board.state[i,j]][0]:
                moveable_positions.append((i-1, j))
            elif i < goal_locations[board.state[i,j]][0]:
                moveable_positions.append((i+1, j))
            #check and add moveable y position
            if j > goal_locations[board.state[i,j]][1]:
                moveable_positions.append((i, j-1))
            elif j < goal_locations[board.state[i,j]][1]:
                moveable_positions.append((i, j+1))
            
            if len(moveable_positions) > 0:
                # Finds the distances between the positions the tile could make a 
                # positive move too and the emptry spaces current position
                min_dist = 4 # 4 is the max value empty can be from a positive moveable position
                for i, j in moveable_positions:
                    curr_dist = abs(i - empty[0]) + abs(j - empty[1])
                    if curr_dist < min_dist:
                        min_dist = curr_dist
                
                # add current distance to distance from empty array
                dists_from_empty[min_dist] = True
    

    # Sum up how many moves the empty space will make that can't move a block in a 
    # positive direction and will move one in a negative direction
    curr_count = 0
    total_count = 0
    for d in dists_from_empty:
        if d:
            total_count += curr_count
            curr_count = 0
        else:
            curr_count += 1

    return city_block_distance + (total_count * 2)



'''
A* Search 
'''
def a_star_search(board: Board, heuristic: Callable[[Board], int]):
    h = 0   # initialize heuristic
    if heuristic is not None: # set h to heuristic value if not None
        h = heuristic(board)

    counter = itertools.count() # use this to make sure each value in heapq is unique, so board doesn't compare with board
    pq = [(h, 0, next(counter), board, "")] # (f:(dist total: h + g), g:(dist from start), board, path)
    visited = set() # set to keep track of already visited board states

    curr = board
    path = None
    while not curr.goal_test(): # Also set max limit on time or nodes searched
        f, g, c, curr, path = heapq.heappop(pq)
        # check if curr board is already in 
        if curr in visited:
            continue
        board_state_tuple = curr.state.tobytes() # convert the board state (which is a numpy arr) into bytes, so that it is hashable and can be stored in the visited set
        visited.add(board_state_tuple)
        # stop search if nodes searched is greater than MAX_NODES_SEARCHED
        if c > MAX_NODES_SEARCHED:
            print(f"Searched {MAX_NODES_SEARCHED} and found no solution")
            return -1
        for b, move in curr.next_action_states():
            b_state_tuple = b.state.tobytes()
            if b_state_tuple in visited:
                continue
            if heuristic is not None: # set h to heuristic value if not None
                h = heuristic(b)
            heapq.heappush(pq, (g+1 + h, g+1, next(counter), b, path + " " + move + " "))

    return path.split()
