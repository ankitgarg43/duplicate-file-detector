import os
import hashlib
from hash_utils import calculate_file_hash
from typing import Callable, List, Tuple, Dict, Optional
import threading

class FileScanner:
    def __init__(self):
        self.stop_scan = False
        self.lock = threading.Lock()

    def scan_directory(self, 
                      root_path: str, 
                      progress_callback: Optional[Callable[[float, str], None]] = None) -> List[List[Tuple[str, int]]]:
        """
        Scan directory for duplicate files

        Args:
            root_path: Root directory to scan
            progress_callback: Optional callback function for progress updates

        Returns:
            List of groups of duplicate files, where each group is a list of (path, size) tuples
        """
        # Reset stop flag
        self.stop_scan = False

        # First pass: collect all files and their sizes
        files_by_size: Dict[int, List[str]] = {}
        total_files = 0
        processed_files = 0

        # Count total files for progress tracking
        for dirpath, _, filenames in os.walk(root_path):
            total_files += len(filenames)

        # First pass: Group files by size
        for dirpath, _, filenames in os.walk(root_path):
            for filename in filenames:
                if self.stop_scan:
                    return []

                try:
                    filepath = os.path.join(dirpath, filename)
                    file_size = os.path.getsize(filepath)

                    with self.lock:
                        if file_size in files_by_size:
                            files_by_size[file_size].append(filepath)
                        else:
                            files_by_size[file_size] = [filepath]

                    processed_files += 1
                    if progress_callback is not None:
                        progress = (processed_files / total_files) * 50  # First pass = 50%
                        progress_callback(progress, f"Scanning files: {processed_files}/{total_files}")
                except (OSError, PermissionError) as e:
                    print(f"Error accessing file {filename}: {e}")
                    continue

        # Second pass: Compare files with same size using hashes
        duplicate_groups = []
        potential_duplicates = {
            size: paths for size, paths in files_by_size.items()
            if len(paths) > 1
        }

        total_potential = sum(len(files) for files in potential_duplicates.values())
        processed_potential = 0

        for size, file_paths in potential_duplicates.items():
            if self.stop_scan:
                return []

            # Group files by their hash
            files_by_hash: Dict[str, List[Tuple[str, int]]] = {}

            for filepath in file_paths:
                try:
                    file_hash = calculate_file_hash(filepath)

                    with self.lock:
                        if file_hash in files_by_hash:
                            files_by_hash[file_hash].append((filepath, size))
                        else:
                            files_by_hash[file_hash] = [(filepath, size)]

                    processed_potential += 1
                    if progress_callback is not None:
                        progress = 50 + (processed_potential / total_potential) * 50  # Second pass = 50%
                        progress_callback(progress, f"Comparing files: {processed_potential}/{total_potential}")
                except (OSError, PermissionError) as e:
                    print(f"Error hashing file {filepath}: {e}")
                    continue

            # Add groups with duplicates to results
            duplicate_groups.extend([group for group in files_by_hash.values() if len(group) > 1])

        if progress_callback is not None:
            progress_callback(100, f"Scan complete. Found {len(duplicate_groups)} duplicate groups")

        return duplicate_groups

    def stop_scanning(self):
        """Stop the ongoing scan operation"""
        self.stop_scan = True