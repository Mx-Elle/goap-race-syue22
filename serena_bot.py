import heapq
import copy
from game_world.racetrack import RaceTrack
from collections import defaultdict
from collections import deque
from copy import deepcopy

Point = tuple[int, int]

def manhattan_dist(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_valid_neighbors(a: Point):
    neighbors = [(a[0] - 1, a[1]), (a[0], a[1] - 1), (a[0] + 1, a[1]), (a[0], a[1] + 1)]
    return neighbors

class State:

    def __init__(self, track: RaceTrack):
        self.doors = dict() # bool & color as a tuple
        self.track = track
        self.buttons = dict()
        self.pos = track.spawn
        self.buttons = {} # color, bool (reachable)
        self.doors = {}
        self.children = [track]


    def bfs(self, child): #finds all visitable cells
        frontier = deque([self.pos])
        visited = set([self.pos])
        
        while frontier:
            current = frontier.popleft()

            for neighbor in find_valid_neighbors(current):
                if (neighbor in self.track.find_traversable_cells() and neighbor not in visited):
                    visited.add(neighbor)
                    frontier.append(neighbor)
        return visited


    def make_move(self, button):
        child = copy.deepcopy(self.track)
        child.toggle(button)
        return child


    def state(self):
        # make new states. loop. check if state is new. if so, add to list.
        for button in self.buttons.values():
            if button == True:
                new_state = self.make_move(button)
                self.children.append(new_state)
                
        

    def astar(self, start: Point, end: Point) -> list[Point] | None:
        start_cell, end_cell = start, end
        closed_list = set()
        if not start_cell or not end_cell:
            return None
        g_scores = defaultdict(lambda: float("inf"))
        g_scores[start_cell] = 0
        f_scores = defaultdict(lambda: float("inf"))
        f_scores[start_cell] = State.manhattan_dist(start_cell, end_cell)

        frontier = [(f_scores[start_cell], start_cell)]
        prev: dict[Point, Point | None] = {start_cell: None}

        while True:
            _, current_cell = heapq.heappop(frontier)
            if current_cell == end_cell:
                break
            for neighbor in find_valid_neighbors(current_cell):
                if not neighbor in self.track.find_traversable_cells():
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



    def smart_move(self) -> Point:
        # path = self.astar(self.pos, self.track.target)
        # next_pos = path[1]
        # return (next_pos[0] - self.pos[0], next_pos[1] - self.pos[1])
        for button in self.track.buttons:
            if button in self.bfs():
                self.buttons[button.color] = True
        for door in self.track.doors:
            if door in self.bfs():
                self.doors[door.color] = True