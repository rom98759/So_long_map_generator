import tkinter as tk
from tkinter import filedialog, messagebox
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
    selected_tile = tk.StringVar(value='0')  # Default selected tile type

    # Colors for different tiles
    color_map = {'P': 'midnightblue', 'E': 'firebrick', 'C': 'gold', '1': 'darkgray', '0': 'darkslategray'}

    canvas = tk.Canvas(editor_window, width=len(map_data[0]) * cell_size, height=len(map_data) * cell_size)
    canvas.grid(row=0, column=0, rowspan=5)

    def draw_map():
        """Draw the map on the canvas."""
        canvas.delete("all")
        for y, row in enumerate(map_data):
            for x, cell in enumerate(row):
                color = color_map.get(cell, 'black')
                canvas.create_rectangle(
                    x * cell_size, y * cell_size,
                    (x + 1) * cell_size, (y + 1) * cell_size,
                    fill=color, outline="black"
                )

    def on_canvas_click(event):
        """Handle clicks to change tile type."""
        x, y = event.x // cell_size, event.y // cell_size
        if 0 <= y < len(map_data) and 0 <= x < len(map_data[0]):
            map_data[y][x] = selected_tile.get()
            draw_map()

    canvas.bind("<Button-1>", on_canvas_click)

    # Tile selection buttons
    tile_types = {'Player': 'P', 'Exit': 'E', 'Coin': 'C', 'Wall': '1', 'Empty': '0'}
    for i, (label, value) in enumerate(tile_types.items()):
        ttkb.Radiobutton(editor_window, text=label, variable=selected_tile, value=value).grid(row=i, column=1, sticky=tk.W)

    def save_map():
        """Save the current map to a file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".ber",
            filetypes=[("Map Files", "*.ber")],
        )
        if file_path:
            save_map_to_file(map_data, file_path)

    ttkb.Button(editor_window, text="Save Map", command=save_map, bootstyle="success").grid(row=5, column=1, sticky=tk.W)

    draw_map()

def main():
    """Main GUI application."""
    root = ttkb.Window(themename="darkly")
    root.title("Map Editor")
    root.geometry("400x200")

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
