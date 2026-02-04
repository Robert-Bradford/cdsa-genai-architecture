import re

def parse_height(height_str: str) -> float:
    """
    Convert height in format 5'4 or 5' 4" to inches.
    Raises ValueError if invalid.
    """
    match = re.fullmatch(r"\s*(\d+)\s*'\s*(\d+)\s*(\"?)\s*", height_str)
    if not match:
        raise ValueError("Height must be in the format feet'inches, e.g., 5'4")
    feet = int(match.group(1))
    inches = int(match.group(2))
    return feet * 12 + inches
