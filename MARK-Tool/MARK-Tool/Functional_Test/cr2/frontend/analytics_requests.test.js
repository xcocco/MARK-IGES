import {jest} from '@jest/globals';

import * as api from '../../../web_gui/static/js/analytics_requests.js';

const BASE = '/api/analytics';

beforeEach(() => {
  global.fetch = jest.fn();
});

afterEach(() => {
  jest.resetAllMocks();
});

//
// ─── GET SUMMARY ─────────────────────────────────────────────────────────────
//
describe('getSummary', () => {
  test('TC-FR-ANA-01: calls correct endpoint and returns parsed data', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => ({ 
        success: true,
        total_models: 100,
        consumer_count: 60,
        producer_count: 40,
        total_projects: 20,
        total_libraries: 15
      }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.getSummary('/path/to/output');
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/summary?output_path=${encodeURIComponent('/path/to/output')}`,
      expect.objectContaining({ 
        method: 'GET', 
        headers: { "Accept": "application/json" }
      })
    );
    expect(result.success).toBe(true);
    expect(result.total_models).toBe(100);
    expect(result.consumer_count).toBe(60);
  });

  test('TC-FR-ANA-02: throws backend message on error', async () => {
    const fakeResponse = { 
      ok: false, 
      status: 400, 
      json: async () => ({ message: 'Output path does not exist' }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.getSummary('/invalid/path')).rejects.toThrow('Output path does not exist');
  });

  test('TC-FR-ANA-03: throws generic message if no backend message', async () => {
    const fakeResponse = { 
      ok: false, 
      status: 500, 
      json: async () => ({}) 
    };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.getSummary('/path')).rejects.toThrow('Server error: 500');
  });

  test('TC-FR-ANA-04: handles invalid JSON response', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => { throw new Error('invalid JSON'); } 
    };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.getSummary('/path');
    expect(result).toEqual({});
  });
});

//
// ─── GET DISTRIBUTION ────────────────────────────────────────────────────────
//
describe('getDistribution', () => {
  test('TC-FR-ANA-05: calls correct endpoint and returns distribution data', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => ({ 
        success: true,
        labels: ['Consumer', 'Producer'],
        counts: [60, 40],
        percentages: [60.0, 40.0]
      }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.getDistribution('/path/to/output');
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/consumer-producer-distribution?output_path=${encodeURIComponent('/path/to/output')}`,
      expect.objectContaining({ 
        method: 'GET', 
        headers: { "Accept": "application/json" }
      })
    );
    expect(result.success).toBe(true);
    expect(result.labels).toEqual(['Consumer', 'Producer']);
    expect(result.counts).toEqual([60, 40]);
  });

  test('TC-FR-ANA-06: handles error response', async () => {
    const fakeResponse = { 
      ok: false, 
      status: 400, 
      json: async () => ({ message: 'Missing CSV files' }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.getDistribution('/path')).rejects.toThrow('Missing CSV files');
  });
});

//
// ─── GET KEYWORDS ────────────────────────────────────────────────────────────
//
describe('getKeywords', () => {
  test('TC-FR-ANA-07: calls with default limit', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => ({ 
        success: true,
        labels: ['.predict(', '.fit(', '.transform('],
        counts: [45, 30, 15]
      }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.getKeywords('/path/to/output');
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/keywords?output_path=${encodeURIComponent('/path/to/output')}&limit=10`,
      expect.objectContaining({ method: 'GET' })
    );
    expect(result.labels).toHaveLength(3);
  });

  test('TC-FR-ANA-08: calls with custom limit', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => ({ 
        success: true,
        labels: ['.predict('],
        counts: [45]
      }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    await api.getKeywords('/path/to/output', 5);
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/keywords?output_path=${encodeURIComponent('/path/to/output')}&limit=5`,
      expect.objectContaining({ method: 'GET' })
    );
  });

  test('TC-FR-ANA-09: handles invalid limit error', async () => {
    const fakeResponse = { 
      ok: false, 
      status: 400, 
      json: async () => ({ message: 'Limit must be between 1 and 100' }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.getKeywords('/path', 0)).rejects.toThrow('Limit must be between 1 and 100');
  });
});

