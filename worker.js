// This script runs in a background thread as a Web Worker.
// It initializes a Python environment once and then waits for tasks.

importScripts("https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.js");

let pyodide = null;

// Asynchronously initialize Pyodide and the Python script.
async function initializePyodide() {
    if (pyodide) {
        return;
    }
    pyodide = await loadPyodide();
    
    const response = await fetch('optimizer_core.py');
    const pythonCode = await response.text();
    pyodide.runPython(pythonCode);
    
    // Signal that this worker is ready to accept tasks.
    self.postMessage({ type: 'ready' });
}

// Listen for messages from the main application thread.
self.onmessage = async (event) => {
    const { id, path, systemsData, timePerPass, isBaseline } = event.data;

    try {
        // Determine which Python function to call
        const funcToRun = isBaseline 
            ? pyodide.globals.get('calculate_baseline_route') 
            : pyodide.globals.get('run_iterative_pass');
        
        const result = isBaseline
            ? funcToRun(path, systemsData, path[0]) // Baseline needs the start system name
            : funcToRun(path, systemsData, timePerPass);
        
        const resultJS = result.toJs({ dict_converter: Object.fromEntries });
        
        self.postMessage({ type: 'result', id: id, result: resultJS });

    } catch (error) {
        self.postMessage({ type: 'error', id: id, error: error.message });
    }
};

// Initialize Pyodide as soon as the worker is created.
initializePyodide();
