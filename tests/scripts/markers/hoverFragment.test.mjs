import assert from 'node:assert/strict';
import test from 'node:test';

import { HoverFragment } from '../../../scripts/markers/hoverFragment.js';

test('Test_CreateHoverTooltip_TestShowHideMove_ExpectVisibility', () => {
   globalThis.window = { ...(globalThis.window || {}), innerWidth: 500, innerHeight: 400 };
   const hoverTooltipEl = {
      style: { display: 'none' },
      textContent: '',
      getBoundingClientRect: () => ({ width: 60, height: 20 }),
   };
   const hover = HoverFragment.createHoverTooltip(hoverTooltipEl);

   hover.show('African Lion', { clientX: 50, clientY: 80 });
   assert.equal(hoverTooltipEl.textContent, 'African Lion');
   assert.equal(hoverTooltipEl.style.display, 'block');
   assert.match(hoverTooltipEl.style.left, /px$/);

   hover.hide();
   assert.equal(hoverTooltipEl.style.display, 'none');
});