//
// ─── GET LIBRARIES ───────────────────────────────────────────────────────────
//
describe('getLibraries', () => {
  test('TC-FR-ANA-10: calls with default limit', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => ({ 
        success: true,
        labels: ['tensorflow', 'torch', 'sklearn'],
        counts: [50, 30, 20]
      }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.getLibraries('/path/to/output');
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/libraries?output_path=${encodeURIComponent('/path/to/output')}&limit=10`,
      expect.objectContaining({ method: 'GET' })
    );
    expect(result.labels).toEqual(['tensorflow', 'torch', 'sklearn']);
  });

  test('TC-FR-ANA-11: calls with custom limit', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => ({ 
        success: true,
        labels: ['tensorflow'],
        counts: [50]
      }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    await api.getLibraries('/path/to/output', 1);
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/libraries?output_path=${encodeURIComponent('/path/to/output')}&limit=1`,
      expect.objectContaining({ method: 'GET' })
    );
  });
});

//
// ─── FILTER BY TYPE ──────────────────────────────────────────────────────────
//
describe('filterByType', () => {
  test('TC-FR-ANA-12: filters by consumer type', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => ({ 
        success: true,
        count: 60,
        results: [{ type: 'consumer', project: 'proj1' }],
        filters_applied: { type: 'consumer' }
      }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.filterByType('/path/to/output', 'consumer');
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/filter?output_path=${encodeURIComponent('/path/to/output')}&type=consumer&limit=1000`,
      expect.objectContaining({ method: 'GET' })
    );
    expect(result.filters_applied.type).toBe('consumer');
  });

  test('TC-FR-ANA-13: filters by producer type', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => ({ 
        success: true,
        count: 40,
        results: [{ type: 'producer', project: 'proj2' }],
        filters_applied: { type: 'producer' }
      }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.filterByType('/path/to/output', 'producer', 500);
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/filter?output_path=${encodeURIComponent('/path/to/output')}&type=producer&limit=500`,
      expect.objectContaining({ method: 'GET' })
    );
    expect(result.count).toBe(40);
  });

  test('TC-FR-ANA-14: handles invalid type error', async () => {
    const fakeResponse = { 
      ok: false, 
      status: 400, 
      json: async () => ({ message: 'Invalid type parameter' }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.filterByType('/path', 'invalid')).rejects.toThrow('Invalid type parameter');
  });
});

//
// ─── FILTER BY KEYWORD ───────────────────────────────────────────────────────
//
describe('filterByKeyword', () => {
  test('TC-FR-ANA-15: filters by keyword', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => ({ 
        success: true,
        count: 25,
        results: [{ keyword: '.predict(', project: 'proj1' }],
        filters_applied: { keyword: '.predict(' }
      }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.filterByKeyword('/path/to/output', '.predict(');
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/filter?output_path=${encodeURIComponent('/path/to/output')}&keyword=${encodeURIComponent('.predict(')}&limit=1000`,
      expect.objectContaining({ method: 'GET' })
    );
    expect(result.count).toBe(25);
    expect(result.filters_applied.keyword).toBe('.predict(');
  });

  test('TC-FR-ANA-16: handles special characters in keyword', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => ({ 
        success: true,
        count: 5,
        results: []
      }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    await api.filterByKeyword('/path', '.fit()');
    const calledUrl = fetch.mock.calls[0][0];
    expect(calledUrl).toContain(encodeURIComponent('.fit()'));
  });
});

//
// ─── FILTER BY LIBRARY ───────────────────────────────────────────────────────
//
describe('filterByLibrary', () => {
  test('TC-FR-ANA-17: filters by library', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => ({ 
        success: true,
        count: 50,
        results: [{ library: 'tensorflow', project: 'proj1' }],
        filters_applied: { library: 'tensorflow' }
      }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.filterByLibrary('/path/to/output', 'tensorflow');
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/filter?output_path=${encodeURIComponent('/path/to/output')}&library=${encodeURIComponent('tensorflow')}&limit=1000`,
      expect.objectContaining({ method: 'GET' })
    );
    expect(result.filters_applied.library).toBe('tensorflow');
  });

  test('TC-FR-ANA-18: handles library with special characters', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => ({ 
        success: true,
        count: 0,
        results: []
      }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    await api.filterByLibrary('/path', 'scikit-learn');
    const calledUrl = fetch.mock.calls[0][0];
    expect(calledUrl).toContain(encodeURIComponent('scikit-learn'));
  });
});

