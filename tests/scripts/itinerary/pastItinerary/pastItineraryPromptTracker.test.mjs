import assert from 'node:assert/strict';
import test from 'node:test';

import { PastItineraryPromptTracker } from '../../../../scripts/itinerary/pastItinerary/pastItineraryPromptTracker.js';


test('Test_IsPastItineraryPromptOpen_TestReset_ExpectClosed', () => {
   PastItineraryPromptTracker.resetPastItineraryPromptSessionForTests();

   const isOpen = PastItineraryPromptTracker.isPastItineraryPromptOpen();

   assert.equal(isOpen, false);
});


test('Test_SetPastItineraryPromptOpen_TestTrue_ExpectOpen', () => {
   PastItineraryPromptTracker.resetPastItineraryPromptSessionForTests();
   const isOpen = true;

   PastItineraryPromptTracker.setPastItineraryPromptOpen(isOpen);
   const isOpenAfterSet = PastItineraryPromptTracker.isPastItineraryPromptOpen();

   assert.equal(isOpenAfterSet, isOpen);
});


test('Test_ResetPastItineraryPromptSessionForTests_TestAfterOpen_ExpectClosed', () => {
   PastItineraryPromptTracker.resetPastItineraryPromptSessionForTests();
   PastItineraryPromptTracker.setPastItineraryPromptOpen(true);

   PastItineraryPromptTracker.resetPastItineraryPromptSessionForTests();
   const isOpen = PastItineraryPromptTracker.isPastItineraryPromptOpen();

   assert.equal(isOpen, false);
});
