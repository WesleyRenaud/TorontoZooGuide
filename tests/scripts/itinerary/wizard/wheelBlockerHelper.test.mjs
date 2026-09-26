import assert from 'node:assert/strict';
import test from 'node:test';

import { WheelBlockerHelper } from '../../../../scripts/itinerary/wizard/wheelBlockerHelper.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_IsScrollable_TestOverflowAndHeight_ExpectTrue', () => {
   const el = document.createElement('div');
   el.scrollHeight = 200;
   el.clientHeight = 100;
   const original = window.getComputedStyle;
   window.getComputedStyle = () => ({ overflowY: 'auto' });
   globalThis.getComputedStyle = window.getComputedStyle;

   try {
      const isScrollable = WheelBlockerHelper.isScrollable(el);

      assert.equal(isScrollable, true);
   } finally {
      window.getComputedStyle = original;
      globalThis.getComputedStyle = original;
   }
});


test('Test_IsScrollable_TestNull_ExpectFalse', () => {
   const el = null;

   const isScrollable = WheelBlockerHelper.isScrollable(el);

   assert.equal(isScrollable, false);
});


test('Test_FindScrollableAncestor_TestTree_ExpectAncestor', () => {
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
      const ancestor = WheelBlockerHelper.findScrollableAncestor(child, stopEl);

      assert.equal(ancestor, scrollable);
   } finally {
      window.getComputedStyle = original;
      globalThis.getComputedStyle = original;
   }
});


test('Test_FindScrollableAncestor_TestStopEl_ExpectNull', () => {
   const stopEl = document.createElement('div');
   const original = window.getComputedStyle;
   window.getComputedStyle = () => ({ overflowY: 'visible' });
   globalThis.getComputedStyle = window.getComputedStyle;

   try {
      const ancestor = WheelBlockerHelper.findScrollableAncestor(stopEl, stopEl);

      assert.equal(ancestor, null);
   } finally {
      window.getComputedStyle = original;
      globalThis.getComputedStyle = original;
   }
});
