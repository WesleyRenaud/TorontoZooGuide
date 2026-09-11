import assert from 'node:assert/strict';
import test from 'node:test';

import { ClosedExhibitFragment } from '../../../scripts/map/closedExhibitFragment.js';
import { DateContext } from '../../../scripts/map/dateContext.js';
import { FocusRequest } from '../../../scripts/map/focusRequest.js';
import { ItineraryPathFragment } from '../../../scripts/map/itineraryPathFragment.js';
import { ItineraryPathModel } from '../../../scripts/itinerary/itineraryPathModel.js';
import { LayerRequest } from '../../../scripts/map/layerRequest.js';
import { MapUpdater } from '../../../scripts/map/mapUpdater.js';
import { SourceHelper } from '../../../scripts/map/sourceHelper.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { TransportationRouteFragment } from '../../../scripts/map/transportationRouteFragment.js';

function _createUpdaterDeps(overrides = {}) {
   const rendered = [];
   const focusScheduled = [];
   const store = {
      byType: {
         animal: [{ species: 'Stored Lion', type: 'animal' }],
         restaurant: [{ name: 'Stored Peaks', type: 'restaurant' }],
      },
   };

   return {
      store,
      sources: {
         animal: {
            fetch: async () => SourceHelper.setSourceRows(store, 'animal', [
               { species: 'Fetched Lion', type: 'animal' },
            ]),
         },
         restaurant: {
            fetch: async () => {
               throw new Error('fetch failed');
            },
         },
      },
      markers: {
         render: (rows) => { rendered.push(rows); },
      },
      focus: { id: 'focus' },
      getIncludeOffDisplay: () => false,
      getIncludeClosedRestaurants: () => false,
      getIncludeClosedRestrooms: () => false,
      getIncludeClosedGiftShops: () => false,
      getIncludeClosedAttractions: () => false,
      getTransportationRoute: () => 'none',
      getSelectedTypes: () => ['animal', 'restaurant'],
      onDateContextChange: null,
      rendered,
      focusScheduled,
      ...overrides,
   };
}

test('Test_BuildUniqueTypes_TestDuplicates_ExpectUnique', () => {
   assert.deepEqual(MapUpdater.buildUniqueTypes(['animal', 'animal', 'restaurant']), [
      'animal',
      'restaurant',
   ]);
   assert.deepEqual(MapUpdater.buildUniqueTypes(), []);
});

test('Test_CreateMapUpdater_TestUpdateMapLayers_ExpectRenderAndFocus', async () => {
   const deps = _createUpdaterDeps();
   const dateContexts = [];
   const closedSyncs = [];
   const layerBuilds = [];
   const focusCalls = [];
   const pathClears = [];
   const routeHides = [];

   const originalBuildDate = DateContext.buildMapDateContext;
   const originalClosed = ClosedExhibitFragment.syncClosedExhibitOverlays;
   const originalBuildLayer = LayerRequest.buildLayerRequest;
   const originalSchedule = FocusRequest.scheduleFocusRequest;
   const originalClearPath = ItineraryPathFragment.clearItineraryPathOverlay;
   const originalHideRoute = TransportationRouteFragment.hideTransportationRouteLayers;

   DateContext.buildMapDateContext = async (preset, dateStr) => ({
      preset,
      dateStr,
      month: 'JUN',
      day: 15,
      year: 2026,
   });
   ClosedExhibitFragment.syncClosedExhibitOverlays = async (...args) => {
      closedSyncs.push(args);
      return [];
   };
   LayerRequest.buildLayerRequest = (options) => {
      layerBuilds.push(options);
      return {
         ctx: {
            ...options.dateCtx,
            selected: options.selectedTypes,
            transportationRoute: options.transportationRoute,
         },
         selectedTypes: options.selectedTypes,
      };
   };
   FocusRequest.scheduleFocusRequest = (focus, request) => {
      focusCalls.push([focus, request]);
   };
   ItineraryPathFragment.clearItineraryPathOverlay = () => { pathClears.push(true); };
   TransportationRouteFragment.hideTransportationRouteLayers = () => { routeHides.push(true); };

   try {
      const updater = MapUpdater.createMapUpdater({
         ...deps,
         onDateContextChange: (ctx) => dateContexts.push(ctx),
      });

      await updater.updateMap('today', null, { focus: { type: 'animal', row: { species: 'Lion' } } });

      assert.equal(dateContexts.length, 1);
      assert.equal(closedSyncs.length, 1);
      assert.ok(pathClears.length >= 1);
      assert.ok(routeHides.length >= 1);
      assert.deepEqual(deps.rendered.at(Position.LAST), [
         { species: 'Fetched Lion', type: 'animal' },
         { name: 'Stored Peaks', type: 'restaurant' },
      ]);
      assert.deepEqual(focusCalls.at(Position.LAST)[1], { type: 'animal', row: { species: 'Lion' } });

      await updater.refetchWithCurrentControls(null);
      assert.equal(deps.rendered.length, 2);
   } finally {
      DateContext.buildMapDateContext = originalBuildDate;
      ClosedExhibitFragment.syncClosedExhibitOverlays = originalClosed;
      LayerRequest.buildLayerRequest = originalBuildLayer;
      FocusRequest.scheduleFocusRequest = originalSchedule;
      ItineraryPathFragment.clearItineraryPathOverlay = originalClearPath;
      TransportationRouteFragment.hideTransportationRouteLayers = originalHideRoute;
   }
});