//
// ─── FILTER RESULTS (MULTIPLE CRITERIA) ──────────────────────────────────────
//
describe('filterResults', () => {
  test('TC-FR-ANA-19: filters with multiple criteria', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => ({ 
        success: true,
        count: 10,
        results: [],
        filters_applied: { type: 'consumer', library: 'tensorflow' }
      }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    const filters = { type: 'consumer', library: 'tensorflow' };
    const result = await api.filterResults('/path/to/output', filters);
    
    const calledUrl = fetch.mock.calls[0][0];
    expect(calledUrl).toContain('type=consumer');
    expect(calledUrl).toContain('library=tensorflow');
    expect(result.count).toBe(10);
  });

  test('TC-FR-ANA-20: filters with all criteria', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => ({ 
        success: true,
        count: 5,
        results: []
      }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    const filters = { 
      type: 'consumer', 
      keyword: '.predict(', 
      library: 'tensorflow' 
    };
    await api.filterResults('/path/to/output', filters, 100);
    
    const calledUrl = fetch.mock.calls[0][0];
    expect(calledUrl).toContain('type=consumer');
    expect(calledUrl).toContain('keyword=');
    expect(calledUrl).toContain('library=tensorflow');
    expect(calledUrl).toContain('limit=100');
  });

  test('TC-FR-ANA-21: works with empty filters', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => ({ 
        success: true,
        count: 100,
        results: []
      }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    await api.filterResults('/path/to/output', {});
    
    const calledUrl = fetch.mock.calls[0][0];
    expect(calledUrl).toContain('output_path=');
    expect(calledUrl).toContain('limit=1000');
    expect(calledUrl).not.toContain('type=');
    expect(calledUrl).not.toContain('keyword=');
    expect(calledUrl).not.toContain('library=');
  });
});

//
// ─── CHECK HEALTH ────────────────────────────────────────────────────────────
//
describe('checkHealth', () => {
  test('TC-FR-ANA-22: calls health endpoint', async () => {
    const fakeResponse = { 
      ok: true, 
      json: async () => ({ 
        status: 'healthy',
        service: 'Analytics API'
      }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.checkHealth();
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/health`,
      expect.objectContaining({ 
        method: 'GET',
        headers: { "Accept": "application/json" }
      })
    );
    expect(result.status).toBe('healthy');
  });

  test('TC-FR-ANA-23: handles health check failure', async () => {
    const fakeResponse = { 
      ok: false, 
      status: 503, 
      json: async () => ({ message: 'Service unavailable' }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.checkHealth()).rejects.toThrow('Service unavailable');
  });
});

//
// ─── ERROR HANDLING ──────────────────────────────────────────────────────────
//
describe('Error handling across all functions', () => {
  test('TC-FR-ANA-24: network error is propagated', async () => {
    fetch.mockRejectedValue(new Error('Network error'));

    await expect(api.getSummary('/path')).rejects.toThrow('Network error');
    await expect(api.getDistribution('/path')).rejects.toThrow('Network error');
    await expect(api.getKeywords('/path')).rejects.toThrow('Network error');
    await expect(api.getLibraries('/path')).rejects.toThrow('Network error');
    await expect(api.checkHealth()).rejects.toThrow('Network error');
  });

  test('TC-FR-ANA-25: handles error field in response', async () => {
    const fakeResponse = { 
      ok: false, 
      status: 400, 
      json: async () => ({ error: 'Invalid request' }) 
    };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.getSummary('/path')).rejects.toThrow('Invalid request');
  });
});
