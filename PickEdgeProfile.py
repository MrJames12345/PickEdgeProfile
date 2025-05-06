#!/usr/bin/env python
# PickEdgeProfile.py - Select Microsoft Edge profile using a grid of tiles

import os
import sys
import tkinter as tk
from tkinter import ttk
import subprocess
import threading

# Constants
TITLE = "Edge Profile Selection"
COLUMNS = 3
PADDING_X = 15  # Horizontal padding between tiles
PADDING_Y = 2   # Further reduced vertical padding between tiles
TILE_SIZE = 180

# Edge profiles configuration
EDGE_PROFILES = [
    {
        "name": "Redi",
        "command": "\"C:\\Program Files (x86)\\Microsoft\\Edge Dev\\Application\\msedge.exe\" --profile-directory=\"Profile 5\""
    },
    {
        "name": "CW",
        "command": "\"C:\\Program Files (x86)\\Microsoft\\Edge Dev\\Application\\msedge.exe\" --profile-directory=\"Profile 14\""
    },
    {
        "name": "CK",
        "command": "\"C:\\Program Files (x86)\\Microsoft\\Edge Dev\\Application\\msedge.exe\" --profile-directory=\"Profile 12\""
    },
    {
        "name": "N-Grave",
        "command": "\"C:\\Program Files (x86)\\Microsoft\\Edge Dev\\Application\\msedge.exe\" --profile-directory=\"Profile 13\""
    },
    {
        "name": "YTMusicAutomator",
        "command": "\"C:\\Program Files (x86)\\Microsoft\\Edge Dev\\Application\\msedge.exe\" --profile-directory=\"Profile 15\""
    },
    {
        "name": "HabitsTogether",
        "command": "\"C:\\Program Files (x86)\\Microsoft\\Edge Dev\\Application\\msedge.exe\" --profile-directory=\"Profile 9\""
    },
    {
        "name": "MoneyBoys",
        "command": "\"C:\\Program Files (x86)\\Microsoft\\Edge Dev\\Application\\msedge.exe\" --profile-directory=\"Profile 10\""
    }
]

def launch_edge_profile(command):
    """Launch Microsoft Edge with the specified profile"""
    try:
        # Run the command in a separate thread to avoid blocking the UI
        subprocess.Popen(command, shell=True)
    except Exception as e:
        print(f"Error launching Edge: {e}")

def select_profile(command):
    """Handle profile selection when a tile is clicked"""
    # Launch Edge with the selected profile
    launch_thread = threading.Thread(target=launch_edge_profile, args=(command,))
    launch_thread.daemon = True
    launch_thread.start()

    # Close the window
    root.destroy()

# Get the script directory
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    base_path = os.path.dirname(sys.executable)
else:
    # Running as script
    base_path = os.path.dirname(os.path.abspath(__file__))

# Create the main window
root = tk.Tk()
root.title(TITLE)
# Let the window size adjust to its contents
root.resizable(True, True)
# Set the background color to #262626 (dark gray)
root.configure(bg="#262626")

# Set the window icon
# Use Edge.png as the window favicon
icon_path = os.path.join(base_path, "images", "Edge.png")
# If Edge.png doesn't exist, fall back to CK.png
if not os.path.exists(icon_path):
    icon_path = os.path.join(base_path, "images", "CK.png")

if os.path.exists(icon_path):
    try:
        # Load the icon image
        icon = tk.PhotoImage(file=icon_path)
        # Set the window icon
        root.iconphoto(True, icon)
    except Exception as e:
        print(f"Error setting window icon: {e}")

# Create main frame with padding
main_frame = tk.Frame(root, padx=20, pady=20, bg="#262626")  # Standard padding
main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 10))  # Add extra bottom padding in pack

# No title needed

# Create a frame for the grid of tiles
grid_frame = tk.Frame(main_frame, bg="#262626")
grid_frame.pack(fill=tk.BOTH, expand=True)

# Create tiles for each profile
row = 0
col = 0

# Calculate total number of profiles and items in the last row
total_profiles = len(EDGE_PROFILES)
last_row_items = total_profiles % COLUMNS
if last_row_items == 0:
    last_row_items = COLUMNS  # If last row is full

# Calculate the starting column for the last row to center it
last_row_start_col = (COLUMNS - last_row_items) // 2 if last_row_items < COLUMNS else 0

