
import sys, pygame
import random
from datetime import datetime
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'

# Customizable items
grid_size = width, height = 800, 600
cell_size = 10 # radius
max_fps = 5

# cell colors
dead_black = 0, 0, 0
alive_coral = 255, 102, 102

# title
pygame.display.set_caption("John Conway's The Game of Life")


# Class for whole game
class GameOfLife:

    # initialize pygame
    def __init__(self):
        pygame.init()
        # set up screen window
        self.screen = pygame.display.set_mode(grid_size)
        self.clear_screen()
        # push drawing to memory with flip
        pygame.display.flip()
        
        self.last_update_completed = 0
        self.desired_milliseconds_between_updates = (1.0 / max_fps) * 1000.0
        
        self.game_grid_active = 0
        self.num_of_columns = int(width / cell_size)
        self.num_of_rows = int(height / cell_size)
        self.grids = []
        self.init_grids()
        self.set_grid()
        self.paused = False
        self.game_over = False

    def init_grids(self):
        
        # set up game grid

        def create_grid():
            rows = []
            for num_of_rows in range(self.num_of_rows):
                list_of_columns = [0] * self.num_of_columns
                rows.append(list_of_columns)
            return rows
        
        self.grids.append(create_grid())
        self.grids.append(create_grid())
        
        
    def set_grid(self, value=None, grid=0):
    # can either zero out the grid or randomize it via value param
    # (1) --> all alive
    # (0) --> all dead
    # ()  --> randomize
    # (None) --> randomize
        for r in range(self.num_of_rows):
            for c in range(self.num_of_columns):
                if value is None:
                    cell_value = random.randint(0,1)
                else:
                    cell_value = value
                # set to value from 0 -1 
                self.grids[grid][r][c] = cell_value

    def draw_grid(self):
        # clear screen first
        self.clear_screen()
        # draw circles on grid
        #(surface, color, center(x,y), radius, width)
        # circle = pygame.draw.circle(self.screen, alive_coral, (50,50), 5, 0) 
        for c in range(self.num_of_columns):
            for r in range(self.num_of_rows):
                # set up colors
                if self.grids[self.game_grid_active][r][c] == 1:
                    color = alive_coral
                else:
                    color = dead_black
                #(surface, color, center(x,y), radius, width)
                pygame.draw.circle(self.screen,
                                            color,
                                            (int(c * cell_size + (cell_size /2)),
                                            int(r * cell_size + (cell_size/2))),
                                            int(cell_size/2),
                                            0) 
        pygame.display.flip()

    # clear the screen
    def clear_screen(self):
        # default screen is dead/black
        self.screen.fill(dead_black)
    

    def get_cell(self,r,c):
        try:
            cell_value = self.grids[self.game_grid_active][r][c]
        except:
            cell_value = 0
        return cell_value

    def check_cell_neighbors(self, row_index, col_index):
        # get number of alive cells around current cell
        num_alive_neighbors = 0

        num_alive_neighbors += self.get_cell(row_index - 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index + 1)

        num_alive_neighbors += self.get_cell(row_index, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index, col_index + 1)

        num_alive_neighbors += self.get_cell(row_index + 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index + 1)


        # Rules
        
        if self.grids[self.game_grid_active][row_index][col_index] == 1: # alive
            if num_alive_neighbors > 3: # overpopulation
                return 0
            
            if num_alive_neighbors < 2: # underpopulation
                return 0

            if num_alive_neighbors == 2 or num_alive_neighbors == 3:
                return 1
        
        elif self.grids[self.game_grid_active][row_index][col_index] == 0: # dead
            if num_alive_neighbors == 3: #rebirth
                return 1
        
        return self.grids[self.game_grid_active][row_index][col_index]
   
    # update the instances
    def update_generation(self):
        '''
        Inspect the current generation state prepare the next generation
        '''
        self.set_grid(0, self.inactive_grid())
        
        for r in range(self.num_of_rows -1):
            for c in range(self.num_of_columns -1):
               next_gen_state = self.check_cell_neighbors(r, c)
               
               # set inactive grid to store next generation
               self.grids[self.inactive_grid()][r][c] = next_gen_state
               
        # look at current generation
        # update inactive gride to store next generation
        self.game_grid_active = self.inactive_grid()

    def inactive_grid(self):
        return (self.game_grid_active + 1) % 2
        

    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print("key pressed")
                # if 's' key is pressed --> toggle game pause
                if event.unicode == 's':
                    print("Paused.")
                    if self.paused:
                        self.paused = False
                        print('Resume')
                    else:
                        self.paused = True

                if event.unicode == 'c':
                    print("Clear grid - Press 'r' to randomize and then 's' to resume.")
                    self.paused = True
                    self.set_grid(0, 0)
                    self.draw_grid()
                
                # if 'r' key is pressed --> randomize gride
                elif event.unicode == 'r':
                    print("Randomizing grid.")
                    self.active_grid = 0
                    self.set_grid(None, self.active_grid)  # randomize
                    self.set_grid(0, self.inactive_grid())  # set to 0
                    self.draw_grid()
                # if 'q' key is pressed --> quit game
                elif event.unicode == 'q':
                    print("Exit Game.")
                    self.game_over = True
            if event.type == pygame.QUIT:
                sys.exit()
            
    # game loop
    def run_game(self):
        print('Press "s" to pause/resume the game.')
        print('Press "r" to randomize the cells')
        print('Press "c" to clear the grid')
        print('Press "q" to quit the game')
        while True:
            if self.game_over:
                return
            self.handle_events()
            if self.paused:
                continue
            self.update_generation()
            self.draw_grid()
            # Slow down the FrameRate
            self.cap_frame_rate()


    def cap_frame_rate(self):
        now = pygame.time.get_ticks()
        milliseconds_since_last_update = now - self.last_update_completed

        time_to_sleep = self.desired_milliseconds_between_updates - milliseconds_since_last_update
        if time_to_sleep > 0:
            pygame.time.delay(int(time_to_sleep))
        self.last_update_completed = now



if __name__ == "__main__":
    game = GameOfLife()
    game.run_game()