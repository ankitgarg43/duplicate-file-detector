import tkinter as tk
from tkinter import ttk
from gui_components import MainApplication
from version import VERSION, APP_NAME

def main():
    root = tk.Tk()
    root.title(f"{APP_NAME} v{VERSION}")

    # Set minimum window size
    root.minsize(800, 600)

    # Configure basic styling
    style = ttk.Style()
    style.theme_use('clam')  # Use clam theme for better cross-platform appearance

    # Modern color palette
    PRIMARY_COLOR = "#2196F3"  # Modern blue
    SECONDARY_COLOR = "#03A9F4"  # Light blue
    BACKGROUND_COLOR = "#FAFAFA"  # Almost white
    TEXT_COLOR = "#212121"  # Dark gray
    ACCENT_COLOR = "#FF4081"  # Pink accent

    # Configure colors and styles
    style.configure("TButton", 
                   padding=6, 
                   relief="flat",
                   background=PRIMARY_COLOR,
                   foreground="white")

    style.configure("TFrame", background=BACKGROUND_COLOR)

    # Configure Treeview colors
    style.configure("Treeview",
                   background="white",
                   fieldbackground="white",
                   foreground=TEXT_COLOR)

    style.configure("Treeview.Heading",
                   background=SECONDARY_COLOR,
                   foreground="white",
                   relief="flat")

    # Configure Progress bar
    style.configure("Horizontal.TProgressbar",
                   background=ACCENT_COLOR,
                   troughcolor="#E3F2FD")

    # Configure Label
    style.configure("TLabel",
                   background=BACKGROUND_COLOR,
                   foreground=TEXT_COLOR)

    # Configure Entry
    style.configure("TEntry",
                   fieldbackground="white",
                   foreground=TEXT_COLOR)

    # Button hover effect
    style.map("TButton",
              background=[("active", SECONDARY_COLOR)],
              foreground=[("active", "white")])

    app = MainApplication(root)
    app.pack(fill="both", expand=True)

    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()

if __name__ == "__main__":
    main()