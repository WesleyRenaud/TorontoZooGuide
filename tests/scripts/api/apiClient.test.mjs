import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { ApiClient } from '../../../scripts/api/apiClient.js';
import { ApiClientHelper } from '../../../scripts/api/apiClientHelper.js';

function _mockResponse({
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
   const url = '/set-itinerary';
   const date = '2026-06-15';
   const animal = 'African Lion';
   const data = {
      date,
      animals: [animal],
   };
   const success = true;
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.deepEqual(options, ApiClientHelper.buildJsonRequestOptions(data));

      return _mockResponse({
         text: JSON.stringify({ success }),
      });
   };

   const payload = await ApiClient.postJson(url, data);

   assert.deepEqual(payload, { success });
});


test('Test_PostJson_TestEmptyBody_ExpectEmptyObject', async () => {
   const url = '/clear-itinerary';
   globalThis.fetch = async () => _mockResponse({ text: '   ' });

   const payload = await ApiClient.postJson(url);

   assert.deepEqual(payload, {});
});


test('Test_PostJson_TestInvalidJson_ExpectThrows', async () => {
   const url = '/get-itinerary';
   globalThis.fetch = async () => _mockResponse({ text: '{not-json' });

   const request = ApiClient.postJson(url);

   await assert.rejects(
      request,
      new RegExp(`Invalid JSON response from ${url}`)
   );
});


test('Test_PostJson_TestHttpError_ExpectApiClientErrorMetadata', async () => {
   const url = '/set-itinerary';
   const status = 500;
   const statusText = 'Internal Server Error';
   const errorMessage = 'Could not save itinerary.';
   const payload = { error: errorMessage };
   globalThis.fetch = async () => _mockResponse({
      ok: false,
      status,
      statusText,
      text: JSON.stringify(payload),
   });

   const request = ApiClient.postJson(url);

   await assert.rejects(
      request,
      (error) => {
         assert.equal(error.name, 'ApiClientError');
         assert.equal(error.message, `${errorMessage} (${url})`);
         assert.equal(error.status, status);
         assert.equal(error.statusText, statusText);
         assert.equal(error.url, url);
         assert.deepEqual(error.payload, payload);
         return true;
      }
   );
});
