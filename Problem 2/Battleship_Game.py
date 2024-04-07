import random
import time

# Signs:
# "." -> Water
# "#" -> Water that has been shot
# "0" -> Part of ship which is not shot
# "X" -> Part of ship which is shot


grid = [[]]
grid_size = 9
num_of_ships = 4
bullets_left = 50
game_over = False
num_of_ships_sunk = 0
ship_positions = [[]]
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
test_mode = True


def validate_grid_and_place_ship(start_row, end_row, start_col, end_col):
    # Will check if it is safe to place a ship there
    # Returns True or False.

    global grid
    global ship_positions

    valid = True

    for i in range(start_row, end_row):
        for j in range(start_col, end_col):
            if grid[i][j] != '.':
                valid = False
                break

    if valid:
        ship_positions.append([start_row, start_col, end_row, end_col])
        for i in range(start_row, end_row):
            for j in range(start_col, end_col):
                grid[i][j] = '0'

    return valid


def try_to_place_ship_on_grid(row, col, direction, length):
    # Based on the direction try to place the ship on the grid

    global grid_size

    start_row, end_row, start_col, end_col = row, row + 1, col, col + 1

    if direction == "left":
        if col - length < 0:
            return False
        start_col = col - length + 1

    elif direction == "right":
        if col + length >= grid_size:
            return False
        end_col = col + length

    elif direction == "up":
        if row - length < 0:
            return False
        start_row = row - length + 1

    elif direction == "down":
        if row + length >= grid_size:
            return False
        end_row = row + length

    return validate_grid_and_place_ship(start_row, end_row, start_col, end_col)


def create_grid():
    # Randomly creates a grid and
    # places ships in random places

    global grid
    global grid_size
    global num_of_ships
    global ship_positions

    random.seed(time.time())

    rows, cols = grid_size, grid_size

    grid = []

    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(".")
        grid.append(row)

    num_of_ships_placed = 0

    ship_positions = []

    while num_of_ships_placed != num_of_ships:
        random_row = random.randint(0, rows - 1)
        random_col = random.randint(0, cols - 1)
        direction = random.choice(["left", "right", "up", "down"])
        ship_size = random.randint(3, 5)

        if try_to_place_ship_on_grid(random_row, random_col, direction, ship_size):
            num_of_ships_placed += 1


def display_grid():
    # Displays the grid

    global grid
    global alphabet
    global test_mode

    alphabet = alphabet[0:len(grid) + 1]

    for row in range(len(grid)):
        print(alphabet[row], end=") ")

        for col in range(len(grid[row])):
            if grid[row][col] == "0":
                if test_mode:
                    print("0", end=" ")
                else:
                    print(".", end=" ")
            else:
                print(grid[row][col], end=" ")
        print("")

    print(" ", end=" ")

    for i in range(len(grid[0])):
        print(str(i), end=" ")
    print("")


def accept_valid_bullet_placement():
    # Gets a valid row & column to shoot a bullet

    global alphabet
    global grid

    valid = False
    row, col = -1, -1

    while valid is False:
        placement = input("Enter row in Alphabet and column in Integer (e.g. A0): ")
        placement = placement.upper()

        if len(placement) != 2:
            print("Please enter a correct placement")
            continue

        row, col = placement[0], placement[1]

        if not row.isalpha() or not col.isnumeric():
            print("Please enter a correct placement")
            continue

        row = alphabet.find(row)

        if not -1 < row < grid_size:
            print("Please enter a correct placement")
            continue

        col = int(col)

        if not -1 < col < grid_size:
            print("Please enter a correct placement")
            continue

        if grid[row][col] == "#" or grid[row][col] == "X":
            print("This place is already shot")
            continue

        if grid[row][col] == "." or grid[row][col] == "0":
            valid = True

    return row, col


def check_for_ship_sunk(row, col):
    # If all parts of the ship is shot,
    # it is taken as sunk

    global ship_positions
    global grid

    for pos in ship_positions:
        stat_row = pos[0]
        end_row = pos[1]
        start_col = pos[2]
        end_col = pos[3]

        if stat_row <= row <= end_row and start_col <= col <= end_col:
            for r in range(stat_row, end_row):
                for c in range(start_col, end_col):
                    if grid[r][c] != "X":
                        return False
    return True


def shoot():
    # This is for actually shooting a bullet

    global grid
    global num_of_ships_sunk
    global bullets_left

    row, col = accept_valid_bullet_placement()
    print("")
    print("---------------------------------------")

    if grid[row][col] == ".":
        print("You missed !!")
        grid[row][col] = "#"
    elif grid[row][col] == "0":
        print("You hit !!", end=" ")
        grid[row][col] = "X"
        if check_for_ship_sunk(row, col):
            print("A ship was sunk !!")
            num_of_ships_sunk += 1
        else:
            print("A ship was shot !!")

    bullets_left -= 1


def check_game_over():
    # Game is over if all the ships are sunk or no bullet is left

    global num_of_ships_sunk
    global num_of_ships
    global bullets_left
    global game_over

    if num_of_ships == num_of_ships_sunk:
        print("You won !!")
        game_over = True
    elif bullets_left <= 0:
        print("You ran out of bullets !!")
        game_over = True


def main():
    # Entry point of the game

    global game_over

    print("-----Welcome to the Battleship game-----")
    print("You have 50 bullets to play with. Let's begin !!")

    create_grid()

    while not game_over:
        display_grid()
        print(f"Ships remaining: {num_of_ships - num_of_ships_sunk}")
        print(f"Bullets left: {bullets_left}")
        shoot()
        print("---------------------------------------")
        print("")
        check_game_over()


if __name__ == "__main__":
    main()
