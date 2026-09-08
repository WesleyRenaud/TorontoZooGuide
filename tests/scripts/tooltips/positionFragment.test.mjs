import assert from 'node:assert/strict';
import test from 'node:test';

import { PositionFragment } from '../../../scripts/tooltips/positionFragment.js';

test('Test_PositionTooltip_TestRects_ExpectClampedStyle', () => {
   const tooltipEl = {
      style: {},
      offsetParent: null,
      parentElement: {
         getBoundingClientRect: () => ({ left: 0, top: 0, width: 400, height: 300 }),
      },
      getBoundingClientRect: () => ({ width: 100, height: 50, left: 0, top: 0, bottom: 50 }),
   };
   const markerEl = {
      getBoundingClientRect: () => ({ left: 100, top: 80, width: 20, height: 20, bottom: 100 }),
   };

   PositionFragment.positionTooltip(tooltipEl, markerEl);
   assert.match(tooltipEl.style.left, /px$/);
   assert.match(tooltipEl.style.top, /px$/);
});

test('Test_PositionTooltip_TestNearTop_ExpectFlipsBelow', () => {
   const tooltipEl = {
      style: {},
      offsetParent: null,
      parentElement: {
         getBoundingClientRect: () => ({ left: 0, top: 0, width: 400, height: 300 }),
      },
      getBoundingClientRect: () => ({ width: 100, height: 50, left: 0, top: 0, bottom: 50 }),
   };
   const markerEl = {
      getBoundingClientRect: () => ({ left: 100, top: 10, width: 20, height: 20, bottom: 30 }),
   };

   PositionFragment.positionTooltip(tooltipEl, markerEl);
   assert.ok(Number.parseFloat(tooltipEl.style.top) >= 12);
});
