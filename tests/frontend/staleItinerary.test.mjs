import assert from 'node:assert/strict';
import { test, beforeEach } from 'node:test';

import { offerPastItineraryClearOrRecovery } from '../../scripts/itinerary/pastItinerary/offerPastItineraryClearOrRecovery.js';
import { resetPastItineraryPromptSessionForTests } from '../../scripts/itinerary/pastItinerary/promptSession.js';

import { makeNoonDate } from './helpers/visitDateMock.mjs';

const tomorrow = makeNoonDate(2026, 5, 16);

beforeEach(() => {
   resetPastItineraryPromptSessionForTests();
});

test('offerPastItineraryClearOrRecovery does nothing for empty itineraries', async () => {
   const pastDatePromptShown = await offerPastItineraryClearOrRecovery({
      itinerary: {
         date: '',
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
      },
      mountEl: { replaceChildren() {} },
      deps: {
         isVisitDateBeforeFloor: () => true,
      },
   });

   assert.equal(pastDatePromptShown, false);
});

test('offerPastItineraryClearOrRecovery prompts when the saved visit date is in the past', async () => {
   const calls = [];
   const mountEl = { replaceChildren() {} };

   const pastDatePromptShown = await offerPastItineraryClearOrRecovery({
      itinerary: {
         date: '2026-06-10',
         animals: [{ species: 'Cheetah', exhibit: 'Africa Savanna' }],
      },
      mountEl,
      onCleared: () => calls.push('cleared'),
      onRecovered: () => calls.push('recovered'),
      deps: {
         isVisitDateBeforeFloor: () => true,
         resolveEarliestVisitDate: async () => tomorrow,
         showChoicePrompt: ({ onRecover }) => {
            calls.push('prompt');
            onRecover();
         },
         recoverItineraryDate: ({ onComplete }) => {
            calls.push('recovery');
            onComplete({ date: '2026-06-20' });
         },
         clearItinerary: async () => {
            calls.push('clear');
         },
      },
   });

   assert.equal(pastDatePromptShown, true);
   assert.deepEqual(calls, ['prompt', 'recovery', 'recovered']);
});

test('offerPastItineraryClearOrRecovery clears when the visitor chooses clear', async () => {
   const calls = [];
   const mountEl = { replaceChildren() {} };

   const pastDatePromptShown = await offerPastItineraryClearOrRecovery({
      itinerary: {
         date: '2026-06-10',
         animals: [{ species: 'Cheetah', exhibit: 'Africa Savanna' }],
      },
      mountEl,
      onCleared: () => calls.push('cleared'),
      deps: {
         isVisitDateBeforeFloor: () => true,
         resolveEarliestVisitDate: async () => tomorrow,
         showChoicePrompt: ({ onClear }) => {
            onClear();
         },
         clearItinerary: async () => {
            calls.push('clear');
         },
      },
   });

   assert.equal(pastDatePromptShown, true);
   assert.deepEqual(calls, ['clear', 'cleared']);
});

test('offerPastItineraryClearOrRecovery does nothing for current itineraries', async () => {
   const pastDatePromptShown = await offerPastItineraryClearOrRecovery({
      itinerary: {
         date: '2026-06-20',
         animals: [{ species: 'Cheetah', exhibit: 'Africa Savanna' }],
      },
      mountEl: { replaceChildren() {} },
      deps: {
         isVisitDateBeforeFloor: () => false,
      },
   });

   assert.equal(pastDatePromptShown, false);
});
