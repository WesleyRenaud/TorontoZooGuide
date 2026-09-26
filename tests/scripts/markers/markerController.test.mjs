import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerController } from '../../../scripts/markers/markerController.js';
import { CoordinateEditor } from '../../../scripts/markers/coordinateEditor.js';
import { MarkerBuilder } from '../../../scripts/markers/markerBuilder.js';
import { MarkerGrouper } from '../../../scripts/markers/markerGrouper.js';
import { MarkerLayerHelper } from '../../../scripts/markers/markerLayerHelper.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


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
         mapInner,
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