test('Test_CreateMapUpdater_TestTransportationRouteNone_ExpectRouteLayersHidden', async () => {
   const deps = _createUpdaterDeps({
      getTransportationRoute: () => 'none',
      getSelectedTypes: () => [ItemType.ANIMAL],
      store: {
         byType: {
            [ItemType.ANIMAL]: [{ species: 'Stored Lion', type: ItemType.ANIMAL }],
            [ItemType.TRANSPORTATION_STATION]: [
               { name: 'Main Zoomobile Station', type: ItemType.TRANSPORTATION_STATION },
            ],
            [ItemType.TRANSPORTATION_ROUTE]: [
               { name: 'summer', type: ItemType.TRANSPORTATION_ROUTE },
            ],
         },
      },
   });
   const routeHides = [];

   const originalBuildDate = DateContext.buildMapDateContext;
   const originalClosed = ClosedExhibitFragment.syncClosedExhibitOverlays;
   const originalBuildLayer = LayerRequest.buildLayerRequest;
   const originalHideRoute = TransportationRouteFragment.hideTransportationRouteLayers;
   const originalClearPath = ItineraryPathFragment.clearItineraryPathOverlay;

   DateContext.buildMapDateContext = async () => ({ month: 'JUL', day: 15, year: 2026 });
   ClosedExhibitFragment.syncClosedExhibitOverlays = async () => [];
   LayerRequest.buildLayerRequest = (options) => ({
      ctx: {
         month: 'JUL',
         day: 15,
         transportationRoute: options.transportationRoute,
      },
      selectedTypes: options.selectedTypes,
   });
   ItineraryPathFragment.clearItineraryPathOverlay = () => {};
   TransportationRouteFragment.hideTransportationRouteLayers = () => { routeHides.push(true); };

   try {
      const updater = MapUpdater.createMapUpdater(deps);
      await updater.updateMap('summer', null);

      assert.ok(routeHides.length >= 1);
      assert.deepEqual(deps.store.byType[ItemType.TRANSPORTATION_STATION], []);
      assert.deepEqual(deps.store.byType[ItemType.TRANSPORTATION_ROUTE], []);
      assert.deepEqual(deps.rendered.at(Position.LAST), [
         { species: 'Stored Lion', type: ItemType.ANIMAL },
      ]);
   } finally {
      DateContext.buildMapDateContext = originalBuildDate;
      ClosedExhibitFragment.syncClosedExhibitOverlays = originalClosed;
      LayerRequest.buildLayerRequest = originalBuildLayer;
      TransportationRouteFragment.hideTransportationRouteLayers = originalHideRoute;
      ItineraryPathFragment.clearItineraryPathOverlay = originalClearPath;
   }
});