for i, profile in enumerate(EDGE_PROFILES):
    # Create a frame for each tile
    tile_frame = tk.Frame(
        grid_frame,
        width=TILE_SIZE,
        height=TILE_SIZE,
        bd=0,  # No border
        relief=tk.FLAT,  # No relief
        cursor="hand2",
        bg="#262626"  # Match the main background color
    )

    # Check if this is the last row and adjust column for centering
    current_row = i // COLUMNS
    current_col = i % COLUMNS

    # If this is the last row and we need to center it
    if current_row == total_profiles // COLUMNS and last_row_items < COLUMNS:
        current_col = last_row_start_col + (i % COLUMNS)

    tile_frame.grid(row=current_row, column=current_col, padx=PADDING_X, pady=PADDING_Y)
    tile_frame.pack_propagate(False)  # Prevent the frame from shrinking

    # Try to load the image based on profile name
    try:
        # Get the profile name and use it to find the corresponding image
        profile_name = profile["name"]
        # Look for <name>.png in the images subdirectory
        image_path = os.path.join(base_path, "images", f"{profile_name}.png")

        # If the specific image doesn't exist, fall back to CK.png
        if not os.path.exists(image_path):
            image_path = os.path.join(base_path, "images", "CK.png")

        if os.path.exists(image_path):
            # Load the image at original size first
            img = tk.PhotoImage(file=image_path)

            # Make the tile size larger to accommodate the image better
            # This will prevent the image from being cut off
            actual_tile_size = TILE_SIZE

            # Use a fixed subsample factor to ensure the image is fully visible
            # A subsample factor of 1 means the image is shown at original size
            # Adjust this value as needed to make the image fit properly
            subsample_factor = 1

            # Only subsample if the image is larger than the tile
            if img.width() > TILE_SIZE or img.height() > TILE_SIZE:
                # Calculate the subsample factor based on the image and tile sizes
                width_factor = max(1, img.width() // TILE_SIZE + 1)
                height_factor = max(1, img.height() // TILE_SIZE + 1)
                subsample_factor = max(width_factor, height_factor)
                img = img.subsample(subsample_factor)
        else:
            # Create a placeholder if image doesn't exist
            img = None
    except Exception as e:
        print(f"Error loading image: {e}")
        img = None

    # Add image or placeholder
    if img:
        # Create a label with the image and center it in the tile
        # Use system background color to match the tile frame
        image_label = tk.Label(tile_frame, image=img, bg=tile_frame.cget('bg'))
        image_label.image = img  # Keep a reference to prevent garbage collection
        # Use place to center the image in the tile
        image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        # Bind click event to the image
        image_label.bind("<Button-1>", lambda e, cmd=profile["command"]: select_profile(cmd))
    else:
        # Create a colored rectangle as placeholder
        canvas = tk.Canvas(tile_frame, width=TILE_SIZE-20, height=TILE_SIZE-20, bg="#7ec7d2")
        canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        # Bind click event to the canvas
        canvas.bind("<Button-1>", lambda e, cmd=profile["command"]: select_profile(cmd))

    # Bind click event to the entire tile
    tile_frame.bind("<Button-1>", lambda e, cmd=profile["command"]: select_profile(cmd))

# Calculate the window size based on the grid
# Update the grid layout to ensure all widgets are properly sized
grid_frame.update_idletasks()

# Get the number of rows based on the number of profiles and columns
num_rows = (len(EDGE_PROFILES) + COLUMNS - 1) // COLUMNS

# Calculate the window width and height based on the grid
window_width = (TILE_SIZE + 2 * PADDING_X) * COLUMNS + 40  # Add padding for the main frame
window_height = (TILE_SIZE + 2 * PADDING_Y) * num_rows + 50  # Adjusted for increased bottom padding

# Set the window size
root.geometry(f"{window_width}x{window_height}")

# Position the window on the second monitor
root.update_idletasks()

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Assuming the second monitor is to the right of the primary monitor
# and has the same resolution (adjust if needed)
second_monitor_x = screen_width  # Start of second monitor
second_monitor_center_x = second_monitor_x + (screen_width // 2)
second_monitor_center_y = screen_height // 2

# Calculate position to center the window on the second monitor
x = second_monitor_center_x - (window_width // 2)
y = second_monitor_center_y - (window_height // 2)

# Set the window position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind Escape key to close the window
root.bind("<Escape>", lambda event: root.destroy())

# Start the main loop
root.mainloop()
