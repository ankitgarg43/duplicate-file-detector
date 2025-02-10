import hashlib
import os

BUFFER_SIZE = 65536  # 64KB chunks

def calculate_file_hash(filepath: str) -> str:
    """
    Calculate SHA-256 hash of a file
    
    Args:
        filepath: Path to the file
        
    Returns:
        Hexadecimal string representation of the file's hash
    
    Raises:
        OSError: If file cannot be read
        PermissionError: If file access is denied
    """
    sha256_hash = hashlib.sha256()
    
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            sha256_hash.update(data)
    
    return sha256_hash.hexdigest()
