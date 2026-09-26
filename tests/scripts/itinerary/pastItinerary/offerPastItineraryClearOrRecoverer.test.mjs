import assert from 'node:assert/strict';
import test from 'node:test';

import { OfferPastItineraryClearOrRecoverer } from '../../../../scripts/itinerary/pastItinerary/offerPastItineraryClearOrRecoverer.js';


test('Test_OfferPastItineraryClearOrRecovery_TestNoMount_ExpectFalse', async () => {
   const itinerary = { animals: [{ species: 'Lion' }] };

   const shown = await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
      itinerary,
   });

   assert.equal(shown, false);
});


test('Test_OfferPastItineraryClearOrRecovery_TestPromptAlreadyOpen_ExpectTrue', async () => {
   const mountEl = {};
   const itinerary = { animals: [{ species: 'Lion' }] };

   const shown = await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
      mountEl,
      itinerary,
      deps: {
         isPromptOpen: () => true,
      },
   });

   assert.equal(shown, true);
});


test('Test_OfferPastItineraryClearOrRecovery_TestNoContent_ExpectFalse', async () => {
   const mountEl = {};
   const itinerary = { animals: [] };

   const shown = await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
      mountEl,
      itinerary,
      deps: {
         isPromptOpen: () => false,
         hasContent: () => false,
      },
   });

   assert.equal(shown, false);
});


test('Test_OfferPastItineraryClearOrRecovery_TestDateStillValid_ExpectFalse', async () => {
   const mountEl = {};
   const visitDate = '2026-09-20';
   const earliestSelectableDate = '2026-09-08';
   const itinerary = {
      date: visitDate,
      animals: [{ species: 'Lion' }],
   };

   const shown = await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
      mountEl,
      itinerary,
      deps: {
         isPromptOpen: () => false,
         hasContent: () => true,
         resolveEarliestVisitDate: async () => earliestSelectableDate,
         isVisitDateBeforeFloor: () => false,
      },
   });

   assert.equal(shown, false);
});


test('Test_OfferPastItineraryClearOrRecovery_TestClearPath_ExpectCleared', async () => {
   const events = [];
   const promptFlags = [];
   const prompt = 'prompt';
   const clear = 'clear';
   const cleared = 'cleared';
   const promptOpened = true;
   const promptClosed = false;
   const visitDate = '2026-01-01';
   const earliestSelectableDate = '2026-09-08';
   const animal = { species: 'Lion' };
   const mountEl = { id: 'mount' };

   const shown = await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
      mountEl,
      itinerary: {
         date: visitDate,
         animals: [animal],
      },
      onCleared: () => {
         events.push(cleared);
      },
      deps: {
         isPromptOpen: () => false,
         setPromptOpen: (value) => {
            promptFlags.push(value);
         },
         hasContent: () => true,
         resolveEarliestVisitDate: async () => earliestSelectableDate,
         isVisitDateBeforeFloor: () => true,
         showChoicePrompt: ({ onClear }) => {
            events.push(prompt);
            onClear();
         },
         clearItinerary: async () => {
            events.push(clear);
         },
      },
   });

   assert.equal(shown, true);
   assert.deepEqual(promptFlags, [promptOpened, promptClosed]);
   assert.deepEqual(events, [prompt, clear, cleared]);
});


test('Test_OfferPastItineraryClearOrRecovery_TestRecoverPath_ExpectRecovered', async () => {
   const events = [];
   const promptFlags = [];
   const prompt = 'prompt';
   const recover = 'recover';
   const recovered = 'recovered';
   const promptOpened = true;
   const promptClosed = false;
   const visitDate = '2026-01-01';
   const earliestSelectableDate = '2026-09-08';
   const recoveredDate = '2026-09-10';
   const recoveredItinerary = { date: recoveredDate };
   const animal = { species: 'Lion' };
   const mountEl = { id: 'mount' };
   let recoverOptions;

   const shown = await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
      mountEl,
      itinerary: {
         date: visitDate,
         animals: [animal],
      },
      onRecovered: (itin) => {
         events.push([recovered, itin]);
      },
      deps: {
         isPromptOpen: () => false,
         setPromptOpen: (value) => {
            promptFlags.push(value);
         },
         hasContent: () => true,
         resolveEarliestVisitDate: async () => earliestSelectableDate,
         isVisitDateBeforeFloor: () => true,
         showChoicePrompt: ({ onRecover }) => {
            events.push(prompt);
            onRecover();
         },
         recoverItineraryDate: (options) => {
            recoverOptions = options;
            events.push(recover);
            options.onComplete(recoveredItinerary);
         },
      },
   });

   assert.equal(shown, true);
   assert.equal(recoverOptions.earliestSelectableDate, earliestSelectableDate);
   assert.deepEqual(promptFlags, [promptOpened, promptClosed]);
   assert.deepEqual(events, [prompt, recover, [recovered, recoveredItinerary]]);
});


test('Test_OfferPastItineraryClearOrRecovery_TestRecoverCancel_ExpectPromptAgain', async () => {
   const events = [];
   const prompt = 'prompt';
   const visitDate = '2026-01-01';
   const earliestSelectableDate = '2026-09-08';
   const animal = { species: 'Lion' };
   const mountEl = { id: 'mount' };
   let recoverOptions;
   let shouldRecover = true;

   const shown = await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
      mountEl,
      itinerary: {
         date: visitDate,
         animals: [animal],
      },
      deps: {
         isPromptOpen: () => false,
         setPromptOpen: () => {},
         hasContent: () => true,
         resolveEarliestVisitDate: async () => earliestSelectableDate,
         isVisitDateBeforeFloor: () => true,
         showChoicePrompt: ({ onRecover }) => {
            events.push(prompt);
            if (shouldRecover) {
               shouldRecover = false;
               onRecover();
            }
         },
         recoverItineraryDate: (options) => {
            recoverOptions = options;
         },
      },
   });

   recoverOptions.onCancel();

   assert.equal(shown, true);
   assert.deepEqual(events, [prompt, prompt]);
});
