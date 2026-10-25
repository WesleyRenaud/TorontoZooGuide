import assert from 'node:assert/strict';
import test from 'node:test';

import { HoverTooltipPositioner } from '../../../scripts/markers/hoverTooltipPositioner.js';


function _installTooltipUnit(width) {
   globalThis.document = {
      documentElement: {
         appendChild() {},
      },
      createElement() {
         return {
            style: {},
            getBoundingClientRect() {
               return { width };
            },
            remove() {},
         };
      },
   };
}


function _withPageZoom(zoomText, closestResult) {
   const originalGetComputedStyle = globalThis.getComputedStyle;
   globalThis.getComputedStyle = () => ({ zoom: zoomText });

   return {
      hoverTooltipEl: {
         style: {},
         closest() {
            return closestResult;
         },
      },
      restore() {
         globalThis.getComputedStyle = originalGetComputedStyle;
      },
   };
}


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
   _installTooltipUnit(1);
   const value = -10;
   const size = 50;
   const viewportSize = 200;

   const clamped = HoverTooltipPositioner.clampToViewport(value, size, viewportSize);

   assert.equal(clamped, HoverTooltipPositioner.HOVER_TOOLTIP_POSITION.viewportPadding);
});


test('Test_ClampToViewport_TestPastEdge_ExpectInnerEdge', () => {
   _installTooltipUnit(1);
   const value = 190;
   const size = 50;
   const viewportSize = 200;

   const clamped = HoverTooltipPositioner.clampToViewport(value, size, viewportSize);

   assert.equal(
      clamped,
      viewportSize - size - HoverTooltipPositioner.HOVER_TOOLTIP_POSITION.viewportPadding
   );
});


test('Test_Length_TestMeasuredUnit_ExpectScaledOffset', () => {
   _installTooltipUnit(1.236);

   const length = HoverTooltipPositioner.length(
      HoverTooltipPositioner.HOVER_TOOLTIP_POSITION.cursorOffsetX
   );

   assert.equal(Math.round(length * 1000) / 1000, 22.248);
});


test('Test_CalculateAndApplyTooltipPosition_TestEvent_ExpectStyle', () => {
   _installTooltipUnit(1);
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
   _installTooltipUnit(1);
   const width = 400;
   const height = 300;
   globalThis.window = { ...(globalThis.window || {}), innerWidth: width, innerHeight: height };
   const clientY = 10;
   const event = { clientX: 100, clientY };
   const tooltipRect = { width: 80, height: 40 };

   const position = HoverTooltipPositioner.calculateTooltipPosition(event, tooltipRect);

   assert.ok(position.y > clientY);
});


test('Test_PageZoom_TestNoStyleReader_ExpectOne', () => {
   const originalGetComputedStyle = globalThis.getComputedStyle;
   globalThis.getComputedStyle = undefined;
   const hoverTooltipEl = {
      closest() {
         return {};
      },
   };

   try {
      const zoom = HoverTooltipPositioner.pageZoom(hoverTooltipEl);

      assert.equal(zoom, 1);
   } finally {
      globalThis.getComputedStyle = originalGetComputedStyle;
   }
});


test('Test_PageZoom_TestOutsidePage_ExpectOne', () => {
   const installed = _withPageZoom('2', null);

   try {
      const zoom = HoverTooltipPositioner.pageZoom(installed.hoverTooltipEl);

      assert.equal(zoom, 1);
   } finally {
      installed.restore();
   }
});


test('Test_PageZoom_TestScaledPage_ExpectZoom', () => {
   const zoomText = '2';
   const installed = _withPageZoom(zoomText, {});

   try {
      const zoom = HoverTooltipPositioner.pageZoom(installed.hoverTooltipEl);

      assert.equal(zoom, Number(zoomText));
   } finally {
      installed.restore();
   }
});


test('Test_PageZoom_TestUnreadableZoom_ExpectOne', () => {
   const installed = _withPageZoom('normal', {});

   try {
      const zoom = HoverTooltipPositioner.pageZoom(installed.hoverTooltipEl);

      assert.equal(zoom, 1);
   } finally {
      installed.restore();
   }
});


test('Test_ApplyTooltipPosition_TestScaledPage_ExpectDividedOffset', () => {
   const x = 80;
   const y = 40;
   const zoomText = '2';
   const installed = _withPageZoom(zoomText, {});

   try {
      HoverTooltipPositioner.applyTooltipPosition(installed.hoverTooltipEl, { x, y });

      assert.equal(installed.hoverTooltipEl.style.left, `${x / Number(zoomText)}px`);
      assert.equal(installed.hoverTooltipEl.style.top, `${y / Number(zoomText)}px`);
   } finally {
      installed.restore();
   }
});
