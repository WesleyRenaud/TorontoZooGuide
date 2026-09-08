import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerBuilder } from '../../../scripts/markers/markerBuilder.js';
import { MarkerHelper } from '../../../scripts/markers/markerHelper.js';
import { MarkerHoverFormatter } from '../../../scripts/markers/markerHoverFormatter.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateMarkerElement_TestGroup_ExpectPositionedMarker', () => {
   const originalHover = MarkerHoverFormatter.buildHoverText;
   const originalVisual = MarkerHelper.applyMarkerVisual;
   const originalCreateElement = document.createElement;
   const visualCalls = [];

   MarkerHoverFormatter.buildHoverText = () => 'African Lion';
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
         x: 12.5,
         y: 40,
         items: [{ type: 'animal', species: 'African Lion' }],
      };
      const markerEl = MarkerBuilder.createMarkerElement(group);

      assert.equal(markerEl.className, 'marker');
      assert.equal(markerEl.style.left, '12.5%');
      assert.equal(markerEl.style.top, '40%');
      assert.equal(markerEl.dataset.hover, 'African Lion');
      assert.equal(markerEl.__items, group.items);
      assert.equal(visualCalls.length, 1);
   } finally {
      document.createElement = originalCreateElement;
      MarkerHoverFormatter.buildHoverText = originalHover;
      MarkerHelper.applyMarkerVisual = originalVisual;
   }
});

test('Test_BindMarkerInteractions_TestCoordinateEditing_ExpectEditor', () => {
   const calls = [];
   MarkerBuilder.bindMarkerInteractions({
      markerEl: { id: 'm1' },
      group: { items: [{ type: 'animal' }] },
      mapInner: { id: 'map' },
      tooltip: { attachToMarker() { assert.fail('should not attach'); } },
      hover: {},
      enableCoordinateEditing: true,
      enableMarkerCoordinateEditing: (markerEl, items, mapInner) => {
         calls.push({ markerEl, items, mapInner });
      },
   });

   assert.equal(calls.length, 1);
   assert.equal(calls[0].markerEl.id, 'm1');
});

test('Test_BindMarkerInteractions_TestTooltip_ExpectAttached', () => {
   const attaches = [];
   MarkerBuilder.bindMarkerInteractions({
      markerEl: { id: 'm2' },
      group: { items: [{ type: 'pavilion' }] },
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

   assert.equal(attaches.length, 1);
   assert.equal(attaches[0].hover.active, true);
});
