import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryValidationResult } from '../../../../scripts/itinerary/itineraryValidationResult.js';
import { ItineraryNormalizer } from '../../../../scripts/itinerary/itineraryNormalizer.js';
import { ItineraryShape } from '../../../../scripts/itinerary/itineraryShape.js';
import { ItineraryDiff } from '../../../../scripts/itinerary/wizard/itineraryDiff.js';
import { Summary } from '../../../../scripts/itinerary/wizard/diff/summary.js';

function draft(overrides = {}) {
   return ItineraryShape.normalizeItineraryDraft(overrides);
}

test('Test_BuildItineraryDiff_TestSeededRemoved_ExpectRemovedAttractionsAndEncounters', () => {
   const previous = draft({
      animals: [{ species: 'African Lion' }],
      attractions: [{ name: 'Conservation Carousel' }],
      guardiansTalks: [{ name: 'Amur Tiger' }],
      wildEncounters: [{ name: 'African Rainforest' }],
   });
   const validated = draft({
      animals: [{ species: ' african lion ' }],
      attractions: [{ name: 'Greenhouse' }],
      guardiansTalks: [{ name: 'Amur Tiger' }],
      wildEncounters: [],
   });

   const diff = ItineraryDiff.buildItineraryDiff(previous, validated, {}, { animalVisibilityChangeThreshold: 20 });

   assert.deepEqual(diff.removed.animals, []);
   assert.deepEqual(diff.removed.attractions, [{ name: 'Conservation Carousel' }]);
   assert.deepEqual(diff.removed.guardiansTalks, []);
   assert.deepEqual(diff.removed.wildEncounters, [{ name: 'African Rainforest' }]);
   assert.equal(Summary.hasRemovedItems(diff.removed), true);
});

test('Test_BuildItineraryDiff_TestBackendProvided_ExpectBackendRows', () => {
   const diff = ItineraryDiff.buildItineraryDiff(
      draft({
         animals: [{ species: 'African Lion' }],
         attractions: [{ name: 'Conservation Carousel' }],
      }),
      draft({
         animals: [{ species: 'African Lion' }],
         attractions: [{ name: 'Conservation Carousel' }],
      }),
      {
         attractions: [{ name: 'Conservation Carousel' }],
      },
      { animalVisibilityChangeThreshold: 20 }
   );

   assert.deepEqual(diff.removed.attractions, [{ name: 'Conservation Carousel' }]);
});

test('Test_BuildItineraryDiff_TestEmptyBackendTalks_ExpectInferredRemoved', () => {
   const previous = draft({
      guardiansTalks: [{ name: 'Only On Mondays' }],
   });
   const validated = draft();

   const diff = ItineraryDiff.buildItineraryDiff(previous, validated, draft(), {
      animalVisibilityChangeThreshold: 20,
   });

   assert.deepEqual(diff.removed.guardiansTalks, [{ name: 'Only On Mondays' }]);
   assert.equal(Summary.hasRemovedItems(diff.removed), true);
});

test('Test_BuildItineraryDiff_TestBackendTalkMerge_ExpectMerged', () => {
   const diff = ItineraryDiff.buildItineraryDiff(
      draft({
         guardiansTalks: [
            { name: 'Not On New Day Schedule' },
            { name: 'Cancelled On Schedule' },
         ],
      }),
      draft(),
      {
         guardiansTalks: [
            {
               name: 'Cancelled On Schedule',
               removalReason: 'Cancelled.',
            },
         ],
      },
      { animalVisibilityChangeThreshold: 20 }
   );

   assert.equal(diff.removed.guardiansTalks.length, 2);
   assert.ok(
      diff.removed.guardiansTalks.some(
         (t) => t.name === 'Cancelled On Schedule' && t.removalReason === 'Cancelled.'
      )
   );
   assert.ok(diff.removed.guardiansTalks.some((t) => t.name === 'Not On New Day Schedule'));
});

