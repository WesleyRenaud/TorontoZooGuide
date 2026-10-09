import assert from 'node:assert/strict';
import test from 'node:test';

import { PastItineraryDateRecoverer } from '../../../../scripts/itinerary/pastItinerary/pastItineraryDateRecoverer.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_RecoverPastItineraryDate_TestMissingArgs_ExpectNull', () => {
   const args = {};

   const result = PastItineraryDateRecoverer.recoverPastItineraryDate(args);

   assert.equal(result, null);
});


test('Test_RecoverPastItineraryDate_TestMountOnly_ExpectNull', () => {
   const args = { mountEl: {} };

   const result = PastItineraryDateRecoverer.recoverPastItineraryDate(args);

   assert.equal(result, null);
});


test('Test_RecoverPastItineraryDate_TestFinish_ExpectSavesAndCompletes', async () => {
   const events = [];
   let capturedControllerOptions;
   const dateController = {
      show() {
         events.push('show');
      },
      hide() {
         events.push('hide');
      },
   };
   const mountId = 'mount';
   const earliestSelectableDate = '2026-09-10';
   const animal = { species: 'African Lion' };
   const selectedExhibits = ['Africa Savanna'];
   const itinerary = {
      animals: [animal],
      selectedExhibits,
   };

   const result = PastItineraryDateRecoverer.recoverPastItineraryDate({
      mountEl: { id: mountId },
      itinerary,
      earliestSelectableDate,
      onComplete: (saved) => {
         events.push(['complete', saved]);
      },
      onCancel: () => {
         events.push('cancel');
      },
      deps: {
         createDateController: (options) => {
            capturedControllerOptions = options;
            return dateController;
         },
         saveItineraryFn: async (draft, extras) => {
            events.push(['save', draft, extras]);
            return { ...draft, saved: true };
         },
         normalizeDraft: (itin) => ({ ...itin, normalized: true }),
         toIso: () => 'unused',
      },
   });

   assert.equal(result, dateController);
   assert.equal(events[Position.FIRST], 'show');
   assert.equal(capturedControllerOptions.mountEl.id, mountId);
   assert.equal(capturedControllerOptions.earliestSelectableDate, earliestSelectableDate);
   assert.equal(capturedControllerOptions.hideNextButton, true);
   assert.equal(capturedControllerOptions.titleText, Strings.itinerary.stale.recoveryTitle);

   capturedControllerOptions.onClose();

   assert.deepEqual(events.slice(1), ['hide', 'cancel']);

   events.length = 0;
   const finishDate = '2026-09-12';
   await capturedControllerOptions.onFinish(finishDate);

   assert.deepEqual(events, [
      [
         'save',
         {
            animals: [animal],
            selectedExhibits,
            normalized: true,
            date: finishDate,
         },
         { selectedExhibits },
      ],
      'hide',
      ['complete', {
         animals: [animal],
         selectedExhibits,
         normalized: true,
         date: finishDate,
         saved: true,
      }],
   ]);
});


test('Test_RecoverPastItineraryDate_TestSaveFails_ExpectNoComplete', async () => {
   const events = [];
   let capturedControllerOptions;
   const finishValue = { year: 2026 };

   PastItineraryDateRecoverer.recoverPastItineraryDate({
      mountEl: {},
      itinerary: { animals: [] },
      onComplete: () => {
         events.push('complete');
      },
      deps: {
         createDateController: (options) => {
            capturedControllerOptions = options;
            return {
               show() {},
               hide() {
                  events.push('hide');
               },
            };
         },
         saveItineraryFn: async () => null,
         normalizeDraft: (itin) => itin,
         toIso: (value) => `iso:${value}`,
      },
   });

   await capturedControllerOptions.onFinish(finishValue);

   assert.deepEqual(events, []);
});
