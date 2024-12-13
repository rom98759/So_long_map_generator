import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import ttkbootstrap as ttkb
import random

def load_map_from_file(file_path):
    """Load map data from a file."""
    try:
        with open(file_path, "r") as file:
            map_data = [list(line.strip()) for line in file.readlines()]
        return map_data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load map: {e}")
        return None

def save_map_to_file(map_data, file_path):
    """Save map data to a file."""
    try:
        with open(file_path, "w") as file:
            for row in map_data:
                file.write("".join(row) + "\n")
        messagebox.showinfo("Success", "Map saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save map: {e}")

def validate_map_data(map_data):
    """Validate the map data."""
    rows = len(map_data)
    cols = len(map_data[0])
    player_count = 0
    exit_count = 0
    coin_count = 0

    for y, row in enumerate(map_data):
        if len(row) != cols:
            return False, "All rows must have the same number of columns."
        for x, cell in enumerate(row):
            if y == 0 or y == rows - 1 or x == 0 or x == cols - 1:
                if cell != '1':
                    return False, "The map must be surrounded by walls."
            if cell == 'P':
                player_count += 1
            elif cell == 'E':
                exit_count += 1
            elif cell == 'C':
                coin_count += 1

    if player_count != 1:
        return False, "There must be exactly one player."
    if exit_count != 1:
        return False, "There must be exactly one exit."
    if coin_count < 1:
        return False, "There must be at least one coin."

    return True, "The map is valid."

