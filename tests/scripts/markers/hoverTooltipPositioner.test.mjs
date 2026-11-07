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
      HoverTooltipPositioner.HOVER_TOOLTIP_POSITION.arrowSize
   );

   assert.equal(Math.round(length * 1000) / 1000, 3.09);
});


test('Test_CalculateAndApplyTooltipPosition_TestMarker_ExpectArrowOnMarker', () => {
   _installTooltipUnit(1);
   const width = 400;
   const height = 300;
   globalThis.window = { ...(globalThis.window || {}), innerWidth: width, innerHeight: height };
   const markerRect = { left: 90, top: 120, width: 20, height: 12 };
   const anchorX = markerRect.left + markerRect.width / 2;
   const tooltipRect = { width: 80, height: 40 };
   const arrowSize = HoverTooltipPositioner.HOVER_TOOLTIP_POSITION.arrowSize;
   const el = { style: {} };

   const position = HoverTooltipPositioner.calculateTooltipPosition(markerRect, tooltipRect);
   HoverTooltipPositioner.applyTooltipPosition(el, position);

   assert.equal(el.style.left, `${anchorX - tooltipRect.width / 2}px`);
   assert.equal(el.style.top, `${markerRect.top - tooltipRect.height - arrowSize}px`);
   assert.equal(position.below, false);
   assert.equal(position.arrowLeft, tooltipRect.width / 2 - arrowSize);
});


test('Test_CalculateTooltipPosition_TestNearTop_ExpectFlippedBelow', () => {
   _installTooltipUnit(1);
   const width = 400;
   const height = 300;
   globalThis.window = { ...(globalThis.window || {}), innerWidth: width, innerHeight: height };
   const markerRect = { left: 90, top: 30, bottom: 42, width: 20, height: 12 };
   const tooltipRect = { width: 80, height: 40 };
   const arrowSize = HoverTooltipPositioner.HOVER_TOOLTIP_POSITION.arrowSize;

   const position = HoverTooltipPositioner.calculateTooltipPosition(markerRect, tooltipRect);

   assert.equal(position.below, true);
   assert.equal(position.y, markerRect.bottom + arrowSize);
});


test('Test_CalculateTooltipPosition_TestPageZoom_ExpectLayoutAnchor', () => {
   _installTooltipUnit(1);
   const width = 1920;
   const height = 1080;
   globalThis.window = { ...(globalThis.window || {}), innerWidth: width, innerHeight: height };
   const zoom = 2;
   const markerRect = { left: 190, top: 150, width: 20, height: 12 };
   const anchorX = markerRect.left + markerRect.width / 2;
   const tooltipRect = { width: 80, height: 40 };
   const arrowSize = HoverTooltipPositioner.HOVER_TOOLTIP_POSITION.arrowSize;

   const position = HoverTooltipPositioner.calculateTooltipPosition(
      markerRect,
      tooltipRect,
      zoom
   );

   assert.equal(position.x / zoom, anchorX - tooltipRect.width / 2);
   assert.equal(position.y / zoom, markerRect.top - tooltipRect.height - arrowSize);
   assert.equal(position.arrowLeft, tooltipRect.width / 2 - arrowSize);
   assert.equal(position.below, false);
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
   const arrowLeft = 12;
   const zoomText = '2';
   const installed = _withPageZoom(zoomText, {});
   const classes = [];
   installed.hoverTooltipEl.classList = {
      toggle(name, on) {
         classes.push([name, on]);
      },
   };
   installed.hoverTooltipEl.style.setProperty = (name, value) => {
      installed.hoverTooltipEl.style[name] = value;
   };

   HoverTooltipPositioner.applyTooltipPosition(installed.hoverTooltipEl, {
      x,
      y,
      below: true,
      arrowLeft,
   });

   assert.equal(installed.hoverTooltipEl.style.left, `${x / Number(zoomText)}px`);
   assert.equal(installed.hoverTooltipEl.style.top, `${y / Number(zoomText)}px`);
   assert.equal(installed.hoverTooltipEl.style['--hover-tooltip-arrow-left'], `${arrowLeft}px`);
   assert.deepEqual(classes, [['hover-tooltip-below', true]]);
   installed.restore();
});
