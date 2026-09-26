import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryValidationResult } from '../../../scripts/itinerary/itineraryValidationResult.js';
import { ItineraryDiff } from '../../../scripts/itinerary/wizard/itineraryDiff.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_ApplyItineraryDiffToValidation_TestDiff_ExpectFlags', () => {
   const originalMerge = ItineraryDiff.mergeRemovedValidationState;
   ItineraryDiff.mergeRemovedValidationState = (existing, incoming) => ({
      ...existing,
      ...incoming,
   });
   const unscheduledAnimal = { species: 'African Lion' };
   const removedAnimal = { species: 'Amur Tiger' };
   const adjustment = { type: 'time' };
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
   const diff = {
      unscheduled: { animals: [unscheduledAnimal], attractions: [] },
      removed: { animals: [removedAnimal] },
   };
   const extras = { adjustments: [adjustment] };

   try {
      ItineraryValidationResult.applyItineraryDiffToValidation(
         normalizedItinerary,
         diff,
         extras
      );

      assert.deepEqual(normalizedItinerary.validation.unscheduled.animals, [unscheduledAnimal]);
      assert.deepEqual(normalizedItinerary.validation.removed.animals, [removedAnimal]);
      assert.equal(normalizedItinerary.validation.adjustments[Position.FIRST], adjustment);
      assert.equal(normalizedItinerary.validation.hasChanges, true);
   } finally {
      ItineraryDiff.mergeRemovedValidationState = originalMerge;
   }
});
