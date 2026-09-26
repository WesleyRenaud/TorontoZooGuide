import assert from 'node:assert/strict';
import test from 'node:test';

import { ShowPastItineraryChoiceFragment } from '../../../../scripts/itinerary/pastItinerary/showPastItineraryChoiceFragment.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_ShowPastItineraryChoicePrompt_TestMissingMount_ExpectNoOp', () => {
   const calls = [];
   const mountEl = null;

   ShowPastItineraryChoiceFragment.showPastItineraryChoicePrompt({
      mountEl,
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
   assert.equal(calls[Position.FIRST].mountEl, mountEl);
   assert.equal(calls[Position.FIRST].title, Strings.itinerary.stale.title);
   assert.equal(calls[Position.FIRST].cancelText, Strings.itinerary.actions.clear);
   assert.equal(calls[Position.FIRST].confirmText, Strings.itinerary.stale.recover);

   calls[Position.FIRST].onCancel();
   calls[Position.FIRST].onConfirm();

   assert.deepEqual(clears, [true]);
   assert.deepEqual(recovers, [true]);
});
