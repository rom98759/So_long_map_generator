# Map Generator for the "so_long" Game

This project allows you to generate maps for the **so_long** game either via a graphical interface or through the command line. You can customize the map's dimensions, coin and wall percentages, and specify the save file location.

## Table of Contents

1. [Graphical Version](#graphical-version)
2. [Editor Version](#editor-version)
3. [Non-Graphical Version](#non-graphical-version)
4. [Improvement of File Names](#improvement-of-file-names)

---

## Graphical Version

The graphical version allows you to generate a map via a graphical user interface (GUI). You can input the width, height, coin and wall percentages, and display the generated map in a new window.

### Screenshot

Below is a screenshot of the graphical interface:

![Graphical Interface Screenshot](img/gui.png)

### Prerequisites

1. **Python 3.x** installed on your machine.
2. Install project dependencies, including those for the graphical interface.

```bash
pip install -r requirements.txt
```

### Usage

Run the `map_generator_gui.py` script to open the graphical interface and generate a map.

```bash
python map_generator_gui.py
```

A window will appear where you can input the following parameters:

- **Width**: Map width (between 3 and 150).
- **Height**: Map height (between 3 and 150).
- **Coin percentage**: Coin percentage (between 0 and 100).
- **Wall percentage**: Wall percentage (between 0 and 99).
- **Save file path**: Path where the generated map will be saved.
- **Editor**: Open the map editor to customize the map.
- **Debug mode**: Enable debug mode to display the generated map in the console.

Once the parameters are defined, click "Generate" to create the map and display a success or failure message.

### Debug Mode

![Screenshot of the debug mode](img/gui_debug.png)

When the debug mode is enabled, the following additional options are available:

- **Iterations**: The number of iterations to attempt to generate a valid map.
- **Show Map**: Display the generated map in the console.
- **Max Iterations**: The maximum number of iterations to attempt to generate a valid map.
- **Stats**: Display the map generation statistics (number of coins, walls, and empty spaces).

---

## Editor Version

The editor version allows you to customize the generated map by adding or removing coins and walls. You can also save the edited map to a file.

### Screenshot

Below is a screenshot of the map editor interface:

![Map Editor Screenshot](img/editor.png)

### Usage

To open the map editor, click the "Editor" button in the graphical interface. The editor window will appear, displaying the generated map.
Or you can run the `map_editor.py` script directly.

```bash
python map_editor.py
```

### Features

Click on a tile to select it, then use the buttons to add or remove coins and walls. You can also change the color of the selected tile and save the edited map to a file.
Right-click on a map to empty the cell.
Left-click on a tile to select it. And click on the map to add the selected tile.

![Screenshot of the map editor features](img/editor_features.png)

The map editor provides the following features:

- **Tile Selection**: Click on a tile to select it (empty, coin, or wall).
- **Add Tile**: Click on buttons to specific tiles to add them to the list.
- **Remove Tile**: Click on buttons to remove selected tiles from the list.
- **Color Selection**: Choose a color from the palette to change the selected tile's color.
- **Save Map**: Save the edited map to a file.
- **Validate Map**: Check if the map is valid (contains a player, exit, and at least one coin, and check if the map is surrounded by walls).
- **Lock outer walls**: Lock the outer walls to prevent them from being removed.

---

## Non-Graphical Version

The non-graphical version allows you to generate a map directly from the command line without a graphical interface. You can specify the map's dimensions, coin percentage, and wall percentage.

⚠️ **Attention**

The non-graphical version has fewer security measures compared to the graphical version. Ensure that the input parameters are validated before running the script.

![Screenshot of the command line interface](img/cli.png)

### Prerequisites

1. **Python 3.x** installed on your machine.

### Usage

To generate a map, run the `map_generator_cli.py` script with your desired parameters. By default, the values are:

- Width: 20
- Height: 10
- Coin percentage: 10
- Wall percentage: 10
- Save file path: `maps/map.ber`

#### Available Commands

```bash
python map_generator_cli.py -W 30 -H 15 -c 20 -w 30 -p "maps/custom_map.ber"
```

- `-W`, `--width`: Map width (between 3 and 150).
- `-H`, `--height`: Map height (between 3 and 150).
- `-c`, `--coins`: Coin percentage (between 0 and 100).
- `-w`, `--walls`: Wall percentage (between 0 and 99).
- `-p`, `--path`: Path to save the generated map file.

### Example

```bash
python map_generator_cli.py -W 50 -H 25 -c 15 -w 25 -p "maps/my_map.ber"
```

This command generates a 50x25 map with 15% coins and 25% walls, and saves it to `maps/my_map.ber`.

### Parameter Validation

The script validates the input parameters to ensure they meet the following requirements:

- Width and height must be between 3 and 150.
- Coin percentage must be between 0 and 100.
- Wall percentage must be between 0 and 99.
- If the map is 5x3 or 3x5, the wall percentage is automatically set to 0%.

### Main Code

The main logic is located in `map_generator_cli.py`, which uses the `main` function to generate and save the map in a `.ber` file. The map is generated until a valid map is produced.

---

## Need to fix
- [ ] The map generation algorithm is not efficient and may take a long time to generate a valid map for large dimensions.
- [ ] The map editor does not check if the map is valid after editing. (flood fill algorithm)


## Contributing

If you'd like to contribute to the project, please fork the repository, make your changes, and submit a pull request.
