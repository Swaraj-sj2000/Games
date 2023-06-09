import pygame
import sys

# Initialize Pygame
pygame.init()

# Create the game window
WINDOW_SIZE = (300, 300)
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set the title of the window
pygame.display.set_caption("Tic Tac Toe")

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Define the font
FONT = pygame.font.Font(None, 50)

# Define the grid
grid = [[None, None, None], [None, None, None], [None, None, None]]

# Define the turn variable
turn = "X"

# Define the function to draw the grid
def draw_grid():
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(screen, WHITE, (j * 100, i * 100, 100, 100), 1)
            if grid[i][j] == "X":
                x = j * 100 + 50
                y = i * 100 + 50
                pygame.draw.line(screen, BLACK, (x - 25, y - 25), (x + 25, y + 25), 2)
                pygame.draw.line(screen, BLACK, (x + 25, y - 25), (x - 25, y + 25), 2)
            elif grid[i][j] == "O":
                x = j * 100 + 50
                y = i * 100 + 50
                pygame.draw.circle(screen, BLACK, (x, y), 25, 2)

# Define the function to check if there is a winner
def check_winner():
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] and grid[i][0] is not None:
            return grid[i][0]
        if grid[0][i] == grid[1][i] == grid[2][i] and grid[0][i] is not None:
            return grid[0][i]
    if grid[0][0] == grid[1][1] == grid[2][2] and grid[0][0] is not None:
        return grid[0][0]
    if grid[0][2] == grid[1][1] == grid[2][0] and grid[0][2] is not None:
        return grid[0][2]
    if all(all(row) for row in grid):
        return "tie"
    return None

# Define the main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and check_winner() is None:
            x, y = pygame.mouse.get_pos()
            row = y // 100
            col = x // 100
            if grid[row][col] is None:
                grid[row][col] = turn
                if turn == "X":
                    turn = "O"
                else:
                    turn = "X"

    screen.fill(GRAY)
    draw_grid()
    if check_winner() is not None:
        winner = check_winner()
        text = FONT.render(f"{winner} wins!", True, BLACK)
        text_rect = text.get_rect(center=(150, 150))
        if winner == "tie":
            text = FONT.render("Tie!", True, BLACK)
            text_rect = text.get_rect(center=(150, 150))
        screen.blit(text, text_rect)
    pygame.display.update()
