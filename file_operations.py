import os
import shutil
from typing import List
import datetime

def delete_files(file_paths: List[str]) -> None:
    """
    Permanently delete the specified files
    
    Args:
        file_paths: List of file paths to delete
    """
    for file_path in file_paths:
        try:
            os.remove(file_path)
        except (OSError, PermissionError) as e:
            print(f"Error deleting {file_path}: {e}")

def move_to_backup(file_paths: List[str], backup_dir: str) -> None:
    """
    Move files to a backup directory
    
    Args:
        file_paths: List of file paths to move
        backup_dir: Destination directory
    """
    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)
    
    # Create timestamp for unique backup folder
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_subdir = os.path.join(backup_dir, f"backup_{timestamp}")
    os.makedirs(backup_subdir)
    
    for file_path in file_paths:
        try:
            # Preserve directory structure in backup
            rel_path = os.path.basename(file_path)
            backup_path = os.path.join(backup_subdir, rel_path)
            
            # Ensure unique filename in backup
            counter = 1
            while os.path.exists(backup_path):
                base, ext = os.path.splitext(rel_path)
                backup_path = os.path.join(backup_subdir, f"{base}_{counter}{ext}")
                counter += 1
            
            shutil.move(file_path, backup_path)
        except (OSError, PermissionError) as e:
            print(f"Error moving {file_path} to backup: {e}")
