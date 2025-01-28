import pygame
import sys
import random
from heapq import heappush, heappop
import copy
import time

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 3
TILE_SIZE = WIDTH // GRID_SIZE
FONT = pygame.font.Font(None, 80)
MAX_TIME = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle Game")

def create_puzzle():
    numbers = list(range(1, GRID_SIZE * GRID_SIZE)) + [0]  # Numbers 1-8 and empty tile (0)
    random.shuffle(numbers)  # Shuffle tiles
    return [numbers[i:i + GRID_SIZE] for i in range(0, len(numbers), GRID_SIZE)]

def draw_grid(grid, highlight=None):
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            x, y = col * TILE_SIZE, row * TILE_SIZE
            if value != 0:  # Draw tiles
                # Shadow effect
                pygame.draw.rect(screen, (200, 200, 200), (x + 5, y + 5, TILE_SIZE - 10, TILE_SIZE - 10), border_radius=10)# to make a shape that isn't actually square
                # Main tile
                pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), border_radius=10)
                # Text
                text = FONT.render(str(value), True, WHITE)
                screen.blit(text, (x + TILE_SIZE // 3, y + TILE_SIZE // 3))
            elif highlight:  # Highlight empty tile during animation
                pygame.draw.rect(screen, (200, 200, 200), (x, y, TILE_SIZE, TILE_SIZE), border_radius=10)
    pygame.display.flip()

def animate_tile(grid, start_pos, end_pos):
    start_x, start_y = start_pos[1] * TILE_SIZE, start_pos[0] * TILE_SIZE
    end_x, end_y = end_pos[1] * TILE_SIZE, end_pos[0] * TILE_SIZE
    dx = (end_x - start_x) / 10
    dy = (end_y - start_y) / 10

    for i in range(10):
        draw_grid(grid, highlight=start_pos)
        pygame.draw.rect(screen, BLACK, (start_x + i * dx, start_y + i * dy, TILE_SIZE, TILE_SIZE))
        pygame.display.flip()
        pygame.time.delay(30)

def find_empty(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                return row, col

def move_tile(grid, direction):
    empty_row, empty_col = find_empty(grid)
    if direction == "UP" and empty_row < GRID_SIZE - 1:
        grid[empty_row][empty_col], grid[empty_row + 1][empty_col] = grid[empty_row + 1][empty_col], grid[empty_row][empty_col]
    elif direction == "DOWN" and empty_row > 0:
        grid[empty_row][empty_col], grid[empty_row - 1][empty_col] = grid[empty_row - 1][empty_col], grid[empty_row][empty_col]
    elif direction == "LEFT" and empty_col < GRID_SIZE - 1:
        grid[empty_row][empty_col], grid[empty_row][empty_col + 1] = grid[empty_row][empty_col + 1], grid[empty_row][empty_col]
    elif direction == "RIGHT" and empty_col > 0:
        grid[empty_row][empty_col], grid[empty_row][empty_col - 1] = grid[empty_row][empty_col - 1], grid[empty_row][empty_col]

def visualize_ai_solution(grid, goal, solution):
    for move in solution:
        empty_row, empty_col = find_empty(grid)
        new_empty_row, new_empty_col = empty_row, empty_col

        if move == "UP":
            new_empty_row += 1 # because we actully moved to the tile not the empty tile therefore moves the empty tile down and the tile up
        elif move == "DOWN":
            new_empty_row -= 1
        elif move == "LEFT":
            new_empty_col += 1
        elif move == "RIGHT":
            new_empty_col -= 1

        animate_tile(grid, (empty_row, empty_col), (new_empty_row, new_empty_col))
        move_tile(grid, move)
        draw_grid(grid)
        pygame.time.wait(200)  # Delay for better visualization
        # end_time = time.time()

def heuristic(grid, goal):
    # Manhattan distance
    distance = 0
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            if value != 0:
                goal_row, goal_col = divmod(value - 1, GRID_SIZE)
                distance += abs(goal_row - row) + abs(goal_col - col)
    return distance

def a_star_solver(start, goal):
    
    def serialize(grid):
        return tuple(tuple(row) for row in grid)

    open_set = []
    heappush(open_set, (0, start, [])) # (f(n), current_state, path_to_state)
    visited = set()
    
    # initialze the timer
    start_time = time.time()  # Record start time in milliseconds
    print(start_time, "start")
    
    while open_set:
        
        if time.time() - start_time > MAX_TIME:
            return None, start_time
        
        _, current, path = heappop(open_set)
        if serialize(current) in visited:
            continue
        visited.add(serialize(current))
        
        if current == goal:
            # end_time = time.time()
            # print(end_time, "end")
            # passsed_time = pygame.time.get_ticks() - start_time
            # print(end_time-start_time, "-minus")
            return path, start_time
        # empty_row, empty_col = find_empty(current)
        for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:

            new_grid = copy.deepcopy(current)
            move_tile(new_grid, direction)
            if serialize(new_grid) not in visited:
                heappush(open_set, (len(path) + heuristic(new_grid, goal), new_grid, path + [direction]))
    # end_time = time.time()
    # passsed_time = pygame.time.get_ticks() - start_time
    return None, start_time # , end_time-start_time

# def format_time(millisec):
#     seconds = millisec // 1000
#     minutes = seconds // 60
#     seconds = seconds % 60

#     return f"{minutes}:{seconds}"

def shuffle_puzzle(grid, steps=20):
    from random import choice
    directions = ["UP", "DOWN", "LEFT", "RIGHT"]

    for _ in range(steps):
        move = choice(directions)
        empty_row, empty_col = find_empty(grid)
        new_empty_row, new_empty_col = empty_row, empty_col

        if move == "UP" and empty_row < GRID_SIZE - 1:
            new_empty_row += 1
        elif move == "DOWN" and empty_row > 0:
            new_empty_row -= 1
        elif move == "LEFT" and empty_col < GRID_SIZE - 1:
            new_empty_col += 1
        elif move == "RIGHT" and empty_col > 0:
            new_empty_col -= 1

        animate_tile(grid, (empty_row, empty_col), (new_empty_row, new_empty_col))
        move_tile(grid, move)
    draw_grid(grid)


def main():
    grid = create_puzzle()
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    # start_time = time.time()  # Record start time
    
    # running = True
    while True:
        draw_grid(grid)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_tile(grid, "UP")
                elif event.key == pygame.K_DOWN:
                    move_tile(grid, "DOWN")
                elif event.key == pygame.K_LEFT:
                    move_tile(grid, "LEFT")
                elif event.key == pygame.K_RIGHT:
                    move_tile(grid, "RIGHT")
                elif event.key == pygame.K_s:  # Shuffle
                    shuffle_puzzle(grid)
                elif event.key == pygame.K_SPACE:  # Solve with AI
                    solution, start_time = a_star_solver(grid, goal)
                    if solution:
                        visualize_ai_solution(grid, goal, solution)
                        end_time = time.time()
                        print(end_time, "end")
                        passed_time = end_time - start_time
                        print(passed_time, "negation")
                        screen.fill(WHITE)
                        draw_grid(grid)
                        timer_text = FONT.render(f"{passed_time:.2f} seconds" , True, (255, 0, 0))
                        screen.blit(timer_text, (10, 50))
                        pygame.display.flip()
                        pygame.time.wait(2000) # pausing to let the user see the time
                    elif time.time() - start_time > MAX_TIME:
                        screen.fill(WHITE)  # Clear the screen
                        draw_grid(grid)
                        time_limit_text = FONT.render(f"Time limit exceeded!", True, (255, 0, 0))
                        screen.blit(time_limit_text, (10, 10))
                        pygame.display.flip()
                        pygame.time.wait(2000)
                    else:
                        # Optional: Inform the user that no solution was found
                        screen.fill(WHITE)  # Clear the screen
                        draw_grid(grid)
                        no_solution_text = FONT.render("No solution found!", True, (255, 0, 0))
                        screen.blit(no_solution_text, (10, 10))
                        pygame.display.flip()
                        pygame.time.wait(2000)  # Pause to let the user see the message
main()