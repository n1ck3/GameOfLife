import sys
import pygame
import copy
from pygame.locals import *

class Grid:
    def __init__(self):
        self.state = "STOPPED"

        self.GRID_I = self.GRID_J = 40
        self.TILE_SIZE = 20
        self.DISPLAY_X = 1 + self.GRID_I * self.TILE_SIZE
        self.DISPLAY_Y = 1 + self.GRID_J * self.TILE_SIZE
        self.DISPLAY_SIZE = self.DISPLAY_X, self.DISPLAY_Y

        self.ALIVE = (0,0,0)
        self.DEAD = (255,255,255)
        self.GRID_COLOR = (200,200,200)
        self.HOVER = (0,255,0)

        self.screen = pygame.display.set_mode(self.DISPLAY_SIZE)
        self.screen_base_caption = "Conway's Game of Live"

        self.locations = [[0 for x in range(self.GRID_I)] for y in range(self.GRID_J)]

        self.set_start()

    def set_start(self):
        # Create some starting points
        self.clear()

        # Blinker
        self.locations[1][2] = 1
        self.locations[2][2] = 1
        self.locations[3][2] = 1

        # Toad
        self.locations[6][2] = 1
        self.locations[7][2] = 1
        self.locations[8][2] = 1
        self.locations[7][3] = 1
        self.locations[8][3] = 1
        self.locations[9][3] = 1

        # Beaon
        self.locations[15][2] = 1
        self.locations[14][2] = 1
        self.locations[14][3] = 1
        self.locations[16][5] = 1
        self.locations[17][5] = 1
        self.locations[17][4] = 1

        # Pulsar
        self.locations[23][1] = 1
        self.locations[24][1] = 1
        self.locations[25][1] = 1
        self.locations[26][3] = 1
        self.locations[26][4] = 1
        self.locations[26][5] = 1
        self.locations[25][6] = 1
        self.locations[24][6] = 1
        self.locations[23][6] = 1
        self.locations[21][5] = 1
        self.locations[21][4] = 1
        self.locations[21][3] = 1
        self.locations[28][3] = 1
        self.locations[28][4] = 1
        self.locations[28][5] = 1
        self.locations[29][6] = 1
        self.locations[30][6] = 1
        self.locations[31][6] = 1
        self.locations[29][1] = 1
        self.locations[30][1] = 1
        self.locations[31][1] = 1
        self.locations[33][3] = 1
        self.locations[33][4] = 1
        self.locations[33][5] = 1
        self.locations[23][8] = 1
        self.locations[24][8] = 1
        self.locations[25][8] = 1
        self.locations[26][9] = 1
        self.locations[26][10] = 1
        self.locations[26][11] = 1
        self.locations[28][11] = 1
        self.locations[28][10] = 1
        self.locations[28][9] = 1
        self.locations[29][8] = 1
        self.locations[30][8] = 1
        self.locations[31][8] = 1
        self.locations[33][9] = 1
        self.locations[33][10] = 1
        self.locations[33][11] = 1
        self.locations[21][9] = 1
        self.locations[21][10] = 1
        self.locations[21][11] = 1
        self.locations[25][13] = 1
        self.locations[24][13] = 1
        self.locations[23][13] = 1
        self.locations[29][13] = 1
        self.locations[30][13] = 1
        self.locations[31][13] = 1

        # Pentadecatlhon
        self.locations[6][16] = 1
        self.locations[5][17] = 1
        self.locations[6][17] = 1
        self.locations[7][17] = 1
        self.locations[4][18] = 1
        self.locations[5][18] = 1
        self.locations[6][18] = 1
        self.locations[7][18] = 1
        self.locations[8][18] = 1
        self.locations[6][25] = 1
        self.locations[7][25] = 1
        self.locations[8][25] = 1
        self.locations[5][25] = 1
        self.locations[4][25] = 1
        self.locations[5][26] = 1
        self.locations[6][26] = 1
        self.locations[7][26] = 1
        self.locations[6][27] = 1

        # Lightweight Spaceship
        self.locations[14][16] = 1
        self.locations[17][16] = 1
        self.locations[18][17] = 1
        self.locations[18][18] = 1
        self.locations[18][19] = 1
        self.locations[17][19] = 1
        self.locations[16][19] = 1
        self.locations[15][19] = 1
        self.locations[14][18] = 1

        # Glider
        self.locations[14][24] = 1
        self.locations[15][24] = 1
        self.locations[16][24] = 1
        self.locations[16][23] = 1
        self.locations[15][22] = 1

        self.draw()

    def neighbors(self, (i,j)):
        """
        Returns all the 8 neighbors of a certain location
        """
        neighbors = []

        if i-1 >= 0: neighbors.append((i-1, j))
        if i+1 < self.GRID_I: neighbors.append((i+1, j))

        if j-1 >= 0: neighbors.append((i, j-1))
        if j+1 < self.GRID_J: neighbors.append((i, j+1))

        if i-1 >= 0 and j-1 >= 0: neighbors.append((i-1, j-1))
        if i-1 >= 0 and j+1 < self.GRID_J: neighbors.append((i-1, j+1))

        if i+1 < self.GRID_I and j-1 >= 0: neighbors.append((i+1, j-1))
        if i+1 < self.GRID_I and j+1 < self.GRID_J: neighbors.append((i+1, j+1))

        return neighbors

    def loc_to_pos(self, (i,j)):
        """
        Converts a location (i,j) (in the grid) to
        a position (x,y) (on the screen)
        """
        return (1 + i * self.TILE_SIZE, 1 + j * self.TILE_SIZE)

    def pos_to_loc(self, (i,j)):
        """
        Converts a position (x,y) (on the screen) to
        a location (i,j) (in the grid).
        """
        return ((x-1) // self.TILE_SIZE, (y-1) // self.TILE_SIZE)

    def progress(self):
        new_locations = copy.deepcopy(self.locations)

        for i in range(self.GRID_I):
            for j in range(self.GRID_J):
                loc = (i,j)
                alive_neighbors = 0
                for (n_i, n_j) in self.neighbors(loc):
                    if self.locations[n_i][n_j] == 1:
                        alive_neighbors = alive_neighbors + 1

                if self.locations[i][j] == 1:
                    # If this location is alive
                    if alive_neighbors == 2 or alive_neighbors == 3:
                        # And if this location has exactly 2 or 3 live
                        # neighbors, it lives for the next generation
                        new_locations[i][j] = 1
                    else:
                        # Else it is dead for the next generation
                        new_locations[i][j] = 0
                else:
                    # If the location is dead
                    if alive_neighbors == 3:
                        # And if the location has exactly 3 neighbors,
                        # it is bord for the next generation.
                        new_locations[i][j] = 1

        self.locations = new_locations
        self.draw()
        return True

    def draw(self):
        # Draw grid lines
        for vert_line in range((self.DISPLAY_X // self.TILE_SIZE)+1):
            pygame.draw.line(
                self.screen,
                self.GRID_COLOR,
                (vert_line * self.TILE_SIZE, 0),
                (vert_line * self.TILE_SIZE, self.DISPLAY_Y)
            )

        for horiz_line in range((self.DISPLAY_Y // self.TILE_SIZE)+1):
            pygame.draw.line(
                self.screen,
                self.GRID_COLOR,
                (0, horiz_line * self.TILE_SIZE),
                (self.DISPLAY_X, horiz_line * self.TILE_SIZE)
            )

        # Draw tiles
        for i in range(self.GRID_I):
            for j in range(self.GRID_J):
                loc = (i,j)
                (x,y) = self.loc_to_pos(loc)
                state = self.ALIVE if self.locations[i][j] == 1 else self.DEAD
                pygame.draw.rect(
                    self.screen,
                    state,
                    (x, y, self.TILE_SIZE - 1, self.TILE_SIZE - 1)
                )

    def toggle_state(self):
        if self.state == "STOPPED":
            self.state = "RUNNING"
        else:
            self.state = "STOPPED"

        pygame.display.set_caption(
            "[" + self.state + "]" +
            " " +
            self.screen_base_caption
        )
        return True

    def toggle_tile(self, (i,j)):
        print "self.locations[" + str(i) + "][" + str(j) + "] = 1"
        self.locations[i][j] = 0 if self.locations[i][j] == 1 else 1
        self.draw()
        return True

    def clear(self):
        self.locations = [[0 for x in range(self.GRID_I)] for y in range(self.GRID_J)]
        self.draw()
        return True


if __name__ == '__main__':
        grid = Grid()

        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption(
            "[" + grid.state + "]" +
            " " +
            grid.screen_base_caption
        )

        pygame.display.flip()
        grid.draw()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                elif event.type  == KEYDOWN:
                    if event.key == K_SPACE:
                        grid.toggle_state()
                    elif event.key == K_c:
                        grid.clear()
                    elif event.key == K_r:
                        grid.set_start()
                    elif event.key == K_ESCAPE:
                        pygame.quite()

                if grid.state == "STOPPED" and \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_i = mouse_pos[0] // (grid.TILE_SIZE)
                    mouse_j = mouse_pos[1] // (grid.TILE_SIZE)
                    grid.toggle_tile((mouse_i,mouse_j))

            if grid.state == "RUNNING":
                grid.progress()

            clock.tick(30)

            pygame.display.update()
