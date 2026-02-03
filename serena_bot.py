from game_world.racetrack import RaceTrack
from Mesh.nav_mesh import NavMeshCell
from collections import defaultdict
import shapely
import heapq


Point = tuple[int, int]

def astar(
    self, start: shapely.Point, end: shapely.Point
) -> list[NavMeshCell] | None:
    start_cell, end_cell = self.map.find_cell(start), self.map.find_cell(end)
    closed_list = set()  # explored
    if not start_cell or not end_cell:
        return None
    g_scores = defaultdict(lambda: float("inf"))
    g_scores[start_cell] = 0
    f_scores = defaultdict(lambda: float("inf"))
    f_scores[start_cell] = start_cell.distance(end_cell)

    frontier = [(f_scores[start_cell], start_cell.id, start_cell)]
    prev: dict[NavMeshCell, NavMeshCell | None] = {start_cell: None}

    while True:
        _, _, current_cell = heapq.heappop(frontier)
        if current_cell == end_cell:
            break

        for neighbor in current_cell.neighbors:
            if neighbor in closed_list:
                continue

            temp_g = g_scores[current_cell] + 1
            if temp_g < g_scores[neighbor]:
                g_scores[neighbor] = temp_g
                f_scores[neighbor] = temp_g + neighbor.distance(end_cell)
                prev[neighbor] = current_cell
                if neighbor not in closed_list:
                    heapq.heappush(
                        frontier, (f_scores[neighbor], neighbor.id, neighbor)
                    )

        closed_list.add(current_cell)

    path = []
    key = end_cell
    while key != None:
        path.append(key)
        key = prev[key]
    return path[::-1]


def smart_move(loc: Point, track: RaceTrack) -> Point:
    safe = track.find_traversable_cells()
    options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = {opt: (loc[0] + opt[0], loc[1] + opt[1]) for opt in options}
    safe_options = [opt for opt in neighbors if neighbors[opt] in safe]
    return ... 
