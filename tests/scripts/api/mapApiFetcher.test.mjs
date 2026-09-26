import assert from 'node:assert/strict';
import test from 'node:test';

import { MapApiFetcher } from '../../../scripts/api/mapApiFetcher.js';
import { ApiClient } from '../../../scripts/api/apiClient.js';


test('Test_AsStringArray_TestValues_ExpectTrimmedStrings', () => {
   const africa = 'a';
   const americas = 'b';
   const values = [` ${africa} `, '', null, americas];

   const names = MapApiFetcher.asStringArray(values);

   assert.deepEqual(names, [africa, americas]);
});


test('Test_ReadResponseCollection_TestKey_ExpectArray', () => {
   const animal = { id: 1 };
   const responseKey = 'animals';
   const response = { [responseKey]: [animal] };

   const animals = MapApiFetcher.readResponseCollection(response, responseKey);

   assert.deepEqual(animals, [animal]);
});


test('Test_ReadResponseCollection_TestNull_ExpectEmpty', () => {
   const responseKey = 'animals';
   const response = null;

   const animals = MapApiFetcher.readResponseCollection(response, responseKey);

   assert.deepEqual(animals, []);
});


test('Test_NormalizeRouteResponse_TestPayload_ExpectLowerRoute', () => {
   const route = 'Zoomobile';
   const station = { name: 'Main' };
   const response = {
      route: ` ${route} `,
      transportation_stations: [station],
   };

   const normalized = MapApiFetcher.normalizeRouteResponse(response);

   assert.deepEqual(normalized, {
      route: route.toLowerCase(),
      transportationStations: [station],
   });
});


test('Test_NormalizeTransportationRoutesResponse_TestEntries_ExpectNamedRoutes', () => {
   const zoomobile = 'Zoomobile';
   const routeA = 'A';
   const routeB = 'B';
   const unnamedRoute = 'X';
   const shuttle = 'Shuttle';
   const response = {
      transportations: [
         { name: ` ${zoomobile} `, routes: [` ${routeA} `, '', routeB] },
         { name: '', routes: [unnamedRoute] },
         { name: shuttle },
      ],
   };

   const routes = MapApiFetcher.normalizeTransportationRoutesResponse(response);

   assert.deepEqual(routes, [
      { name: zoomobile, routes: [routeA, routeB] },
      { name: shuttle, routes: [] },
   ]);
});


test('Test_FetchCollection_TestEndpoint_ExpectPostedCollection', async () => {
   const endpoint = '/get-animals';
   const responseKey = 'animals';
   const payload = { day: 1 };
   const animal = { id: 1 };
   const original = ApiClient.postJson;
   ApiClient.postJson = async (postedEndpoint, postedPayload) => {
      assert.equal(postedEndpoint, endpoint);
      assert.deepEqual(postedPayload, payload);
      return { [responseKey]: [animal] };
   };

   try {
      const animals = await MapApiFetcher.fetchCollection(endpoint, responseKey, payload);

      assert.deepEqual(animals, [animal]);
   } finally {
      ApiClient.postJson = original;
   }
});


test('Test_FetchStringCollection_TestEndpoint_ExpectStrings', async () => {
   const endpoint = '/get-closed-exhibits';
   const responseKey = 'closed_exhibits';
   const africa = 'Africa';
   const americas = 'Americas';
   const original = ApiClient.postJson;
   ApiClient.postJson = async () => ({ [responseKey]: [` ${africa} `, '', americas] });

   try {
      const exhibits = await MapApiFetcher.fetchStringCollection(endpoint, responseKey);

      assert.deepEqual(exhibits, [africa, americas]);
   } finally {
      ApiClient.postJson = original;
   }
});
