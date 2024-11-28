import random
import sys
from copy import deepcopy
import argparse

# ======================================================================================================================
# Generate a valid map for the so_long game
# ======================================================================================================================

# Fonction pour générer une carte valide
def generate_map(width, height, coin_rate, wall_rate):
    """
    Generates a 2D map for a game with specified dimensions and rates for coins and walls.
    Args:
        width (int): The width of the map.
        height (int): The height of the map.
        coin_rate (int): The percentage chance to place a coin in an empty space.
        wall_rate (int): The percentage chance to place a wall in an empty space.
    Returns:
        list: A 2D list representing the generated map, where:
            '1' represents a wall,
            '0' represents an empty space,
            'E' represents the exit,
            'P' represents the player start position,
            'C' represents a coin.
    """
    map_data = [['1' for _ in range(width)] for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            map_data[y][x] = '0'

    # Place exit and player randomly on the map
    exit_placed = False
    player_placed = False

    while not exit_placed or not player_placed:
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if map_data[y][x] == '0':
                    if not exit_placed and random.random() < 0.05:
                        map_data[y][x] = 'E'
                        exit_placed = True
                    elif not player_placed and random.random() < 0.05:
                        map_data[y][x] = 'P'
                        player_placed = True

    # Place coins randomly based on coin_rate
    coin_rate = int(coin_rate) / 100
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if map_data[y][x] == '0' and random.random() < coin_rate:
                map_data[y][x] = 'C'

    # If coins haven't already taken all the space
    # Place walls randomly based on wall_rate
    wall_rate = int(wall_rate) / 100
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if map_data[y][x] == '0' and random.random() < wall_rate:
                map_data[y][x] = '1'

    return map_data

def flood_fill(map_data, x, y, visited, target):
    """
    Perform a flood fill algorithm to count the number of target cells in a 2D map.
    Args:
        map_data (list of list of str): The 2D map represented as a list of lists of strings.
        x (int): The starting x-coordinate for the flood fill.
        y (int): The starting y-coordinate for the flood fill.
        visited (list of list of bool): A 2D list to keep track of visited cells.
        target (str): The target character to count in the map.
    Returns:
        int: The count of target cells found in the map.
    """
    stack = [(x, y)]
    count = 0

    while stack:
        cx, cy = stack.pop()
        if cx < 0 or cy < 0 or cy >= len(map_data) or cx >= len(map_data[0]):
            continue
        if visited[cy][cx] or map_data[cy][cx] == '1':
            continue

        visited[cy][cx] = True
        if map_data[cy][cx] == target:
            count += 1

        stack.append((cx + 1, cy))
        stack.append((cx - 1, cy))
        stack.append((cx, cy + 1))
        stack.append((cx, cy - 1))

    return count

def validate_map(map_data):
    """
    Validates a game map to ensure it meets specific criteria.
    Args:
        map_data (list of list of str): The game map represented as a 2D list of strings.
    Returns:
        bool: True if the map is valid, False otherwise.
    The validation checks include:
    - The map must be surrounded by walls ('1').
    - The map must contain exactly one player ('P'), one exit ('E'), and at least one collectible ('C').
    - All collectibles must be reachable from the player's starting position.
    - The exit must be reachable from the player's starting position.
    """
    height = len(map_data)
    width = len(map_data[0])

    # Check if the map is surrounded by walls
    if any(map_data[0][x] != '1' or map_data[-1][x] != '1' for x in range(width)):
        return False
    if any(row[0] != '1' or row[-1] != '1' for row in map_data):
        return False

    # Check for exactly one player, one exit, and at least one collectible
    player_count = sum(row.count('P') for row in map_data)
    exit_count = sum(row.count('E') for row in map_data)
    collectible_count = sum(row.count('C') for row in map_data)

    if player_count != 1 or exit_count != 1 or collectible_count < 1:
        return False

    # Check if all collectibles are reachable from the player's starting position
    visited = [[False for _ in range(width)] for _ in range(height)]
    player_pos = [(y, x) for y in range(height) for x in range(width) if map_data[y][x] == 'P'][0]

    reachable_collectibles = flood_fill(deepcopy(map_data), player_pos[1], player_pos[0], visited, 'C')
    if reachable_collectibles < collectible_count:
        return False

    # Check if the exit is reachable from the player's starting position
    visited = [[False for _ in range(width)] for _ in range(height)]
    exit_accessible = flood_fill(deepcopy(map_data), player_pos[1], player_pos[0], visited, 'E') > 0

    return exit_accessible

# ======================================================================================================================
# SAVE MAP TO FILE
# ======================================================================================================================

def save_map_to_file(map_data, filename="maps/map.ber"):
    with open(filename, "w") as file:
        for row in map_data:
            file.write("".join(row) + "\n")


# ======================================================================================================================
# MAIN FUNCTION
# ======================================================================================================================

def main(width=20, height=10, coin_rate="10", wall_rate="10", path="maps/map.ber"):
    while True:
        map_data = generate_map(width, height, coin_rate, wall_rate)
        if validate_map(map_data):
            save_map_to_file(map_data, path)
            print("Map generated and saved to map.ber")
            break
        else:
            print("Error: The generated map is invalid. Generating a new map...")

def check_invalid_args(args):
    if args.width < 3:
        raise argparse.ArgumentTypeError("Width must be greater than or equal to 3")
    if args.height < 3:
        raise argparse.ArgumentTypeError("Height must be greater than or equal to 3")
    if args.width > 150:
        raise argparse.ArgumentTypeError("Width must be less than or equal to 150, otherwise the map is too large")
    if args.height > 150:
        raise argparse.ArgumentTypeError("Height must be less than or equal to 150, otherwise the map is too large")
    if (int(args.coins) < 0 or int(args.coins) > 100):
        raise argparse.ArgumentTypeError("Coin percentage must be between 0 and 100")
    if int(args.walls) < 0 or int(args.walls) > 99:
        raise argparse.ArgumentTypeError("Wall percentage must be between 0 and 99, 100 is not allowed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Map generator for the so_long game.")
    parser.add_argument("-W", "--width", type=int, default=20, help="Width of the map (default: 20)")
    parser.add_argument("-H", "--height", type=int, default=10, help="Height of the map (default: 10)")
    parser.add_argument("-c", "--coins", type=str, default="10", help="Percentage or 'all' for coins (default: 10)")
    parser.add_argument("-w", "--walls", type=str, default="10", help="Percentage of walls (default: 10)")
    parser.add_argument("-p", "--path", type=str, default="maps/map.ber", help="Path to the save file (default: maps/map.ber)")
    args = parser.parse_args()
    check_invalid_args(args)

    main(width=args.width, height=args.height, coin_rate=args.coins, wall_rate=args.walls, path=args.path)