test('Test_BuildItineraryDiff_TestVisibilityDelta_ExpectReducedAndImproved', () => {
   const previous = draft({
      animals: [
         { species: 'African Lion', likelihood: 90 },
         { species: 'Amur Tiger', likelihood: 0.25 },
         { species: 'Snow Leopard', likelihood: 70 },
      ],
   });
   const validated = draft({
      animals: [
         { species: 'African Lion', likelihood: 60 },
         { species: 'Amur Tiger', likelihood: 0.7 },
         { species: 'Snow Leopard', likelihood: 55 },
      ],
   });

   const diff = ItineraryDiff.buildItineraryDiff(previous, validated, {}, { animalVisibilityChangeThreshold: 20 });

   assert.deepEqual(
      diff.reducedVisibility.animals.map((animal) => animal.species),
      ['African Lion']
   );
   assert.deepEqual(
      diff.improvedVisibility.animals.map((animal) => animal.species),
      ['Amur Tiger']
   );
   assert.equal(Summary.hasReducedVisibility(diff.reducedVisibility), true);
   assert.equal(Summary.hasImprovedVisibility(diff.improvedVisibility), true);
});

test('Test_BuildItineraryDiff_TestLostTimes_ExpectUnscheduled', () => {
   const diff = ItineraryDiff.buildItineraryDiff(
      draft({
         animals: [
            {
               species: 'African Lion',
               exhibit: 'Africa Savanna',
               start_time: '09:00',
               end_time: '09:08',
            },
         ],
         attractions: [
            {
               name: 'Conservation Carousel',
               start_time: '09:08',
               end_time: '09:16',
            },
         ],
      }),
      draft({
         animals: [
            {
               species: 'African Lion',
               exhibit: 'Africa Savanna',
               start_time: '',
               end_time: '',
            },
         ],
         attractions: [
            {
               name: 'Conservation Carousel',
               start_time: '',
               end_time: '',
            },
         ],
      }),
      {},
      { animalVisibilityChangeThreshold: 20 }
   );

   assert.deepEqual(
      diff.unscheduled.animals.map((animal) => animal.species),
      ['African Lion']
   );
   assert.deepEqual(
      diff.unscheduled.attractions.map((attraction) => attraction.name),
      ['Conservation Carousel']
   );
   assert.equal(Summary.hasUnscheduledItems(diff.unscheduled), true);
});

test('Test_BuildItineraryDiff_TestDeletedTalks_ExpectNotUnscheduled', () => {
   const diff = ItineraryDiff.buildItineraryDiff(
      draft({
         guardiansTalks: [
            {
               name: 'Spotted Hyena',
               start_time: '13:00',
               end_time: '13:30',
               location: 'Africa Savanna',
            },
         ],
      }),
      draft({
         guardiansTalks: [
            {
               name: 'Spotted Hyena',
               is_deleted: true,
               location: 'Africa Savanna',
            },
         ],
      }),
      {},
      { animalVisibilityChangeThreshold: 20 }
   );

   assert.equal(diff.unscheduled.guardiansTalks, undefined);
   assert.deepEqual(diff.removed.guardiansTalks, []);
});

test('Test_BuildItineraryDiff_TestDeletedEncounters_ExpectNotUnscheduled', () => {
   const diff = ItineraryDiff.buildItineraryDiff(
      draft({
         wildEncounters: [
            {
               name: 'African Rainforest',
               start_time: '13:00',
               end_time: '13:45',
            },
         ],
      }),
      draft({
         wildEncounters: [
            {
               name: 'African Rainforest',
               is_deleted: true,
            },
         ],
      }),
      {},
      { animalVisibilityChangeThreshold: 20 }
   );

   assert.equal(diff.unscheduled.wildEncounters, undefined);
   assert.deepEqual(diff.removed.wildEncounters, []);
});

