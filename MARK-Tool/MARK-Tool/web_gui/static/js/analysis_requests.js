const BACKEND_BASE_URL = 'http://localhost:5000'
const API_URL = BACKEND_BASE_URL + '/api/analysis'

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

    return data
}

async function requestCancel(jobId) {
    const apiPath = `${API_URL}/cancel/${jobId}`

    const response = await fetch(
        apiPath, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        }
    );

    // Check if response is OK
    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
    }

    return handleResponse(response);
}

async function requestJobs() {
    const apiPath = API_URL + "/jobs"

    const response = await fetch(
        apiPath, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        }
    );

    // Check if response is OK
    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }

    return handleResponse(response)
}

async function requestLogs(jobId) {
    const apiPath = `${API_URL}/jobs/${jobId}`

    const response = await fetch(
        apiPath, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        }
    );

    // Check if response is OK
    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }

    return handleResponse(response);
}

export async function requestStart(
    input_path,
    output_path,
    github_csv = null,
    run_cloner = github_csv !== null
) {
    let requestJson = {
        input_path: input_path,
        output_path: output_path,
        ...(github_csv && { github_csv }),
        ...(run_cloner && { run_cloner })
    }

    const apiPath = API_URL + '/start'

    const response = await fetch(
        apiPath, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
                },
            body: JSON.stringify(requestJson)
        }
    );

    // Check if response is OK
    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }

    return handleResponse(response);
}

export async function requestStatus(jobId) {
    const apiPath = `${API_URL}/status/${jobId}`

    const response = await fetch(
        apiPath, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        }
    );

    // Check if response is OK
    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }

    return handleResponse(response);
}
