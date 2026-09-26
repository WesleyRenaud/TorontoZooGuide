import assert from 'node:assert/strict';
import test from 'node:test';

import { HoverTooltipPositioner } from '../../../scripts/markers/hoverTooltipPositioner.js';


test('Test_IsTooltipVisible_TestBlock_ExpectTrue', () => {
   const hoverTooltipEl = { style: { display: 'block' } };

   const visible = HoverTooltipPositioner.isTooltipVisible(hoverTooltipEl);

   assert.equal(visible, true);
});


test('Test_IsTooltipVisible_TestNone_ExpectFalse', () => {
   const hoverTooltipEl = { style: { display: 'none' } };

   const visible = HoverTooltipPositioner.isTooltipVisible(hoverTooltipEl);

   assert.equal(visible, false);
});


test('Test_IsTooltipVisible_TestNull_ExpectFalse', () => {
   const hoverTooltipEl = null;

   const visible = HoverTooltipPositioner.isTooltipVisible(hoverTooltipEl);

   assert.equal(visible, false);
});


test('Test_ClampToViewport_TestBelowPadding_ExpectPadding', () => {
   const value = -10;
   const size = 50;
   const viewportSize = 200;

   const clamped = HoverTooltipPositioner.clampToViewport(value, size, viewportSize);

   assert.equal(clamped, HoverTooltipPositioner.HOVER_TOOLTIP_POSITION.viewportPadding);
});


test('Test_ClampToViewport_TestPastEdge_ExpectInnerEdge', () => {
   const value = 190;
   const size = 50;
   const viewportSize = 200;

   const clamped = HoverTooltipPositioner.clampToViewport(value, size, viewportSize);

   assert.equal(
      clamped,
      viewportSize - size - HoverTooltipPositioner.HOVER_TOOLTIP_POSITION.viewportPadding
   );
});


test('Test_CalculateAndApplyTooltipPosition_TestEvent_ExpectStyle', () => {
   const width = 400;
   const height = 300;
   globalThis.window = { ...(globalThis.window || {}), innerWidth: width, innerHeight: height };
   const event = { clientX: 100, clientY: 120 };
   const tooltipRect = { width: 80, height: 40 };
   const el = { style: {} };

   const position = HoverTooltipPositioner.calculateTooltipPosition(event, tooltipRect);
   HoverTooltipPositioner.applyTooltipPosition(el, position);

   assert.match(el.style.left, /px$/);
   assert.match(el.style.top, /px$/);
});


test('Test_CalculateTooltipPosition_TestNearTop_ExpectFlippedBelow', () => {
   const width = 400;
   const height = 300;
   globalThis.window = { ...(globalThis.window || {}), innerWidth: width, innerHeight: height };
   const clientY = 10;
   const event = { clientX: 100, clientY };
   const tooltipRect = { width: 80, height: 40 };

   const position = HoverTooltipPositioner.calculateTooltipPosition(event, tooltipRect);

   assert.ok(position.y > clientY);
});