test('Test_CreateMapUpdater_TestEmptySelectedTypes_ExpectCleared', async () => {
   const deps = _createUpdaterDeps({
      getSelectedTypes: () => [],
   });
   const routeHides = [];
   const pathClears = [];

   const originalBuildDate = DateContext.buildMapDateContext;
   const originalClosed = ClosedExhibitFragment.syncClosedExhibitOverlays;
   const originalBuildLayer = LayerRequest.buildLayerRequest;
   const originalClearPath = ItineraryPathFragment.clearItineraryPathOverlay;
   const originalHideRoute = TransportationRouteFragment.hideTransportationRouteLayers;

   DateContext.buildMapDateContext = async () => ({ month: 'JUN', day: 1, year: 2026 });
   ClosedExhibitFragment.syncClosedExhibitOverlays = async () => [];
   LayerRequest.buildLayerRequest = () => ({
      ctx: {},
      selectedTypes: [],
   });
   ItineraryPathFragment.clearItineraryPathOverlay = () => { pathClears.push(true); };
   TransportationRouteFragment.hideTransportationRouteLayers = () => { routeHides.push(true); };

   try {
      const updater = MapUpdater.createMapUpdater(deps);
      await updater.updateMap('today', null);
      assert.deepEqual(deps.rendered.at(Position.LAST), []);
      assert.ok(routeHides.length >= 1);
      assert.ok(pathClears.length >= 1);
   } finally {
      DateContext.buildMapDateContext = originalBuildDate;
      ClosedExhibitFragment.syncClosedExhibitOverlays = originalClosed;
      LayerRequest.buildLayerRequest = originalBuildLayer;
      ItineraryPathFragment.clearItineraryPathOverlay = originalClearPath;
      TransportationRouteFragment.hideTransportationRouteLayers = originalHideRoute;
   }
});

test('Test_CreateMapUpdater_TestItineraryMode_ExpectPathAndRoute', async () => {
   const deps = _createUpdaterDeps();
   const shownRoutes = [];
   const pathRenders = [];
   const focusCalls = [];

   const originalBuildDate = DateContext.buildMapDateContext;
   const originalResolveRoute = LayerRequest.resolveItineraryTransportationRouteMarkers;
   const originalBuildRows = LayerRequest.buildItineraryRows;
   const originalShowRoute = TransportationRouteFragment.showTransportationRouteMarkers;
   const originalHideRoute = TransportationRouteFragment.hideTransportationRouteLayers;
   const originalResolvePath = ItineraryPathModel.resolveItineraryPath;
   const originalRenderPath = ItineraryPathFragment.renderItineraryPathOverlay;
   const originalSchedule = FocusRequest.scheduleFocusRequest;

   DateContext.buildMapDateContext = async () => ({ month: 'JUN', day: 1, year: 2026 });
   LayerRequest.resolveItineraryTransportationRouteMarkers = () => ({
      route: 'summer',
      markerSequences: [[1, 2]],
   });
   LayerRequest.buildItineraryRows = () => ([{ type: 'animal', species: 'Lion' }]);
   TransportationRouteFragment.showTransportationRouteMarkers = (route, sequences) => {
      shownRoutes.push([route, sequences]);
   };
   TransportationRouteFragment.hideTransportationRouteLayers = () => {};
   ItineraryPathModel.resolveItineraryPath = () => ({ path: true });
   ItineraryPathFragment.renderItineraryPathOverlay = (path) => { pathRenders.push(path); };
   FocusRequest.scheduleFocusRequest = (...args) => focusCalls.push(args);

   try {
      const updater = MapUpdater.createMapUpdater(deps);
      await updater.updateMap('today', null, {
         itinerary: { animals: [] },
         focus: { type: 'animal' },
      });

      assert.deepEqual(shownRoutes, [['summer', [[1, 2]]]]);
      assert.deepEqual(deps.rendered.at(Position.LAST), [{ type: 'animal', species: 'Lion' }]);
      assert.deepEqual(pathRenders, [{ path: true }]);
      assert.equal(focusCalls.length, 1);

      LayerRequest.resolveItineraryTransportationRouteMarkers = () => null;
      const hides = [];
      TransportationRouteFragment.hideTransportationRouteLayers = () => hides.push(true);
      await updater.updateMap('today', null, { itinerary: { animals: [] } });
      assert.equal(hides.length, 1);
   } finally {
      DateContext.buildMapDateContext = originalBuildDate;
      LayerRequest.resolveItineraryTransportationRouteMarkers = originalResolveRoute;
      LayerRequest.buildItineraryRows = originalBuildRows;
      TransportationRouteFragment.showTransportationRouteMarkers = originalShowRoute;
      TransportationRouteFragment.hideTransportationRouteLayers = originalHideRoute;
      ItineraryPathModel.resolveItineraryPath = originalResolvePath;
      ItineraryPathFragment.renderItineraryPathOverlay = originalRenderPath;
      FocusRequest.scheduleFocusRequest = originalSchedule;
   }
});

