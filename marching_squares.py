import pygame
from vector import Vector2D
from random import randint





def Default_Cellular_Automata_Rule(current, num_neighbours):
    birth_requirement = 4
    death_requirement = 2
    if current:
        if num_neighbours < death_requirement:
            return False
        else:
            return True
    else:
        if num_neighbours > birth_requirement:
            return True
        else:
            return False

def ConwaysGameOfLifeRule(current, num_neighbours):
    """
    If a living cell has less than two living neighbours, it dies.
    If a living cell has two or three living neighbours, it stays alive.
    If a living cell has more than three living neighbours, it dies.
    If a dead cell has exactly three living neighbours, it becomes alive.
    """
    if current and num_neighbours < 2:
        return False
    elif current and num_neighbours in [2, 3]:
        return True
    elif current and num_neighbours > 3:
        return False
    elif not current and num_neighbours == 3:
        return True
    else:
        return current



def Generate_Cellular_Automata_Grid(marchin_squares_object, iterations=10, fill=60, rule=Default_Cellular_Automata_Rule):
    grid = []

    for y in range(marchin_squares_object.h+1):
        temp = []
        for x in range(marchin_squares_object.w+1):
            if x == 0 or y == 0 or x == marchin_squares_object.w or y == marchin_squares_object.h:
                state = 0
            elif randint(0, 100) > fill:
                state = 1
            else:
                state = 0

            temp.append(state)

        grid.append(temp)

    for _ in range(iterations):
        temp = grid
        for y in range(1, marchin_squares_object.h - 1):
            for x in range(1, marchin_squares_object.w - 1):
                state = grid[y][x]
                n = [
                    grid[y-1][x],
                    grid[y+1][x],
                    grid[y][x-1],
                    grid[y][x+1],
                    grid[y-1][x-1],
                    grid[y+1][x+1],
                    grid[y-1][x+1],
                    grid[y+1][x-1],
                ]

                temp[y][x] = rule(state, n.count(True))

        grid = temp

    return grid

def Generate_Surface_from_Grid(grid):
    w, h = len(grid[0]), len(grid)

    surface = pygame.Surface((w, h))
    for y in range(h):
        for x in range(w):
            state = grid[y][x]
            color = [state * 255 for _ in range(3)]

            surface.set_at((x, y), color)
    
    return surface



def Draw_Basic_algorithm(screen, rect, resolution, wall_colour):
    rect.sort(key=lambda elem: Vector2D(0, -1000).dist(elem, use_sqrt=False))
    rect[2], rect[3] = rect[3], rect[2]
    nibble = ''.join([str(int(i.data["state"])) for i in rect])

    x, y = rect[0].get_xy(int)
    r = resolution

    polygon1 = []
    polygon2 = []
    #region cases
    if nibble in ['0000']: # Case 0
        pass

    if nibble in ['0001', '1110']: # Case 1 and 14
        polygon1.append((x, y + r/2))
        polygon1.append((x + r/2, y + r))
        polygon1.append((x, y+r))

    if nibble in ['0010', '1101']: # Case 2 and 13
        polygon1.append((x + r, y + r/2))
        polygon1.append((x + r/2, y + r))
        polygon1.append((x + r, y + r))

    if nibble in ['0011']: # Case 3
        polygon1.append((x, y + r/2))
        polygon1.append((x + r, y + r/2))
        polygon1.append((x + r, y + r))
        polygon1.append((x, y + r))

    if nibble in ['0100', '1011']: # Case 4 and 11
        polygon1.append((x + r/2, y))
        polygon1.append((x + r, y + r/2))
        polygon1.append((x + r, y))

    if nibble in ['0101']: # Case 5
        polygon1.append((x + r, y + r/2))
        polygon1.append((x + r/2, y + r))
        polygon1.append((x + r, y + r))

        polygon2.append((x + r/2, y))
        polygon2.append((x, y + r/2))
        polygon2.append((x, y))

    if nibble in ['0110']: # Case 6
        polygon1.append((x + r/2, y))
        polygon1.append((x + r/2, y + r))
        polygon1.append((x + r, y + r))
        polygon1.append((x + r, y))

    if nibble in ['0111', '1000']: # Case 7 and 8
        polygon1.append((x + r/2, y))
        polygon1.append((x, y + r/2))
        polygon1.append((x, y))

    if nibble in ['1001']: # Case 9
        polygon1.append((x + r/2, y))
        polygon1.append((x + r/2, y + r))
        polygon1.append((x, y + r))
        polygon1.append((x, y))

    if nibble in ['1010']: # Case 10
        polygon1.append((x, y + r/2))
        polygon1.append((x + r/2, y + r))
        polygon1.append((x, y+r))

        polygon2.append((x + r/2, y))
        polygon2.append((x + r, y + r/2))
        polygon2.append((x + r, y))

    if nibble in ['1100']: # Case 12
        polygon1.append((x, y))
        polygon1.append((x + r, y))
        polygon1.append((x + r, y + r/2))
        polygon1.append((x, y + r/2))

    if nibble in ['1111']: # Case 15
        polygon1.append((x, y))
        polygon1.append((x + r, y))
        polygon1.append((x + r, y + r))
        polygon1.append((x, y + r))

    #endregion

    if len(polygon1) > 2:
        pygame.draw.polygon(screen, wall_colour, polygon1)
    if len(polygon2) > 2:
        pygame.draw.polygon(screen, wall_colour, polygon2)

