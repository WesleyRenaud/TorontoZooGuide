import assert from 'node:assert/strict';
import test from 'node:test';

import { ShowPastItineraryChoiceFragment } from '../../../../scripts/itinerary/pastItinerary/showPastItineraryChoiceFragment.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_ShowPastItineraryChoicePrompt_TestMissingMount_ExpectNoOp', () => {
   const calls = [];
   ShowPastItineraryChoiceFragment.showPastItineraryChoicePrompt({
      mountEl: null,
      deps: {
         showConfirmPopup: (args) => { calls.push(args); },
      },
   });
   assert.deepEqual(calls, []);
});

test('Test_ShowPastItineraryChoicePrompt_TestActions_ExpectClearAndRecover', () => {
   const calls = [];
   const clears = [];
   const recovers = [];
   const mountEl = { id: 'mount' };

   ShowPastItineraryChoiceFragment.showPastItineraryChoicePrompt({
      mountEl,
      onClear: () => { clears.push(true); },
      onRecover: () => { recovers.push(true); },
      deps: {
         showConfirmPopup: (args) => { calls.push(args); },
      },
   });

   assert.equal(calls.length, 1);
   assert.equal(calls[0].mountEl, mountEl);
   assert.equal(calls[0].title, Strings.itinerary.stale.title);
   assert.equal(calls[0].cancelText, Strings.itinerary.actions.clear);
   assert.equal(calls[0].confirmText, Strings.itinerary.stale.recover);
   calls[0].onCancel();
   calls[0].onConfirm();
   assert.deepEqual(clears, [true]);
   assert.deepEqual(recovers, [true]);
});
