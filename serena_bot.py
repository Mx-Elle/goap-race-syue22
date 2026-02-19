import heapq
import copy
from game_world.racetrack import RaceTrack
from game_world.racetrack import find_buttons
from collections import defaultdict
from collections import deque
from copy import deepcopy

Point = tuple[int, int]

def manhattan_dist(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_valid_neighbors(a: Point):
    neighbors = [(a[0] - 1, a[1]), (a[0], a[1] - 1), (a[0] + 1, a[1]), (a[0], a[1] + 1)]
    return neighbors

def make_move(track: RaceTrack, button: int): #int = color
        #makes new board of after move
        child = copy.deepcopy(track)
        child.toggle(button)
        return child


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


class State:

    def __init__(self, track: RaceTrack, parent: State, prev_button=None):
        self.parent = parent
        self.prev_button = prev_button
        self.track = track
        self.pos = track.spawn
        self.frontier = []


    def __call__(self) -> Point:
        # final boss
        # path = astar(self.pos, self.track.target, track)
        # next_pos = path[1]
        # return (next_pos[0] - self.pos[0], next_pos[1] - self.pos[1])
        for button in find_buttons(self):
            if button in self.bfs():
                self.buttons[button.color] = True
        tracker = None
        while tracker == None:
            current = self.frontier.pop()
            tracker = self.check_state()


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


def goal_state(self, track: RaceTrack) -> bool:
        #checks if state is goal state
        for x, y in astar(self.pos, track.target, track):
            if track.buttons[x][y] == 0: #no button in the way
                return True
        return False


    def check_state(self, track: RaceTrack):
        if self.goal_state(track):
            return track
        for button in track.find_buttons(track, None):
            if button in self.bfs(track):
                new_state = State(make_move(track, button))
                self.frontier.append(new_state)
        return None


def main(current: State, track: RaceTrack):
    # retrace my steps to first parent
    frontier = []
    button_path = []
    current = State(track, None, None)
    while current.parent != None:
        button_path.append(current.prev_button)
        current = current.parent

