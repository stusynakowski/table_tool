# Table Tool Widget Setup

## 1. Install Dependencies
First, install the required Python packages, including the new server dependencies:

```bash
pip install -r requirements.txt
```

## 2. Start the Local Server
The Chrome extension needs to talk to your local Python environment. Start the server with:

```bash
python src/table_tool/server.py
```
You should see output indicating the server is running on `http://127.0.0.1:5000`.

## 3. Load the Chrome Extension
1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode** in the top right corner.
3. Click **Load unpacked** in the top left.
4. Select the `chrome_extension` folder inside this repository (`/Users/stuartsynakowski/Github/table_tool/chrome_extension`).
5. The "Table Tool Widget" should appear in your extensions list.

## 4. Use the Widget
1. Open a Google Sheet in Chrome.
2. Click the **Table Tool Widget** icon in your browser toolbar.
3. The widget will check for the local server connection.
4. Click **Get from Current Tab** to automatically fill in the Sheet ID.
5. Enter the target cell (e.g., `A1`) you want to modify.
6. Select an operation (e.g., `uppercase`, `double`) from the dropdown.
7. Click **Execute Operation**.

## Troubleshooting
- **Connection Failed**: Ensure `server.py` is running.
- **Sheet Not Found**: Ensure you have shared the Google Sheet with the service account email defined in your `service_account.json`.
