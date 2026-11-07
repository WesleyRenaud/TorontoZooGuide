import assert from 'node:assert/strict';
import test from 'node:test';

import { HoverFragment } from '../../../scripts/markers/hoverFragment.js';


function _installTooltipUnit() {
   globalThis.document = {
      documentElement: {
         appendChild() {},
      },
      createElement() {
         return {
            style: {},
            getBoundingClientRect() {
               return { width: 1 };
            },
            remove() {},
         };
      },
   };
}


function _markerAt(top) {
   return {
      getBoundingClientRect: () => ({ left: 40, top, width: 20, height: 12 }),
   };
}


test('Test_CreateHoverTooltip_TestShow_ExpectVisible', () => {
   _installTooltipUnit();
   globalThis.window = { ...(globalThis.window || {}), innerWidth: 500, innerHeight: 400 };
   const species = 'African Lion';
   const hoverTooltipEl = {
      style: { display: 'none' },
      textContent: '',
      getBoundingClientRect: () => ({ width: 60, height: 20 }),
   };
   const hover = HoverFragment.createHoverTooltip(hoverTooltipEl);

   hover.show(species, _markerAt(70));

   assert.equal(hoverTooltipEl.textContent, species);
   assert.equal(hoverTooltipEl.style.display, 'block');
   assert.match(hoverTooltipEl.style.left, /px$/);
});


test('Test_CreateHoverTooltip_TestMove_ExpectStaysOnMarker', () => {
   _installTooltipUnit();
   globalThis.window = { ...(globalThis.window || {}), innerWidth: 500, innerHeight: 400 };
   const hoverTooltipEl = {
      style: { display: 'none' },
      textContent: '',
      getBoundingClientRect: () => ({ width: 60, height: 20 }),
   };
   const hover = HoverFragment.createHoverTooltip(hoverTooltipEl);
   hover.show('African Lion', _markerAt(70));
   const left = hoverTooltipEl.style.left;
   const top = hoverTooltipEl.style.top;

   hover.move({ clientX: 400, clientY: 300 });

   assert.equal(hoverTooltipEl.style.left, left);
   assert.equal(hoverTooltipEl.style.top, top);
});


test('Test_CreateHoverTooltip_TestReposition_ExpectFollowsMarker', () => {
   _installTooltipUnit();
   globalThis.window = { ...(globalThis.window || {}), innerWidth: 500, innerHeight: 400 };
   let markerTop = 70;
   const markerEl = {
      getBoundingClientRect: () => ({ left: 40, top: markerTop, width: 20, height: 12 }),
   };
   const hoverTooltipEl = {
      style: { display: 'none' },
      textContent: '',
      getBoundingClientRect: () => ({ width: 60, height: 20 }),
   };
   const hover = HoverFragment.createHoverTooltip(hoverTooltipEl);
   hover.show('African Lion', markerEl);
   const top = hoverTooltipEl.style.top;

   markerTop = 110;
   hover.reposition();

   assert.notEqual(hoverTooltipEl.style.top, top);
});


test('Test_CreateHoverTooltip_TestHide_ExpectHidden', () => {
   _installTooltipUnit();
   globalThis.window = { ...(globalThis.window || {}), innerWidth: 500, innerHeight: 400 };
   const hoverTooltipEl = {
      style: { display: 'none' },
      textContent: '',
      getBoundingClientRect: () => ({ width: 60, height: 20 }),
   };
   const hover = HoverFragment.createHoverTooltip(hoverTooltipEl);
   hover.show('African Lion', _markerAt(80));

   hover.hide();

   assert.equal(hoverTooltipEl.style.display, 'none');
});
