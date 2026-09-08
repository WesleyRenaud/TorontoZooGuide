import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryValidationResult } from '../../../scripts/itinerary/itineraryValidationResult.js';
import { ItineraryDiff } from '../../../scripts/itinerary/wizard/itineraryDiff.js';

test('Test_ApplyItineraryDiffToValidation_TestDiff_ExpectFlags', () => {
   const originalMerge = ItineraryDiff.mergeRemovedValidationState;
   ItineraryDiff.mergeRemovedValidationState = (existing, incoming) => ({
      ...existing,
      ...incoming,
   });

   try {
      const normalizedItinerary = {
         validation: {
            added: { animals: [] },
            removed: {},
            reducedVisibility: { animals: [] },
            improvedVisibility: { animals: [] },
            unscheduled: {},
            adjustments: [],
            hasChanges: false,
         },
      };

      ItineraryValidationResult.applyItineraryDiffToValidation(
         normalizedItinerary,
         {
            unscheduled: { animals: [{ species: 'Lion' }], attractions: [] },
            removed: { animals: [{ species: 'Tiger' }] },
         },
         { adjustments: [{ type: 'time' }] }
      );

      assert.deepEqual(normalizedItinerary.validation.unscheduled.animals, [{ species: 'Lion' }]);
      assert.deepEqual(normalizedItinerary.validation.removed.animals, [{ species: 'Tiger' }]);
      assert.equal(normalizedItinerary.validation.adjustments.length, 1);
      assert.equal(normalizedItinerary.validation.hasChanges, true);
   } finally {
      ItineraryDiff.mergeRemovedValidationState = originalMerge;
   }
});