test('Test_CreateMapUpdater_TestItineraryFailure_ExpectCleared', async () => {
   const deps = _createUpdaterDeps();
   const originalBuildDate = DateContext.buildMapDateContext;
   const originalResolveRoute = LayerRequest.resolveItineraryTransportationRouteMarkers;
   const originalHideRoute = TransportationRouteFragment.hideTransportationRouteLayers;
   const originalClearPath = ItineraryPathFragment.clearItineraryPathOverlay;
   const originalWarn = console.warn;
   const warnings = [];

   DateContext.buildMapDateContext = async () => ({ month: 'JUN', day: 1, year: 2026 });
   LayerRequest.resolveItineraryTransportationRouteMarkers = () => {
      throw new Error('route boom');
   };
   TransportationRouteFragment.hideTransportationRouteLayers = () => {};
   ItineraryPathFragment.clearItineraryPathOverlay = () => {};
   console.warn = (...args) => warnings.push(args);

   try {
      const updater = MapUpdater.createMapUpdater(deps);
      await updater.updateMap('today', null, { itinerary: { animals: [] } });
      assert.deepEqual(deps.rendered.at(Position.LAST), []);
      assert.equal(warnings.length, 1);
   } finally {
      DateContext.buildMapDateContext = originalBuildDate;
      LayerRequest.resolveItineraryTransportationRouteMarkers = originalResolveRoute;
      TransportationRouteFragment.hideTransportationRouteLayers = originalHideRoute;
      ItineraryPathFragment.clearItineraryPathOverlay = originalClearPath;
      console.warn = originalWarn;
   }
});

