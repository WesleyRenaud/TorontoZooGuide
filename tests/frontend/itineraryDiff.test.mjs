import assert from 'node:assert/strict';
import test from 'node:test';

import {
   buildItineraryDiff,
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
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

   const diff = buildItineraryDiff(previous, validated);

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
      }
   );

   assert.deepEqual(diff.removed.attractions, [{ name: 'Conservation Carousel' }]);
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

   const diff = buildItineraryDiff(previous, validated);

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
   assert.equal(hasReducedVisibility({ animals: [] }), false);
   assert.equal(hasImprovedVisibility({ animals: [] }), false);
});
