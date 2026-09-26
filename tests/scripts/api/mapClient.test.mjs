import assert from 'node:assert/strict';
import test from 'node:test';

import { MapClient } from '../../../scripts/api/mapClient.js';
import { MapApiFetcher } from '../../../scripts/api/mapApiFetcher.js';
import { ApiClient } from '../../../scripts/api/apiClient.js';
import { ScheduleItemKind } from '../../../scripts/shared/enums/scheduleItemKind.js';
import { Position } from '../../../scripts/shared/enums/position.js';

const _originalFetchCollection = MapApiFetcher.fetchCollection;
const _originalFetchStringCollection = MapApiFetcher.fetchStringCollection;
const _originalPostJson = ApiClient.postJson;
const _originalNormalizeRouteResponse = MapApiFetcher.normalizeRouteResponse;
const _originalNormalizeTransportationRoutesResponse = MapApiFetcher.normalizeTransportationRoutesResponse;

function _installCollectionMock(items) {
   const calls = [];
   MapApiFetcher.fetchCollection = async (...args) => {
      calls.push(args);
      return items;
   };
   return calls;
}

function _installStringCollectionMock(items) {
   const calls = [];
   MapApiFetcher.fetchStringCollection = async (...args) => {
      calls.push(args);
      return items;
   };
   return calls;
}

function _restoreMapClientMocks() {
   MapApiFetcher.fetchCollection = _originalFetchCollection;
   MapApiFetcher.fetchStringCollection = _originalFetchStringCollection;
   ApiClient.postJson = _originalPostJson;
   MapApiFetcher.normalizeRouteResponse = _originalNormalizeRouteResponse;
   MapApiFetcher.normalizeTransportationRoutesResponse = _originalNormalizeTransportationRoutesResponse;
}


