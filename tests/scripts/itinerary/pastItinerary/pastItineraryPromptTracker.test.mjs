import assert from 'node:assert/strict';
import test from 'node:test';

import { PastItineraryPromptTracker } from '../../../../scripts/itinerary/pastItinerary/pastItineraryPromptTracker.js';

test('Test_PastItineraryPromptTracker_TestOpenFlag_ExpectToggled', () => {
   PastItineraryPromptTracker.resetPastItineraryPromptSessionForTests();
   assert.equal(PastItineraryPromptTracker.isPastItineraryPromptOpen(), false);

   PastItineraryPromptTracker.setPastItineraryPromptOpen(true);
   assert.equal(PastItineraryPromptTracker.isPastItineraryPromptOpen(), true);

   PastItineraryPromptTracker.resetPastItineraryPromptSessionForTests();
   assert.equal(PastItineraryPromptTracker.isPastItineraryPromptOpen(), false);
});
