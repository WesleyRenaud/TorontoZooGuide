import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryValidator } from '../../../scripts/itinerary/itineraryValidator.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_BuildItineraryValidationState_TestRemovedSaved_ExpectRemoved', () => {
   const africanLion = 'African Lion';
   const africaSavanna = 'Africa Savanna';
   const conservationCarousel = 'Conservation Carousel';
   const africanRainforest = 'African Rainforest';
   const animalVisibilityChangeThreshold = 20;
   const itineraryAnimalMinLikelihood = 40;

   const validation = ItineraryValidator.buildItineraryValidationState({
      animals: [
         {
            species: africanLion,
            exhibit: africaSavanna,
            old_likelihood: 90,
            likelihood: 0,
         },
      ],
      attractions: [
         {
            name: conservationCarousel,
            old_likelihood: 100,
            likelihood: 0,
         },
      ],
      guardiansTalks: [
         {
            name: africanLion,
            is_deleted: true,
         },
      ],
      wildEncounters: [
         {
            name: africanRainforest,
            is_deleted: true,
         },
      ],
   }, {
      animalVisibilityChangeThreshold,
      itineraryAnimalMinLikelihood,
   });

   assert.equal(validation.hasChanges, true);
   assert.equal(validation.removed.animals[Position.FIRST].species, africanLion);
   assert.deepEqual(validation.reducedVisibility.animals, []);
   assert.equal(validation.removed.attractions[Position.FIRST].name, conservationCarousel);
   assert.equal(validation.removed.guardiansTalks[Position.FIRST].name, africanLion);
   assert.equal(validation.removed.wildEncounters[Position.FIRST].name, africanRainforest);
});


test('Test_BuildItineraryValidationState_TestVisibility_ExpectReducedAndImproved', () => {
   const africanPenguin = 'African Penguin';
   const amurTiger = 'Amur Tiger';
   const animalVisibilityChangeThreshold = 20;
   const itineraryAnimalMinLikelihood = 40;

   const validation = ItineraryValidator.buildItineraryValidationState({
      animals: [
         {
            species: africanPenguin,
            exhibit: 'Africa Savanna',
            old_likelihood: 90,
            likelihood: 60,
         },
         {
            species: amurTiger,
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
      animalVisibilityChangeThreshold,
      itineraryAnimalMinLikelihood,
   });

   assert.equal(validation.reducedVisibility.animals[Position.FIRST].species, africanPenguin);
   assert.equal(validation.improvedVisibility.animals[Position.FIRST].species, amurTiger);
   assert.equal(validation.hasChanges, true);
});


test('Test_BuildItineraryValidationState_TestUnchanged_ExpectNoChanges', () => {
   const animalVisibilityChangeThreshold = 20;
   const itineraryAnimalMinLikelihood = 40;

   const validation = ItineraryValidator.buildItineraryValidationState({
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
      animalVisibilityChangeThreshold,
      itineraryAnimalMinLikelihood,
   });

   assert.equal(validation.hasChanges, false);
});


test('Test_BuildItineraryValidationState_TestAddedAnimals_ExpectAdded', () => {
   const whiteRhino = 'White Rhino';
   const africanLion = 'African Lion';
   const likelihoodBefore = 20;
   const likelihoodAfter = 80;
   const animalVisibilityChangeThreshold = 20;
   const itineraryAnimalMinLikelihood = 40;

   const validation = ItineraryValidator.buildItineraryValidationState({
      animals: [
         {
            species: whiteRhino,
            exhibit: 'Africa Savanna',
            old_likelihood: likelihoodBefore,
            likelihood: likelihoodAfter,
            is_added: true,
         },
         {
            species: africanLion,
            exhibit: 'Africa Savanna',
            old_likelihood: 50,
            likelihood: 90,
         },
      ],
   }, {
      animalVisibilityChangeThreshold,
      itineraryAnimalMinLikelihood,
   });

   const addedAnimal = validation.added.animals[Position.FIRST];
   assert.equal(addedAnimal.species, whiteRhino);
   assert.equal(addedAnimal.likelihoodBefore, likelihoodBefore);
   assert.equal(addedAnimal.likelihoodAfter, likelihoodAfter);
   assert.equal(validation.improvedVisibility.animals[Position.FIRST].species, africanLion);
   assert.equal(validation.hasChanges, true);
});


test('Test_BuildItineraryValidationState_TestHighIndoor_ExpectNoVisibilityChange', () => {
   const animalVisibilityChangeThreshold = 20;
   const itineraryAnimalMinLikelihood = 40;

   const validation = ItineraryValidator.buildItineraryValidationState({
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
      animalVisibilityChangeThreshold,
      itineraryAnimalMinLikelihood,
   });

   assert.equal(validation.hasChanges, false);
   assert.deepEqual(validation.reducedVisibility.animals, []);
   assert.deepEqual(validation.improvedVisibility.animals, []);
});


test('Test_BuildItineraryValidationState_TestZeroLikelihood_ExpectNotReduced', () => {
   const commonWarthog = 'Common Warthog';
   const marabouStork = 'Marabou Stork';
   const animalVisibilityChangeThreshold = 20;
   const itineraryAnimalMinLikelihood = 40;

   const validation = ItineraryValidator.buildItineraryValidationState({
      animals: [
         {
            species: commonWarthog,
            exhibit: 'Africa Savanna',
            old_likelihood: 80,
            likelihood: 0,
         },
         {
            species: marabouStork,
            exhibit: 'Africa Savanna',
            old_likelihood: 60,
            likelihood: 0,
         },
      ],
   }, {
      animalVisibilityChangeThreshold,
      itineraryAnimalMinLikelihood,
   });

   assert.equal(validation.removed.animals[Position.FIRST].species, commonWarthog);
   assert.equal(validation.removed.animals[Position.SECOND].species, marabouStork);
   assert.deepEqual(validation.reducedVisibility.animals, []);
});


test('Test_BuildItineraryValidationState_TestMissingOldLikelihood_ExpectIgnored', () => {
   const animalVisibilityChangeThreshold = 20;
   const itineraryAnimalMinLikelihood = 40;

   const validation = ItineraryValidator.buildItineraryValidationState({
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
      animalVisibilityChangeThreshold,
      itineraryAnimalMinLikelihood,
   });

   assert.equal(validation.hasChanges, false);
   assert.deepEqual(validation.removed.animals, []);
   assert.deepEqual(validation.reducedVisibility.animals, []);
   assert.deepEqual(validation.improvedVisibility.animals, []);
   assert.deepEqual(validation.removed.attractions, []);
});
