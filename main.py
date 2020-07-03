import pygame
from marching_squares import *

pygame.init()
size = (600, 600)
screen = pygame.display.set_mode(size)
screen.fill([255, 255, 255])
pygame.display.set_icon(screen)
pygame.display.set_caption('')
clock, fps = pygame.time.Clock(), 30

marching_squares = Marching_Squares((600, 600), resolution=25, celular_automata_iterations=1)

grid = Generate_Cellular_Automata_Grid(marching_squares)
surface = Generate_Surface_from_Grid(grid)

key_block = False
while True:
    #region events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    mouse_pressed = pygame.mouse.get_pressed()
    #endregion
    screen.fill(0)

    if mouse_pressed == (1, 0, 0) and not key_block:
        key_block = True
        grid = Generate_Cellular_Automata_Grid(marching_squares)

    if sum(mouse_pressed) == 0:
        key_block = False

    marching_squares.from_grid(grid)
    marching_squares.draw(screen, wall_colour=[255, 255, 255], line_width=5)

    pygame.display.update()
    clock.tick(fps)