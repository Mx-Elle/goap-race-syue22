import heapq
import copy
from game_world.racetrack import RaceTrack
from collections import defaultdict
from collections import deque
from copy import deepcopy

"""
    Note: This only works for tracks that don't have buttons. I suspect that astar is taking the final
    target (track.target) as the target instead of the next button as the target. Unfortunately, due to
    squash nationals (I've learned I can't work on a bus unless I want motion sickness) I couldn't finish
    debugging before the deadline.
"""

Point = tuple[int, int]
button_path = None

class State:

    def __init__(self, track: RaceTrack, parent: RaceTrack, prev_button: set):
        self.parent = parent
        self.prev_button = prev_button
        self.track = track
        self.pos = track.spawn
        self.frontier = []

def manhattan_dist(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_valid_neighbors(a: Point):
    neighbors = [(a[0] - 1, a[1]), (a[0], a[1] - 1), (a[0] + 1, a[1]), (a[0], a[1] + 1)]
    return neighbors

def make_move(track: RaceTrack, button: int): #int = color
        #makes new board of after move
        new_track = copy.deepcopy(track)
        new_track.toggle(button)
        return new_track


def astar(start: Point, end: Point, track: RaceTrack) -> list[Point] | None:
        start_cell, end_cell = start, end
        closed_list = set()
        if not start_cell or not end_cell:
            return None
        g_scores = defaultdict(lambda: float("inf"))
        g_scores[start_cell] = 0
        f_scores = defaultdict(lambda: float("inf"))
        f_scores[start_cell] = manhattan_dist(start_cell, end_cell)

        frontier = [(f_scores[start_cell], start_cell)]
        prev: dict[Point, Point | None] = {start_cell: None}

        while True:
            _, current_cell = heapq.heappop(frontier)
            if current_cell == end_cell:
                break
            for neighbor in find_valid_neighbors(current_cell):
                if not neighbor in track.find_traversable_cells():
                    continue

                if neighbor in closed_list:
                    continue

                temp_g = g_scores[current_cell] + 1
                if temp_g < g_scores[neighbor]:
                    g_scores[neighbor] = temp_g
                    f_scores[neighbor] = temp_g + manhattan_dist(neighbor, end_cell)
                    prev[neighbor] = current_cell
                    if neighbor not in closed_list:
                        heapq.heappush(frontier, (f_scores[neighbor], neighbor))

            closed_list.add(current_cell)

        path = []
        key = end_cell
        while key != None:
            path.append(key)
            key = prev[key]
        return path[::-1]


def bfs(curr: State, track: RaceTrack):
        #finds all visitable cells
        frontier = deque([curr.pos])
        visited = set([curr.pos])
        
        while frontier:
            current = frontier.popleft()

            for neighbor in find_valid_neighbors(current):
                if (neighbor in track.find_traversable_cells() and neighbor not in visited):
                    visited.add(neighbor)
                    frontier.append(neighbor)
        return visited


def goal_state(curr: State, track: RaceTrack) -> bool:
        #checks if state is goal state
        for x, y in astar(curr.pos, track.target, track):
            if track.buttons[x][y] == 0: #no button in the way
                return True
        return False


def check_state(curr: State, track: RaceTrack, frontier: list):
    if goal_state(curr, track):
        return track
    for button in track.find_buttons(None):
        if button in bfs(curr, track):
            child = State(make_move(track, button), curr, button)
            frontier.append(child)
    return None


def main(track: RaceTrack):
    b_path = []
    root = State(track, None, None)
    frontier = [root]
    current = root
    while frontier:
        current = frontier.pop()
        if check_state(current, current.track, frontier) is not None:
             break

    # retrace my steps to root
    while current.parent != None:
        b_path.append(current.prev_button)
        current = current.parent

    return b_path[::-1]

def act(loc: Point, track: RaceTrack):
    button_path = main(track)
    if button_path is None:
         button_path = main(track)
    if not button_path:
         step = astar(loc, track.target, track)[1]
         return (step[0]-loc[0], step[1]-loc[1])
    next_button = button_path[0]
    if loc == next_button:
         button_path.pop(0)
    path = astar(loc, next_button, track)
    step = path[1]
    return (step[0]-loc[0], step[1]-loc[1])
