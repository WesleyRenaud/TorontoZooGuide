import assert from 'node:assert/strict';
import test from 'node:test';

import {
   buildItineraryDiff,
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
   hasUnscheduledItems,
   isValidatedItineraryEmpty,
} from '../../scripts/itinerary/wizard/itineraryDiff.js';

test('reports seeded itinerary items removed during validation', () => {
   const previous = {
      animals: [{ species: 'African Lion' }],
      attractions: [{ name: 'Conservation Carousel' }],
      guardiansTalks: [{ name: 'Amur Tiger' }],
      wildEncounters: [{ name: 'African Rainforest' }],
   };
   const validated = {
      animals: [{ species: ' african lion ' }],
      attractions: [{ name: 'Greenhouse' }],
      guardiansTalks: [{ name: 'Amur Tiger' }],
      wildEncounters: [],
   };

   const diff = buildItineraryDiff(previous, validated, {}, { animalVisibilityChangeThreshold: 20 });

   assert.deepEqual(diff.removed.animals, []);
   assert.deepEqual(diff.removed.attractions, [{ name: 'Conservation Carousel' }]);
   assert.deepEqual(diff.removed.guardiansTalks, []);
   assert.deepEqual(diff.removed.wildEncounters, [{ name: 'African Rainforest' }]);
   assert.equal(hasRemovedItems(diff.removed), true);
});

test('uses backend removed items when validation already provides them', () => {
   const diff = buildItineraryDiff(
      {
         animals: [{ species: 'African Lion' }],
         attractions: [{ name: 'Conservation Carousel' }],
      },
      {
         animals: [{ species: 'African Lion' }],
         attractions: [{ name: 'Conservation Carousel' }],
      },
      {
         attractions: [{ name: 'Conservation Carousel' }],
      },
      { animalVisibilityChangeThreshold: 20 }
   );

   assert.deepEqual(diff.removed.attractions, [{ name: 'Conservation Carousel' }]);
});

test('infers guardians talks removed when backend sends empty removed but previous had them', () => {
   const previous = {
      animals: [],
      attractions: [],
      guardiansTalks: [{ name: 'Only On Mondays' }],
      wildEncounters: [],
   };
   const validated = {
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   };

   const diff = buildItineraryDiff(previous, validated, {
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   }, { animalVisibilityChangeThreshold: 20 });

   assert.deepEqual(diff.removed.guardiansTalks, [{ name: 'Only On Mondays' }]);
   assert.equal(hasRemovedItems(diff.removed), true);
});

test('merges backend removed guardians talks with items missing from validated', () => {
   const diff = buildItineraryDiff(
      {
         animals: [],
         attractions: [],
         guardiansTalks: [
            { name: 'Not On New Day Schedule' },
            { name: 'Cancelled On Schedule' },
         ],
         wildEncounters: [],
      },
      {
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
      },
      {
         animals: [],
         attractions: [],
         guardiansTalks: [
            {
               name: 'Cancelled On Schedule',
               removalReason: 'Cancelled.',
            },
         ],
         wildEncounters: [],
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
   const previous = {
      animals: [
         { species: 'African Lion', likelihood: 90 },
         { species: 'Amur Tiger', likelihood: 0.25 },
         { species: 'Snow Leopard', likelihood: 70 },
      ],
   };
   const validated = {
      animals: [
         { species: 'African Lion', likelihood: 60 },
         { species: 'Amur Tiger', likelihood: 0.7 },
         { species: 'Snow Leopard', likelihood: 55 },
      ],
   };

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
      {
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
      },
      {
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
      },
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

test('reports guardians talks and wild encounters removed when dropped from validated', () => {
   const diff = buildItineraryDiff(
      {
         animals: [],
         attractions: [],
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
      },
      {
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
      },
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

test('summary helpers handle empty validation results', () => {
   assert.equal(isValidatedItineraryEmpty(null), true);
   assert.equal(isValidatedItineraryEmpty({
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   }), true);
   assert.equal(isValidatedItineraryEmpty({
      animals: [{ species: 'African Lion' }],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   }), false);
   assert.equal(hasRemovedItems(null), false);
   assert.equal(hasUnscheduledItems(null), false);
   assert.equal(hasReducedVisibility({ animals: [] }), false);
   assert.equal(hasImprovedVisibility({ animals: [] }), false);
});
