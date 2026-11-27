import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerController } from '../../../scripts/markers/markerController.js';
import { CoordinateEditor } from '../../../scripts/markers/coordinateEditor.js';
import { MarkerBuilder } from '../../../scripts/markers/markerBuilder.js';
import { MarkerGrouper } from '../../../scripts/markers/markerGrouper.js';
import { MarkerLayerHelper } from '../../../scripts/markers/markerLayerHelper.js';
import { MarkerTargetSizer } from '../../../scripts/markers/markerTargetSizer.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


function _createMarkerSurface() {
   const markerSurface = document.createElement('div');
   const originalAppend = markerSurface.appendChild.bind(markerSurface);

   markerSurface.appendChild = (child) => {
      if (child?.tagName === '#fragment') {
         for (const nested of [...child.children]) {
            originalAppend(nested);
         }
         return child;
      }
      return originalAppend(child);
   };

   return markerSurface;
}


test('Test_CreateMarkerLayer_TestRenderAndLookup_ExpectMarkers', () => {
   const originalRemove = MarkerLayerHelper.removeRenderedMarkers;
   const originalCreate = MarkerBuilder.createMarkerElement;
   const originalBind = MarkerBuilder.bindMarkerInteractions;
   const originalGroup = MarkerGrouper.groupMarkersByCoordinate;
   const originalShould = MarkerLayerHelper.shouldRenderMarkerGroup;
   const binds = [];
   const removes = [];
   const renderedKey = '1|2';
   const skippedKey = '3|4';
   const mapId = 'map';

   MarkerLayerHelper.removeRenderedMarkers = (mapInner) => {
      removes.push(mapInner.id);
   };
   MarkerBuilder.createMarkerElement = (group) => {
      const el = document.createElement('div');
      el.id = group.key;
      return el;
   };
   MarkerBuilder.bindMarkerInteractions = (options) => {
      binds.push(options);
   };
   MarkerGrouper.groupMarkersByCoordinate = () => new Map([
      [renderedKey, { key: renderedKey, items: [{ type: ItemType.ANIMAL }] }],
      [skippedKey, { key: skippedKey, items: [{ type: 'skip' }] }],
   ]);
   MarkerLayerHelper.shouldRenderMarkerGroup = (group) => group.key === renderedKey;

   try {
      const mapInner = document.createElement('div');
      mapInner.id = mapId;
      const originalAppend = mapInner.appendChild.bind(mapInner);
      mapInner.appendChild = (child) => {
         if (child?.tagName === '#fragment') {
            for (const nested of [...child.children]) {
               originalAppend(nested);
            }
            return child;
         }
         return originalAppend(child);
      };

      const layer = MarkerController.createMarkerLayer({
         markerSurface: mapInner,
         tooltip: {},
         hover: {},
         enableCoordinateEditing: true,
      });
      layer.render([{ type: ItemType.ANIMAL }]);

      assert.deepEqual(removes, [mapId]);
      assert.equal(mapInner.children.length, Position.SECOND);
      assert.equal(mapInner.children.at(Position.FIRST).id, renderedKey);
      assert.equal(
         binds.at(Position.FIRST).enableMarkerCoordinateEditing,
         CoordinateEditor.enableMarkerCoordinateEditing
      );
      assert.equal(layer.getMarkerByCoord(renderedKey).id, renderedKey);
      assert.equal(layer.getMarkerByCoord('missing'), null);
      assert.equal(layer.getAllMarkers().length, Position.SECOND);
   } finally {
      MarkerLayerHelper.removeRenderedMarkers = originalRemove;
      MarkerBuilder.createMarkerElement = originalCreate;
      MarkerBuilder.bindMarkerInteractions = originalBind;
      MarkerGrouper.groupMarkersByCoordinate = originalGroup;
      MarkerLayerHelper.shouldRenderMarkerGroup = originalShould;
   }
});


