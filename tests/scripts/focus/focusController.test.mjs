import assert from 'node:assert/strict';
import test from 'node:test';

import { FocusController } from '../../../scripts/focus/focusController.js';
import { FocusAnimator } from '../../../scripts/focus/focusAnimator.js';
import { FocusTargetFinder } from '../../../scripts/focus/focusTargetFinder.js';
import { Position } from '../../../scripts/shared/enums/position.js';

const species = 'Amur Tiger';


function _createController(overrides = {}) {
   return FocusController.createFocusController({
      panzoom: { id: 'pz' },
      getMarkerByCoord: () => ({}),
      getViewportEl: () => ({ id: 'viewport' }),
      tooltip: { id: 'tip' },
      getAllMarkers: () => [{ id: 'm1' }],
      ...overrides,
   });
}


test('Test_CreateFocusController_TestMissingRow_ExpectNoFocus', () => {
   const originalFocus = FocusAnimator.focusMarker;
   const focuses = [];
   FocusAnimator.focusMarker = (options) => {
      focuses.push(options);
   };

   try {
      const controller = _createController({
         getViewportEl: () => ({ id: 'viewport' }),
      });

      controller.focus({ row: null, type: 'animal' });

      assert.equal(focuses.length, Position.FIRST);
   } finally {
      FocusAnimator.focusMarker = originalFocus;
   }
});


test('Test_CreateFocusController_TestMissingViewport_ExpectNoFocus', () => {
   const originalFocus = FocusAnimator.focusMarker;
   const focuses = [];
   FocusAnimator.focusMarker = (options) => {
      focuses.push(options);
   };

   try {
      const controller = _createController({
         getViewportEl: () => null,
      });

      controller.focus({ row: { species }, type: 'animal' });

      assert.equal(focuses.length, Position.FIRST);
   } finally {
      FocusAnimator.focusMarker = originalFocus;
   }
});


test('Test_CreateFocusController_TestCoordinates_ExpectCoordMarker', () => {
   const originalFocus = FocusAnimator.focusMarker;
   const originalMatch = FocusTargetFinder.createFocusMatch;
   const originalByCoord = FocusTargetFinder.findMarkerByCoordinates;
   const originalScan = FocusTargetFinder.findBestMarkerByScan;
   const focuses = [];
   const coordMarkerId = 'coord-marker';
   const xCoord = 1;
   const yCoord = 2;

   FocusAnimator.focusMarker = (options) => {
      focuses.push(options);
   };
   FocusTargetFinder.createFocusMatch = () => ({
      typeKey: 'animal',
      matchFn: () => true,
   });
   FocusTargetFinder.findMarkerByCoordinates = () => ({
      id: coordMarkerId,
      __items: [{ type: 'animal' }],
   });
   FocusTargetFinder.findBestMarkerByScan = () => ({
      marker: { id: 'scan-marker' },
      items: [{ type: 'animal' }],
   });

   try {
      const controller = _createController();

      controller.focus({
         row: { x_coord: xCoord, y_coord: yCoord, species },
         type: 'animal',
      });

      assert.equal(focuses.at(Position.FIRST).marker.id, coordMarkerId);
   } finally {
      FocusAnimator.focusMarker = originalFocus;
      FocusTargetFinder.createFocusMatch = originalMatch;
      FocusTargetFinder.findMarkerByCoordinates = originalByCoord;
      FocusTargetFinder.findBestMarkerByScan = originalScan;
   }
});


test('Test_CreateFocusController_TestScan_ExpectScanMarker', () => {
   const originalFocus = FocusAnimator.focusMarker;
   const originalMatch = FocusTargetFinder.createFocusMatch;
   const originalByCoord = FocusTargetFinder.findMarkerByCoordinates;
   const originalScan = FocusTargetFinder.findBestMarkerByScan;
   const focuses = [];
   const scanMarkerId = 'scan-marker';

   FocusAnimator.focusMarker = (options) => {
      focuses.push(options);
   };
   FocusTargetFinder.createFocusMatch = () => ({
      typeKey: 'animal',
      matchFn: () => true,
   });
   FocusTargetFinder.findMarkerByCoordinates = () => null;
   FocusTargetFinder.findBestMarkerByScan = () => ({
      marker: { id: scanMarkerId },
      items: [{ type: 'animal' }],
   });

   try {
      const controller = _createController();

      controller.focus({
         row: { species },
         type: 'animal',
      });

      assert.equal(focuses.at(Position.FIRST).marker.id, scanMarkerId);
   } finally {
      FocusAnimator.focusMarker = originalFocus;
      FocusTargetFinder.createFocusMatch = originalMatch;
      FocusTargetFinder.findMarkerByCoordinates = originalByCoord;
      FocusTargetFinder.findBestMarkerByScan = originalScan;
   }
});


