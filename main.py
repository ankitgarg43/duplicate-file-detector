import tkinter as tk
from tkinter import ttk
from gui_components import MainApplication

def main():
    root = tk.Tk()
    root.title("Duplicate File Detector")
    
    # Set minimum window size
    root.minsize(800, 600)
    
    # Configure basic styling
    style = ttk.Style()
    style.theme_use('clam')  # Use clam theme for better cross-platform appearance
    
    # Configure colors and styles
    style.configure("TButton", padding=6, relief="flat")
    style.configure("TFrame", background="#f0f0f0")
    
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