test('Test_CreateMarkerLayer_TestMarkerSurface_ExpectMarkersOnSurface', () => {
   const originalCreate = MarkerBuilder.createMarkerElement;
   const originalBind = MarkerBuilder.bindMarkerInteractions;
   const originalGroup = MarkerGrouper.groupMarkersByCoordinate;
   const originalShould = MarkerLayerHelper.shouldRenderMarkerGroup;
   const binds = [];
   const markerSurface = document.createElement('div');
   const renderedKey = '10|20';
   const originalAppend = markerSurface.appendChild.bind(markerSurface);
   markerSurface.appendChild = (child) => {
      if (child?.tagName === '#fragment') {
         for (const nested of [...child.children]) {
            originalAppend(nested);
         }
         return child;
      }
      return originalAppend(child);
   };

   MarkerBuilder.createMarkerElement = (group) => {
      const el = document.createElement('div');
      el.id = group.key;
      return el;
   };
   MarkerBuilder.bindMarkerInteractions = (options) => {
      binds.push(options);
   };
   MarkerGrouper.groupMarkersByCoordinate = () => new Map([
      [renderedKey, { key: renderedKey, items: [{ type: ItemType.ANIMAL }] }],
   ]);
   MarkerLayerHelper.shouldRenderMarkerGroup = () => true;

   try {
      const layer = MarkerController.createMarkerLayer({
         markerSurface,
         tooltip: {},
         hover: {},
      });
      layer.render([{ type: ItemType.ANIMAL }]);

      assert.equal(markerSurface.children.length, Position.SECOND);
      assert.equal(markerSurface.children.at(Position.FIRST).id, renderedKey);
      assert.equal(binds.at(Position.FIRST).mapInner, markerSurface);
      assert.equal(layer.getMarkerByCoord(renderedKey).id, renderedKey);
   } finally {
      MarkerBuilder.createMarkerElement = originalCreate;
      MarkerBuilder.bindMarkerInteractions = originalBind;
      MarkerGrouper.groupMarkersByCoordinate = originalGroup;
      MarkerLayerHelper.shouldRenderMarkerGroup = originalShould;
   }
});


test('Test_Render_TestMarkers_ExpectTargetSizesApplied', () => {
   const originalCreate = MarkerBuilder.createMarkerElement;
   const originalBind = MarkerBuilder.bindMarkerInteractions;
   const originalGroup = MarkerGrouper.groupMarkersByCoordinate;
   const originalApply = MarkerTargetSizer.applyToMarkers;
   const renderedKey = '10|20';
   const appliedMarkerLists = [];

   MarkerBuilder.createMarkerElement = (group) => {
      const el = document.createElement('div');
      el.id = group.key;
      return el;
   };
   MarkerBuilder.bindMarkerInteractions = () => {};
   MarkerGrouper.groupMarkersByCoordinate = () => new Map([
      [renderedKey, { key: renderedKey, items: [{ type: ItemType.ANIMAL }] }],
   ]);
   MarkerTargetSizer.applyToMarkers = (markerEls) => {
      appliedMarkerLists.push(markerEls);
   };

   try {
      const layer = MarkerController.createMarkerLayer({
         markerSurface: _createMarkerSurface(),
         tooltip: {},
         hover: {},
      });
      layer.render([{ type: ItemType.ANIMAL }]);

      assert.equal(appliedMarkerLists.length, Position.SECOND);
      assert.equal(appliedMarkerLists.at(Position.FIRST).at(Position.FIRST).id, renderedKey);
   } finally {
      MarkerBuilder.createMarkerElement = originalCreate;
      MarkerBuilder.bindMarkerInteractions = originalBind;
      MarkerGrouper.groupMarkersByCoordinate = originalGroup;
      MarkerTargetSizer.applyToMarkers = originalApply;
   }
});


test('Test_CreateMarkerLayer_TestResize_ExpectTargetSizesRecomputed', () => {
   const originalObserver = globalThis.ResizeObserver;
   const originalApply = MarkerTargetSizer.applyToMarkers;
   const observed = [];
   const callbacks = [];
   let applyCount = 0;

   globalThis.ResizeObserver = class ResizeObserver {
      constructor(callback) {
         callbacks.push(callback);
      }

      observe(element) {
         observed.push(element);
      }
   };
   MarkerTargetSizer.applyToMarkers = () => {
      applyCount += 1;
   };

   try {
      const markerSurface = _createMarkerSurface();

      MarkerController.createMarkerLayer({ markerSurface, tooltip: {}, hover: {} });
      callbacks.at(Position.FIRST)();

      assert.deepEqual(observed, [markerSurface]);
      assert.equal(applyCount, Position.SECOND);
   } finally {
      globalThis.ResizeObserver = originalObserver;
      MarkerTargetSizer.applyToMarkers = originalApply;
   }
});
