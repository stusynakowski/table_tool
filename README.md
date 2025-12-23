# Table Tool

This tool allows you to define custom Python functions and apply them to cells in Google Sheets.

## Setup

### 1. Install the Package

You can install the package in editable mode so you can modify the code and have changes take effect immediately.

```bash
pip install -e .
```

### 2. Google Cloud Credentials

To interact with Google Sheets, you need a Service Account.

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project.
3.  Enable the **Google Sheets API** and **Google Drive API**.
4.  Go to **APIs & Services > Credentials**.
5.  Click **Create Credentials > Service Account**.
6.  Fill in the details and create the account.
7.  Click on the newly created service account email.
8.  Go to the **Keys** tab and click **Add Key > Create new key**.
9.  Select **JSON** and download the file.
10. Rename this file to `service_account.json` and place it in the root of this project.

### 3. Share the Sheet

1.  Open your Google Sheet.
2.  Click the **Share** button.
3.  Copy the `client_email` from your `service_account.json` file.
4.  Paste the email into the share dialog and give it **Editor** access.

## Usage

### Define Custom Operations

Open `src/table_tool/custom_ops.py` and add your own functions. Register them in the `OPERATIONS` dictionary.

```python
def my_custom_func(value):
    return value + " modified"

OPERATIONS = {
    'my_op': my_custom_func
}
```

### Run Operations

You can run the tool using the `table-tool` command (installed by the package).

```bash
table-tool "Name of Your Sheet" "A1:B10" "uppercase"
```

Arguments:
1.  **Sheet Name**: The name of the Google Sheet file.
2.  **Range**: The range of cells to process (e.g., "A1:B10").
3.  **Operation**: The name of the operation defined in `src/table_tool/custom_ops.py` (e.g., "uppercase", "double").

Optional:
-   `--worksheet`: Specify a worksheet name if it's not the first one.

Example:
```bash
table-tool "My Data" "C2:C100" "double"
```
