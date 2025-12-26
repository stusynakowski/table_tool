from flask import Flask, jsonify, request
from flask_cors import CORS
from table_tool import custom_ops, sheet_client
import gspread

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes to allow Chrome Extension to communicate

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "connected", "message": "Table Tool Server is running"})

@app.route('/operations', methods=['GET'])
def list_operations():
    ops = list(custom_ops.OPERATIONS.keys())
    return jsonify({"operations": ops})

@app.route('/execute', methods=['POST'])
def execute_operation():
    data = request.json
    sheet_id = data.get('sheet_id')
    operation_name = data.get('operation_name')
    # Optional: range or selection could be passed here
    
    if not sheet_id or not operation_name:
        return jsonify({"error": "Missing sheet_id or operation_name"}), 400

    try:
        # Open the sheet by ID (URL usually contains ID)
        client = sheet_client.get_gspread_client()
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.sheet1 # Default to first sheet for now, or pass worksheet name
        
        # For this example, let's apply the operation to the currently selected cell or a specific range.
        # Since we don't have the user's selection from the browser easily without more complex API usage,
        # let's assume we are operating on the whole sheet or a specific column for demonstration,
        # OR we can just read all data, process it, and write it back?
        # 
        # Better approach for "Excel-like" functions:
        # The user might want to apply it to a selection. 
        # Getting selection from Chrome Extension is possible via Google Sheets API if we have the spreadsheet ID.
        # But `gspread` doesn't easily give "current user selection".
        #
        # Let's simplify: The user selects a range in the extension (e.g. "A1:B10") or we just apply to all data.
        # Let's accept a 'range_name' in the request. If not provided, maybe just warn.
        
        range_name = data.get('range_name', 'A1') # Default to A1 if not specified
        
        # Read the value
        cell_value = worksheet.acell(range_name).value
        
        # Apply operation
        new_value = custom_ops.apply_operation(operation_name, cell_value)
        
        # Update the cell
        worksheet.update_acell(range_name, new_value)
        
        return jsonify({"status": "success", "old_value": cell_value, "new_value": new_value})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
