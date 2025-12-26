const SERVER_URL = 'http://127.0.0.1:5000';

document.addEventListener('DOMContentLoaded', () => {
    const statusDiv = document.getElementById('status');
    const operationSelect = document.getElementById('operation');
    const executeBtn = document.getElementById('executeBtn');
    const sheetIdInput = document.getElementById('sheetId');
    const rangeInput = document.getElementById('range');
    const resultDiv = document.getElementById('result');
    const getCurrentUrlBtn = document.getElementById('getCurrentUrl');

    // Check connection to local server
    fetch(`${SERVER_URL}/health`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'connected') {
                statusDiv.textContent = 'Connected to Python';
                statusDiv.className = 'status connected';
                loadOperations();
            }
        })
        .catch(err => {
            statusDiv.textContent = 'Disconnected (Start Server)';
            statusDiv.className = 'status disconnected';
            console.error('Error connecting to server:', err);
        });

    // Load available operations
    function loadOperations() {
        fetch(`${SERVER_URL}/operations`)
            .then(response => response.json())
            .then(data => {
                operationSelect.innerHTML = '';
                data.operations.forEach(op => {
                    const option = document.createElement('option');
                    option.value = op;
                    option.textContent = op;
                    operationSelect.appendChild(option);
                });
                operationSelect.disabled = false;
                executeBtn.disabled = false;
            })
            .catch(err => console.error('Error loading operations:', err));
    }

    // Get Sheet ID from current tab URL
    getCurrentUrlBtn.addEventListener('click', () => {
        chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
            const url = tabs[0].url;
            // Extract Sheet ID from URL: https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit...
            const match = url.match(/\/spreadsheets\/d\/([a-zA-Z0-9-_]+)/);
            if (match && match[1]) {
                sheetIdInput.value = match[1];
            } else {
                resultDiv.textContent = 'Could not find Sheet ID in current URL.';
            }
        });
    });

    // Execute operation
    executeBtn.addEventListener('click', () => {
        const sheetId = sheetIdInput.value;
        const operation = operationSelect.value;
        const range = rangeInput.value;

        if (!sheetId) {
            resultDiv.textContent = 'Please enter a Sheet ID.';
            return;
        }

        resultDiv.textContent = 'Executing...';
        executeBtn.disabled = true;

        fetch(`${SERVER_URL}/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                sheet_id: sheetId,
                operation_name: operation,
                range_name: range
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultDiv.textContent = `Error: ${data.error}`;
            } else {
                resultDiv.textContent = `Success! Changed '${data.old_value}' to '${data.new_value}'`;
            }
        })
        .catch(err => {
            resultDiv.textContent = `Error: ${err.message}`;
        })
        .finally(() => {
            executeBtn.disabled = false;
        });
    });
});
