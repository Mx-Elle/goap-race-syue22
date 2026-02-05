from game_world.racetrack import RaceTrack
from collections import defaultdict
import heapq

Point = tuple[int, int]

def manhattan_dist(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(start: Point):
    return (start[0]-1, start[1]), (start[0], start[1]-1), (start[0]+1, start[1]), (start[0], start[1]-1)

def astar(
    start: Point, end: Point
) -> list[Point] | None:
    start_cell, end_cell = start, end
    closed_list = set()  # explored
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

        for neighbor in neighbors(current_cell):
            if neighbor in closed_list:
                continue

            temp_g = g_scores[current_cell] + 1
            if temp_g < g_scores[neighbor]:
                g_scores[neighbor] = temp_g
                f_scores[neighbor] = temp_g + manhattan_dist(neighbor, end_cell)
                prev[neighbor] = current_cell
                if neighbor not in closed_list:
                    heapq.heappush(
                        frontier, (f_scores[neighbor], neighbor)
                    )

        closed_list.add(current_cell)

    path = []
    key = end_cell
    while key != None:
        path.append(key)
        key = prev[key]
    return path[::-1]


def heuristic(): 
    # choosing which path to take. value = distance from star. 
    ...


def smart_move(loc: Point, track: RaceTrack) -> Point:
    path = astar(loc, track.target)
    return path[0]
