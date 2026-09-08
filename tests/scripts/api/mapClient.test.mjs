import assert from 'node:assert/strict';
import test from 'node:test';

import { MapClient } from '../../../scripts/api/mapClient.js';
import { MapApiFetcher } from '../../../scripts/api/mapApiFetcher.js';
import { ApiClient } from '../../../scripts/api/apiClient.js';

test('Test_MapClientCollections_TestDelegation_ExpectFetcherCalls', async () => {
   const calls = [];
   const originalFetch = MapApiFetcher.fetchCollection;
   const originalStrings = MapApiFetcher.fetchStringCollection;
   MapApiFetcher.fetchCollection = async (...args) => {
      calls.push(['collection', ...args]);
      return [{ id: 1 }];
   };
   MapApiFetcher.fetchStringCollection = async (...args) => {
      calls.push(['strings', ...args]);
      return ['closed'];
   };

   try {
      assert.deepEqual(await MapClient.getVisibleAnimals({ day: 1 }), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getPavilions(), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getRestaurants(), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getRestrooms(), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getGiftShops(), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getAttractions(), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getTransportations(), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getGuardiansTalks({ day: 2 }), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getWildEncounters(), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getDrinkingFountains(), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getDefibrillators(), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getEmergencyIntercoms(), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getGuestServices(), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getPicnicSites(), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getEventSites(), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getEvents(), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getUpdates(), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getExhibits(), [{ id: 1 }]);
      assert.deepEqual(await MapClient.getClosedExhibits(), ['closed']);

      assert.deepEqual(calls[0], ['collection', '/get-visible-animals', 'animals', { day: 1 }]);
      assert.deepEqual(calls.at(-1), ['strings', '/get-closed-exhibits', 'closed_exhibits', MapApiFetcher.EMPTY_PAYLOAD]);
   } finally {
      MapApiFetcher.fetchCollection = originalFetch;
      MapApiFetcher.fetchStringCollection = originalStrings;
   }
});

test('Test_GetTransportationRouteAndRoutes_TestNormalize_ExpectMapped', async () => {
   const originalPost = ApiClient.postJson;
   const originalRoute = MapApiFetcher.normalizeRouteResponse;
   const originalRoutes = MapApiFetcher.normalizeTransportationRoutesResponse;
   ApiClient.postJson = async (url, payload) => ({ url, payload });
   MapApiFetcher.normalizeRouteResponse = (response) => ({ route: response });
   MapApiFetcher.normalizeTransportationRoutesResponse = (response) => ({ routes: response });

   try {
      assert.deepEqual(await MapClient.getTransportationRoute({ name: 'Zoomobile' }), {
         route: { url: '/get-transportation-route', payload: { name: 'Zoomobile' } },
      });
      assert.deepEqual(await MapClient.getTransportationRoutes(), {
         routes: { url: '/get-transportation-routes', payload: MapApiFetcher.EMPTY_PAYLOAD },
      });
   } finally {
      ApiClient.postJson = originalPost;
      MapApiFetcher.normalizeRouteResponse = originalRoute;
      MapApiFetcher.normalizeTransportationRoutesResponse = originalRoutes;
   }
});