test('Test_CreateFocusController_TestScanMiss_ExpectNoFocus', () => {
   const originalFocus = FocusAnimator.focusMarker;
   const originalMatch = FocusTargetFinder.createFocusMatch;
   const originalByCoord = FocusTargetFinder.findMarkerByCoordinates;
   const originalScan = FocusTargetFinder.findBestMarkerByScan;
   const focuses = [];

   FocusAnimator.focusMarker = (options) => {
      focuses.push(options);
   };
   FocusTargetFinder.createFocusMatch = () => ({
      typeKey: 'animal',
      matchFn: () => true,
   });
   FocusTargetFinder.findMarkerByCoordinates = () => null;
   FocusTargetFinder.findBestMarkerByScan = () => null;

   try {
      const controller = _createController();

      controller.focus({ row: { species }, type: 'animal' });

      assert.equal(focuses.length, Position.FIRST);
   } finally {
      FocusAnimator.focusMarker = originalFocus;
      FocusTargetFinder.createFocusMatch = originalMatch;
      FocusTargetFinder.findMarkerByCoordinates = originalByCoord;
      FocusTargetFinder.findBestMarkerByScan = originalScan;
   }
});


test('Test_CreateFocusController_TestCoordMiss_ExpectNoFocus', () => {
   const originalFocus = FocusAnimator.focusMarker;
   const originalMatch = FocusTargetFinder.createFocusMatch;
   const originalByCoord = FocusTargetFinder.findMarkerByCoordinates;
   const originalScan = FocusTargetFinder.findBestMarkerByScan;
   const focuses = [];
   const xCoord = 3;
   const yCoord = 4;

   FocusAnimator.focusMarker = (options) => {
      focuses.push(options);
   };
   FocusTargetFinder.createFocusMatch = () => ({
      typeKey: 'animal',
      matchFn: () => true,
   });
   FocusTargetFinder.findMarkerByCoordinates = () => null;
   FocusTargetFinder.findBestMarkerByScan = () => ({
      marker: { id: 'scan-marker' },
      items: [{ type: 'animal' }],
   });

   try {
      const controller = _createController();

      controller.focus({
         row: { x_coord: xCoord, y_coord: yCoord, species },
         type: 'animal',
      });

      assert.equal(focuses.length, Position.FIRST);
   } finally {
      FocusAnimator.focusMarker = originalFocus;
      FocusTargetFinder.createFocusMatch = originalMatch;
      FocusTargetFinder.findMarkerByCoordinates = originalByCoord;
      FocusTargetFinder.findBestMarkerByScan = originalScan;
   }
});


test('Test_CreateFocusController_TestEmptyMarkers_ExpectNoFocus', () => {
   const originalFocus = FocusAnimator.focusMarker;
   const originalMatch = FocusTargetFinder.createFocusMatch;
   const originalByCoord = FocusTargetFinder.findMarkerByCoordinates;
   const originalScan = FocusTargetFinder.findBestMarkerByScan;
   const focuses = [];

   FocusAnimator.focusMarker = (options) => {
      focuses.push(options);
   };
   FocusTargetFinder.createFocusMatch = () => ({
      typeKey: 'animal',
      matchFn: () => true,
   });
   FocusTargetFinder.findMarkerByCoordinates = () => null;
   FocusTargetFinder.findBestMarkerByScan = () => ({
      marker: { id: 'scan-marker' },
      items: [{ type: 'animal' }],
   });

   try {
      const controller = _createController({
         getAllMarkers: () => [],
      });

      controller.focus({ row: { species }, type: 'animal' });

      assert.equal(focuses.length, Position.FIRST);
   } finally {
      FocusAnimator.focusMarker = originalFocus;
      FocusTargetFinder.createFocusMatch = originalMatch;
      FocusTargetFinder.findMarkerByCoordinates = originalByCoord;
      FocusTargetFinder.findBestMarkerByScan = originalScan;
   }
});


test('Test_CreateFocusController_TestScanWithoutMarker_ExpectNoFocus', () => {
   const originalFocus = FocusAnimator.focusMarker;
   const originalMatch = FocusTargetFinder.createFocusMatch;
   const originalByCoord = FocusTargetFinder.findMarkerByCoordinates;
   const originalScan = FocusTargetFinder.findBestMarkerByScan;
   const focuses = [];

   FocusAnimator.focusMarker = (options) => {
      focuses.push(options);
   };
   FocusTargetFinder.createFocusMatch = () => ({
      typeKey: 'animal',
      matchFn: () => true,
   });
   FocusTargetFinder.findMarkerByCoordinates = () => null;
   FocusTargetFinder.findBestMarkerByScan = () => ({
      items: [{ type: 'animal' }],
   });

   try {
      const controller = _createController();

      controller.focus({ row: { species }, type: 'animal' });

      assert.equal(focuses.length, Position.FIRST);
   } finally {
      FocusAnimator.focusMarker = originalFocus;
      FocusTargetFinder.createFocusMatch = originalMatch;
      FocusTargetFinder.findMarkerByCoordinates = originalByCoord;
      FocusTargetFinder.findBestMarkerByScan = originalScan;
   }
});
