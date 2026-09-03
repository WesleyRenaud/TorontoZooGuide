import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { ApiClient } from '../../../scripts/api/apiClient.js';

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

test('Test_PostJson_TestValidPayload_ExpectParsedResponse', async () => {
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

   assert.deepEqual(await ApiClient.postJson('/set-itinerary', {
      date: '2026-06-15',
      animals: ['African Lion'],
   }), {
      success: true,
   });
});

test('Test_PostJson_TestEmptyBody_ExpectEmptyObject', async () => {
   globalThis.fetch = async () => mockResponse({ text: '   ' });

   assert.deepEqual(await ApiClient.postJson('/clear-itinerary'), {});
});

test('Test_PostJson_TestInvalidJson_ExpectThrows', async () => {
   globalThis.fetch = async () => mockResponse({ text: '{not-json' });

   await assert.rejects(
      () => ApiClient.postJson('/get-itinerary'),
      /Invalid JSON response from \/get-itinerary/
   );
});

test('Test_PostJson_TestHttpError_ExpectApiClientErrorMetadata', async () => {
   globalThis.fetch = async () => mockResponse({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
      text: '{"error":"Could not save itinerary."}',
   });

   await assert.rejects(
      async () => {
         await ApiClient.postJson('/set-itinerary');
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
