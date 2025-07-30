// This worker's sole responsibility is to fetch and parse the large
// universe data file in a background thread to avoid freezing the UI.

self.onmessage = async (event) => {
    if (event.data.action === 'loadData') {
        try {
            // Fetch the local JSON file.
            const response = await fetch('universe_data.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            // Parse the JSON data.
            const data = await response.json();
            
            // Pre-process the data array into a more efficient dictionary format.
            const universeDataMap = data.reduce((acc, system) => {
                acc[system.name] = system;
                return acc;
            }, {});

            // Send the successfully processed data back to the main thread.
            self.postMessage({ type: 'success', data: universeDataMap });
        } catch (error) {
            // If anything goes wrong, send an error message back.
            self.postMessage({ type: 'error', error: error.message });
        }
    }
};
