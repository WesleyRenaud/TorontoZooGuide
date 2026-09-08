import assert from 'node:assert/strict';
import test from 'node:test';

import { WheelBlockerHelper } from '../../../../scripts/itinerary/wizard/wheelBlockerHelper.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_IsScrollable_TestOverflowAndHeight_ExpectBoolean', () => {
   const el = document.createElement('div');
   el.scrollHeight = 200;
   el.clientHeight = 100;

   const original = window.getComputedStyle;
   window.getComputedStyle = () => ({ overflowY: 'auto' });
   globalThis.getComputedStyle = window.getComputedStyle;

   try {
      assert.equal(WheelBlockerHelper.isScrollable(el), true);
      assert.equal(WheelBlockerHelper.isScrollable(null), false);
   } finally {
      window.getComputedStyle = original;
      globalThis.getComputedStyle = original;
   }
});

test('Test_FindScrollableAncestor_TestTree_ExpectAncestorOrNull', () => {
   const stopEl = document.createElement('div');
   const scrollable = document.createElement('div');
   const child = document.createElement('div');
   scrollable.scrollHeight = 200;
   scrollable.clientHeight = 50;
   stopEl.appendChild(scrollable);
   scrollable.appendChild(child);

   const original = window.getComputedStyle;
   window.getComputedStyle = (element) => ({
      overflowY: element === scrollable ? 'scroll' : 'visible',
   });
   globalThis.getComputedStyle = window.getComputedStyle;

   try {
      assert.equal(WheelBlockerHelper.findScrollableAncestor(child, stopEl), scrollable);
      assert.equal(WheelBlockerHelper.findScrollableAncestor(stopEl, stopEl), null);
   } finally {
      window.getComputedStyle = original;
      globalThis.getComputedStyle = original;
   }
});
