import assert from 'node:assert/strict';
import test from 'node:test';

import { MapClient } from '../../../scripts/api/mapClient.js';
import { MapDataSourceFactory } from '../../../scripts/map/mapDataSourceFactory.js';
import { SourceHelper } from '../../../scripts/map/sourceHelper.js';
import { TransportationRouteFragment } from '../../../scripts/map/transportationRouteFragment.js';
import { TransportationRouteProvider } from '../../../scripts/map/transportationRouteProvider.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_CreateNoCacheSource_TestFetchRows_ExpectNoCachePolicy', async () => {
   const rows = [{ id: 1 }];

   const source = MapDataSourceFactory.createNoCacheSource(async () => rows);
   const fetched = await source.fetch({ month: 'JUN' });

   assert.equal(source.cachePolicy, 'no-cache');
   assert.deepEqual(fetched, rows);
});


test('Test_BuildDatePayload_TestExtraFields_ExpectMerged', () => {
   const date = { month: 'JUN', day: 15, year: 2026 };
   const extra = { temp: 22, itineraryMode: true };

   const payload = MapDataSourceFactory.buildDatePayload(date, extra);

   assert.deepEqual(payload, { ...date, ...extra });
});


test('Test_CreateTypedDynamicApiSource_TestFetch_ExpectNormalizedRows', async () => {
   const store = { byType: {} };
   const payloads = [];
   const originalCreate = SourceHelper.createDynamicTypedSource;
   const originalNormalize = SourceHelper.normalizeTypedRows;
   const africanLion = { species: 'African Lion' };
   const type = ItemType.ANIMAL;
   const ctx = { month: 'JUN', day: 1, year: 2026, temp: 18 };

   SourceHelper.createDynamicTypedSource = (s, nextType, fetchFn) => ({
      store: s,
      type: nextType,
      fetch: fetchFn,
   });
   SourceHelper.normalizeTypedRows = (rows, nextType) => rows.map((row) => ({ ...row, type: nextType }));

   try {
      const source = MapDataSourceFactory.createTypedDynamicApiSource(
         store,
         type,
         async (payload) => {
            payloads.push(payload);
            return [africanLion];
         },
         (nextCtx) => MapDataSourceFactory.buildDatePayload(nextCtx, { temp: nextCtx.temp })
      );
      const rows = await source.fetch(ctx);

      assert.deepEqual(payloads, [ctx]);
      assert.deepEqual(rows, [{ ...africanLion, type }]);
   } finally {
      SourceHelper.createDynamicTypedSource = originalCreate;
      SourceHelper.normalizeTypedRows = originalNormalize;
   }
});


test('Test_CreateTypedStaticApiSource_TestFetch_ExpectNormalizedRows', async () => {
   const store = { byType: {} };
   const originalCreate = SourceHelper.createStaticTypedSource;
   const originalNormalize = SourceHelper.normalizeTypedRows;
   const pavilion = { name: 'African Pavilion' };
   const type = ItemType.PAVILION;

   SourceHelper.createStaticTypedSource = (s, nextType, fetchFn) => ({
      store: s,
      type: nextType,
      fetch: fetchFn,
   });
   SourceHelper.normalizeTypedRows = (rows, nextType) => rows.map((row) => ({ ...row, type: nextType }));

   try {
      const source = MapDataSourceFactory.createTypedStaticApiSource(
         store,
         type,
         async () => [pavilion]
      );
      const rows = await source.fetch();

      assert.deepEqual(rows, [{ ...pavilion, type }]);
   } finally {
      SourceHelper.createStaticTypedSource = originalCreate;
      SourceHelper.normalizeTypedRows = originalNormalize;
   }
});


