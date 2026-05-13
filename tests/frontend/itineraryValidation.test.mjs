import assert from 'node:assert/strict';
import test from 'node:test';

import { buildItineraryValidationState } from '../../scripts/itinerary/itineraryValidation.js';

test('buildItineraryValidationState reports removed saved items', () => {
   const validation = buildItineraryValidationState({
      animals: [
         {
            species: 'African Lion',
            exhibit: 'Africa Savanna',
            old_likelihood: 90,
            new_likelihood: 0,
         },
      ],
      attractions: [
         {
            name: 'Conservation Carousel',
            old_likelihood: 100,
            new_likelihood: 0,
         },
      ],
      guardiansTalks: [
         {
            name: 'African Lion',
            is_deleted: true,
         },
      ],
      wildEncounters: [
         {
            name: 'African Rainforest',
            is_deleted: true,
         },
      ],
   });

   assert.equal(validation.hasChanges, true);
   assert.deepEqual(
      validation.removed.animals.map((animal) => animal.species),
      ['African Lion']
   );
   assert.deepEqual(
      validation.removed.attractions.map((attraction) => attraction.name),
      ['Conservation Carousel']
   );
   assert.deepEqual(
      validation.removed.guardiansTalks.map((talk) => talk.name),
      ['African Lion']
   );
   assert.deepEqual(
      validation.removed.wildEncounters.map((encounter) => encounter.name),
      ['African Rainforest']
   );
});

test('buildItineraryValidationState reports animal visibility changes', () => {
   const validation = buildItineraryValidationState({
      animals: [
         {
            species: 'African Penguin',
            exhibit: 'Africa Savanna',
            old_likelihood: 90,
            new_likelihood: 60,
         },
         {
            species: 'Amur Tiger',
            exhibit: 'Eurasia Wilds',
            old_likelihood: 40,
            new_likelihood: 80,
         },
         {
            species: 'Snow Leopard',
            exhibit: 'Eurasia Wilds',
            old_likelihood: 80,
            new_likelihood: 75,
         },
      ],
   });

   assert.deepEqual(
      validation.reducedVisibility.animals.map((animal) => animal.species),
      ['African Penguin']
   );
   assert.deepEqual(
      validation.improvedVisibility.animals.map((animal) => animal.species),
      ['Amur Tiger']
   );
   assert.equal(validation.hasChanges, true);
});

test('buildItineraryValidationState ignores active unchanged items', () => {
   const validation = buildItineraryValidationState({
      animals: [
         {
            species: 'African Lion',
            exhibit: 'Africa Savanna',
            old_likelihood: 90,
            new_likelihood: 80,
         },
      ],
      attractions: [
         {
            name: 'Greenhouse',
            old_likelihood: 100,
            new_likelihood: 100,
         },
      ],
      guardiansTalks: [
         {
            name: 'African Lion',
            is_deleted: false,
         },
      ],
      wildEncounters: [
         {
            name: 'African Rainforest',
            is_deleted: false,
         },
      ],
   });

   assert.equal(validation.hasChanges, false);
});

test('buildItineraryValidationState ignores items without old likelihood values', () => {
   const validation = buildItineraryValidationState({
      animals: [
         {
            species: 'African Lion',
            exhibit: 'Africa Savanna',
            old_likelihood: null,
            new_likelihood: 90,
         },
      ],
      attractions: [
         {
            name: 'Greenhouse',
            old_likelihood: null,
            new_likelihood: 100,
         },
      ],
   });

   assert.equal(validation.hasChanges, false);
   assert.deepEqual(validation.removed.animals, []);
   assert.deepEqual(validation.reducedVisibility.animals, []);
   assert.deepEqual(validation.improvedVisibility.animals, []);
   assert.deepEqual(validation.removed.attractions, []);
});
