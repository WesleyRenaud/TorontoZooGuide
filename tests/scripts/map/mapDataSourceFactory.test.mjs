import assert from 'node:assert/strict';
import test from 'node:test';

import { MapClient } from '../../../scripts/api/mapClient.js';
import { MapDataSourceFactory } from '../../../scripts/map/mapDataSourceFactory.js';
import { SourceHelper } from '../../../scripts/map/sourceHelper.js';
import { TransportationRouteFragment } from '../../../scripts/map/transportationRouteFragment.js';
import { TransportationRouteProvider } from '../../../scripts/map/transportationRouteProvider.js';

test('Test_CreateNoCacheSource_TestFetchRows_ExpectNoCachePolicy', async () => {
   const rows = [{ id: 1 }];
   const source = MapDataSourceFactory.createNoCacheSource(async () => rows);

   assert.equal(source.cachePolicy, 'no-cache');
   assert.deepEqual(await source.fetch({ month: 'JUN' }), rows);
});

test('Test_BuildDatePayload_TestExtraFields_ExpectMerged', () => {
   assert.deepEqual(
      MapDataSourceFactory.buildDatePayload(
         { month: 'JUN', day: 15, year: 2026 },
         { temp: 22, itineraryMode: true }
      ),
      {
         month: 'JUN',
         day: 15,
         year: 2026,
         temp: 22,
         itineraryMode: true,
      }
   );
});

test('Test_CreateTypedDynamicApiSource_TestFetch_ExpectNormalizedRows', async () => {
   const store = { byType: {} };
   const payloads = [];
   const originalCreate = SourceHelper.createDynamicTypedSource;
   const originalNormalize = SourceHelper.normalizeTypedRows;

   SourceHelper.createDynamicTypedSource = (s, type, fetchFn) => ({
      store: s,
      type,
      fetch: fetchFn,
   });
   SourceHelper.normalizeTypedRows = (rows, type) => rows.map((row) => ({ ...row, type }));

   try {
      const source = MapDataSourceFactory.createTypedDynamicApiSource(
         store,
         'animal',
         async (payload) => {
            payloads.push(payload);
            return [{ species: 'African Lion' }];
         },
         (ctx) => MapDataSourceFactory.buildDatePayload(ctx, { temp: ctx.temp })
      );

      const rows = await source.fetch({ month: 'JUN', day: 1, year: 2026, temp: 18 });
      assert.deepEqual(payloads, [{
         month: 'JUN',
         day: 1,
         year: 2026,
         temp: 18,
      }]);
      assert.deepEqual(rows, [{ species: 'African Lion', type: 'animal' }]);
   } finally {
      SourceHelper.createDynamicTypedSource = originalCreate;
      SourceHelper.normalizeTypedRows = originalNormalize;
   }
});

test('Test_CreateTypedStaticApiSource_TestFetch_ExpectNormalizedRows', async () => {
   const store = { byType: {} };
   const originalCreate = SourceHelper.createStaticTypedSource;
   const originalNormalize = SourceHelper.normalizeTypedRows;

   SourceHelper.createStaticTypedSource = (s, type, fetchFn) => ({
      store: s,
      type,
      fetch: fetchFn,
   });
   SourceHelper.normalizeTypedRows = (rows, type) => rows.map((row) => ({ ...row, type }));

   try {
      const source = MapDataSourceFactory.createTypedStaticApiSource(
         store,
         'pavilion',
         async () => [{ name: 'African Pavilion' }]
      );

      assert.deepEqual(await source.fetch(), [{ name: 'African Pavilion', type: 'pavilion' }]);
   } finally {
      SourceHelper.createStaticTypedSource = originalCreate;
      SourceHelper.normalizeTypedRows = originalNormalize;
   }
});

