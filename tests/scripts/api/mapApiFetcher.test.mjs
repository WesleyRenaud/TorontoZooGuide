import assert from 'node:assert/strict';
import test from 'node:test';

import { MapApiFetcher } from '../../../scripts/api/mapApiFetcher.js';
import { ApiClient } from '../../../scripts/api/apiClient.js';

test('Test_AsStringArray_TestValues_ExpectTrimmedStrings', () => {
   assert.deepEqual(MapApiFetcher.asStringArray([' a ', '', null, 'b']), ['a', 'b']);
});

test('Test_ReadResponseCollection_TestKey_ExpectArray', () => {
   assert.deepEqual(
      MapApiFetcher.readResponseCollection({ animals: [{ id: 1 }] }, 'animals'),
      [{ id: 1 }]
   );
   assert.deepEqual(MapApiFetcher.readResponseCollection(null, 'animals'), []);
});

test('Test_NormalizeRouteResponse_TestPayload_ExpectLowerRoute', () => {
   assert.deepEqual(
      MapApiFetcher.normalizeRouteResponse({
         route: ' Zoomobile ',
         transportation_stations: [{ name: 'Main' }],
      }),
      {
         route: 'zoomobile',
         transportationStations: [{ name: 'Main' }],
      }
   );
});

test('Test_NormalizeTransportationRoutesResponse_TestEntries_ExpectNamedRoutes', () => {
   assert.deepEqual(
      MapApiFetcher.normalizeTransportationRoutesResponse({
         transportations: [
            { name: ' Zoomobile ', routes: [' A ', '', 'B'] },
            { name: '', routes: ['X'] },
            { name: 'Shuttle' },
         ],
      }),
      [
         { name: 'Zoomobile', routes: ['A', 'B'] },
         { name: 'Shuttle', routes: [] },
      ]
   );
});

test('Test_FetchCollection_TestEndpoint_ExpectPostedCollection', async () => {
   const original = ApiClient.postJson;
   ApiClient.postJson = async (endpoint, payload) => {
      assert.equal(endpoint, '/get-animals');
      assert.deepEqual(payload, { day: 1 });
      return { animals: [{ id: 1 }] };
   };

   try {
      assert.deepEqual(
         await MapApiFetcher.fetchCollection('/get-animals', 'animals', { day: 1 }),
         [{ id: 1 }]
      );
   } finally {
      ApiClient.postJson = original;
   }
});

test('Test_FetchStringCollection_TestEndpoint_ExpectStrings', async () => {
   const original = ApiClient.postJson;
   ApiClient.postJson = async () => ({ closed_exhibits: [' Africa ', '', 'Americas'] });

   try {
      assert.deepEqual(
         await MapApiFetcher.fetchStringCollection('/get-closed-exhibits', 'closed_exhibits'),
         ['Africa', 'Americas']
      );
   } finally {
      ApiClient.postJson = original;
   }
});
