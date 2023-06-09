import pygame
from pygame.locals import QUIT
from queue import PriorityQueue
import time

from collections import deque, defaultdict
from WindowUtils import update_cells
from Strategy import PathFinderStrategy


def generate_path(parent, end):
    curr = end
    path = []
    while curr:
        curr.make_path()
        path.append(curr)
        curr = parent[curr]

    return path



class BFS(PathFinderStrategy):
    def find(self, window, wait, grid, start, end):
        parent = defaultdict()
        parent[start] = None
        queue = deque()
        queue.append(start)
        visited = set()
        path_length = 0
        start_time = time.time()

        while queue:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return False

            curr_cell = queue.popleft()

            if curr_cell == end:
                path_cells = generate_path(parent, end)
                update_cells(window, wait, path_cells)
                end_time = time.time()
                time_taken = end_time - start_time
                path_length = len(path_cells) - 1
                print(f"Shortest Path Length : {path_length}")
                print(f"Time Taken : {time_taken:.4f} seconds\n")
                return True

            grid.update_neighbors(curr_cell)
            neighbors = curr_cell.get_neighbors()
            for neighbor_cell in neighbors:
                if neighbor_cell in parent:  # Already visited
                    continue

                parent[neighbor_cell] = curr_cell
                queue.append(neighbor_cell)
                if neighbor_cell != start and neighbor_cell != end:
                    neighbor_cell.make_open()

            if curr_cell != start and curr_cell != end:
                curr_cell.make_closed()
            update_cells(window, wait, [curr_cell] + neighbors)

        return False


class AStar(PathFinderStrategy):
    def __init__(self, distance_function):
        self.distance_function = distance_function

    def find(self, window, wait, grid, start, end):
        min_heap = PriorityQueue()
        min_heap.put((0, start))  # (heuristic distance, degree, cell)

        parent = defaultdict()
        parent[start] = None
        g_score = {cell: float('inf') for row in grid.cells for cell in row}
        g_score[start] = 0
        f_score = {cell: float('inf') for row in grid.cells for cell in row}
        f_score[start] = self.distance_function(start.get_position(), end.get_position())

        visiting = {start}

        start_time = time.time()

        while not min_heap.empty():
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return False

            curr_f_score, curr_cell = min_heap.get()

            if curr_cell == end:
                path_cells = generate_path(parent, end)
                update_cells(window, wait, path_cells)
                end_time = time.time()
                shortest_path_length = len(path_cells)-1
                time_taken = end_time - start_time
                print(f"Shortest path length  : {shortest_path_length}")
                print(f"Time taken  : {time_taken:.4f} seconds\n")
                return True

            grid.update_neighbors(curr_cell)
            neighbors = curr_cell.get_neighbors()

            for neighbor_cell in neighbors:

                curr_g_score = g_score[curr_cell] + self.distance_function(curr_cell.get_position(),
                                                                           neighbor_cell.get_position())

                if curr_g_score < g_score[neighbor_cell]:
                    g_score[neighbor_cell] = curr_g_score
                    parent[neighbor_cell] = curr_cell

                    # calculate h-distance based on the distance function supplied by the user
                    h_score = self.distance_function(neighbor_cell.get_position(), end.get_position())
                    f_score[neighbor_cell] = curr_g_score + h_score

                    if neighbor_cell not in visiting:
                        min_heap.put((f_score[neighbor_cell], neighbor_cell))
                        visiting.add(neighbor_cell)
                        if neighbor_cell != start and neighbor_cell != end:
                            neighbor_cell.make_open()

            visiting.discard(curr_cell)
            if curr_cell != start and curr_cell != end:
                curr_cell.make_closed()
            update_cells(window, wait, [curr_cell] + neighbors)

        return False

class GBFS(PathFinderStrategy):
    def __init__(self, distance_function):
        self.distance_function = distance_function

    def find(self, window, wait, grid, start, end):
        min_heap = PriorityQueue()
        min_heap.put((0, start))  # (heuristic distance, cell)

        parent = defaultdict()
        parent[start] = None
        f_score = {cell: float('inf') for row in grid.cells for cell in row}
        f_score[start] = self.distance_function(start.get_position(), end.get_position())

        visiting = {start}

        start_time = time.time()

        while not min_heap.empty():
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return False

            curr_f_score, curr_cell = min_heap.get()

            if curr_cell == end:
                path_cells = generate_path(parent, end)
                update_cells(window, wait, path_cells)
                end_time = time.time()
                shortest_path_length = len(path_cells)-1
                time_taken = end_time - start_time
                print(f"Shortest path length : {shortest_path_length}")
                print(f"Time taken : {time_taken:.4f} seconds\n")
                return True

            grid.update_neighbors(curr_cell)
            neighbors = curr_cell.get_neighbors()

            for neighbor_cell in neighbors:

                if neighbor_cell not in visiting:
                    parent[neighbor_cell] = curr_cell

                    # calculate h-distance based on the distance function supplied by the user
                    h_score = self.distance_function(neighbor_cell.get_position(), end.get_position())
                    f_score[neighbor_cell] = h_score

                    min_heap.put((f_score[neighbor_cell], neighbor_cell))
                    visiting.add(neighbor_cell)
                    if neighbor_cell != start and neighbor_cell != end:
                        neighbor_cell.make_open()

            visiting.discard(curr_cell)
            if curr_cell != start and curr_cell != end:
                curr_cell.make_closed()
            update_cells(window, wait, [curr_cell] + neighbors)

        return False
