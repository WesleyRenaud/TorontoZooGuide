import assert from 'node:assert/strict';
import test from 'node:test';

import { FocusController } from '../../../scripts/focus/focusController.js';
import { FocusAnimator } from '../../../scripts/focus/focusAnimator.js';
import { FocusTargetFinder } from '../../../scripts/focus/focusTargetFinder.js';

test('Test_CreateFocusController_TestMissingRowOrViewport_ExpectNoFocus', () => {
   const originalFocus = FocusAnimator.focusMarker;
   let focused = 0;
   FocusAnimator.focusMarker = () => { focused += 1; };

   try {
      const controller = FocusController.createFocusController({
         panzoom: {},
         getMarkerByCoord: () => null,
         getViewportEl: () => null,
         tooltip: {},
         getAllMarkers: () => [],
      });
      controller.focus({ row: { species: 'Tiger' }, type: 'animal' });
      controller.focus({ row: null, type: 'animal' });
      assert.equal(focused, 0);
   } finally {
      FocusAnimator.focusMarker = originalFocus;
   }
});

test('Test_CreateFocusController_TestCoordinateAndScan_ExpectAnimator', () => {
   const originalFocus = FocusAnimator.focusMarker;
   const originalMatch = FocusTargetFinder.createFocusMatch;
   const originalByCoord = FocusTargetFinder.findMarkerByCoordinates;
   const originalScan = FocusTargetFinder.findBestMarkerByScan;
   const focuses = [];

   FocusAnimator.focusMarker = (options) => { focuses.push(options); };
   FocusTargetFinder.createFocusMatch = () => ({
      typeKey: 'animal',
      matchFn: () => true,
   });
   FocusTargetFinder.findMarkerByCoordinates = () => ({
      id: 'coord-marker',
      __items: [{ type: 'animal' }],
   });
   FocusTargetFinder.findBestMarkerByScan = () => ({
      marker: { id: 'scan-marker' },
      items: [{ type: 'animal' }],
   });

   try {
      const controller = FocusController.createFocusController({
         panzoom: { id: 'pz' },
         getMarkerByCoord: () => ({}),
         getViewportEl: () => ({ id: 'viewport' }),
         tooltip: { id: 'tip' },
         getAllMarkers: () => [{ id: 'm1' }],
      });

      controller.focus({
         row: { x_coord: 1, y_coord: 2, species: 'Tiger' },
         type: 'animal',
      });
      assert.equal(focuses[0].marker.id, 'coord-marker');

      focuses.length = 0;
      FocusTargetFinder.findMarkerByCoordinates = () => null;
      controller.focus({
         row: { species: 'Tiger' },
         type: 'animal',
      });
      assert.equal(focuses[0].marker.id, 'scan-marker');

      focuses.length = 0;
      FocusTargetFinder.findBestMarkerByScan = () => null;
      controller.focus({ row: { species: 'Tiger' }, type: 'animal' });
      assert.equal(focuses.length, 0);

      focuses.length = 0;
      FocusTargetFinder.findMarkerByCoordinates = () => null;
      controller.focus({
         row: { x_coord: 3, y_coord: 4, species: 'Tiger' },
         type: 'animal',
      });
      assert.equal(focuses.length, 0);

      focuses.length = 0;
      const emptyMarkersController = FocusController.createFocusController({
         panzoom: { id: 'pz' },
         getMarkerByCoord: () => ({}),
         getViewportEl: () => ({ id: 'viewport' }),
         tooltip: { id: 'tip' },
         getAllMarkers: () => [],
      });
      emptyMarkersController.focus({ row: { species: 'Tiger' }, type: 'animal' });
      assert.equal(focuses.length, 0);

      FocusTargetFinder.findBestMarkerByScan = () => ({
         items: [{ type: 'animal' }],
      });
      const noMarkerController = FocusController.createFocusController({
         panzoom: { id: 'pz' },
         getMarkerByCoord: () => ({}),
         getViewportEl: () => ({ id: 'viewport' }),
         tooltip: { id: 'tip' },
         getAllMarkers: () => [{ id: 'm1' }],
      });
      noMarkerController.focus({ row: { species: 'Tiger' }, type: 'animal' });
      assert.equal(focuses.length, 0);
   } finally {
      FocusAnimator.focusMarker = originalFocus;
      FocusTargetFinder.createFocusMatch = originalMatch;
      FocusTargetFinder.findMarkerByCoordinates = originalByCoord;
      FocusTargetFinder.findBestMarkerByScan = originalScan;
   }
});
