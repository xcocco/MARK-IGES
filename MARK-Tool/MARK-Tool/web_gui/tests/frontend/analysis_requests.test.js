import {jest} from '@jest/globals';

import * as api from '../../static/js/analysis_requests.js'

const BASE = 'http://localhost:5000/api/analysis';

beforeEach(() => {
  global.fetch = jest.fn();
});

afterEach(() => {
  jest.resetAllMocks();
});

//
// ─── REQUEST STATUS ──────────────────────────────────────────────────────────────
//
describe('requestStatus', () => {
  test('calls correct endpoint and returns parsed data', async () => {
    const fakeResponse = { ok: true, json: async () => ({ id: 'job-1', status: 'done' }) };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.requestStatus('job-1');
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/status/job-1`,
      expect.objectContaining({ method: 'GET', headers: { "Accept": "application/json" }})
    );
    expect(result).toEqual({ id: 'job-1', status: 'done' });
  });

  test('throws backend message on error', async () => {
    const fakeResponse = { ok: false, status: 400, json: async () => ({ message: 'Invalid ID' }) };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.requestStatus('job-1')).rejects.toThrow('Invalid ID');
  });

  test('throws generic message if no backend message', async () => {
    const fakeResponse = { ok: false, status: 500, json: async () => ({}) };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.requestStatus('job-1')).rejects.toThrow('Server error: 500');
  });
});

//
// ─── REQUEST START ───────────────────────────────────────────────────────────────
//
describe('requestStart', () => {
  test('sends POST with correct headers and body', async () => {
    const fakeResponse = { ok: true, json: async () => ({ jobId: 'job-99' }) };
    fetch.mockResolvedValue(fakeResponse);

    const res = await api.requestStart('input.txt', 'outdir');
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/start`,
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }),
        body: JSON.stringify({
          input_path: 'input.txt',
          output_path: 'outdir'
        })
      })
    );
    expect(res).toEqual({ jobId: 'job-99' });
  });

  test('includes optional github_csv and run_cloner if provided', async () => {
    const fakeResponse = { ok: true, json: async () => ({ jobId: 'job-22' }) };
    fetch.mockResolvedValue(fakeResponse);

    await api.requestStart('in', 'out', 'repos.csv');
    const body = JSON.parse(fetch.mock.calls[0][1].body);
    expect(body.github_csv).toBe('repos.csv');
    expect(body.run_cloner).toBe(true);
  });

  test('throws if server error', async () => {
    const fakeResponse = { ok: false, status: 502, json: async () => ({}) };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.requestStart('in', 'out')).rejects.toThrow('Server error: 502');
  });
});

//
// ─── EDGE CASE: INVALID JSON HANDLING ────────────────────────────────────────────
//
describe('handleResponse integration via exported functions', () => {
  test('returns empty object when json parsing fails', async () => {
    const fakeResponse = { ok: true, json: async () => { throw new Error('invalid JSON'); } };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.requestStatus('job-1');
    expect(result).toEqual({});
  });
});