import pygame
from pygame.locals import QUIT, KEYDOWN, K_c, K_1, K_2, K_3, K_4, K_5

from Utils import manhattan_distance, euclidean_distance
from Grid import Grid
from WindowUtils import draw, get_cell_from_mouse_click
from Strategy import Context
from SearchAlgorithms import BFS, AStar, GBFS


def get_inputs():
    WIDTH = 800
    ROWS = 50
    FPS = 10

    return WIDTH, ROWS, FPS


def left_mouse_pressed(curr_cell, start_position, end_position):
    if not start_position and curr_cell != end_position:
        curr_cell.make_start()
        start_position = curr_cell
    elif not end_position and curr_cell != start_position:
        curr_cell.make_end()
        end_position = curr_cell
    elif curr_cell != start_position and curr_cell != end_position:
        curr_cell.make_barrier()

    return start_position, end_position


def choose_algorithm(event, finder_context):
    if event.key == K_1:
        print("BFS Algorithm")
        finder_context.set_strategy(BFS())
    elif event.key == K_2:
        print("A* Algorithm using manhattan distance")
        finder_context.set_strategy(AStar(manhattan_distance))
    elif event.key == K_3:
        print("A* Algorithm using euclidean_distance")
        finder_context.set_strategy(AStar(euclidean_distance))
    elif event.key == K_4:
        print("GBFS Algorithm using manhattan_distance")
        finder_context.set_strategy(AStar(manhattan_distance))
    elif event.key == K_5:
        print("GBFS Algorithm using euclidean_distance")
        finder_context.set_strategy(AStar(euclidean_distance))


def start():
    pygame.init()
    WIDTH, ROWS, FPS = get_inputs()

    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("~ Path Finder Visualizer ~")
    grid = Grid(WIDTH, ROWS)

    start_position = None
    end_position = None
    finder_context = Context(BFS())

    run = True
    while run:
        draw(WIN, grid)
        event_list = pygame.event.get()

        for event in event_list:

            if event.type == QUIT:
                pygame.quit()
                run = False
                break

            if pygame.mouse.get_pressed(num_buttons=3)[0]:  # LEFT mouse button
                curr_cell = get_cell_from_mouse_click(grid)
                start_position, end_position = left_mouse_pressed(curr_cell, start_position, end_position)

            elif pygame.mouse.get_pressed()[2]:  # RIGHT mouse button
                curr_cell = get_cell_from_mouse_click(grid)
                curr_cell.reset()
                if curr_cell == start_position:
                    start_position = None
                elif curr_cell == end_position:
                    end_position = None

            if event.type == KEYDOWN:
                valid_keys = [K_1, K_2, K_3, K_4, K_5, K_c]
                if event.key not in valid_keys:
                    continue

                if event.key == K_c:
                    start_position = None
                    end_position = None
                    grid = Grid(WIDTH, ROWS)
                    continue

                choose_algorithm(event, finder_context)

                found_path = finder_context.find(WIN, lambda: pygame.time.wait(FPS), grid, start_position, end_position)

                if not found_path:
                    print("Path not found")



start()

