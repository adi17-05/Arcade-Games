print("Launching Minesweeper...")




import pygame
import random
import sys


pygame.init()


GRID_SIZE = 10
TILE_SIZE = 40
MINE_COUNT = 15
WIDTH, HEIGHT = GRID_SIZE * TILE_SIZE, GRID_SIZE * TILE_SIZE
FPS = 10


WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


FONT = pygame.font.SysFont("Arial", 24)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.revealed = False
        self.flagged = False
        self.neighboring_mines = 0

    def reveal(self):
        self.revealed = True

    def toggle_flag(self):
        self.flagged = not self.flagged

    def set_mine(self):
        self.is_mine = True

    def set_neighbors(self, count):
        self.neighboring_mines = count


def initialize_grid():
    grid = [[Tile(x, y) for y in range(GRID_SIZE)] for x in range(GRID_SIZE)]
    
    mines_placed = 0
    while mines_placed < MINE_COUNT:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if not grid[x][y].is_mine:
            grid[x][y].set_mine()
            mines_placed += 1


    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if not grid[x][y].is_mine:
                
                count = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[nx][ny].is_mine:
                            count += 1
                grid[x][y].set_neighbors(count)

    return grid


def draw_grid(grid):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            tile = grid[x][y]
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            
            if tile.revealed:
                pygame.draw.rect(screen, WHITE, rect)
                if tile.is_mine:
                    pygame.draw.circle(screen, BLACK, rect.center, TILE_SIZE // 4)
                elif tile.neighboring_mines > 0:
                    text = FONT.render(str(tile.neighboring_mines), True, BLACK)
                    screen.blit(text, (x * TILE_SIZE + TILE_SIZE // 4, y * TILE_SIZE + TILE_SIZE // 4))
            else:
                pygame.draw.rect(screen, GRAY, rect)

            pygame.draw.rect(screen, BLACK, rect, 2)

            if tile.flagged:
                pygame.draw.line(screen, BLUE, rect.topleft, rect.bottomright, 2)
                pygame.draw.line(screen, BLUE, rect.bottomleft, rect.topright, 2)


def reveal_neighbors(grid, x, y):
    if grid[x][y].neighboring_mines == 0:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    if not grid[nx][ny].revealed and not grid[nx][ny].flagged:
                        grid[nx][ny].reveal()
                        if grid[nx][ny].neighboring_mines == 0:
                            reveal_neighbors(grid, nx, ny)


def check_game_over(grid):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if not grid[x][y].revealed and not grid[x][y].is_mine:
                return False  # The game is not over yet
    return True  # All non-mine tiles are revealed, the game is won


def main():
    grid = initialize_grid()
    clock = pygame.time.Clock()
    game_over = False
    win = False

    while True:
        screen.fill(WHITE)

        if game_over:
            if win:
                message = "You Win!"
            else:
                message = "Game Over!"
            text = FONT.render(message, True, RED)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        else:
            draw_grid(grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                x //= TILE_SIZE
                y //= TILE_SIZE
                tile = grid[x][y]

                if event.button == 1:  
                    if tile.is_mine:
                        game_over = True
                    else:
                        tile.reveal()
                        reveal_neighbors(grid, x, y)
                        if check_game_over(grid):
                            game_over = True
                            win = True
                elif event.button == 3:  
                    tile.toggle_flag()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()