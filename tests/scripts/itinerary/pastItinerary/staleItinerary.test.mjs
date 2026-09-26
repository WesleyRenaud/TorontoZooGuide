import assert from 'node:assert/strict';
import { test, beforeEach } from 'node:test';

import { OfferPastItineraryClearOrRecoverer } from '../../../../scripts/itinerary/pastItinerary/offerPastItineraryClearOrRecoverer.js';
import { PastItineraryPromptTracker } from '../../../../scripts/itinerary/pastItinerary/pastItineraryPromptTracker.js';

import { makeNoonDate } from '../../helpers/visitDateMock.mjs';

const tomorrow = makeNoonDate(2026, 5, 16);

beforeEach(() => {
   PastItineraryPromptTracker.resetPastItineraryPromptSessionForTests();
});


test('Test_OfferPastItineraryClearOrRecovery_TestEmpty_ExpectNoPrompt', async () => {
   const itinerary = {
      date: '',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   };

   const pastDatePromptShown = await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
      itinerary,
      mountEl: { replaceChildren() {} },
      deps: {
         isVisitDateBeforeFloor: () => true,
      },
   });

   assert.equal(pastDatePromptShown, false);
});


test('Test_OfferPastItineraryClearOrRecovery_TestPastDate_ExpectPrompt', async () => {
   const calls = [];
   const mountEl = { replaceChildren() {} };
   const date = '2026-06-10';
   const recoveredDate = '2026-06-20';
   const animal = { species: 'Cheetah', exhibit: 'Africa Savanna' };
   const prompt = 'prompt';
   const recovery = 'recovery';
   const recovered = 'recovered';

   const pastDatePromptShown = await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
      itinerary: {
         date,
         animals: [animal],
      },
      mountEl,
      onCleared: () => calls.push('cleared'),
      onRecovered: () => calls.push(recovered),
      deps: {
         isVisitDateBeforeFloor: () => true,
         resolveEarliestVisitDate: async () => tomorrow,
         showChoicePrompt: ({ onRecover }) => {
            calls.push(prompt);
            onRecover();
         },
         recoverItineraryDate: ({ onComplete }) => {
            calls.push(recovery);
            onComplete({ date: recoveredDate });
         },
         clearItinerary: async () => {
            calls.push('clear');
         },
      },
   });

   assert.equal(pastDatePromptShown, true);
   assert.deepEqual(calls, [prompt, recovery, recovered]);
});


test('Test_OfferPastItineraryClearOrRecovery_TestChooseClear_ExpectCleared', async () => {
   const calls = [];
   const mountEl = { replaceChildren() {} };
   const date = '2026-06-10';
   const animal = { species: 'Cheetah', exhibit: 'Africa Savanna' };
   const clear = 'clear';
   const cleared = 'cleared';

   const pastDatePromptShown = await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
      itinerary: {
         date,
         animals: [animal],
      },
      mountEl,
      onCleared: () => calls.push(cleared),
      deps: {
         isVisitDateBeforeFloor: () => true,
         resolveEarliestVisitDate: async () => tomorrow,
         showChoicePrompt: ({ onClear }) => {
            onClear();
         },
         clearItinerary: async () => {
            calls.push(clear);
         },
      },
   });

   assert.equal(pastDatePromptShown, true);
   assert.deepEqual(calls, [clear, cleared]);
});


test('Test_OfferPastItineraryClearOrRecovery_TestCurrent_ExpectNoPrompt', async () => {
   const date = '2026-06-20';
   const animal = { species: 'Cheetah', exhibit: 'Africa Savanna' };

   const pastDatePromptShown = await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
      itinerary: {
         date,
         animals: [animal],
      },
      mountEl: { replaceChildren() {} },
      deps: {
         isVisitDateBeforeFloor: () => false,
      },
   });

   assert.equal(pastDatePromptShown, false);
});