def open_map_editor(map_data):
    """Open the map editor window."""
    if map_data is None:
        messagebox.showerror("Error", "No map data to edit!")
        return

    editor_window = tk.Toplevel()
    editor_window.title("Map Editor")

    cell_size = 30
    selected_tile = tk.StringVar(value='0')

    # Colors for different tiles
    color_map = {'P': 'midnightblue', 'E': 'firebrick', 'C': 'gold', '1': 'darkgray', '0': 'darkslategray'}
    tile_types = {'Player': 'P', 'Exit': 'E', 'Coin': 'C', 'Wall': '1', 'Empty': '0'}

    # Canvas for map
    canvas = tk.Canvas(editor_window, width=len(map_data[0]) * cell_size, height=len(map_data) * cell_size)
    canvas.grid(row=0, column=1, rowspan=5, padx=10, pady=10)

    def draw_map():
        """Draw the map on the canvas."""
        canvas.delete("all")
        for y, row in enumerate(map_data):
            for x, cell in enumerate(row):
                color = color_map.get(cell, 'white')
                canvas.create_rectangle(
                    x * cell_size, y * cell_size,
                    (x + 1) * cell_size, (y + 1) * cell_size,
                    fill=color, outline="black"
                )
                if color == 'white':
                    canvas.create_text(
                        x * cell_size + cell_size / 2, y * cell_size + cell_size / 2,
                        text=cell, fill='black', font=('Helvetica', 10)
                    )

    # Global variable to track the dragging state left-click
    is_dragging_left = False
    is_dragging_right = False
    is_locked = tk.BooleanVar(value=False)

    def on_canvas_click(event):
        """Handle clicks to change tile type."""
        global is_dragging_left, is_dragging_right
        x, y = event.x // cell_size, event.y // cell_size
        if is_locked.get() and (x == 0 or y == 0 or x == len(map_data[0]) - 1 or y == len(map_data) - 1):
            return  # Prevent editing of outer walls if locked
        if 0 <= y < len(map_data) and 0 <= x < len(map_data[0]):
            if event.num == 1:  # Left click
                map_data[y][x] = selected_tile.get()
            elif event.num == 3:  # Right click
                map_data[y][x] = '0'  # Set to EMPTY
            draw_map()
            is_dragging_left = event.num == 1
            is_dragging_right = event.num == 3

    def on_canvas_motion(event):
        """Handle mouse movement to change tile type while dragging."""
        global is_dragging_left, is_dragging_right
        x, y = event.x // cell_size, event.y // cell_size
        if is_locked.get() and (x == 0 or y == 0 or x == len(map_data[0]) - 1 or y == len(map_data) - 1):
            return  # Prevent editing of outer walls if locked
        if is_dragging_left and 0 <= y < len(map_data) and 0 <= x < len(map_data[0]):
            map_data[y][x] = selected_tile.get()
            draw_map()
        elif is_dragging_right and 0 <= y < len(map_data) and 0 <= x < len(map_data[0]):
            map_data[y][x] = '0'
            draw_map()

    def on_canvas_release(event):
        """Stop the drag when mouse button is released."""
        global is_dragging_left, is_dragging_right
        is_dragging_left = False
        is_dragging_right = False

    canvas.bind("<Button-1>", on_canvas_click) # Handle clicks to change tile type
    canvas.bind("<B1-Motion>", on_canvas_motion)  # Handle dragging/moving with click held
    canvas.bind("<ButtonRelease-1>", on_canvas_release)  # Stop dragging when mouse is released
    canvas.bind("<Button-3>", on_canvas_click)  # Bind right-click event to change to EMPTY
    canvas.bind("<B3-Motion>", on_canvas_motion)  # Bind right-click dragging to change to EMPTY
    canvas.bind("<ButtonRelease-3>", on_canvas_release)  # Stop dragging when mouse is released

    def save_map():
        """Save the current map to a file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".ber",
            filetypes=[("Map Files", "*.ber")],
        )
        if file_path:
            save_map_to_file(map_data, file_path)

    # Update tile selection buttons dynamically
    def update_tile_buttons_and_legend():
        """Update the tile selection buttons and legend."""
        for widget in tile_frame.winfo_children():
            widget.destroy()

        # Add tile type buttons and legend
        ttkb.Label(tile_frame, text="Tile Types & Legend", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=3, padx=10, pady=5)

        row = 1
        for label, value in tile_types.items():
            ttkb.Radiobutton(tile_frame, text=label, variable=selected_tile, value=value).grid(row=row, column=1, sticky=tk.W, padx=10, pady=5)
            color_box = ttkb.Label(tile_frame, text="   ", background=color_map[value], width=10)
            color_box.grid(row=row, column=0, padx=10, pady=5)
            color_box.bind("<Button-1>", lambda e, name=value: edit_tile_color(name))
            legend_label = ttkb.Label(tile_frame, text=f'[{value}]', width=10, anchor="w")
            legend_label.grid(row=row, column=2, padx=10, pady=5)
            row += 1

    tile_frame = ttkb.Frame(editor_window)
    tile_frame.grid(row=0, column=0, padx=10, pady=10, rowspan=5)

    # Add/Edit Tile Type Features
    def add_tile_type():
        """Add a new tile type with a character and color."""
        def save_new_type():
            type_name = type_name_entry.get()
            char = char_entry.get()
            if char in tile_types.values():
                messagebox.showerror("Error", "Tile type already exists!")
                return
            if type_name in tile_types:
                messagebox.showerror("Error", "Tile type name already exists!")
                return
            if len(char) != 1:
                messagebox.showerror("Error", "Character must be a single character!")
                return
            color = colorchooser.askcolor()[1]
            if type_name and char and color:
                color_map[type_name] = color
                tile_types[type_name] = char
                update_tile_buttons_and_legend()
                add_window.destroy()
                draw_map()

        # Window to add a new tile type
        add_window = tk.Toplevel(editor_window)
        add_window.title("Add New Tile Type")

        ttkb.Label(add_window, text="Type Name:").grid(row=0, column=0, padx=10, pady=5)
        type_name_entry = ttkb.Entry(add_window)
        type_name_entry.grid(row=0, column=1, padx=10, pady=5)

        ttkb.Label(add_window, text="Character:").grid(row=1, column=0, padx=10, pady=5)
        char_entry = ttkb.Entry(add_window)
        char_entry.grid(row=1, column=1, padx=10, pady=5)

        ttkb.Button(add_window, text="Save", command=save_new_type).grid(row=2, column=0, columnspan=2, pady=10)

    def edit_tile_color(type_name):
        """Edit the color of an existing tile type."""
        color = colorchooser.askcolor()[1]
        if color:
            color_map[type_name] = color
            update_tile_buttons_and_legend()
            draw_map()

    def detect_unknown_tiles():
        """Detect unknown tiles in the map and add them dynamically."""
        for row in map_data:
            for cell in row:
                if cell not in tile_types.values():
                    # Add unknown character with a random color
                    random_color = "#%06x" % random.randint(0, 0xFFFFFF)
                    tile_types[f"Unknown ({cell})"] = cell
                    color_map[cell] = random_color
        update_tile_buttons_and_legend()

    def delete_tile_type():
        """Delete the currently selected tile type."""
        selected_label = selected_tile.get()
        for label, value in list(tile_types.items()):
            if value == selected_label:
                del tile_types[label]
                del color_map[value]
                update_tile_buttons_and_legend()
                return

    ttkb.Button(editor_window, text="Add Tile Type", command=add_tile_type, bootstyle="primary").grid(row=6, column=0, pady=5)
    ttkb.Button(editor_window, text="Delete Tile Type", command=delete_tile_type, bootstyle="danger").grid(row=7, column=0, pady=5)

    def validate_map():
        """Validate the current map."""
        is_valid, message = validate_map_data(map_data)
        if is_valid:
            messagebox.showinfo("Validation", message)
        else:
            messagebox.showerror("Validation Error", message)

    ttkb.Button(editor_window, text="Validate Map", command=validate_map, bootstyle="warning").grid(row=1, column=2, pady=0, padx=10)
    ttkb.Checkbutton(editor_window, text="Lock Outer Walls", variable=is_locked, bootstyle="info").grid(row=2, column=2, pady=0, padx=10)
    ttkb.Button(editor_window, text="Save Map", command=save_map, bootstyle="success").grid(row=3, column=2, pady=0, padx=10)

    ttkb.Label(editor_window, text=" ").grid(row=0, column=3, padx=20)

    detect_unknown_tiles()
    draw_map()

def help_button():
    import os
    os.system("README.md")

def main():
    """Main GUI application."""
    root = ttkb.Window(themename="darkly")
    root.title("Map Editor")
    root.geometry("500x400")

    def load_map():
        """Load a map from a file and open the editor."""
        file_path = filedialog.askopenfilename(
            title="Open Map File",
            filetypes=[("Map Files", "*.ber")]
        )
        if file_path:
            map_data = load_map_from_file(file_path)
            if map_data:
                # Reduit la fenêtre principale
                root.iconify()
                open_map_editor(map_data)

    ttkb.Label(root, text="Welcome to the Map Editor", font=("Helvetica", 16)).pack(pady=10)
    ttkb.Button(root, text="Open Map", command=load_map, bootstyle="primary", width=20).pack(pady=5)
    ttkb.Button(root, text="Quit", command=root.quit, bootstyle="danger", width=20).pack(pady=5)

    # HELP BUTTON
    ttkb.Button(root, text="Help", command=help_button, bootstyle="info", width=20).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
