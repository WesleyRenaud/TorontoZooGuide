import assert from 'node:assert/strict';
import test from 'node:test';

import { applyItineraryDiffToValidation } from '../../scripts/itinerary/itineraryValidationResult.js';
import { ItineraryNormalizer } from '../../scripts/itinerary/itineraryNormalizer.js';
import { normalizeItineraryDraft } from '../../scripts/itinerary/itineraryShape.js';
import {
   buildItineraryDiff,
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
   hasUnscheduledItems,
   isValidatedItineraryEmpty,
} from '../../scripts/itinerary/wizard/itineraryDiff.js';

function draft(overrides = {}) {
   return normalizeItineraryDraft(overrides);
}

test('reports seeded itinerary items removed during validation', () => {
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

   const diff = buildItineraryDiff(previous, validated, {}, { animalVisibilityChangeThreshold: 20 });

   assert.deepEqual(diff.removed.animals, []);
   assert.deepEqual(diff.removed.attractions, [{ name: 'Conservation Carousel' }]);
   assert.deepEqual(diff.removed.guardiansTalks, []);
   assert.deepEqual(diff.removed.wildEncounters, [{ name: 'African Rainforest' }]);
   assert.equal(hasRemovedItems(diff.removed), true);
});

test('uses backend removed items when validation already provides them', () => {
   const diff = buildItineraryDiff(
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

test('infers guardians talks removed when backend sends empty removed but previous had them', () => {
   const previous = draft({
      guardiansTalks: [{ name: 'Only On Mondays' }],
   });
   const validated = draft();

   const diff = buildItineraryDiff(previous, validated, draft(), {
      animalVisibilityChangeThreshold: 20,
   });

   assert.deepEqual(diff.removed.guardiansTalks, [{ name: 'Only On Mondays' }]);
   assert.equal(hasRemovedItems(diff.removed), true);
});

test('merges backend removed guardians talks with items missing from validated', () => {
   const diff = buildItineraryDiff(
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

test('reports meaningful animal visibility changes after date validation', () => {
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

   const diff = buildItineraryDiff(previous, validated, {}, { animalVisibilityChangeThreshold: 20 });

   assert.deepEqual(
      diff.reducedVisibility.animals.map((animal) => animal.species),
      ['African Lion']
   );
   assert.deepEqual(
      diff.improvedVisibility.animals.map((animal) => animal.species),
      ['Amur Tiger']
   );
   assert.equal(hasReducedVisibility(diff.reducedVisibility), true);
   assert.equal(hasImprovedVisibility(diff.improvedVisibility), true);
});

test('reports items unscheduled during validation', () => {
   const diff = buildItineraryDiff(
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
   assert.equal(hasUnscheduledItems(diff.unscheduled), true);
});

test('does not list deleted guardians talks as unscheduled when date removes schedule', () => {
   const diff = buildItineraryDiff(
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

test('does not list deleted wild encounters as unscheduled when date removes schedule', () => {
   const diff = buildItineraryDiff(
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

test('date change validation lists deleted guardians talk only once in removed', () => {
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
   const diff = buildItineraryDiff(
      previous,
      validatedItinerary,
      {},
      validatedItinerary.itineraryConfig ?? {}
   );

   applyItineraryDiffToValidation(validatedItinerary, diff);

   assert.equal(validatedItinerary.validation.unscheduled.guardiansTalks, undefined);
   assert.deepEqual(
      validatedItinerary.validation.removed.guardiansTalks.map((talk) => talk.name),
      ['Spotted Hyena']
   );
   assert.equal(hasUnscheduledItems(validatedItinerary.validation.unscheduled), false);
   assert.equal(hasRemovedItems(validatedItinerary.validation.removed), true);
});

test('reports guardians talks and wild encounters removed when dropped from validated', () => {
   const diff = buildItineraryDiff(
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
   assert.equal(hasRemovedItems(diff.removed), true);
   assert.equal(hasUnscheduledItems(diff.unscheduled), false);
});

test('does not treat also-transportation attractions as removed after save', () => {
   const previous = draft({
      attractions: [{ name: 'Zoomobile', addedAsAttraction: true }],
   });
   const validated = draft({
      transportations: [{
         name: 'Zoomobile',
         added_as_attraction: true,
      }],
   });

   const diff = buildItineraryDiff(previous, validated);

   assert.deepEqual(diff.removed.attractions, []);
   assert.equal(hasRemovedItems(diff.removed), false);
   assert.equal(isValidatedItineraryEmpty(validated), false);
});

test('still treats also-transportation attractions as removed when saved as transportation only', () => {
   const previous = draft({
      attractions: [{ name: 'Zoomobile', addedAsAttraction: true }],
   });
   const validated = draft({
      transportations: [{
         name: 'Zoomobile',
         added_as_attraction: false,
      }],
   });

   const diff = buildItineraryDiff(previous, validated);

   assert.deepEqual(diff.removed.attractions, [{ name: 'Zoomobile', addedAsAttraction: true }]);
   assert.equal(hasRemovedItems(diff.removed), true);
});

test('summary helpers handle empty validation results', () => {
   assert.equal(isValidatedItineraryEmpty(null), true);
   assert.equal(isValidatedItineraryEmpty(draft()), true);
   assert.equal(isValidatedItineraryEmpty(draft({
      animals: [{ species: 'African Lion' }],
   })), false);
   assert.equal(isValidatedItineraryEmpty(draft({
      transportations: [{ name: 'Zoomobile' }],
   })), false);
   assert.equal(hasRemovedItems(null), false);
   assert.equal(hasUnscheduledItems(null), false);
   assert.equal(hasReducedVisibility({ animals: [] }), false);
   assert.equal(hasImprovedVisibility({ animals: [] }), false);
});