test('Test_CreateClosedExhibitSource_TestFetch_ExpectMapClientPayload', async () => {
   const originalGet = MapClient.getClosedExhibits;
   const payloads = [];
   const closed = ['african-rainforest'];
   const ctx = {
      month: 'JUN',
      day: 15,
      year: 2026,
      dayOfWeek: 'Monday',
   };
   MapClient.getClosedExhibits = async (payload) => {
      payloads.push(payload);
      return closed;
   };

   try {
      const source = MapDataSourceFactory.createClosedExhibitSource();
      const rows = await source.fetch(ctx);

      assert.equal(source.cachePolicy, 'no-cache');
      assert.deepEqual(rows, closed);
      assert.deepEqual(payloads, [ctx]);
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
      const animalCall = dynamicCalls.at(Position.FIRST);
      const animalCtx = {
         month: 'JUN',
         day: 1,
         year: 2026,
         temp: 20,
         includeOffDisplayAnimals: true,
         speciesToInclude: ['African Lion'],
         animalsToInclude: ['a1'],
         itineraryMode: true,
      };
      const julyCtx = { month: 'JUL', day: 2, year: 2026 };
      const restaurantCtx = {
         ...julyCtx,
         includeClosedRestaurants: true,
         restaurantsToInclude: ['Peaks Cafe'],
      };
      const restroomCtx = { ...julyCtx, includeClosedRestrooms: true };
      const giftShopCtx = {
         ...julyCtx,
         includeClosedGiftShops: false,
         giftShopsToInclude: ['Zootique'],
      };
      const attractionCtx = {
         ...julyCtx,
         includeClosedAttractions: true,
         attractionsToInclude: ['Conservation Carousel'],
         itineraryMode: false,
      };
      const talkCtx = {
         ...julyCtx,
         guardiansTalksToInclude: ['Amur Tiger'],
         itineraryMode: true,
      };
      const encounterCtx = {
         ...julyCtx,
         wildEncountersToInclude: ['African Rainforest'],
         itineraryMode: true,
      };

      assert.deepEqual(Object.keys(sources).sort(), [
         ItemType.ANIMAL,
         ItemType.ATTRACTION,
         'closedExhibit',
         ItemType.DEFIBRILLATOR,
         ItemType.DRINKING_FOUNTAIN,
         ItemType.EMERGENCY_INTERCOM,
         ItemType.EVENT_SITE,
         ItemType.EXHIBIT,
         ItemType.GIFT_SHOP,
         ItemType.GUARDIANS_TALK,
         ItemType.GUEST_SERVICE,
         ItemType.PAVILION,
         ItemType.PICNIC_SITE,
         ItemType.RESTAURANT,
         ItemType.RESTROOM,
         ItemType.TRANSPORTATION_ROUTE,
         ItemType.WILD_ENCOUNTER,
      ]);
      assert.equal(sources[ItemType.ANIMAL].kind, 'dynamic');
      assert.equal(sources[ItemType.PAVILION].kind, 'static');
      assert.equal(sources[ItemType.TRANSPORTATION_ROUTE].kind, 'route');
      assert.equal(sources.closedExhibit.kind, 'closed');
      assert.equal(animalCall.store, store);
      assert.equal(animalCall.type, ItemType.ANIMAL);
      assert.equal(animalCall.fetchRows, MapClient.getVisibleAnimals);
      assert.deepEqual(animalCall.buildPayload(animalCtx), animalCtx);
      assert.deepEqual(
         dynamicCalls.find((call) => call.type === ItemType.RESTAURANT).buildPayload(restaurantCtx),
         restaurantCtx
      );
      assert.deepEqual(
         dynamicCalls.find((call) => call.type === ItemType.RESTROOM).buildPayload(restroomCtx),
         restroomCtx
      );
      assert.deepEqual(
         dynamicCalls.find((call) => call.type === ItemType.GIFT_SHOP).buildPayload(giftShopCtx),
         giftShopCtx
      );
      assert.deepEqual(
         dynamicCalls.find((call) => call.type === ItemType.ATTRACTION).buildPayload(attractionCtx),
         attractionCtx
      );
      assert.deepEqual(
         dynamicCalls.find((call) => call.type === ItemType.GUARDIANS_TALK).buildPayload(talkCtx),
         talkCtx
      );
      assert.deepEqual(
         dynamicCalls.find((call) => call.type === ItemType.WILD_ENCOUNTER).buildPayload(encounterCtx),
         encounterCtx
      );
      assert.deepEqual(
         dynamicCalls.find((call) => call.type === ItemType.DRINKING_FOUNTAIN).buildPayload(julyCtx),
         julyCtx
      );
      assert.equal(routeCalls.at(Position.FIRST).store, store);
      assert.equal(
         routeCalls.at(Position.FIRST).options.fetchTransportationRoute,
         MapClient.getTransportationRoute
      );
      assert.equal(
         routeCalls.at(Position.FIRST).options.hideRouteLayers,
         TransportationRouteFragment.hideTransportationRouteLayers
      );
      assert.equal(
         routeCalls.at(Position.FIRST).options.showRouteLayer,
         TransportationRouteFragment.showTransportationRouteLayer
      );
      assert.equal(
         staticCalls.find((call) => call.type === ItemType.PAVILION).fetchRows,
         MapClient.getPavilions
      );
      assert.equal(
         staticCalls.find((call) => call.type === ItemType.DEFIBRILLATOR).fetchRows,
         MapClient.getDefibrillators
      );
      assert.equal(
         staticCalls.find((call) => call.type === ItemType.EMERGENCY_INTERCOM).fetchRows,
         MapClient.getEmergencyIntercoms
      );
      assert.equal(
         staticCalls.find((call) => call.type === ItemType.GUEST_SERVICE).fetchRows,
         MapClient.getGuestServices
      );
      assert.equal(
         staticCalls.find((call) => call.type === ItemType.PICNIC_SITE).fetchRows,
         MapClient.getPicnicSites
      );
      assert.equal(
         staticCalls.find((call) => call.type === ItemType.EVENT_SITE).fetchRows,
         MapClient.getEventSites
      );
      assert.equal(
         staticCalls.find((call) => call.type === ItemType.EXHIBIT).fetchRows,
         MapClient.getExhibits
      );
   } finally {
      MapDataSourceFactory.createTypedDynamicApiSource = originalDynamic;
      MapDataSourceFactory.createTypedStaticApiSource = originalStatic;
      MapDataSourceFactory.createClosedExhibitSource = originalClosed;
      TransportationRouteProvider.createTransportationRouteSource = originalRoute;
   }
});
