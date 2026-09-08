import assert from 'node:assert/strict';
import test from 'node:test';

import { PastItineraryDateRecoverer } from '../../../../scripts/itinerary/pastItinerary/pastItineraryDateRecoverer.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_RecoverPastItineraryDate_TestMissingArgs_ExpectNull', () => {
   assert.equal(PastItineraryDateRecoverer.recoverPastItineraryDate({}), null);
   assert.equal(
      PastItineraryDateRecoverer.recoverPastItineraryDate({ mountEl: {} }),
      null
   );
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

   const result = PastItineraryDateRecoverer.recoverPastItineraryDate({
      mountEl: { id: 'mount' },
      itinerary: {
         animals: [{ species: 'Lion' }],
         selectedExhibits: ['Savanna'],
      },
      earliestSelectableDate: '2026-09-10',
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
   assert.equal(events[0], 'show');
   assert.equal(capturedControllerOptions.mountEl.id, 'mount');
   assert.equal(capturedControllerOptions.initialDate, '2026-09-10');
   assert.equal(capturedControllerOptions.hideNextButton, true);
   assert.equal(capturedControllerOptions.titleText, Strings.itinerary.stale.recoveryTitle);

   capturedControllerOptions.onClose();
   assert.deepEqual(events.slice(1), ['hide', 'cancel']);

   events.length = 0;
   await capturedControllerOptions.onFinish('2026-09-12');
   assert.deepEqual(events, [
      [
         'save',
         {
            animals: [{ species: 'Lion' }],
            selectedExhibits: ['Savanna'],
            normalized: true,
            date: '2026-09-12',
         },
         { selectedExhibits: ['Savanna'] },
      ],
      'hide',
      ['complete', {
         animals: [{ species: 'Lion' }],
         selectedExhibits: ['Savanna'],
         normalized: true,
         date: '2026-09-12',
         saved: true,
      }],
   ]);
});

test('Test_RecoverPastItineraryDate_TestSaveFails_ExpectNoComplete', async () => {
   const events = [];
   let capturedControllerOptions;

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

   await capturedControllerOptions.onFinish({ year: 2026 });
   assert.deepEqual(events, []);
});
