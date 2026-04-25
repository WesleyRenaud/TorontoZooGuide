import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { postJson } from '../../scripts/api/apiClient.js';

function mockResponse({
   ok = true,
   status = 200,
   statusText = 'OK',
   text = '{}',
} = {}) {
   return {
      ok,
      status,
      statusText,
      text: async () => text,
   };
}

afterEach(() => {
   delete globalThis.fetch;
});

test('postJson sends JSON POST requests', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/set-itinerary');
      assert.deepEqual(options, {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
         },
         body: JSON.stringify({
            date: '2026-06-15',
            animals: ['African Lion'],
         }),
      });

      return mockResponse({
         text: '{"success":true}',
      });
   };

   assert.deepEqual(await postJson('/set-itinerary', {
      date: '2026-06-15',
      animals: ['African Lion'],
   }), {
      success: true,
   });
});

test('postJson treats empty response bodies as empty objects', async () => {
   globalThis.fetch = async () => mockResponse({ text: '   ' });

   assert.deepEqual(await postJson('/clear-itinerary'), {});
});

test('postJson throws a clear error for invalid JSON responses', async () => {
   globalThis.fetch = async () => mockResponse({ text: '{not-json' });

   await assert.rejects(
      () => postJson('/get-itinerary'),
      /Invalid JSON response from \/get-itinerary/
   );
});

test('postJson throws API errors with response metadata', async () => {
   globalThis.fetch = async () => mockResponse({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
      text: '{"error":"Could not save itinerary."}',
   });

   await assert.rejects(
      async () => {
         await postJson('/set-itinerary');
      },
      (error) => {
         assert.equal(error.name, 'ApiClientError');
         assert.equal(error.message, 'Could not save itinerary. (/set-itinerary)');
         assert.equal(error.status, 500);
         assert.equal(error.statusText, 'Internal Server Error');
         assert.equal(error.url, '/set-itinerary');
         assert.deepEqual(error.payload, { error: 'Could not save itinerary.' });
         return true;
      }
   );
});