test('Test_CreateClosedExhibitSource_TestFetch_ExpectMapClientPayload', async () => {
   const originalGet = MapClient.getClosedExhibits;
   const payloads = [];

   MapClient.getClosedExhibits = async (payload) => {
      payloads.push(payload);
      return ['african-rainforest'];
   };

   try {
      const source = MapDataSourceFactory.createClosedExhibitSource();
      assert.equal(source.cachePolicy, 'no-cache');
      assert.deepEqual(await source.fetch({
         month: 'JUN',
         day: 15,
         year: 2026,
         dayOfWeek: 'Monday',
      }), ['african-rainforest']);
      assert.deepEqual(payloads, [{
         month: 'JUN',
         day: 15,
         year: 2026,
         dayOfWeek: 'Monday',
      }]);
   } finally {
      MapClient.getClosedExhibits = originalGet;
   }
});

test('Test_CreateDataSources_TestStore_ExpectAllKeysAndWiring', async () => {
   const store = { id: 'store' };
   const dynamicCalls = [];
   const staticCalls = [];
   const routeCalls = [];
   const originalDynamic = MapDataSourceFactory.createTypedDynamicApiSource;
   const originalStatic = MapDataSourceFactory.createTypedStaticApiSource;
   const originalClosed = MapDataSourceFactory.createClosedExhibitSource;
   const originalRoute = TransportationRouteProvider.createTransportationRouteSource;

   MapDataSourceFactory.createTypedDynamicApiSource = (s, type, fetchRows, buildPayload) => {
      dynamicCalls.push({ store: s, type, fetchRows, buildPayload });
      return { kind: 'dynamic', type };
   };
   MapDataSourceFactory.createTypedStaticApiSource = (s, type, fetchRows) => {
      staticCalls.push({ store: s, type, fetchRows });
      return { kind: 'static', type };
   };
   MapDataSourceFactory.createClosedExhibitSource = () => ({ kind: 'closed' });
   TransportationRouteProvider.createTransportationRouteSource = (s, options) => {
      routeCalls.push({ store: s, options });
      return { kind: 'route' };
   };

   try {
      const sources = MapDataSourceFactory.createDataSources(store);

      assert.deepEqual(Object.keys(sources).sort(), [
         'animal',
         'attraction',
         'closedExhibit',
         'defibrillator',
         'drinkingFountain',
         'emergencyIntercom',
         'eventSite',
         'exhibit',
         'giftShop',
         'guardiansTalk',
         'guestService',
         'pavilion',
         'picnicSite',
         'restaurant',
         'restroom',
         'transportationRoute',
         'wildEncounter',
      ]);

      assert.equal(sources.animal.kind, 'dynamic');
      assert.equal(sources.pavilion.kind, 'static');
      assert.equal(sources.transportationRoute.kind, 'route');
      assert.equal(sources.closedExhibit.kind, 'closed');

      assert.equal(dynamicCalls[0].store, store);
      assert.equal(dynamicCalls[0].type, 'animal');
      assert.equal(dynamicCalls[0].fetchRows, MapClient.getVisibleAnimals);
      assert.deepEqual(
         dynamicCalls[0].buildPayload({
            month: 'JUN',
            day: 1,
            year: 2026,
            temp: 20,
            includeOffDisplayAnimals: true,
            speciesToInclude: ['Lion'],
            animalsToInclude: ['a1'],
            itineraryMode: true,
         }),
         {
            month: 'JUN',
            day: 1,
            year: 2026,
            temp: 20,
            includeOffDisplayAnimals: true,
            speciesToInclude: ['Lion'],
            animalsToInclude: ['a1'],
            itineraryMode: true,
         }
      );

      const restaurant = dynamicCalls.find((call) => call.type === 'restaurant');
      assert.deepEqual(
         restaurant.buildPayload({
            month: 'JUL',
            day: 2,
            year: 2026,
            includeClosedRestaurants: true,
            restaurantsToInclude: ['Peaks'],
         }),
         {
            month: 'JUL',
            day: 2,
            year: 2026,
            includeClosedRestaurants: true,
            restaurantsToInclude: ['Peaks'],
         }
      );

      const restroom = dynamicCalls.find((call) => call.type === 'restroom');
      assert.deepEqual(
         restroom.buildPayload({
            month: 'JUL',
            day: 2,
            year: 2026,
            includeClosedRestrooms: true,
         }),
         {
            month: 'JUL',
            day: 2,
            year: 2026,
            includeClosedRestrooms: true,
         }
      );

      const giftShop = dynamicCalls.find((call) => call.type === 'giftShop');
      assert.deepEqual(
         giftShop.buildPayload({
            month: 'JUL',
            day: 2,
            year: 2026,
            includeClosedGiftShops: false,
            giftShopsToInclude: ['Zootique'],
         }),
         {
            month: 'JUL',
            day: 2,
            year: 2026,
            includeClosedGiftShops: false,
            giftShopsToInclude: ['Zootique'],
         }
      );

      const attraction = dynamicCalls.find((call) => call.type === 'attraction');
      assert.deepEqual(
         attraction.buildPayload({
            month: 'JUL',
            day: 2,
            year: 2026,
            includeClosedAttractions: true,
            attractionsToInclude: ['Carousel'],
            itineraryMode: false,
         }),
         {
            month: 'JUL',
            day: 2,
            year: 2026,
            includeClosedAttractions: true,
            attractionsToInclude: ['Carousel'],
            itineraryMode: false,
         }
      );

      const guardiansTalk = dynamicCalls.find((call) => call.type === 'guardiansTalk');
      assert.deepEqual(
         guardiansTalk.buildPayload({
            month: 'JUL',
            day: 2,
            year: 2026,
            guardiansTalksToInclude: ['Talk'],
            itineraryMode: true,
         }),
         {
            month: 'JUL',
            day: 2,
            year: 2026,
            guardiansTalksToInclude: ['Talk'],
            itineraryMode: true,
         }
      );

      const wildEncounter = dynamicCalls.find((call) => call.type === 'wildEncounter');
      assert.deepEqual(
         wildEncounter.buildPayload({
            month: 'JUL',
            day: 2,
            year: 2026,
            wildEncountersToInclude: ['Encounter'],
            itineraryMode: true,
         }),
         {
            month: 'JUL',
            day: 2,
            year: 2026,
            wildEncountersToInclude: ['Encounter'],
            itineraryMode: true,
         }
      );

      const drinkingFountain = dynamicCalls.find((call) => call.type === 'drinkingFountain');
      assert.deepEqual(
         drinkingFountain.buildPayload({ month: 'JUL', day: 2, year: 2026 }),
         { month: 'JUL', day: 2, year: 2026 }
      );

      assert.equal(routeCalls[0].store, store);
      assert.equal(routeCalls[0].options.fetchTransportationRoute, MapClient.getTransportationRoute);
      assert.equal(
         routeCalls[0].options.hideRouteLayers,
         TransportationRouteFragment.hideTransportationRouteLayers
      );
      assert.equal(
         routeCalls[0].options.showRouteLayer,
         TransportationRouteFragment.showTransportationRouteLayer
      );

      assert.equal(staticCalls.find((call) => call.type === 'pavilion').fetchRows, MapClient.getPavilions);
      assert.equal(
         staticCalls.find((call) => call.type === 'defibrillator').fetchRows,
         MapClient.getDefibrillators
      );
      assert.equal(
         staticCalls.find((call) => call.type === 'emergencyIntercom').fetchRows,
         MapClient.getEmergencyIntercoms
      );
      assert.equal(
         staticCalls.find((call) => call.type === 'guestService').fetchRows,
         MapClient.getGuestServices
      );
      assert.equal(staticCalls.find((call) => call.type === 'picnicSite').fetchRows, MapClient.getPicnicSites);
      assert.equal(staticCalls.find((call) => call.type === 'eventSite').fetchRows, MapClient.getEventSites);
      assert.equal(staticCalls.find((call) => call.type === 'exhibit').fetchRows, MapClient.getExhibits);
   } finally {
      MapDataSourceFactory.createTypedDynamicApiSource = originalDynamic;
      MapDataSourceFactory.createTypedStaticApiSource = originalStatic;
      MapDataSourceFactory.createClosedExhibitSource = originalClosed;
      TransportationRouteProvider.createTransportationRouteSource = originalRoute;
   }
});
