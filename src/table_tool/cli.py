import argparse
import sys
from .sheet_client import open_worksheet
from .custom_ops import apply_operation, OPERATIONS

def process_range(sheet_name, worksheet_name, cell_range, operation_name):
    print(f"Connecting to sheet '{sheet_name}'...")
    try:
        worksheet = open_worksheet(sheet_name, worksheet_name)
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    print(f"Reading range {cell_range}...")
    # Get the values from the range
    # gspread's get returns a list of lists
    cell_values = worksheet.get(cell_range)
    
    if not cell_values:
        print("No data found in the specified range.")
        return

    print(f"Applying operation '{operation_name}'...")
    updated_values = []
    for row in cell_values:
        new_row = []
        for cell in row:
            new_val = apply_operation(operation_name, cell)
            new_row.append(new_val)
        updated_values.append(new_row)

    print("Updating sheet...")
    # Update the sheet with the new values
    worksheet.update(cell_range, updated_values)
    print("Done!")

def main():
    parser = argparse.ArgumentParser(description="Apply custom operations to Google Sheets cells.")
    parser.add_argument("sheet_name", help="The name of the Google Sheet")
    parser.add_argument("range", help="The A1 notation range to process (e.g., 'A1:B10')")
    parser.add_argument("operation", help=f"The operation to apply. Available: {', '.join(OPERATIONS.keys())}")
    parser.add_argument("--worksheet", help="The specific worksheet name (optional)", default=None)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    process_range(args.sheet_name, args.worksheet, args.range, args.operation)

if __name__ == "__main__":
    main()
