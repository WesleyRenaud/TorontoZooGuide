import assert from 'node:assert/strict';
import test from 'node:test';

import { ApiClientHelper } from '../../../scripts/api/apiClientHelper.js';

test('Test_BuildJsonRequestOptions_TestPayload_ExpectPostJson', () => {
   assert.deepEqual(ApiClientHelper.buildJsonRequestOptions({ name: 'African Lion' }), {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json',
         'Accept': 'application/json',
      },
      body: '{"name":"African Lion"}',
   });
});

test('Test_ParseJsonText_TestEmptyAndValid_ExpectObject', () => {
   assert.deepEqual(ApiClientHelper.parseJsonText(''), {});
   assert.deepEqual(ApiClientHelper.parseJsonText('  '), {});
   assert.deepEqual(ApiClientHelper.parseJsonText('{"ok":true}'), { ok: true });
});

test('Test_BuildHttpError_TestPayloadMessage_ExpectApiClientError', () => {
   const error = ApiClientHelper.buildHttpError(
      { status: 400, statusText: 'Bad Request' },
      { error: '  Missing date  ' },
      '/api/itinerary'
   );

   assert.equal(error.name, 'ApiClientError');
   assert.equal(error.message, 'Missing date (/api/itinerary)');
   assert.equal(error.status, 400);
   assert.equal(error.statusText, 'Bad Request');
   assert.equal(error.url, '/api/itinerary');
   assert.deepEqual(error.payload, { error: '  Missing date  ' });
});

test('Test_BuildHttpError_TestMissingPayloadMessage_ExpectStatusFallback', () => {
   const error = ApiClientHelper.buildHttpError(
      { status: 500, statusText: 'Server Error' },
      {},
      '/api/map'
   );

   assert.equal(error.message, 'Request failed: 500 Server Error (/api/map)');
});

test('Test_ReadJsonResponse_TestValidBody_ExpectParsed', async () => {
   const payload = await ApiClientHelper.readJsonResponse({
      text: async () => '{"animals":[]}',
   }, '/api/animals');

   assert.deepEqual(payload, { animals: [] });
});

test('Test_ReadJsonResponse_TestInvalidBody_ExpectThrows', async () => {
   await assert.rejects(
      () => ApiClientHelper.readJsonResponse({
         text: async () => '{bad',
      }, '/api/animals'),
      /Invalid JSON response from \/api\/animals/
   );
});