class Marching_Squares():
    def __init__(self, size, resolution=25, celular_automata_iterations=10):
        self.resolution = resolution
        self.size = size

        self.points = []
        self.grid = []

        self.w = int(self.size[1] / self.resolution)
        self.h = int(self.size[0] / self.resolution)

    def draw(self, screen, display_points=False, wall_colour=[120, 60, 0]):
        if self.grid != [] and self.points != []:

            for rect in self.grid:
                Draw_Basic_algorithm(screen, rect, self.resolution, wall_colour)

            if not display_points : return

            for point in self.points:
                color = [(point.data["state"]) * 255 for _ in range(3)]
                pygame.draw.circle(screen, color, point.get_xy(int), 4)

        else:
            raise Exception("Please first run either from_grid or randomise")

    def randomise(self):
        # create points
        self.points = []
        for y in range(self.h + 1):
            for x in range(self.w + 1):
        
                vec = Vector2D((x * self.resolution), (y * self.resolution))
                vec.data["state"] = randint(0, 1)
        
                self.points.append(vec)
        
        # create squares
        self.grid = []
        for y in range(self.h + 1):
            for x in range(self.w + 1):
                vec = Vector2D((x * self.resolution) + self.resolution/2, (y * self.resolution) + self.resolution/2)

                dist = []
                for point in self.points:
                    dist.append(int(point.dist(vec)))
                dist = min(dist)

                temp = []
                for point in self.points:
                    if int(point.dist(vec)) == dist : temp.append(point)
                
                if len(temp) == 4:
                    self.grid.append(temp)

    def from_grid(self, grid):
        # create points
        self.points = []
        for y in range(self.h + 1):
            for x in range(self.w + 1):
        
                vec = Vector2D((x * self.resolution), (y * self.resolution))
                vec.data["state"] = not grid[y][x]
        
                self.points.append(vec)
        
        # create squares
        self.grid = []
        for y in range(self.h + 1):
            for x in range(self.w + 1):
                vec = Vector2D((x * self.resolution) + self.resolution/2, (y * self.resolution) + self.resolution/2)

                dist = []
                for point in self.points:
                    dist.append(int(point.dist(vec, use_sqrt=False)))
                dist = min(dist)

                temp = []
                for point in self.points:
                    if int(point.dist(vec, use_sqrt=False)) == dist : temp.append(point)
                
                if len(temp) == 4:
                    self.grid.append(temp)


