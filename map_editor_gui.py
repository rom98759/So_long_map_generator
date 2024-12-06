import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import ttkbootstrap as ttkb

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

    # Global variable to track the dragging state
    is_dragging = False

    def on_canvas_click(event):
        """Handle clicks to change tile type."""
        global is_dragging
        x, y = event.x // cell_size, event.y // cell_size
        if 0 <= y < len(map_data) and 0 <= x < len(map_data[0]):
            map_data[y][x] = selected_tile.get()
            draw_map()
            is_dragging = True

    def on_canvas_motion(event):
        """Handle mouse movement to change tile type while dragging."""
        global is_dragging
        x, y = event.x // cell_size, event.y // cell_size
        if is_dragging and 0 <= y < len(map_data) and 0 <= x < len(map_data[0]):
            map_data[y][x] = selected_tile.get()
            draw_map()

    def on_canvas_release(event):
        """Stop the drag when mouse button is released."""
        global is_dragging
        is_dragging = False

    canvas.bind("<Button-1>", on_canvas_click) # Handle clicks to change tile type
    canvas.bind("<B1-Motion>", on_canvas_motion)  # Handle dragging/moving with click held
    canvas.bind("<ButtonRelease-1>", on_canvas_release)  # Stop dragging when mouse is released

    # Update tile selection buttons dynamically
    def update_tile_buttons():
        """Update the tile selection buttons."""
        for widget in tile_buttons_frame.winfo_children():
            widget.destroy()

        for i, (label, value) in enumerate(tile_types.items()):
            ttkb.Radiobutton(tile_buttons_frame, text=label, variable=selected_tile, value=value).grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)

    tile_buttons_frame = ttkb.Frame(editor_window)
    tile_buttons_frame.grid(row=0, column=0, padx=10, pady=5)

    # Initial update of the buttons
    update_tile_buttons()

    def save_map():
        """Save the current map to a file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".ber",
            filetypes=[("Map Files", "*.ber")],
        )
        if file_path:
            save_map_to_file(map_data, file_path)

    ttkb.Button(editor_window, text="Save Map", command=save_map, bootstyle="success").grid(row=5, column=1, pady=5)

    # Add/Edit Tile Type Features
    def add_tile_type():
        """Add a new tile type with a character and color."""
        def save_new_type():
            type_name = type_name_entry.get()
            char = char_entry.get()
            if char in tile_types.values():
                messagebox.showerror("Error", "Tile type already exists!")
                return
            if len(char) != 1:
                messagebox.showerror("Error", "Character must be a single character!")
                return
            color = colorchooser.askcolor()[1]
            if type_name and char and color:
                color_map[type_name] = color
                tile_types[type_name] = char
                update_tile_buttons()  # Re-update tile buttons to include the new type
                update_tile_legend()
                add_window.destroy()

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
            update_tile_legend()

    def update_tile_legend():
        """Update the tile legend displayed on the editor."""
        for widget in tile_legend_frame.winfo_children():
            widget.destroy()

        # Add legend entries
        row = 0
        for tile_name, color in color_map.items():
            label = ttkb.Label(tile_legend_frame, text=tile_name, width=10, anchor="w")
            label.grid(row=row, column=0, padx=10, pady=5)
            color_box = ttkb.Label(tile_legend_frame, text="   ", background=color, width=10)
            color_box.grid(row=row, column=1)
            color_box.bind("<Button-1>", lambda e, name=tile_name: edit_tile_color(name))
            row += 1

    tile_legend_frame = ttkb.Frame(editor_window)
    tile_legend_frame.grid(row=0, column=2, padx=10, pady=10, rowspan=5)

    # Add button to add new tile type
    ttkb.Button(editor_window, text="Add Tile Type", command=add_tile_type, bootstyle="primary").grid(row=5, column=0, pady=5)

    update_tile_legend()
    draw_map()

def main():
    """Main GUI application."""
    root = ttkb.Window(themename="darkly")
    root.title("Map Editor")
    root.geometry("600x400")

    def load_map():
        """Load a map from a file and open the editor."""
        file_path = filedialog.askopenfilename(
            title="Open Map File",
            filetypes=[("Map Files", "*.ber")]
        )
        if file_path:
            map_data = load_map_from_file(file_path)
            if map_data:
                open_map_editor(map_data)

    ttkb.Label(root, text="Welcome to the Map Editor", font=("Helvetica", 16)).pack(pady=10)
    ttkb.Button(root, text="Open Map", command=load_map, bootstyle="primary", width=20).pack(pady=5)
    ttkb.Button(root, text="Quit", command=root.quit, bootstyle="danger", width=20).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
