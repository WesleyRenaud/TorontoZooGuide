import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerController } from '../../../scripts/markers/markerController.js';
import { CoordinateEditor } from '../../../scripts/markers/coordinateEditor.js';
import { MarkerBuilder } from '../../../scripts/markers/markerBuilder.js';
import { MarkerGrouper } from '../../../scripts/markers/markerGrouper.js';
import { MarkerLayerHelper } from '../../../scripts/markers/markerLayerHelper.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
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

   MarkerLayerHelper.removeRenderedMarkers = (mapInner) => { removes.push(mapInner.id); };
   MarkerBuilder.createMarkerElement = (group) => {
      const el = document.createElement('div');
      el.id = group.key;
      return el;
   };
   MarkerBuilder.bindMarkerInteractions = (options) => { binds.push(options); };
   MarkerGrouper.groupMarkersByCoordinate = () => new Map([
      ['1|2', { key: '1|2', items: [{ type: ItemType.ANIMAL }] }],
      ['3|4', { key: '3|4', items: [{ type: 'skip' }] }],
   ]);
   MarkerLayerHelper.shouldRenderMarkerGroup = (group) => group.key === '1|2';

   try {
      const mapInner = document.createElement('div');
      mapInner.id = 'map';
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
      assert.deepEqual(removes, ['map']);
      assert.equal(mapInner.children.length, 1);
      assert.equal(mapInner.children[0].id, '1|2');
      assert.equal(binds[0].enableMarkerCoordinateEditing, CoordinateEditor.enableMarkerCoordinateEditing);
      assert.equal(layer.getMarkerByCoord('1|2').id, '1|2');
      assert.equal(layer.getMarkerByCoord('missing'), null);
      assert.equal(layer.getAllMarkers().length, 1);
   } finally {
      MarkerLayerHelper.removeRenderedMarkers = originalRemove;
      MarkerBuilder.createMarkerElement = originalCreate;
      MarkerBuilder.bindMarkerInteractions = originalBind;
      MarkerGrouper.groupMarkersByCoordinate = originalGroup;
      MarkerLayerHelper.shouldRenderMarkerGroup = originalShould;
   }
});
