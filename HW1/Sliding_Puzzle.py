import random

# Display a brief introduction about the game
print('Welcome to 8-tile sliding puzzle!')
print('The objective is to rearrange the numbered tiles into a sequential order(left to right, top to bottom).')

# Get user input for moves
rawStr = input('Enter 4 letters used for the left, right, up and down moves >').lower()
rawStr_without_spaces = rawStr.replace(' ', '')
while len(set(rawStr_without_spaces)) != 4 or not all(c.isalpha() for c in set(rawStr_without_spaces)):
    print('Invalid input. Please make sure you enter exactly 4 unique letters (a-z).')
    rawStr = input('Enter 4 letters used for the left, right, up and down moves >').lower()
    rawStr_without_spaces = rawStr.replace(' ', '')
else:
    left, right, up, down = rawStr_without_spaces


# Function to generate a random solvable puzzle state
def generate_random_puzzle():
    # 0 represents the empty space
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    random_state = goal_state.copy()
    random.shuffle(random_state)

    # Shuffle the puzzle until a solvable state is achieved
    while not is_solvable(random_state):
        random.shuffle(random_state)

    return random_state


# Function to check if a puzzle state is solvable
def is_solvable(puzzle):
    inversions = count_inversions(puzzle)
    return inversions % 2 == 1


# Function to count inversions in a puzzle state
def count_inversions(puzzle):
    inversions = 0
    for i in range(len(puzzle)):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] > puzzle[j] > 0:
                inversions += 1
    return inversions


# Function to print the puzzle in a readable format
def print_table(puzzle):
    result = ''
    for i in range(3):
        if i % 2 == 0:
            for j in range(3):
                index = i * 3 + j
                result += str(puzzle[index]) + ' ' if puzzle[index] != 0 else '  '
        else:
            for j in range(2, -1, -1):
                index = i * 3 + j
                result += str(puzzle[index]) + ' ' if puzzle[index] != 0 else '  '
        result += '\n'
    return result


# Functions to handle movement in different directions
def move_left(puzzle):
    reordered_list = reorder(puzzle)
    empty_index = reordered_list.index(0)
    if empty_index % 3 != 2:
        reordered_list[empty_index], reordered_list[empty_index + 1] = reordered_list[empty_index + 1], reordered_list[
            empty_index]
        reordered_list = reorder(reordered_list)
        return reordered_list
    else:
        print("Invalid move. Cannot move left.")
        reordered_list = reorder(reordered_list)
        return reordered_list


def move_right(puzzle):
    reordered_list = reorder(puzzle)
    empty_index = reordered_list.index(0)
    if empty_index % 3 != 0:
        reordered_list[empty_index], reordered_list[empty_index - 1] = reordered_list[empty_index - 1], reordered_list[
            empty_index]
        reordered_list = reorder(reordered_list)
        return reordered_list
    else:
        print("Invalid move. Cannot move right.")
        reordered_list = reorder(reordered_list)
        return reordered_list


def move_up(puzzle):
    reordered_list = reorder(puzzle)
    empty_index = reordered_list.index(0)
    if empty_index not in [6, 7, 8]:
        reordered_list[empty_index], reordered_list[empty_index + 3] = reordered_list[empty_index + 3], reordered_list[
            empty_index]
        reordered_list = reorder(reordered_list)
        return reordered_list
    else:
        print("Invalid move. Cannot move up.")
        reordered_list = reorder(reordered_list)
        return reordered_list


def move_down(puzzle):
    reordered_list = reorder(puzzle)
    empty_index = reordered_list.index(0)
    if empty_index not in [0, 1, 2]:
        reordered_list[empty_index], reordered_list[empty_index - 3] = reordered_list[empty_index - 3], reordered_list[
            empty_index]
        reordered_list = reorder(reordered_list)
        return reordered_list
    else:
        print("Invalid move. Cannot move down.")
        reordered_list = reorder(reordered_list)
        return reordered_list


# Function to reorder puzzle elements
def reorder(puzzle):
    reordered_list = puzzle[:]
    reordered_list[3], reordered_list[5] = reordered_list[5], reordered_list[3]
    return reordered_list


# Main game loop
def main():
    total_steps = 0
    current_puzzle = generate_random_puzzle()
    while True:
        print(print_table(current_puzzle))
        empty_index = current_puzzle.index(0)
        possible_moves = []
        # Check possible moves based on the empty space position
        if empty_index not in [2, 3, 8]:
            possible_moves.append(f'Left-{left}')
        if empty_index not in [0, 5, 6]:
            possible_moves.append(f'Right-{right}')
        if empty_index not in [0, 1, 2]:
            possible_moves.append(f'Down-{down}')
        if empty_index not in [6, 7, 8]:
            possible_moves.append(f'Up-{up}')

        # Check if the puzzle is solved
        if current_puzzle == [1, 2, 3, 6, 5, 4, 7, 8, 0]:
            print(f"Congratulations! You've solved the puzzle in {total_steps} moves!\n")
            reply = input("Enter 'n' for another game, or 'q' to end the game >").lower()
            reply_without_spaces = reply.replace(' ', '')
            while reply_without_spaces not in ['n', 'q']:
                print('Invalid input.')
                reply = input("Enter 'n' for another game, or 'q' to end the game >").lower()
                reply_without_spaces = reply.replace(' ', '')
            if reply_without_spaces == 'q':
                break
            elif reply_without_spaces == 'n':
                main()
        else:
            move = input("Enter your move" + f"({', '.join(possible_moves)})" + '>').lower()
            move_without_spaces = move.replace(' ', '')
            while move_without_spaces not in [left, right, up, down]:
                print('Invalid input.')
                move = input("Enter your move" + f"({', '.join(possible_moves)})" + '>').lower()
                move_without_spaces = move.replace(' ', '')
            # Perform the chosen move
            if move_without_spaces == left:
                current_puzzle = move_left(current_puzzle)
            elif move_without_spaces == right:
                current_puzzle = move_right(current_puzzle)
            elif move_without_spaces == up:
                current_puzzle = move_up(current_puzzle)
            elif move_without_spaces == down:
                current_puzzle = move_down(current_puzzle)
            total_steps += 1


# Run the game if the script is executed
if __name__ == "__main__":
    main()