test('Test_ApplyItineraryDiffToValidation_TestPriorRemoved_ExpectPreserved', () => {
   const previous = draft({
      date: '2026-06-21',
      guardiansTalks: [
         {
            name: 'Spotted Hyena',
            start_time: '13:00',
            end_time: '13:30',
            location: 'Africa Savanna',
         },
      ],
   });
   const validatedItinerary = ItineraryNormalizer.normalizeItinerary({
      date: '2026-06-22',
      guardiansTalks: [
         {
            name: 'Spotted Hyena',
            is_deleted: true,
            location: 'Africa Savanna',
         },
      ],
   });
   const diff = ItineraryDiff.buildItineraryDiff(
      previous,
      validatedItinerary,
      {},
      validatedItinerary.itineraryConfig ?? {}
   );

   ItineraryValidationResult.applyItineraryDiffToValidation(validatedItinerary, diff);

   assert.equal(validatedItinerary.validation.unscheduled.guardiansTalks, undefined);
   assert.deepEqual(
      validatedItinerary.validation.removed.guardiansTalks.map((talk) => talk.name),
      ['Spotted Hyena']
   );
   assert.equal(Summary.hasUnscheduledItems(validatedItinerary.validation.unscheduled), false);
   assert.equal(Summary.hasRemovedItems(validatedItinerary.validation.removed), true);
});

test('Test_BuildItineraryDiff_TestDroppedTalksEncounters_ExpectRemoved', () => {
   const diff = ItineraryDiff.buildItineraryDiff(
      draft({
         guardiansTalks: [
            {
               name: 'African Lion',
               start_time: '16:30',
               end_time: '16:45',
            },
         ],
         wildEncounters: [
            {
               name: 'African Rainforest',
               start_time: '16:30',
               end_time: '16:45',
            },
         ],
      }),
      draft(),
      {},
      { animalVisibilityChangeThreshold: 20 }
   );

   assert.deepEqual(
      diff.removed.guardiansTalks.map((talk) => talk.name),
      ['African Lion']
   );
   assert.deepEqual(
      diff.removed.wildEncounters.map((encounter) => encounter.name),
      ['African Rainforest']
   );
   assert.equal(Summary.hasRemovedItems(diff.removed), true);
   assert.equal(Summary.hasUnscheduledItems(diff.unscheduled), false);
});

test('Test_BuildItineraryDiff_TestMatchingAttraction_ExpectTransportKept', () => {
   const previous = draft({
      attractions: [{ name: 'Zoomobile', addedAsAttraction: true }],
   });
   const validated = draft({
      transportations: [{
         name: 'Zoomobile',
         added_as_attraction: true,
      }],
   });

   const diff = ItineraryDiff.buildItineraryDiff(previous, validated);

   assert.deepEqual(diff.removed.attractions, []);
   assert.equal(Summary.hasRemovedItems(diff.removed), false);
   assert.equal(Summary.isValidatedItineraryEmpty(validated), false);
});

test('Test_BuildItineraryDiff_TestTransportOnly_ExpectAttractionRemoved', () => {
   const previous = draft({
      attractions: [{ name: 'Zoomobile', addedAsAttraction: true }],
   });
   const validated = draft({
      transportations: [{
         name: 'Zoomobile',
         added_as_attraction: false,
      }],
   });

   const diff = ItineraryDiff.buildItineraryDiff(previous, validated);

   assert.deepEqual(diff.removed.attractions, [{ name: 'Zoomobile', addedAsAttraction: true }]);
   assert.equal(Summary.hasRemovedItems(diff.removed), true);
});

test('Test_SummaryHelpers_TestEmptyResults_ExpectSafeDefaults', () => {
   assert.equal(Summary.isValidatedItineraryEmpty(null), true);
   assert.equal(Summary.isValidatedItineraryEmpty(draft()), true);
   assert.equal(Summary.isValidatedItineraryEmpty(draft({
      animals: [{ species: 'African Lion' }],
   })), false);
   assert.equal(Summary.isValidatedItineraryEmpty(draft({
      transportations: [{ name: 'Zoomobile' }],
   })), false);
   assert.equal(Summary.hasRemovedItems(null), false);
   assert.equal(Summary.hasUnscheduledItems(null), false);
   assert.equal(Summary.hasReducedVisibility({ animals: [] }), false);
   assert.equal(Summary.hasImprovedVisibility({ animals: [] }), false);
});
