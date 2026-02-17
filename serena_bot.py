from game_world.racetrack import RaceTrack
from collections import defaultdict
import heapq

Point = tuple[int, int]

class State:

    def __init__(self, loc: Point, track: RaceTrack):
        self.doors = dict() # bool & color as a tuple
        self.track = track
        self.buttons = dict()
        self.pos = track.spawn
        self.states = []


    def manhattan_dist(a: Point, b: Point) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    def find_valid_neighbors(a: Point):
        neighbors = [(a[0] - 1, a[1]), (a[0], a[1] - 1), (a[0] + 1, a[1]), (a[0], a[1] + 1)]
        return neighbors

    # def state(loc: Point, track: RaceTrack):
    #     # make new states. loop. check if state is new. if so, add to list.
    #     if astar(loc, track.target, track):
            

    #     new_doors = []
    #     new_buttons = []
    #     if new_doors != doors or new_buttons != buttons or new_agent != agent:
    #         states.append(current_state)

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



    def smart_move(loc: Point, track: RaceTrack) -> Point:
        # if move not illegal
        path = astar(loc, track.target, track)
        # self.track.target
        next_pos = path[1]
        return (next_pos[0] - loc[0], next_pos[1] - loc[1])
