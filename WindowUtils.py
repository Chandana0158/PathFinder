import pygame
from Utils import GREY, WHITE, is_valid_num



def draw_grid_lines(win, grid):
    rows = grid.rows
    width = grid.width

    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid):
    win.fill(WHITE)

    for row in grid.cells:
        for cell in row:
            cell.draw_cell(win)

    draw_grid_lines(win, grid)
    pygame.display.update()


def update_cells(win, wait, cells):
    for cell in cells:
        if cell:
            cell.draw_cell(win)
        wait()
        pygame.display.update()


def get_cell_from_mouse_click(grid):
    mouse_position = pygame.mouse.get_pos()
    row, col = grid.get_clicked_position(mouse_position)
    return grid.get_cell(row, col)