test('Test_GetVisibleAnimals_TestPayload_ExpectFetcherCall', async () => {
   const payload = { day: 1 };
   const animals = [{ id: 1 }];
   const calls = _installCollectionMock(animals);

   try {
      const result = await MapClient.getVisibleAnimals(payload);

      assert.deepEqual(result, animals);
      assert.deepEqual(calls[Position.FIRST], [
         '/get-visible-animals',
         ScheduleItemKind.ANIMAL.itemType,
         payload,
      ]);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetPavilions_TestDelegation_ExpectFetcherCall', async () => {
   const pavilions = [{ id: 1 }];
   const calls = _installCollectionMock(pavilions);

   try {
      const result = await MapClient.getPavilions();

      assert.deepEqual(result, pavilions);
      assert.deepEqual(calls[Position.FIRST], ['/get-pavilions', 'pavilions']);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetRestaurants_TestDelegation_ExpectFetcherCall', async () => {
   const restaurants = [{ id: 1 }];
   const calls = _installCollectionMock(restaurants);

   try {
      const result = await MapClient.getRestaurants();

      assert.deepEqual(result, restaurants);
      assert.deepEqual(calls[Position.FIRST], [
         '/get-restaurants',
         'restaurants',
         MapApiFetcher.EMPTY_PAYLOAD,
      ]);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetRestrooms_TestDelegation_ExpectFetcherCall', async () => {
   const restrooms = [{ id: 1 }];
   const calls = _installCollectionMock(restrooms);

   try {
      const result = await MapClient.getRestrooms();

      assert.deepEqual(result, restrooms);
      assert.deepEqual(calls[Position.FIRST], [
         '/get-restrooms',
         'restrooms',
         MapApiFetcher.EMPTY_PAYLOAD,
      ]);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetGiftShops_TestDelegation_ExpectFetcherCall', async () => {
   const giftShops = [{ id: 1 }];
   const calls = _installCollectionMock(giftShops);

   try {
      const result = await MapClient.getGiftShops();

      assert.deepEqual(result, giftShops);
      assert.deepEqual(calls[Position.FIRST], [
         '/get-gift-shops',
         'gift_shops',
         MapApiFetcher.EMPTY_PAYLOAD,
      ]);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetAttractions_TestDelegation_ExpectFetcherCall', async () => {
   const attractions = [{ id: 1 }];
   const calls = _installCollectionMock(attractions);

   try {
      const result = await MapClient.getAttractions();

      assert.deepEqual(result, attractions);
      assert.deepEqual(calls[Position.FIRST], [
         '/get-attractions',
         ScheduleItemKind.ATTRACTION.itemType,
         MapApiFetcher.EMPTY_PAYLOAD,
      ]);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetTransportations_TestDelegation_ExpectFetcherCall', async () => {
   const transportations = [{ id: 1 }];
   const calls = _installCollectionMock(transportations);

   try {
      const result = await MapClient.getTransportations();

      assert.deepEqual(result, transportations);
      assert.deepEqual(calls[Position.FIRST], [
         '/get-transportations',
         ScheduleItemKind.TRANSPORTATION.itemType,
         MapApiFetcher.EMPTY_PAYLOAD,
      ]);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetGuardiansTalks_TestPayload_ExpectFetcherCall', async () => {
   const payload = { day: 2 };
   const talks = [{ id: 1 }];
   const calls = _installCollectionMock(talks);

   try {
      const result = await MapClient.getGuardiansTalks(payload);

      assert.deepEqual(result, talks);
      assert.deepEqual(calls[Position.FIRST], [
         '/get-guardians-talks',
         ScheduleItemKind.GUARDIANS_TALK.itemType,
         payload,
      ]);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetWildEncounters_TestDelegation_ExpectFetcherCall', async () => {
   const encounters = [{ id: 1 }];
   const calls = _installCollectionMock(encounters);

   try {
      const result = await MapClient.getWildEncounters();

      assert.deepEqual(result, encounters);
      assert.deepEqual(calls[Position.FIRST], [
         '/get-wild-encounters',
         ScheduleItemKind.WILD_ENCOUNTER.itemType,
         MapApiFetcher.EMPTY_PAYLOAD,
      ]);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetDrinkingFountains_TestDelegation_ExpectFetcherCall', async () => {
   const fountains = [{ id: 1 }];
   const calls = _installCollectionMock(fountains);

   try {
      const result = await MapClient.getDrinkingFountains();

      assert.deepEqual(result, fountains);
      assert.deepEqual(calls[Position.FIRST], [
         '/get-drinking-fountains',
         'drinking_fountains',
         MapApiFetcher.EMPTY_PAYLOAD,
      ]);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetDefibrillators_TestDelegation_ExpectFetcherCall', async () => {
   const defibrillators = [{ id: 1 }];
   const calls = _installCollectionMock(defibrillators);

   try {
      const result = await MapClient.getDefibrillators();

      assert.deepEqual(result, defibrillators);
      assert.deepEqual(calls[Position.FIRST], ['/get-defibrillators', 'defibrillators']);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetEmergencyIntercoms_TestDelegation_ExpectFetcherCall', async () => {
   const intercoms = [{ id: 1 }];
   const calls = _installCollectionMock(intercoms);

   try {
      const result = await MapClient.getEmergencyIntercoms();

      assert.deepEqual(result, intercoms);
      assert.deepEqual(calls[Position.FIRST], ['/get-emergency-intercoms', 'emergency_intercoms']);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetGuestServices_TestDelegation_ExpectFetcherCall', async () => {
   const guestServices = [{ id: 1 }];
   const calls = _installCollectionMock(guestServices);

   try {
      const result = await MapClient.getGuestServices();

      assert.deepEqual(result, guestServices);
      assert.deepEqual(calls[Position.FIRST], ['/get-guest-services', 'guest_services']);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetPicnicSites_TestDelegation_ExpectFetcherCall', async () => {
   const picnicSites = [{ id: 1 }];
   const calls = _installCollectionMock(picnicSites);

   try {
      const result = await MapClient.getPicnicSites();

      assert.deepEqual(result, picnicSites);
      assert.deepEqual(calls[Position.FIRST], ['/get-picnic-sites', 'picnic_sites']);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetEventSites_TestDelegation_ExpectFetcherCall', async () => {
   const eventSites = [{ id: 1 }];
   const calls = _installCollectionMock(eventSites);

   try {
      const result = await MapClient.getEventSites();

      assert.deepEqual(result, eventSites);
      assert.deepEqual(calls[Position.FIRST], ['/get-event-sites', 'event_sites']);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetEvents_TestDelegation_ExpectFetcherCall', async () => {
   const events = [{ id: 1 }];
   const calls = _installCollectionMock(events);

   try {
      const result = await MapClient.getEvents();

      assert.deepEqual(result, events);
      assert.deepEqual(calls[Position.FIRST], [
         '/get-events',
         'events',
         MapApiFetcher.EMPTY_PAYLOAD,
      ]);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetUpdates_TestDelegation_ExpectFetcherCall', async () => {
   const updates = [{ id: 1 }];
   const calls = _installCollectionMock(updates);

   try {
      const result = await MapClient.getUpdates();

      assert.deepEqual(result, updates);
      assert.deepEqual(calls[Position.FIRST], [
         '/get-updates',
         'updates',
         MapApiFetcher.EMPTY_PAYLOAD,
      ]);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetExhibits_TestDelegation_ExpectFetcherCall', async () => {
   const exhibits = [{ id: 1 }];
   const calls = _installCollectionMock(exhibits);

   try {
      const result = await MapClient.getExhibits();

      assert.deepEqual(result, exhibits);
      assert.deepEqual(calls[Position.FIRST], ['/get-exhibits', 'exhibits']);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetClosedExhibits_TestDelegation_ExpectStringFetcherCall', async () => {
   const closedExhibits = ['closed'];
   const calls = _installStringCollectionMock(closedExhibits);

   try {
      const result = await MapClient.getClosedExhibits();

      assert.deepEqual(result, closedExhibits);
      assert.deepEqual(calls[Position.FIRST], [
         '/get-closed-exhibits',
         'closed_exhibits',
         MapApiFetcher.EMPTY_PAYLOAD,
      ]);
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetTransportationRoute_TestPayload_ExpectNormalized', async () => {
   const payload = { name: 'Zoomobile' };
   const url = '/get-transportation-route';
   ApiClient.postJson = async (postedUrl, postedPayload) => ({ url: postedUrl, payload: postedPayload });
   MapApiFetcher.normalizeRouteResponse = (response) => ({ route: response });

   try {
      const result = await MapClient.getTransportationRoute(payload);

      assert.deepEqual(result, {
         route: { url, payload },
      });
   } finally {
      _restoreMapClientMocks();
   }
});


test('Test_GetTransportationRoutes_TestDelegation_ExpectNormalized', async () => {
   const url = '/get-transportation-routes';
   ApiClient.postJson = async (postedUrl, postedPayload) => ({ url: postedUrl, payload: postedPayload });
   MapApiFetcher.normalizeTransportationRoutesResponse = (response) => ({ routes: response });

   try {
      const result = await MapClient.getTransportationRoutes();

      assert.deepEqual(result, {
         routes: { url, payload: MapApiFetcher.EMPTY_PAYLOAD },
      });
   } finally {
      _restoreMapClientMocks();
   }
});
