/**
 * Analytics API Requests Module
 * Handles all API calls to the analytics endpoints
 */

const BASE_URL = '/api/analytics';

/**
 * Generic response handler
 * @param {Response} response - Fetch API response object
 * @returns {Promise<Object>} Parsed JSON data
 * @throws {Error} If response is not ok
 */
async function handleResponse(response) {
    let data;
    try {
        data = await response.json();
    } catch (e) {
        data = {};
    }

    if (!response.ok) {
        const message = data.message || data.error || `Server error: ${response.status}`;
        throw new Error(message);
    }

    return data;
}

/**
 * Get summary analytics
 * @param {string} outputPath - Path to analysis output directory
 * @returns {Promise<Object>} Summary data
 */
export async function getSummary(outputPath) {
    const url = `${BASE_URL}/summary?output_path=${encodeURIComponent(outputPath)}`;
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    });
    return handleResponse(response);
}

/**
 * Get consumer/producer distribution
 * @param {string} outputPath - Path to analysis output directory
 * @returns {Promise<Object>} Distribution data with labels, counts, and percentages
 */
export async function getDistribution(outputPath) {
    const url = `${BASE_URL}/consumer-producer-distribution?output_path=${encodeURIComponent(outputPath)}`;
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    });
    return handleResponse(response);
}

/**
 * Get top keywords
 * @param {string} outputPath - Path to analysis output directory
 * @param {number} limit - Maximum number of keywords to return (1-100)
 * @returns {Promise<Object>} Keywords data with labels and counts
 */
export async function getKeywords(outputPath, limit = 10) {
    const url = `${BASE_URL}/keywords?output_path=${encodeURIComponent(outputPath)}&limit=${limit}`;
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    });
    return handleResponse(response);
}

/**
 * Get library distribution
 * @param {string} outputPath - Path to analysis output directory
 * @param {number} limit - Maximum number of libraries to return (1-100)
 * @returns {Promise<Object>} Library distribution data with labels and counts
 */
export async function getLibraries(outputPath, limit = 10) {
    const url = `${BASE_URL}/libraries?output_path=${encodeURIComponent(outputPath)}&limit=${limit}`;
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    });
    return handleResponse(response);
}

/**
 * Filter results by type
 * @param {string} outputPath - Path to analysis output directory
 * @param {string} type - Filter type ('consumer' or 'producer')
 * @param {number} limit - Maximum number of results
 * @returns {Promise<Object>} Filtered results
 */
export async function filterByType(outputPath, type, limit = 1000) {
    const url = `${BASE_URL}/filter?output_path=${encodeURIComponent(outputPath)}&type=${type}&limit=${limit}`;
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    });
    return handleResponse(response);
}

/**
 * Filter results by keyword
 * @param {string} outputPath - Path to analysis output directory
 * @param {string} keyword - Keyword to filter by
 * @param {number} limit - Maximum number of results
 * @returns {Promise<Object>} Filtered results
 */
export async function filterByKeyword(outputPath, keyword, limit = 1000) {
    const url = `${BASE_URL}/filter?output_path=${encodeURIComponent(outputPath)}&keyword=${encodeURIComponent(keyword)}&limit=${limit}`;
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    });
    return handleResponse(response);
}

/**
 * Filter results by library
 * @param {string} outputPath - Path to analysis output directory
 * @param {string} library - Library name to filter by
 * @param {number} limit - Maximum number of results
 * @returns {Promise<Object>} Filtered results
 */
export async function filterByLibrary(outputPath, library, limit = 1000) {
    const url = `${BASE_URL}/filter?output_path=${encodeURIComponent(outputPath)}&library=${encodeURIComponent(library)}&limit=${limit}`;
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    });
    return handleResponse(response);
}

/**
 * Filter results with multiple criteria
 * @param {string} outputPath - Path to analysis output directory
 * @param {Object} filters - Filter criteria {type, keyword, library}
 * @param {number} limit - Maximum number of results
 * @returns {Promise<Object>} Filtered results
 */
export async function filterResults(outputPath, filters = {}, limit = 1000) {
    const params = new URLSearchParams({
        output_path: outputPath,
        limit: limit.toString()
    });

    if (filters.type) params.append('type', filters.type);
    if (filters.keyword) params.append('keyword', filters.keyword);
    if (filters.library) params.append('library', filters.library);

    const url = `${BASE_URL}/filter?${params.toString()}`;
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    });
    return handleResponse(response);
}

/**
 * Check analytics service health
 * @returns {Promise<Object>} Health status
 */
export async function checkHealth() {
    const url = `${BASE_URL}/health`;
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    });
    return handleResponse(response);
}
