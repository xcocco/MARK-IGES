import {jest} from '@jest/globals';

import * as api from '../../static/js/results_requests.js';

const BASE = 'http://localhost:5000/api/results';

beforeEach(() => {
  global.fetch = jest.fn();
});

afterEach(() => {
  jest.resetAllMocks();
});

//
// ─── REQUEST LIST ───────────────────────────────────────────────────────────────
//
describe('requestList', () => {
  test('calls correct GET endpoint with query params and returns parsed data', async () => {
    const fakeResponse = { ok: true, json: async () => ({ files: ['a.csv', 'b.csv'] }) };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.requestList('/output/path');
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/list?output_path=%2Foutput%2Fpath`,
      expect.objectContaining({
        method: 'GET',
        headers: { Accept: 'application/json' }
      })
    );
    expect(result).toEqual({ files: ['a.csv', 'b.csv'] });
  });

  test('throws backend message when ok=false and message provided', async () => {
    const fakeResponse = { ok: false, status: 400, json: async () => ({ message: 'Bad output path' }) };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.requestList('/bad/path'))
      .rejects.toThrow('Bad output path');
  });

  test('throws generic message when backend fails without message', async () => {
    const fakeResponse = { ok: false, status: 404, json: async () => ({}) };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.requestList('/missing'))
      .rejects.toThrow('Server error: 404');
  });

  test('returns {} if JSON parsing fails but ok=true', async () => {
    const fakeResponse = { ok: true, json: async () => { throw new Error('invalid json'); } };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.requestList('/corrupted');
    expect(result).toEqual({});
  });

  test('throws Server error if ok=false and JSON parsing fails', async () => {
    const fakeResponse = { ok: false, status: 500, json: async () => { throw new Error('parse fail'); } };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.requestList('/crash'))
      .rejects.toThrow('Server error: 500');
  });
});

//
// ─── REQUEST VIEW ───────────────────────────────────────────────────────────────
//
describe('requestView', () => {
  test('calls correct GET with only filepath', async () => {
    const fakeResponse = { ok: true, json: async () => ({ rows: [1, 2, 3] }) };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.requestView('/data/result.csv');
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/view?filepath=%2Fdata%2Fresult.csv`,
      expect.objectContaining({
        method: 'GET',
        headers: { Accept: 'application/json' }
      })
    );
    expect(result).toEqual({ rows: [1, 2, 3] });
  });

  test('calls correct GET with limit and offset', async () => {
    const fakeResponse = { ok: true, json: async () => ({ rows: ['limited'] }) };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.requestView('/data/file.csv', 10, 20);

    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/view?filepath=%2Fdata%2Ffile.csv&limit=10&offset=20`,
      expect.any(Object)
    );
    expect(result).toEqual({ rows: ['limited'] });
  });

  test('throws backend message when provided', async () => {
    const fakeResponse = { ok: false, status: 400, json: async () => ({ message: 'Invalid file path' }) };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.requestView('/badfile.csv'))
      .rejects.toThrow('Invalid file path');
  });

  test('throws generic message if backend returns no message', async () => {
    const fakeResponse = { ok: false, status: 500, json: async () => ({}) };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.requestView('/badfile.csv'))
      .rejects.toThrow('Server error: 500');
  });

  test('returns {} when JSON parse fails but ok=true', async () => {
    const fakeResponse = { ok: true, json: async () => { throw new Error('parse error'); } };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.requestView('/corrupted.csv');
    expect(result).toEqual({});
  });

  test('throws correct message when ok=false and JSON parse fails', async () => {
    const fakeResponse = { ok: false, status: 503, json: async () => { throw new Error('parse fail'); } };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.requestView('/error.csv'))
      .rejects.toThrow('Server error: 503');
  });
});

//
// ─── NETWORK FAILURE HANDLING ───────────────────────────────────────────────────
//
describe('network failure', () => {
  test('throws if fetch itself rejects', async () => {
    fetch.mockRejectedValue(new Error('Network unreachable'));

    await expect(api.requestList('/any'))
      .rejects.toThrow('Network unreachable');
  });
});
