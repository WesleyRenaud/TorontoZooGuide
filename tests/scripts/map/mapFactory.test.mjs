import assert from 'node:assert/strict';
import test from 'node:test';

import { MapFactory } from '../../../scripts/map/mapFactory.js';
import { MapRuntimeFactory } from '../../../scripts/map/mapRuntimeFactory.js';
import { MapDataSourceFactory } from '../../../scripts/map/mapDataSourceFactory.js';
import { MapStore } from '../../../scripts/map/mapStore.js';
import { MapUpdater } from '../../../scripts/map/mapUpdater.js';
import { HoverFragment } from '../../../scripts/markers/hoverFragment.js';
import { MarkerController } from '../../../scripts/markers/markerController.js';
import { SpeciesFragment } from '../../../scripts/overlays/speciesFragment.js';
import { PanzoomAdapter } from '../../../scripts/map/panzoomAdapter.js';
import { AppConfig } from '../../../scripts/config/appConfig.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateMapRuntime_TestMissingElements_ExpectNull', () => {
   const originalHas = MapRuntimeFactory.hasRequiredRuntimeElements;
   MapRuntimeFactory.hasRequiredRuntimeElements = () => false;
   try {
      assert.equal(MapFactory.createMapRuntime({ mapInner: {} }), null);
   } finally {
      MapRuntimeFactory.hasRequiredRuntimeElements = originalHas;
   }
});

test('Test_CreateMapRuntime_TestWiredDeps_ExpectRuntimeParts', () => {
   const originalHas = MapRuntimeFactory.hasRequiredRuntimeElements;
   const originalPanzoom = PanzoomAdapter.createPanzoom;
   const originalStore = MapStore.createMapStore;
   const originalSources = MapDataSourceFactory.createDataSources;
   const originalHover = HoverFragment.createHoverTooltip;
   const originalSpecies = SpeciesFragment.initSpeciesOverlay;
   const originalTooltip = MapRuntimeFactory.createMapTooltip;
   const originalLabels = MapRuntimeFactory.initMapLabels;
   const originalMarkers = MarkerController.createMarkerLayer;
   const originalFocus = MapRuntimeFactory.createMapFocus;
   const originalUpdater = MapUpdater.createMapUpdater;
   const originalRepositioner = MapRuntimeFactory.createTooltipRepositioner;
   const labelInits = [];

   MapRuntimeFactory.hasRequiredRuntimeElements = () => true;
   PanzoomAdapter.createPanzoom = (el, options) => {
      assert.equal(options.contain, AppConfig.DEFAULT_MAP_CONTAIN);
      return { panzoom: true, el };
   };
   MapStore.createMapStore = () => ({ store: true });
   MapDataSourceFactory.createDataSources = (store) => ({ sources: true, store });
   HoverFragment.createHoverTooltip = () => ({ hover: true });
   SpeciesFragment.initSpeciesOverlay = () => ({ overlay: true });
   MapRuntimeFactory.createMapTooltip = () => ({ tooltip: true });
   MapRuntimeFactory.initMapLabels = (checkbox) => { labelInits.push(checkbox); };
   MarkerController.createMarkerLayer = () => ({ markers: true });
   MapRuntimeFactory.createMapFocus = () => ({ focus: true });
   MapUpdater.createMapUpdater = (options) => ({ updater: true, options });
   MapRuntimeFactory.createTooltipRepositioner = () => () => 'repositioned';

   try {
      const parent = document.createElement('div');
      const mapInner = document.createElement('div');
      parent.appendChild(mapInner);
      const checkbox = { id: 'labels' };

      const runtime = MapFactory.createMapRuntime({
         mapInner,
         tooltipEl: { id: 'tip' },
         hoverTooltipEl: { id: 'hover' },
         showMapLabelsCheckbox: checkbox,
      });

      assert.equal(runtime.panzoom.panzoom, true);
      assert.equal(runtime.store.store, true);
      assert.equal(runtime.sources.sources, true);
      assert.equal(runtime.hover.hover, true);
      assert.equal(runtime.tooltip.tooltip, true);
      assert.equal(runtime.markers.markers, true);
      assert.equal(runtime.focus.focus, true);
      assert.equal(runtime.updater.updater, true);
      assert.equal(runtime.repositionTooltips(), 'repositioned');
      assert.deepEqual(labelInits, [checkbox]);
   } finally {
      MapRuntimeFactory.hasRequiredRuntimeElements = originalHas;
      PanzoomAdapter.createPanzoom = originalPanzoom;
      MapStore.createMapStore = originalStore;
      MapDataSourceFactory.createDataSources = originalSources;
      HoverFragment.createHoverTooltip = originalHover;
      SpeciesFragment.initSpeciesOverlay = originalSpecies;
      MapRuntimeFactory.createMapTooltip = originalTooltip;
      MapRuntimeFactory.initMapLabels = originalLabels;
      MarkerController.createMarkerLayer = originalMarkers;
      MapRuntimeFactory.createMapFocus = originalFocus;
      MapUpdater.createMapUpdater = originalUpdater;
      MapRuntimeFactory.createTooltipRepositioner = originalRepositioner;
   }
});
