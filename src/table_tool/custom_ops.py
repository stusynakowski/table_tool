"""
This module defines custom operations that can be applied to Google Sheets cells.
"""

def to_uppercase(value):
    """
    Example operation: Converts a string to uppercase.
    """
    if isinstance(value, str):
        return value.upper()
    return value

def multiply_by_two(value):
    """
    Example operation: Multiplies a number by 2.
    """
    try:
        return float(value) * 2
    except (ValueError, TypeError):
        return value

# Register your operations here
OPERATIONS = {
    'uppercase': to_uppercase,
    'double': multiply_by_two,
}

def apply_operation(operation_name, value):
    """
    Applies a registered operation to a value.
    """
    func = OPERATIONS.get(operation_name)
    if func:
        return func(value)
    else:
        print(f"Warning: Operation '{operation_name}' not found.")
        return value
