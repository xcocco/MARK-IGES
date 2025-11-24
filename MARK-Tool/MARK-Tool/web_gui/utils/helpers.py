"""
Utility functions for the web GUI
"""
import os
import secrets
from datetime import datetime
from typing import Optional


def generate_secret_key() -> str:
    """
    Generate a secure random secret key
    
    Returns:
        Hex string suitable for Flask SECRET_KEY
    """
    return secrets.token_hex(32)


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def format_timestamp(timestamp: float) -> str:
    """
    Format Unix timestamp to human-readable string
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        Formatted datetime string
    """
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def safe_path_join(*paths) -> Optional[str]:
    """
    Safely join paths and ensure they don't escape a base directory
    
    Args:
        *paths: Path components to join
        
    Returns:
        Joined path or None if invalid
    """
    try:
        joined = os.path.normpath(os.path.join(*paths))
        # Prevent path traversal
        if '..' in joined:
            return None
        return joined
    except Exception:
        return None


def is_safe_path(path: str, base_path: str) -> bool:
    """
    Check if a path is safe (doesn't escape base directory)
    
    Args:
        path: Path to check
        base_path: Base directory
        
    Returns:
        True if safe, False otherwise
    """
    try:
        abs_path = os.path.abspath(path)
        abs_base = os.path.abspath(base_path)
        
        # Ensure the path starts with base_path
        common = os.path.commonpath([abs_path, abs_base])
        return common == abs_base
    except Exception:
        return False


def truncate_string(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Truncate a string to a maximum length
    
    Args:
        text: String to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing/replacing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove/replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    # Ensure filename is not empty
    if not filename:
        filename = 'file'
    
    return filename


def parse_csv_filename(filename: str) -> dict:
    """
    Parse information from a CSV filename
    
    Args:
        filename: CSV filename
        
    Returns:
        Dictionary with parsed information
    """
    info = {
        'filename': filename,
        'type': 'unknown',  # consumer, producer, or unknown
        'basename': os.path.splitext(filename)[0],
        'extension': os.path.splitext(filename)[1]
    }
    
    filename_lower = filename.lower()
    
    if 'consumer' in filename_lower:
        info['type'] = 'consumer'
    elif 'producer' in filename_lower:
        info['type'] = 'producer'
    
    return info


if __name__ == '__main__':
    # Generate a secret key for production use
    print("Generated SECRET_KEY:")
    print(generate_secret_key())
