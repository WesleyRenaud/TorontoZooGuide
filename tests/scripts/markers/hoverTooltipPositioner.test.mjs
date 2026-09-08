import assert from 'node:assert/strict';
import test from 'node:test';

import { HoverTooltipPositioner } from '../../../scripts/markers/hoverTooltipPositioner.js';

test('Test_IsTooltipVisible_TestDisplay_ExpectBoolean', () => {
   assert.equal(HoverTooltipPositioner.isTooltipVisible({ style: { display: 'block' } }), true);
   assert.equal(HoverTooltipPositioner.isTooltipVisible({ style: { display: 'none' } }), false);
   assert.equal(HoverTooltipPositioner.isTooltipVisible(null), false);
});

test('Test_ClampToViewport_TestEdges_ExpectClamped', () => {
   assert.equal(HoverTooltipPositioner.clampToViewport(-10, 50, 200), 14);
   assert.equal(HoverTooltipPositioner.clampToViewport(190, 50, 200), 136);
});

test('Test_CalculateAndApplyTooltipPosition_TestEvent_ExpectStyle', () => {
   globalThis.window = { ...(globalThis.window || {}), innerWidth: 400, innerHeight: 300 };
   const position = HoverTooltipPositioner.calculateTooltipPosition(
      { clientX: 100, clientY: 120 },
      { width: 80, height: 40 }
   );
   const el = { style: {} };
   HoverTooltipPositioner.applyTooltipPosition(el, position);
   assert.match(el.style.left, /px$/);
   assert.match(el.style.top, /px$/);

   const flipped = HoverTooltipPositioner.calculateTooltipPosition(
      { clientX: 100, clientY: 10 },
      { width: 80, height: 40 }
   );
   assert.ok(flipped.y > 10);
});
