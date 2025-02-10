import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import json
import csv
from datetime import datetime
from file_scanner import FileScanner
from file_operations import move_to_backup, delete_files
from version import VERSION, RELEASE_DATE, APP_NAME

class AboutDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("About")
        self.geometry("400x300")
        self.resizable(False, False)

        # Center the dialog
        self.transient(parent)
        self.grab_set()

        # Create main frame with padding
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        # App name with custom font
        app_name_label = ttk.Label(
            main_frame,
            text=APP_NAME,
            font=("Helvetica", 16, "bold")
        )
        app_name_label.pack(pady=(0, 5))

        # Version and release date
        version_frame = ttk.Frame(main_frame)
        version_frame.pack(pady=(0, 10))
        ttk.Label(version_frame, text=f"Version {VERSION}").pack()
        ttk.Label(version_frame, text=f"Released: {RELEASE_DATE}").pack()

        # Description
        description = (
            "A modern, cross-platform desktop application for detecting\n"
            "and managing duplicate files with an intuitive user interface."
        )
        desc_label = ttk.Label(
            main_frame,
            text=description,
            justify="center",
            wraplength=350
        )
        desc_label.pack(pady=(0, 15))

        # Features
        features = (
            "• Advanced file scanning with SHA-256 hashing\n"
            "• Real-time progress tracking\n"
            "• Multiple file management options\n"
            "• Cross-platform compatibility"
        )
        features_label = ttk.Label(
            main_frame,
            text=features,
            justify="left",
            wraplength=350
        )
        features_label.pack(pady=(0, 15))

        # License info
        license_text = "Licensed under MIT License"
        license_label = ttk.Label(main_frame, text=license_text)
        license_label.pack(pady=(0, 10))

        # Close button
        close_button = ttk.Button(
            main_frame,
            text="Close",
            command=self.destroy,
            width=15
        )
        close_button.pack(pady=(0, 10))

        # Bind escape key to close
        self.bind("<Escape>", lambda e: self.destroy())

class MainApplication(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.scanner = FileScanner()
        self.duplicate_groups = []
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        # Top frame for controls
        self.controls_frame = ttk.Frame(self)
        self.controls_frame.pack(fill="x", padx=10, pady=5)

        # Folder selection
        self.folder_path = tk.StringVar()
        self.folder_label = ttk.Label(self.controls_frame, text="Select Folder:")
        self.folder_label.pack(side="left", padx=5)
        
        self.folder_entry = ttk.Entry(self.controls_frame, textvariable=self.folder_path, width=50)
        self.folder_entry.pack(side="left", padx=5)
        
        self.browse_button = ttk.Button(self.controls_frame, text="Browse", command=self.browse_folder)
        self.browse_button.pack(side="left", padx=5)
        
        self.scan_button = ttk.Button(self.controls_frame, text="Scan", command=self.start_scan)
        self.scan_button.pack(side="left", padx=5)

        # Progress frame
        self.progress_frame = ttk.Frame(self)
        self.progress_frame.pack(fill="x", padx=10, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, mode='determinate')
        self.progress_bar.pack(fill="x", pady=5)
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.progress_frame, textvariable=self.status_var)
        self.status_label.pack(fill="x")

        # Results frame
        self.results_frame = ttk.Frame(self)
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create treeview for results
        self.tree = ttk.Treeview(self.results_frame, columns=("Size", "Path"), show="tree headings")
        self.tree.heading("Size", text="Size (bytes)")
        self.tree.heading("Path", text="Path")
        self.tree.pack(fill="both", expand=True)
        
        # Scrollbar for treeview
        self.scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Actions frame
        self.actions_frame = ttk.Frame(self)
        self.actions_frame.pack(fill="x", padx=10, pady=5)
        
        self.delete_button = ttk.Button(self.actions_frame, text="Delete Selected", command=self.delete_selected)
        self.delete_button.pack(side="left", padx=5)
        
        self.backup_button = ttk.Button(self.actions_frame, text="Move to Backup", command=self.backup_selected)
        self.backup_button.pack(side="left", padx=5)
        
        self.export_button = ttk.Button(self.actions_frame, text="Export Report", command=self.export_report)
        self.export_button.pack(side="left", padx=5)

    def create_menu(self):
        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.parent.quit)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def show_about(self):
        AboutDialog(self.parent)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def start_scan(self):
        if not self.folder_path.get():
            messagebox.showwarning("Warning", "Please select a folder first!")
            return

        self.tree.delete(*self.tree.get_children())
        self.progress_var.set(0)
        self.status_var.set("Scanning...")
        self.scan_button.state(["disabled"])

        # Start scanning in a separate thread
        thread = threading.Thread(target=self.scan_thread)
        thread.daemon = True
        thread.start()

    def scan_thread(self):
        try:
            self.duplicate_groups = self.scanner.scan_directory(
                self.folder_path.get(),
                progress_callback=self.update_progress
            )
            self.parent.after(0, self.display_results)
        except Exception as e:
            self.parent.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.parent.after(0, lambda: self.scan_button.state(["!disabled"]))

    def update_progress(self, progress, status):
        self.progress_var.set(progress)
        self.status_var.set(status)

    def display_results(self):
        for group_id, group in enumerate(self.duplicate_groups):
            group_node = self.tree.insert("", "end", text=f"Duplicate Group {group_id + 1}")
            for file_path, file_size in group:
                self.tree.insert(group_node, "end", values=(file_size, file_path))
        
        self.status_var.set(f"Found {len(self.duplicate_groups)} duplicate groups")

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select files to delete")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected files?"):
            files_to_delete = []
            for item in selected:
                values = self.tree.item(item)["values"]
                if values:  # Only if it's a file (not a group header)
                    files_to_delete.append(values[1])  # Path is in second column
            
            delete_files(files_to_delete)
            self.refresh_tree()

    def backup_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select files to backup")
            return
            
        backup_dir = filedialog.askdirectory(title="Select Backup Directory")
        if backup_dir:
            files_to_backup = []
            for item in selected:
                values = self.tree.item(item)["values"]
                if values:
                    files_to_backup.append(values[1])
            
            move_to_backup(files_to_backup, backup_dir)
            self.refresh_tree()

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.start_scan()

    def export_report(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ask user for export format
        export_format = messagebox.askyesno(
            "Export Format",
            "Would you like to export as JSON? (No for CSV)"
        )
        
        if export_format:  # JSON
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                initialfile=f"duplicate_files_report_{timestamp}.json"
            )
            if file_path:
                self.export_json(file_path)
        else:  # CSV
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                initialfile=f"duplicate_files_report_{timestamp}.csv"
            )
            if file_path:
                self.export_csv(file_path)

    def export_json(self, file_path):
        report_data = []
        for group_id, group in enumerate(self.duplicate_groups):
            group_data = {
                "group_id": group_id + 1,
                "files": [{"path": path, "size": size} for path, size in group]
            }
            report_data.append(group_data)
        
        with open(file_path, 'w') as f:
            json.dump(report_data, f, indent=2)

    def export_csv(self, file_path):
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Group ID", "File Path", "Size (bytes)"])
            for group_id, group in enumerate(self.duplicate_groups):
                for path, size in group:
                    writer.writerow([group_id + 1, path, size])