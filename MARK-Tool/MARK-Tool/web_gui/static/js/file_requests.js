const BACKEND_BASE_URL = "http://localhost:5000";
const API_URL = "/api/file";
const FULL_BASE_URL = BACKEND_BASE_URL + API_URL;

async function handleResponse(response) {
    let data;
    try {
        data = await response.json();
    } catch {
        data = {};
    }

    if (!response.ok) {
        // If backend sent a message, use it; otherwise, show status text
        const message = data.message || `Server error: ${response.status}`;
        throw new Error(message);
    }

    return data;
}

async function requestUpload(csvFile) {
    const ENDPOINT = FULL_BASE_URL + "/upload";
    const response = await fetch(ENDPOINT, {
        method: "POST",
        body: csvFile
    });
    return handleResponse(response);
}

async function requestValidateInputFolder(path) {
    const ENDPOINT = FULL_BASE_URL + "/validate/input";
    const response = await fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path })
    });
    return handleResponse(response);
}

async function requestValidateOutputFolder(path) {
    const ENDPOINT = FULL_BASE_URL + "/validate/output";
    const response = await fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path })
    });
    return handleResponse(response);
}

async function requestValidateCSV(filePath) {
    const ENDPOINT = FULL_BASE_URL + "/validate/csv";
    const response = await fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filepath: filePath })
    });
    return handleResponse(response);
}

async function requestDownloadFile(filePath) {
    const ENDPOINT = FULL_BASE_URL + "/download";
    const response = await fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path: filePath })
    });
    return handleResponse(response);
}

async function requestListFiles(directory) {
    const ENDPOINT = FULL_BASE_URL + "/list";
    const response = await fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path: directory })
    });
    return handleResponse(response);
}
