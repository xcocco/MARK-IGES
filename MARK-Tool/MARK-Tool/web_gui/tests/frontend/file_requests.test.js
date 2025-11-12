import {jest} from '@jest/globals';

import * as api from '../../static/js/file_requests.js';

const BASE = 'http://localhost:5000/api/file';

beforeEach(() => {
  global.fetch = jest.fn();
});

afterEach(() => {
  jest.resetAllMocks();
});

//
// ─── REQUEST VALIDATE INPUT FOLDER ──────────────────────────────────────────────
//
describe('requestValidateInputFolder', () => {
  test('sends POST with JSON body and returns parsed data', async () => {
    const fakeResponse = { ok: true, json: async () => ({ valid: true }) };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.requestValidateInputFolder('/path/to/input');
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/validate/input`,
      expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: '/path/to/input' })
      })
    );
    expect(result).toEqual({ valid: true });
  });

  test('throws backend message if provided', async () => {
    const fakeResponse = { ok: false, status: 400, json: async () => ({ message: 'Invalid folder' }) };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.requestValidateInputFolder('/bad'))
      .rejects.toThrow('Invalid folder');
  });

  test('throws generic error when no backend message', async () => {
    const fakeResponse = { ok: false, status: 500, json: async () => ({}) };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.requestValidateInputFolder('/error'))
      .rejects.toThrow('Server error: 500');
  });
});

//
// ─── REQUEST VALIDATE OUTPUT FOLDER ─────────────────────────────────────────────
//
describe('requestValidateOutputFolder', () => {
  test('sends POST to correct endpoint with JSON body', async () => {
    const fakeResponse = { ok: true, json: async () => ({ writable: true }) };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.requestValidateOutputFolder('/path/to/output');
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/validate/output`,
      expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: '/path/to/output' })
      })
    );
    expect(result).toEqual({ writable: true });
  });

  test('throws backend message when available', async () => {
    const fakeResponse = { ok: false, status: 403, json: async () => ({ message: 'Permission denied' }) };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.requestValidateOutputFolder('/readonly'))
      .rejects.toThrow('Permission denied');
  });
});

//
// ─── REQUEST VALIDATE CSV ───────────────────────────────────────────────────────
//
describe('requestValidateCSV', () => {
  test('sends POST with filepath JSON and returns parsed response', async () => {
    const fakeResponse = { ok: true, json: async () => ({ valid: true, rows: 42 }) };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.requestValidateCSV('data.csv');
    expect(fetch).toHaveBeenCalledWith(
      `${BASE}/validate/csv`,
      expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filepath: 'data.csv' })
      })
    );
    expect(result).toEqual({ valid: true, rows: 42 });
  });

  test('throws generic error if backend fails with no message', async () => {
    const fakeResponse = { ok: false, status: 404, json: async () => ({}) };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.requestValidateCSV('missing.csv'))
      .rejects.toThrow('Server error: 404');
  });
});

//
// ─── EDGE CASES FOR HANDLE RESPONSE ─────────────────────────────────────────────
//
describe('handleResponse edge behavior (via exported functions)', () => {
  test('returns {} when JSON parse fails but ok is true', async () => {
    const fakeResponse = { ok: true, json: async () => { throw new Error('invalid'); } };
    fetch.mockResolvedValue(fakeResponse);

    const result = await api.requestValidateCSV('broken.csv');
    expect(result).toEqual({});
  });

  test('throws correct message when ok=false and parse fails', async () => {
    const fakeResponse = { ok: false, status: 500, json: async () => { throw new Error('parse fail'); } };
    fetch.mockResolvedValue(fakeResponse);

    await expect(api.requestValidateCSV('broken.csv'))
      .rejects.toThrow('Server error: 500');
  });
});
