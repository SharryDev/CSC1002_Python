import turtle
import random

tile_size = 80
dimension = 3
puzzle = []
screen = turtle.Screen()


def prompt_for_size():
    """
    Prompt the user to enter the size of the puzzle.

    Returns:
        int: The dimension of the puzzle.
    """
    global dimension
    dimension = int(screen.numinput("Puzzle", "Puzzle Dimension >", minval=3, maxval=5))
    return dimension


def generate_random_puzzle():
    """
    Generate a random solvable puzzle of given dimension.

    Returns:
        list: A randomly generated solvable puzzle.
    """
    goal_state = list(range(1, dimension*dimension)) + [0]
    global puzzle
    puzzle = goal_state.copy()
    random.shuffle(puzzle)

    while not is_solvable():
        random.shuffle(puzzle)

    return puzzle


def is_solvable():
    """
    Check if a puzzle state is solvable.

    Returns:
        bool: True if the puzzle is solvable, False otherwise.
    """
    inversions = count_inversions()
    if dimension == 3 or dimension == 4:
        return inversions % 2 == 1
    elif dimension == 5:
        return inversions % 2 == 0


def count_inversions():
    """
    Count inversions in a puzzle state.

    Returns:
        int: The number of inversions.
    """
    inversions = 0
    for i in range(len(puzzle)):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] > puzzle[j] > 0:
                inversions += 1
    return inversions


def draw_tile(x, y, value, color):
    """
    Draw a single tile on the screen.

    Args:
        x (int): X-coordinate of the tile.
        y (int): Y-coordinate of the tile.
        value (int): Value of the tile.
        color (str): Color of the tile.
    """
    turtle.penup()
    turtle.goto(x - tile_size / 2, y - tile_size / 2)
    turtle.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(tile_size)
        turtle.left(90)
    turtle.end_fill()

    # Draw white dividing lines
    turtle.penup()
    turtle.goto(x - tile_size / 2, y + tile_size / 2)
    turtle.pendown()
    turtle.pencolor("white")
    turtle.setheading(0)
    for _ in range(4):
        turtle.forward(tile_size)
        turtle.right(90)

    # Write the value in the center
    turtle.penup()
    turtle.goto(x, y - tile_size / 4)  # Adjusting y position for better centering
    turtle.write(value, align="center", font=("Arial", int(tile_size / 2), "normal"))


def display_puzzle(color):
    """
    Display the puzzle on the screen.

    Args:
        color (str): Color of the puzzle tiles.
    """
    canvas_size = dimension * tile_size + 100
    screen.setup(canvas_size, canvas_size)
    global puzzle
    puzzle = reorder()
    turtle.tracer(0)
    turtle.speed(0)
    turtle.hideturtle()
    turtle.clear()
    total_size = dimension * tile_size
    start_x = -total_size // 2 + tile_size // 2  # Start x coordinate for centering
    start_y = total_size // 2 - tile_size // 2  # Start y coordinate for centering
    for i in range(len(puzzle)):
        row = i // dimension
        col = i % dimension
        x = start_x + col * tile_size
        y = start_y - row * tile_size
        if puzzle[i] > 0:
            draw_tile(x, y, puzzle[i], color)
    puzzle = reorder()
    turtle.update()


def reorder():
    """
    Reorder the puzzle based on its dimension.

    Returns:
        list: The reordered puzzle state.
    """
    global puzzle
    reordered_puzzle = puzzle[:]
    if dimension == 3:
        reordered_puzzle[3], reordered_puzzle[5] = reordered_puzzle[5], reordered_puzzle[3]
    elif dimension == 4:
        reordered_puzzle[4:8], reordered_puzzle[12:16] = reordered_puzzle[7:3:-1], reordered_puzzle[15:11:-1]
    elif dimension == 5:
        reordered_puzzle[5:10], reordered_puzzle[15:20] = reordered_puzzle[9:4:-1], reordered_puzzle[19:14:-1]
    return reordered_puzzle


def move_tile(x, y):
    """
    Move a tile to the empty space.

    Args:
        x (int): X-coordinate of the clicked position.
        y (int): Y-coordinate of the clicked position.
    """
    global puzzle
    total_size = dimension * tile_size
    col = int((x + total_size / 2) // tile_size) + 1
    row = int(abs(y - total_size / 2) // tile_size) + 1
    index = (row-1) * dimension + col
    puzzle = reorder()
    if 0 < row <= dimension and 0 < col <= dimension and is_adjacent(index, puzzle.index(0)+1):
        index = index - 1
        empty_index = puzzle.index(0)
        puzzle[index], puzzle[empty_index] = puzzle[empty_index], puzzle[index]
        puzzle = reorder()
        display_puzzle('blue')
        reorder_puzzle = reorder()
        if reorder_puzzle == list(range(1, dimension*dimension)) + [0]:
            change_tiles_color()
    else:
        puzzle = reorder()
        reorder_puzzle = reorder()
        if reorder_puzzle == list(range(1, dimension*dimension)) + [0]:
            change_tiles_color()


def is_adjacent(index1, index2):
    """
    Check if two tiles are adjacent.

    Args:
        index1 (int): Index of the first tile.
        index2 (int): Index of the second tile.

    Returns:
        bool: True if the tiles are adjacent, False otherwise.
    """
    row1, col1 = ((index1-1) // dimension) + 1, ((index1-1) % dimension) + 1
    row2, col2 = ((index2-1) // dimension) + 1, ((index2-1) % dimension) + 1
    if row1 == row2 and abs(col1 - col2) == 1:
        return True
    elif col1 == col2 and abs(row1 - row2) == 1:
        return True
    else:
        return False


def change_tiles_color():
    """
    Change the color of tiles and end the game.
    """
    turtle.clear()
    display_puzzle('red')
    turtle.done()


def on_click(x, y):
    # Handle click event on the screen.
    move_tile(int(x), int(y))


def main():
    """
    Main function to run the game.
    """
    global dimension
    global puzzle
    dimension = prompt_for_size()
    screen.setup(340, 340)
    puzzle = generate_random_puzzle()
    display_puzzle('blue')
    turtle.onscreenclick(on_click)
    turtle.done()


# Run the game if the script is executed
if __name__ == "__main__":
    main()
