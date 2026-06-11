import tkinter as tk
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25
GAME_SPEED_MS = 120

WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Tile) and self.x == other.x and self.y == other.y


def random_food_position(snake_body):
    while True:
        x = random.randint(0, COLS - 1) * TILE_SIZE
        y = random.randint(0, ROWS - 1) * TILE_SIZE
        candidate = Tile(x, y)
        if candidate not in snake_body:
            return candidate


# game window
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

canvas = tk.Canvas(
    window,
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    bg="black",
    borderwidth=0,
    highlightthickness=0,
)
canvas.pack()
window.update()

# center the window
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int(screen_width // 2) - (WINDOW_WIDTH // 2)
window_y = int(screen_height // 2) - (WINDOW_HEIGHT // 2)
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{window_x}+{window_y}")
window.focus_set()

# initialize game
snake_body = [
    Tile(5 * TILE_SIZE, 5 * TILE_SIZE),
]
food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
velocity_x = 1
velocity_y = 0


def change_directions(event):
    global velocity_x, velocity_y

    if event.keysym == "Up" and velocity_y == 0:
        velocity_x = 0
        velocity_y = -1
    elif event.keysym == "Down" and velocity_y == 0:
        velocity_x = 0
        velocity_y = 1
    elif event.keysym == "Left" and velocity_x == 0:
        velocity_x = -1
        velocity_y = 0
    elif event.keysym == "Right" and velocity_x == 0:
        velocity_x = 1
        velocity_y = 0


def wrap_position(tile):
    if tile.x < 0:
        tile.x = (COLS - 1) * TILE_SIZE
    elif tile.x >= WINDOW_WIDTH:
        tile.x = 0

    if tile.y < 0:
        tile.y = (ROWS - 1) * TILE_SIZE
    elif tile.y >= WINDOW_HEIGHT:
        tile.y = 0


def move_snake():
    global snake_body, food

    head = snake_body[0]
    new_head = Tile(head.x + velocity_x * TILE_SIZE, head.y + velocity_y * TILE_SIZE)
    wrap_position(new_head)

    if new_head in snake_body:
        game_over()
        return

    snake_body.insert(0, new_head)

    if new_head == food:
        food = random_food_position(snake_body)
    else:
        snake_body.pop()


def draw():
    canvas.delete("all")
    for segment in snake_body:
        canvas.create_rectangle(
            segment.x,
            segment.y,
            segment.x + TILE_SIZE,
            segment.y + TILE_SIZE,
            fill="lime green",
            outline="black",
        )
    canvas.create_rectangle(
        food.x,
        food.y,
        food.x + TILE_SIZE,
        food.y + TILE_SIZE,
        fill="red",
    )


def game_over():
    canvas.delete("all")
    canvas.create_text(
        WINDOW_WIDTH // 2,
        WINDOW_HEIGHT // 2,
        text="Game Over",
        fill="white",
        font=("Arial", 24, "bold"),
    )


def game_loop():
    move_snake()
    draw()
    window.after(GAME_SPEED_MS, game_loop)


window.bind("<KeyPress>", change_directions)

game_loop()
window.mainloop()