test('Test_CreateMapUpdater_TestPendingAndFocusHelpers_ExpectDeferredAndDirect', async () => {
   const deps = _createUpdaterDeps();
   const dateCalls = [];
   const directFocus = [];

   const originalBuildDate = DateContext.buildMapDateContext;
   const originalClosed = ClosedExhibitFragment.syncClosedExhibitOverlays;
   const originalBuildLayer = LayerRequest.buildLayerRequest;
   const originalNormalize = FocusRequest.normalizeSearchFocusRequest;
   const originalResolveDeep = FocusRequest.resolveDeepLinkFocus;
   const originalSchedule = FocusRequest.scheduleFocusRequest;
   const originalClearPath = ItineraryPathFragment.clearItineraryPathOverlay;
   const originalHideRoute = TransportationRouteFragment.hideTransportationRouteLayers;

   DateContext.buildMapDateContext = async (preset, dateStr) => {
      dateCalls.push([preset, dateStr]);
      return { month: 'JUN', day: 1, year: 2026 };
   };
   ClosedExhibitFragment.syncClosedExhibitOverlays = async () => [];
   LayerRequest.buildLayerRequest = () => ({
      ctx: {},
      selectedTypes: ['animal'],
   });
   ItineraryPathFragment.clearItineraryPathOverlay = () => {};
   TransportationRouteFragment.hideTransportationRouteLayers = () => {};
   FocusRequest.normalizeSearchFocusRequest = (payload) => payload?.ok ? payload.focus : null;
   FocusRequest.resolveDeepLinkFocus = (payload) => payload?.resolved || null;
   FocusRequest.scheduleFocusRequest = (...args) => directFocus.push(args);

   try {
      const updater = MapUpdater.createMapUpdater({
         ...deps,
         sources: {
            animal: {
               fetch: async () => SourceHelper.setSourceRows(deps.store, 'animal', [
                  { species: 'Lion', type: 'animal' },
               ]),
            },
         },
         getSelectedTypes: () => ['animal', 'missing'],
      });

      assert.equal(updater.refetchWithCurrentControls({ pending: true }), null);
      updater.focusFromSearchRow({ ok: false });
      updater.focusFromDeepLink({ resolved: null });

      await updater.updateMap('today', '2026-06-01', null);
      assert.equal(dateCalls.length, 1);

      const searchResult = updater.focusFromSearchRow({
         ok: true,
         focus: { type: 'animal', row: { species: 'Lion' } },
      });
      assert.ok(searchResult);
      await searchResult;

      const direct = updater.focusFromDeepLink({
         resolved: {
            mode: 'direct',
            focusRequest: { type: 'animal' },
         },
      });
      assert.equal(direct, null);
      assert.deepEqual(directFocus.at(Position.LAST)[1], { type: 'animal' });

      const refetchDeep = updater.focusFromDeepLink({
         resolved: {
            mode: 'refetch',
            focusRequest: { type: 'restaurant' },
         },
      });
      assert.ok(refetchDeep);
      await refetchDeep;
   } finally {
      DateContext.buildMapDateContext = originalBuildDate;
      ClosedExhibitFragment.syncClosedExhibitOverlays = originalClosed;
      LayerRequest.buildLayerRequest = originalBuildLayer;
      FocusRequest.normalizeSearchFocusRequest = originalNormalize;
      FocusRequest.resolveDeepLinkFocus = originalResolveDeep;
      FocusRequest.scheduleFocusRequest = originalSchedule;
      ItineraryPathFragment.clearItineraryPathOverlay = originalClearPath;
      TransportationRouteFragment.hideTransportationRouteLayers = originalHideRoute;
   }
});

test('Test_CreateMapUpdater_TestMissingSource_ExpectStoredRows', async () => {
   const deps = _createUpdaterDeps({
      sources: {},
      getSelectedTypes: () => ['animal'],
   });

   const originalBuildDate = DateContext.buildMapDateContext;
   const originalClosed = ClosedExhibitFragment.syncClosedExhibitOverlays;
   const originalBuildLayer = LayerRequest.buildLayerRequest;
   const originalClearPath = ItineraryPathFragment.clearItineraryPathOverlay;

   DateContext.buildMapDateContext = async () => ({ month: 'JUN', day: 1, year: 2026 });
   ClosedExhibitFragment.syncClosedExhibitOverlays = async () => [];
   LayerRequest.buildLayerRequest = () => ({
      ctx: {},
      selectedTypes: ['animal'],
   });
   ItineraryPathFragment.clearItineraryPathOverlay = () => {};

   try {
      const updater = MapUpdater.createMapUpdater(deps);
      await updater.updateMap('today', null);
      assert.deepEqual(deps.rendered.at(Position.LAST), [
         { species: 'Stored Lion', type: 'animal' },
      ]);
   } finally {
      DateContext.buildMapDateContext = originalBuildDate;
      ClosedExhibitFragment.syncClosedExhibitOverlays = originalClosed;
      LayerRequest.buildLayerRequest = originalBuildLayer;
      ItineraryPathFragment.clearItineraryPathOverlay = originalClearPath;
   }
});
