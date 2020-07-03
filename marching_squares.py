import pygame
from vector import Vector2D, randint

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

def Draw_Basic_algorithm(screen, rect, resolution, wall_colour, line_width):
    rect.sort(key=lambda elem: Vector2D(0, -1000).dist(elem, use_sqrt=False))
    rect[2], rect[3] = rect[3], rect[2]
    nibble = ''.join([str(int(i.data["state"])) for i in rect])

    x, y = rect[0].get_xy(int)
    hr, r = resolution/2, resolution

    #region cases
    if nibble == '0000' : pass

    if nibble == '0001' or nibble == '1110' : pygame.draw.line(screen, wall_colour, (x, y + hr), (x + hr, y + r), line_width)

    if nibble == '0010' or nibble == '1101' : pygame.draw.line(screen, wall_colour, (x + r, y + hr), (x + hr, y + r), line_width)

    if nibble == '1011' or nibble == '0100' : pygame.draw.line(screen, wall_colour, (x + hr, y), (x + r, y + hr), line_width)

    if nibble == '0111' or nibble == '1000' : pygame.draw.line(screen, wall_colour, (x + hr, y), (x, y + hr), line_width)


    if nibble == '1100' or nibble == '0011' : pygame.draw.line(screen, wall_colour, (x, y + hr), (x + r, y + hr), line_width)

    if nibble == '1001' or nibble == '0110' : pygame.draw.line(screen, wall_colour, (x + hr, y), (x + hr, y + r), line_width)
    
    if nibble == '1010':
        pygame.draw.line(screen, wall_colour, (x + hr, y), (x, y + hr), line_width)
        pygame.draw.line(screen, wall_colour, (x + r, y + hr), (x + hr, y + r), line_width)

    if nibble == '0101':
        pygame.draw.line(screen, wall_colour, (x + hr, y), (x + r, y + hr), line_width)
        pygame.draw.line(screen, wall_colour, (x, y + hr), (x + hr, y + r), line_width)
    #endregion

class Marching_Squares():
    def __init__(self, size, resolution=25, celular_automata_iterations=10):
        self.resolution = resolution
        self.size = size

        self.points = []
        self.grid = []

        self.w = int(self.size[1] / self.resolution)
        self.h = int(self.size[0] / self.resolution)

    def draw(self, screen, display_points=False, wall_colour=[120, 60, 0], line_width=3):
        if self.grid != [] and self.points != []:

            for rect in self.grid:
                Draw_Basic_algorithm(screen, rect, self.resolution, wall_colour, line_width)

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


