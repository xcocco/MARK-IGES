const BACKEND_BASE_URL = 'http://localhost:5000'
const API_URL = BACKEND_BASE_URL + '/api/results'

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

export async function requestList(output_path) {
    const apiPath = `${API_URL}/list?`

    let queryParams = new URLSearchParams(
        {output_path: output_path}
    )

    const response = await fetch(
        apiPath + queryParams.toString(), {
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

async function requestSearch(
    filepath,
    query,
    column = null
) {
    let requestJson = {
        filepath: filepath,
        query: query,
        ...(column && { column })
    }

    const apiPath = `${API_URL}/search`

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
        throw new Error(`Server error: ${response.status}`)
    }

    return handleResponse(response);
}

async function requestStats(output_path) {
    const apiPath = `${API_URL}/stats?`

    let queryParams = new URLSearchParams(
        {output_path: output_path}
    )

    const response = await fetch(
        apiPath + queryParams.toString(), {
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

async function requestView(
    filepath,
    limit = null,
    offset = null
) {
    const apiPath = `${API_URL}/view?`

    let queryParams = new URLSearchParams(
        {filepath: filepath}
    )
    if (limit !== null) queryParams.set("limit", limit)
    if (offset !== null) queryParams.set("offset", offset)

    const response = await fetch(
        apiPath + queryParams.toString(), {
            method: "GET",
            headers: {
                "Accept": "application/json"
            },
        }
    );

    // Check if response is OK
    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
    }

    return handleResponse(response);
}