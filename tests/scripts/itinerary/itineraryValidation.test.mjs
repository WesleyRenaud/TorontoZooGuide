import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryValidation } from '../../../scripts/itinerary/itineraryValidation.js';

test('Test_BuildItineraryValidationState_TestRemovedSaved_ExpectRemoved', () => {
   const validation = ItineraryValidation.buildItineraryValidationState({
      animals: [
         {
            species: 'African Lion',
            exhibit: 'Africa Savanna',
            old_likelihood: 90,
            likelihood: 0,
         },
      ],
      attractions: [
         {
            name: 'Conservation Carousel',
            old_likelihood: 100,
            likelihood: 0,
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
   }, {
      animalVisibilityChangeThreshold: 20,
      itineraryAnimalMinLikelihood: 40,
   });

   assert.equal(validation.hasChanges, true);
   assert.deepEqual(
      validation.removed.animals.map((animal) => animal.species),
      ['African Lion']
   );
   assert.deepEqual(validation.reducedVisibility.animals, []);
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

test('Test_BuildItineraryValidationState_TestVisibility_ExpectReducedAndImproved', () => {
   const validation = ItineraryValidation.buildItineraryValidationState({
      animals: [
         {
            species: 'African Penguin',
            exhibit: 'Africa Savanna',
            old_likelihood: 90,
            likelihood: 60,
         },
         {
            species: 'Amur Tiger',
            exhibit: 'Eurasia Wilds',
            old_likelihood: 40,
            likelihood: 80,
         },
         {
            species: 'Snow Leopard',
            exhibit: 'Eurasia Wilds',
            old_likelihood: 80,
            likelihood: 75,
         },
      ],
   }, {
      animalVisibilityChangeThreshold: 20,
      itineraryAnimalMinLikelihood: 40,
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

test('Test_BuildItineraryValidationState_TestUnchanged_ExpectNoChanges', () => {
   const validation = ItineraryValidation.buildItineraryValidationState({
      animals: [
         {
            species: 'African Lion',
            exhibit: 'Africa Savanna',
            old_likelihood: 90,
            likelihood: 80,
         },
      ],
      attractions: [
         {
            name: 'Greenhouse',
            old_likelihood: 100,
            likelihood: 100,
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
   }, {
      animalVisibilityChangeThreshold: 20,
      itineraryAnimalMinLikelihood: 40,
   });

   assert.equal(validation.hasChanges, false);
});

test('Test_BuildItineraryValidationState_TestAddedAnimals_ExpectAdded', () => {
   const validation = ItineraryValidation.buildItineraryValidationState({
      animals: [
         {
            species: 'White Rhino',
            exhibit: 'Africa Savanna',
            old_likelihood: 20,
            likelihood: 80,
            is_added: true,
         },
         {
            species: 'African Lion',
            exhibit: 'Africa Savanna',
            old_likelihood: 50,
            likelihood: 90,
         },
      ],
   }, {
      animalVisibilityChangeThreshold: 20,
      itineraryAnimalMinLikelihood: 40,
   });

   assert.deepEqual(
      validation.added.animals.map((animal) => ({
         species: animal.species,
         likelihoodBefore: animal.likelihoodBefore,
         likelihoodAfter: animal.likelihoodAfter,
      })),
      [
         {
            species: 'White Rhino',
            likelihoodBefore: 20,
            likelihoodAfter: 80,
         },
      ]
   );
   assert.deepEqual(
      validation.improvedVisibility.animals.map((animal) => animal.species),
      ['African Lion']
   );
   assert.equal(validation.hasChanges, true);
});

test('Test_BuildItineraryValidationState_TestHighIndoor_ExpectNoVisibilityChange', () => {
   const validation = ItineraryValidation.buildItineraryValidationState({
      animals: [
         {
            species: 'Masai Giraffe',
            exhibit: 'Africa Savanna',
            enclosure_type: 'Indoor',
            old_likelihood: 100,
            likelihood: 100,
         },
         {
            species: 'Masai Giraffe',
            exhibit: 'Africa Savanna',
            enclosure_type: 'Outdoor',
            old_likelihood: 100,
            likelihood: 78,
         },
      ],
   }, {
      animalVisibilityChangeThreshold: 20,
      itineraryAnimalMinLikelihood: 40,
   });

   assert.equal(validation.hasChanges, false);
   assert.deepEqual(validation.reducedVisibility.animals, []);
   assert.deepEqual(validation.improvedVisibility.animals, []);
});

test('Test_BuildItineraryValidationState_TestZeroLikelihood_ExpectNotReduced', () => {
   const validation = ItineraryValidation.buildItineraryValidationState({
      animals: [
         {
            species: 'Common Warthog',
            exhibit: 'Africa Savanna',
            old_likelihood: 80,
            likelihood: 0,
         },
         {
            species: 'Marabou Stork',
            exhibit: 'Africa Savanna',
            old_likelihood: 60,
            likelihood: 0,
         },
      ],
   }, {
      animalVisibilityChangeThreshold: 20,
      itineraryAnimalMinLikelihood: 40,
   });

   assert.deepEqual(
      validation.removed.animals.map((animal) => animal.species),
      ['Common Warthog', 'Marabou Stork']
   );
   assert.deepEqual(validation.reducedVisibility.animals, []);
});

test('Test_BuildItineraryValidationState_TestMissingOldLikelihood_ExpectIgnored', () => {
   const validation = ItineraryValidation.buildItineraryValidationState({
      animals: [
         {
            species: 'African Lion',
            exhibit: 'Africa Savanna',
            old_likelihood: null,
            likelihood: 90,
         },
         {
            species: 'Marabou Stork',
            exhibit: 'Africa Savanna',
            old_likelihood: null,
            likelihood: 0,
         },
      ],
      attractions: [
         {
            name: 'Greenhouse',
            old_likelihood: null,
            likelihood: 100,
         },
         {
            name: 'Conservation Carousel',
            old_likelihood: null,
            likelihood: 0,
         },
      ],
   }, {
      animalVisibilityChangeThreshold: 20,
      itineraryAnimalMinLikelihood: 40,
   });

   assert.equal(validation.hasChanges, false);
   assert.deepEqual(validation.removed.animals, []);
   assert.deepEqual(validation.reducedVisibility.animals, []);
   assert.deepEqual(validation.improvedVisibility.animals, []);
   assert.deepEqual(validation.removed.attractions, []);
});
