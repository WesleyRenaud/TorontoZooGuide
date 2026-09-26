import assert from 'node:assert/strict';
import test from 'node:test';

import { ApiClientHelper } from '../../../scripts/api/apiClientHelper.js';


test('Test_BuildJsonRequestOptions_TestPayload_ExpectPostJson', () => {
   const name = 'African Lion';
   const data = { name };

   const options = ApiClientHelper.buildJsonRequestOptions(data);

   assert.deepEqual(options, {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json',
         'Accept': 'application/json',
      },
      body: JSON.stringify(data),
   });
});


test('Test_ParseJsonText_TestEmpty_ExpectObject', () => {
   const text = '';

   const payload = ApiClientHelper.parseJsonText(text);

   assert.deepEqual(payload, {});
});


test('Test_ParseJsonText_TestWhitespace_ExpectObject', () => {
   const text = '  ';

   const payload = ApiClientHelper.parseJsonText(text);

   assert.deepEqual(payload, {});
});


test('Test_ParseJsonText_TestValid_ExpectObject', () => {
   const ok = true;
   const text = JSON.stringify({ ok });

   const payload = ApiClientHelper.parseJsonText(text);

   assert.deepEqual(payload, { ok });
});


test('Test_BuildHttpError_TestPayloadMessage_ExpectApiClientError', () => {
   const status = 400;
   const statusText = 'Bad Request';
   const url = '/api/itinerary';
   const errorMessage = 'Missing date';
   const payload = { error: `  ${errorMessage}  ` };

   const error = ApiClientHelper.buildHttpError(
      { status, statusText },
      payload,
      url
   );

   assert.equal(error.name, 'ApiClientError');
   assert.equal(error.message, `${errorMessage} (${url})`);
   assert.equal(error.status, status);
   assert.equal(error.statusText, statusText);
   assert.equal(error.url, url);
   assert.deepEqual(error.payload, payload);
});


test('Test_BuildHttpError_TestMissingPayloadMessage_ExpectStatusFallback', () => {
   const status = 500;
   const statusText = 'Server Error';
   const url = '/api/map';

   const error = ApiClientHelper.buildHttpError(
      { status, statusText },
      {},
      url
   );

   assert.equal(error.message, `Request failed: ${status} ${statusText} (${url})`);
});


test('Test_ReadJsonResponse_TestValidBody_ExpectParsed', async () => {
   const animals = [];
   const url = '/api/animals';

   const payload = await ApiClientHelper.readJsonResponse({
      text: async () => JSON.stringify({ animals }),
   }, url);

   assert.deepEqual(payload, { animals });
});


test('Test_ReadJsonResponse_TestInvalidBody_ExpectThrows', async () => {
   const url = '/api/animals';
   const response = {
      text: async () => '{bad',
   };

   const read = () => ApiClientHelper.readJsonResponse(response, url);

   await assert.rejects(
      read,
      new RegExp(`Invalid JSON response from ${url}`)
   );
});
