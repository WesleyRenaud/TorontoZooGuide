import assert from 'node:assert/strict';
import test from 'node:test';

import { OfferPastItineraryClearOrRecoverer } from '../../../../scripts/itinerary/pastItinerary/offerPastItineraryClearOrRecoverer.js';

test('Test_OfferPastItineraryClearOrRecovery_TestNoMount_ExpectFalse', async () => {
   assert.equal(
      await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
         itinerary: { animals: [{ species: 'Lion' }] },
      }),
      false
   );
});

test('Test_OfferPastItineraryClearOrRecovery_TestPromptAlreadyOpen_ExpectTrue', async () => {
   assert.equal(
      await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
         mountEl: {},
         itinerary: { animals: [{ species: 'Lion' }] },
         deps: {
            isPromptOpen: () => true,
         },
      }),
      true
   );
});

test('Test_OfferPastItineraryClearOrRecovery_TestNoContent_ExpectFalse', async () => {
   assert.equal(
      await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
         mountEl: {},
         itinerary: { animals: [] },
         deps: {
            isPromptOpen: () => false,
            hasContent: () => false,
         },
      }),
      false
   );
});

test('Test_OfferPastItineraryClearOrRecovery_TestDateStillValid_ExpectFalse', async () => {
   assert.equal(
      await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
         mountEl: {},
         itinerary: {
            date: '2026-09-20',
            animals: [{ species: 'Lion' }],
         },
         deps: {
            isPromptOpen: () => false,
            hasContent: () => true,
            resolveEarliestVisitDate: async () => '2026-09-08',
            isVisitDateBeforeFloor: () => false,
         },
      }),
      false
   );
});

test('Test_OfferPastItineraryClearOrRecovery_TestClearPath_ExpectCleared', async () => {
   const events = [];
   const promptFlags = [];

   const shown = await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
      mountEl: { id: 'mount' },
      itinerary: {
         date: '2026-01-01',
         animals: [{ species: 'Lion' }],
      },
      onCleared: () => {
         events.push('cleared');
      },
      deps: {
         isPromptOpen: () => false,
         setPromptOpen: (value) => {
            promptFlags.push(value);
         },
         hasContent: () => true,
         resolveEarliestVisitDate: async () => '2026-09-08',
         isVisitDateBeforeFloor: () => true,
         showChoicePrompt: ({ onClear }) => {
            events.push('prompt');
            onClear();
         },
         clearItinerary: async () => {
            events.push('clear');
         },
      },
   });

   assert.equal(shown, true);
   assert.deepEqual(promptFlags, [true, false]);
   assert.deepEqual(events, ['prompt', 'clear', 'cleared']);
});

test('Test_OfferPastItineraryClearOrRecovery_TestRecoverPath_ExpectRecovered', async () => {
   const events = [];
   const promptFlags = [];
   let recoverOptions;
   let promptCount = 0;

   const shown = await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
      mountEl: { id: 'mount' },
      itinerary: {
         date: '2026-01-01',
         animals: [{ species: 'Lion' }],
      },
      onRecovered: (itin) => {
         events.push(['recovered', itin]);
      },
      deps: {
         isPromptOpen: () => false,
         setPromptOpen: (value) => {
            promptFlags.push(value);
         },
         hasContent: () => true,
         resolveEarliestVisitDate: async () => '2026-09-08',
         isVisitDateBeforeFloor: () => true,
         showChoicePrompt: ({ onRecover }) => {
            events.push('prompt');
            promptCount += 1;
            if (promptCount === 1) {
               onRecover();
            }
         },
         recoverItineraryDate: (options) => {
            recoverOptions = options;
            events.push('recover');
            options.onComplete({ date: '2026-09-10' });
         },
      },
   });

   assert.equal(shown, true);
   assert.equal(recoverOptions.earliestSelectableDate, '2026-09-08');
   assert.deepEqual(promptFlags, [true, false]);
   assert.deepEqual(events, ['prompt', 'recover', ['recovered', { date: '2026-09-10' }]]);

   events.length = 0;
   recoverOptions.onCancel();
   assert.deepEqual(events, ['prompt']);
});