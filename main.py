import pygame
from marching_squares import *

pygame.init()
size = (1000, 500)
screen = pygame.display.set_mode(size)
screen.fill([255, 255, 255])
pygame.display.set_icon(screen)
pygame.display.set_caption('')
clock, fps = pygame.time.Clock(), 30

marching_squares = Marching_Squares((500, 500), resolution=25)

grid = Generate_Cellular_Automata_Grid(marching_squares)
surface = Generate_Surface_from_Grid(grid)

while True:
    #region events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    key = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    #endregion
    screen.fill([120, 60, 0])

    if key[pygame.K_SPACE]:
        grid = Generate_Cellular_Automata_Grid(marching_squares)
        surface = Generate_Surface_from_Grid(grid)

    image = pygame.transform.scale(surface, (500, 500))
    screen.blit(image, (500, 0))

    marching_squares.from_grid(grid)
    marching_squares.draw(screen, wall_colour=[60, 30, 0])

    pygame.display.update()
    clock.tick(fps)