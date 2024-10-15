import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp as youtube_dl
import configparser
import os

#  _________     _____  ________ __________   _______   ____________   _________   
#  \_   ___ \   /     \ \______ \\______   \  \      \  \_____  \   \ /   /  _  \  
#  /    \  \/  /  \ /  \ |    |  \|       _/  /   |   \  /   |   \   Y   /  /_\  \ 
#  \     \____/    Y    \|    `   \    |   \ /    |    \/    |    \     /    |    \
#   \______  /\____|__  /_______  /____|_  / \____|__  /\_______  /\___/\____|__  /
#          \/         \/        \/       \/          \/         \/              \/ 


# Configurate that path, boooooyyyy!
config_file = 'config.ini'

# Set us up the config, all your Youtubers are belong to us!
config = configparser.ConfigParser()
if os.path.exists(config_file):
    config.read(config_file)
    last_directory = config.get('Settings', 'last_directory', fallback='')
else:
    last_directory = ''

def select_directory():
    directory = filedialog.askdirectory(initialdir=last_directory)
    if directory:
        directory_path.set(directory)
        # Save the selected directory to the configuration file SO YOU DON'T HAVE TO REMEMBER A THING!
        config['Settings'] = {'last_directory': directory}
        with open(config_file, 'w') as configfile:
            config.write(configfile)

def download_video():
    url = url_entry.get()
    directory = directory_path.get()
    if not url or not directory:
        messagebox.showerror("Error", "Please provide both URL and directory.")
        return
    
    # Ensure the URL starts with https://, always go secure, my friend.
    if not url.startswith("https://"):
        url = "https://" + url.lstrip("http://")

    ydl_opts = {
        'format': 'best[height<=720]',  # Limit to 720p, cause we ain't gotta fill up that hdd with 100 bajillion gigabytes of 4k video
        'outtmpl': f'{directory}/%(title)s.%(ext)s',  # Save to selected directory, like a BOSS
        'noplaylist': True,  # Only download single video, because we ain't got time for playlists
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Video downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {e}")
        print(f"Error: {e}")

def create_gradient(canvas, width, height):
    # Create a gradient to make it look all beautiful and pretty
    for i in range(height):
        color = f'#{int(0x00 + (0xFF - 0x00) * (i / height)):02x}{int(0xFF - (0xFF - 0x00) * (i / height)):02x}{int(0xFF - (0xFF - 0x00) * (i / height)):02x}'
        canvas.create_line(0, i, width, i, fill=color)

def get_gradient_color(y, height):
    # Calculate the gradient color at position y
    return f'#{int(0x00 + (0xFF - 0x00) * (y / height)):02x}{int(0xFF - (0xFF - 0x00) * (y / height)):02x}{int(0xFF - (0xFF - 0x00) * (y / height)):02x}'

# Create the main window
root = tk.Tk()
root.title("ExTube: The YouTube Destroyer")

# Set the custom icon, cause we don't use default stuff, mfer
icon_path = os.path.join(os.path.dirname(__file__), 'v_logo.ico')
root.iconbitmap(icon_path)

# Calculate the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window width and height
window_width = 400
window_height = 200

# Calculate the position to center the window
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

# Set the geometry of the window
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Create a canvas to draw the gradient
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack(fill="both", expand=True)

# Draw the gradient, DRAW!
create_gradient(canvas, window_width, window_height)

# URL input
url_label = tk.Label(canvas, text="YouTube URL:", fg="black")
url_label.pack(pady=5)
url_label.configure(bg=get_gradient_color(url_label.winfo_y(), window_height))

url_entry = tk.Entry(canvas, width=50)
url_entry.pack(pady=5)
url_entry.configure(bg=get_gradient_color(url_entry.winfo_y(), window_height))

# Directory selection
directory_path = tk.StringVar(value=last_directory)
select_button = tk.Button(canvas, text="Select Directory", command=select_directory)
select_button.pack(pady=5)
select_button.configure(bg=get_gradient_color(select_button.winfo_y(), window_height))

directory_label = tk.Label(canvas, textvariable=directory_path, fg="black")
directory_label.pack(pady=5)
directory_label.configure(bg=get_gradient_color(directory_label.winfo_y(), window_height))

# Download button
download_button = tk.Button(canvas, text="Download", command=download_video)
download_button.pack(pady=20)
download_button.configure(bg=get_gradient_color(download_button.winfo_y(), window_height))

# Run the application
root.mainloop()
