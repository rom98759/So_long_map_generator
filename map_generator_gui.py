import random
import sys
from copy import deepcopy
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttkb

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
# INTERFACE GRAPH
# ======================================================================================================================

# Show the generated map in a new window
def show_map_in_new_window(map_data):
    def draw_map(canvas, map_data):
        color_map = {'P': 'midnightblue', 'E': 'firebrick', 'C': 'gold', '1': 'darkgray', '0': 'darkslategray'}
        canvas.delete("all")
        for y, row in enumerate(map_data):
            for x, cell in enumerate(row):
                color = color_map.get(cell, 'black')
                canvas.create_rectangle(
                    x * 20, y * 20, (x + 1) * 20, (y + 1) * 20,
                    fill=color, outline="black"
                )

    def on_mouse_wheel(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def on_shift_mouse_wheel(event):
        canvas.xview_scroll(-1 * (event.delta // 120), "units")

    map_window = tk.Toplevel()
    map_window.title("Map Visualization")

    canvas_width = len(map_data[0]) * 20
    canvas_height = len(map_data) * 20

    base_width = min(canvas_width, 800)
    base_height = min(canvas_height, 600)

    window_width = base_width + 20 if canvas_width > 800 else base_width
    window_height = base_height + 20 if canvas_height > 600 else base_height

    frame = tk.Frame(map_window)
    frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(frame, width=base_width, height=base_height, bg="white")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    h_scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
    h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    v_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.config(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
    canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))

    draw_map(canvas, map_data)

    canvas.bind("<MouseWheel>", on_mouse_wheel)
    canvas.bind("<Shift-MouseWheel>", on_shift_mouse_wheel)

    map_window.geometry(f"{window_width+4}x{window_height+4}")

def validate_arguments(width, height, wall_rate, debug=False):
    """
    Validate the arguments for generating a map.
    Parameters:
    width (int): The width of the map. Must be between 5 and 150 inclusive.
    height (int): The height of the map. Must be between 3 and 150 inclusive.
    wall_rate (int): The percentage of walls in the map. Must not exceed 60%.
    Raises:
    ValueError: If the width is less than 5 or greater than 150.
    ValueError: If the height is less than 3 or greater than 150.
    ValueError: If the wall_rate exceeds 60%.
    Returns:
    bool: True if all arguments are valid.
    """
    if not debug:
        if width < 5 or height < 3:
            raise ValueError("The map dimensions must be at least 5x3.")
        if width > 150 or height > 150:
            raise ValueError("The map dimensions cannot exceed 150x150.")
        if wall_rate > 50:
            raise ValueError("The wall percentage cannot exceed 50%.")

    if (width == 5 and height == 3) or (width == 3 and height == 5):
        wall_rate = 0


    return True

# Graphical User Interface
def gui():
    def generate_action():
        nonlocal map_data
        try:
            width = width_entry.get()
            height = height_entry.get()
            coins = coins_entry.get()
            walls = walls_entry.get()
            path = path_entry.get()

            # Check if all fields are filled
            if not width or not height or not coins or not walls or not path:
                messagebox.showerror("Error", "All fields must be filled.")
                return

            # Check if the values are valid integers
            if not width.isdigit() or not height.isdigit() or not coins.isdigit() or not walls.isdigit():
                messagebox.showerror("Error", "Values must be integers.")
                return

            # Convert the inputs to integers
            width = int(width)
            height = int(height)
            coins = int(coins)
            walls = int(walls)

            # If debug mode is enabled, get the max iterations value
            max_iterations = None
            if debug_mode.get():
                max_iterations = max_iterations_entry.get()
                if not max_iterations.isdigit() or int(max_iterations) <= 0:
                    messagebox.showerror("Error", "Max iterations must be a positive integer.")
                    return
                max_iterations = int(max_iterations)

            # Validate arguments considering the debug mode
            if validate_arguments(width, height, walls, debug=debug_mode.get()):
                try:
                    iterations = 0
                    while iterations < (max_iterations if max_iterations else 5000):
                        map_data = generate_map(width, height, coins, walls)
                        if print_iterations.get() and debug_mode.get():
                            print(f"Iteration {iterations}")
                        if validate_map(map_data):
                            save_map_to_file(map_data, path)
                            status_label.config(text="Map generated successfully.", bootstyle="success")
                            visualize_button.config(state=tk.NORMAL)
                            show_map_in_new_window(map_data)
                            if print_map_in_terminal.get() and debug_mode.get():
                                show_map_in_terminal(map_data)
                            if print_map_stats.get() and debug_mode.get():
                                show_stats(map_data)
                            break
                        else:
                            iterations += 1
                            if iterations >= (max_iterations if max_iterations else 5000):
                                status_label.config(text="Max iterations reached.", bootstyle="danger")
                                break
                            status_label.config(text=f"Invalid map, trying again... (Attempt {iterations}/{max_iterations})", bootstyle="warning")
                except TimeoutError as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showerror("Error", "The provided arguments are invalid.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def browse_action():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".ber",
            filetypes=[("Files .ber", "*.ber")],
        )
        if file_path:
            path_entry.delete(0, tk.END)
            path_entry.insert(0, file_path)

    def quit_action():
        root.quit()

    def show_stats(map_data):
        """ Affiche les statistiques de la carte générée """
        num_coins = sum(row.count('C') for row in map_data)
        num_walls = sum(row.count('1') for row in map_data)
        num_empty = sum(row.count('0') for row in map_data)
        print(f"Coins: {num_coins}")
        print(f"Walls: {num_walls}")
        print(f"Empty spaces: {num_empty}")
        show_debug_stats(map_data)

    def show_debug_stats(map_data):
        player_pos = None
        exit_pos = None
        for y, row in enumerate(map_data):
            for x, cell in enumerate(row):
                if cell == 'P':
                    player_pos = (x, y)
                if cell == 'E':
                    exit_pos = (x, y)
        if player_pos and exit_pos:
            print(f"Player position: {player_pos}")
            print(f"Exit position: {exit_pos}")
        else:
            print("Player or Exit not found in map.")

    def show_map_in_terminal(map_data):
        """ Display the map in the terminal with characters 1, 0, C, P, E """
        print("Map in terminal:")
        for row in map_data:
            print(' '.join(row))

    # Create the main window
    root = ttkb.Window(themename="vapor")
    root.title("So_long Map Generator")
    root.geometry("400x400")
    root.resizable(True, True)

    # Add the input fields
    ttkb.Label(root, text="Width :").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    width_entry = ttkb.Entry(root)
    width_entry.insert(0, "20")
    width_entry.grid(row=0, column=1, padx=10, pady=5)

    ttkb.Label(root, text="Height :").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    height_entry = ttkb.Entry(root)
    height_entry.insert(0, "20")
    height_entry.grid(row=1, column=1, padx=10, pady=5)

    ttkb.Label(root, text="Coins :").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    coins_entry = ttkb.Entry(root)
    coins_entry.insert(0, "10")
    coins_entry.grid(row=2, column=1, padx=10, pady=5)
    ttkb.Label(root, text="%").grid(row=2, column=2, padx=10, pady=5, sticky="w")


    ttkb.Label(root, text="Walls:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    walls_entry = ttkb.Entry(root)
    walls_entry.insert(0, "10")
    walls_entry.grid(row=3, column=1, padx=10, pady=5)
    ttkb.Label(root, text="%").grid(row=3, column=2, padx=10, pady=5, sticky="w")


    ttkb.Label(root, text="Save path :").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    path_entry = ttkb.Entry(root)
    path_entry.insert(0, "maps/map.ber")
    path_entry.grid(row=4, column=1, padx=10, pady=5)

    browse_button = ttkb.Button(root, text="Browse", command=browse_action, bootstyle="info-outline")
    browse_button.grid(row=4, column=2, padx=10, pady=5)

    map_data = None

    # Generate button
    generate_button = ttkb.Button(root, text="Generate", command=generate_action, bootstyle="success-outline", width=12)
    generate_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

    # Visualize button
    visualize_button = ttkb.Button(root, text="Visualize", state=tk.DISABLED, command=lambda: show_map_in_new_window(map_data), bootstyle="info-outline", width=12)
    visualize_button.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

    # Quit button
    quit_button = ttkb.Button(root, text="Quit", command=quit_action, bootstyle="danger-outline", width=12)
    quit_button.grid(row=5, column=2, padx=10, pady=5, sticky="ew")

    # Status label
    status_label = ttkb.Label(root, text="Ready.", bootstyle="secondary", anchor="w")
    status_label.grid(row=6, column=0, columnspan=3, pady=5)

    # Debug mode checkbox
    debug_mode = tk.BooleanVar()  # This variable will track if debug mode is enabled
    debug_checkbox = ttkb.Checkbutton(root, text="Enable Debug Mode", variable=debug_mode)
    debug_checkbox.grid(row=7, column=0, columnspan=3, pady=5)

    # Max iterations label and entry (hidden by default)
    max_iterations_label = ttkb.Label(root, text="Max Iterations :")
    max_iterations_entry = ttkb.Entry(root)
    max_iterations_entry.insert(0, "5000")

    # Initially hide the max iterations label and entry
    max_iterations_label.grid_forget()
    max_iterations_entry.grid_forget()

    # Print iterations to the console when debug mode is enabled checkbox (hidden by default)
    print_iterations = tk.BooleanVar()
    print_iterations_checkbox = ttkb.Checkbutton(root, text="Print Iterations ", variable=print_iterations)
    print_iterations_checkbox.grid_forget()

    # Show the map in the terminal when debug mode is enabled checkbox (hidden by default)
    print_map_in_terminal = tk.BooleanVar()
    print_map_in_terminal_checkbox = ttkb.Checkbutton(root, text="Print Map in Terminal ", variable=print_map_in_terminal)
    print_map_in_terminal_checkbox.grid_forget()

    # Show the map statistics when debug mode is enabled checkbox (hidden by default)
    print_map_stats = tk.BooleanVar()
    print_map_stats_checkbox = ttkb.Checkbutton(root, text="Show Map Stats ", variable=print_map_stats)
    print_map_stats_checkbox.grid_forget()

    # Show or hide max iterations input based on the debug mode
    def toggle_debug_mode():
        if debug_mode.get():
            max_iterations_label.grid(row=11, column=0, padx=10, pady=5, sticky="w")
            max_iterations_entry.grid(row=11, column=1, padx=10, pady=5, sticky="ew")
            print_map_stats_checkbox.grid(row=9, column=0, padx=10, pady=5, sticky="w", columnspan=2)
            print_map_in_terminal_checkbox.grid(row=10, column=0, padx=10, pady=5, sticky="w", columnspan=2)
            print_iterations_checkbox.grid(row=8, column=0, padx=10, pady=5, sticky="w", columnspan=2)

            # Resize the window to accommodate debug mode fields
            root.geometry("400x500")  # Resize the window to make space for debug elements
        else:
            max_iterations_label.grid_forget()
            max_iterations_entry.grid_forget()
            print_iterations_checkbox.grid_forget()
            print_map_in_terminal_checkbox.grid_forget()
            print_map_stats_checkbox.grid_forget()

            # Resize the window back to its original size when debug mode is off
            root.geometry("400x400")

    # Link the checkbox to toggle debug mode
    debug_checkbox.config(command=toggle_debug_mode)

    # Configure the layout
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    root.grid_rowconfigure(5, weight=0)
    root.grid_rowconfigure(6, weight=0)

    root.mainloop()


if __name__ == "__main__":
    gui()
