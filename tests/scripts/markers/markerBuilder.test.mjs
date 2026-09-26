import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerBuilder } from '../../../scripts/markers/markerBuilder.js';
import { MarkerHelper } from '../../../scripts/markers/markerHelper.js';
import { MarkerHoverFormatter } from '../../../scripts/markers/markerHoverFormatter.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateMarkerElement_TestGroup_ExpectPositionedMarker', () => {
   const originalHover = MarkerHoverFormatter.buildHoverText;
   const originalVisual = MarkerHelper.applyMarkerVisual;
   const originalCreateElement = document.createElement;
   const visualCalls = [];
   const hoverText = 'African Lion';
   const x = 12.5;
   const y = 40;

   MarkerHoverFormatter.buildHoverText = () => hoverText;
   MarkerHelper.applyMarkerVisual = (el, items) => {
      visualCalls.push({ el, items });
   };
   document.createElement = (tagName) => {
      const el = originalCreateElement(tagName);
      el.removeAttribute = () => {};
      return el;
   };

   try {
      const group = {
         x,
         y,
         items: [{ type: ItemType.ANIMAL, species: hoverText }],
      };

      const markerEl = MarkerBuilder.createMarkerElement(group);

      assert.equal(markerEl.className, 'marker');
      assert.equal(markerEl.style.left, `${x}%`);
      assert.equal(markerEl.style.top, `${y}%`);
      assert.equal(markerEl.dataset.hover, hoverText);
      assert.equal(markerEl.__items, group.items);
      assert.equal(visualCalls.length, Position.SECOND);
   } finally {
      document.createElement = originalCreateElement;
      MarkerHoverFormatter.buildHoverText = originalHover;
      MarkerHelper.applyMarkerVisual = originalVisual;
   }
});


test('Test_BindMarkerInteractions_TestCoordinateEditing_ExpectEditor', () => {
   const calls = [];
   const markerId = 'm1';

   MarkerBuilder.bindMarkerInteractions({
      markerEl: { id: markerId },
      group: { items: [{ type: ItemType.ANIMAL }] },
      mapInner: { id: 'map' },
      tooltip: {
         attachToMarker() {
            assert.fail('should not attach');
         },
      },
      hover: {},
      enableCoordinateEditing: true,
      enableMarkerCoordinateEditing: (markerEl, items, mapInner) => {
         calls.push({ markerEl, items, mapInner });
      },
   });

   assert.equal(calls.length, Position.SECOND);
   assert.equal(calls.at(Position.FIRST).markerEl.id, markerId);
});


test('Test_BindMarkerInteractions_TestTooltip_ExpectAttached', () => {
   const attaches = [];

   MarkerBuilder.bindMarkerInteractions({
      markerEl: { id: 'm2' },
      group: { items: [{ type: ItemType.PAVILION }] },
      mapInner: {},
      tooltip: {
         attachToMarker(markerEl, items, hover) {
            attaches.push({ markerEl, items, hover });
         },
      },
      hover: { active: true },
      enableCoordinateEditing: false,
      enableMarkerCoordinateEditing: () => {},
   });

   assert.equal(attaches.length, Position.SECOND);
   assert.equal(attaches.at(Position.FIRST).hover.active, true);
});
