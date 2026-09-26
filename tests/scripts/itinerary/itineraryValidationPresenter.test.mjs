import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryValidationPresenter } from '../../../scripts/itinerary/itineraryValidationPresenter.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_MaxStoredLikelihood_TestValues_ExpectMax', () => {
   const first = 10;
   const second = 40;

   const max = ItineraryValidationPresenter.maxStoredLikelihood(null, '', first, second);

   assert.equal(max, Math.max(first, second));
});


test('Test_MaxStoredLikelihood_TestEmpty_ExpectNull', () => {
   const max = ItineraryValidationPresenter.maxStoredLikelihood(null, '');

   assert.equal(max, null);
});


test('Test_AggregateAnimalsForVisibilityComparison_TestSameKey_ExpectMaxLikelihood', () => {
   const lion = 'African Lion';
   const exhibit = 'Africa Savanna';
   const tiger = 'Amur Tiger';
   const tigerExhibit = 'Tundra Trek';
   const lowerLikelihood = 20;
   const higherLikelihood = 50;
   const oldLikelihood = 10;
   const animals = [
      { species: lion, exhibit, likelihood: lowerLikelihood, old_likelihood: oldLikelihood },
      { species: lion, exhibit, likelihood: higherLikelihood, old_likelihood: 5 },
      { species: tiger, exhibit: tigerExhibit, likelihood: 30, old_likelihood: 40 },
      { species: '', exhibit, likelihood: 99 },
   ];

   const aggregated = ItineraryValidationPresenter.aggregateAnimalsForVisibilityComparison(animals);

   assert.equal(aggregated.length, 2);
   assert.equal(
      aggregated.find((row) => row.species === lion).likelihood,
      higherLikelihood
   );
   assert.equal(
      aggregated.find((row) => row.species === lion).old_likelihood,
      oldLikelihood
   );
});


test('Test_HasMeaningfulVisibilityChange_TestAboveThreshold_ExpectTrue', () => {
   const oldLikelihood = 80;
   const likelihood = 40;
   const threshold = 20;
   const animal = { old_likelihood: oldLikelihood, likelihood };

   const hasChange = ItineraryValidationPresenter.hasMeaningfulVisibilityChange(
      animal,
      threshold
   );

   assert.equal(hasChange, true);
});


test('Test_HasMeaningfulVisibilityChange_TestBelowThreshold_ExpectFalse', () => {
   const oldLikelihood = 50;
   const likelihood = 45;
   const threshold = 20;
   const animal = { old_likelihood: oldLikelihood, likelihood };

   const hasChange = ItineraryValidationPresenter.hasMeaningfulVisibilityChange(
      animal,
      threshold
   );

   assert.equal(hasChange, false);
});


test('Test_HasMeaningfulVisibilityChange_TestMissingOld_ExpectFalse', () => {
   const likelihood = 40;
   const threshold = 20;
   const animal = { old_likelihood: null, likelihood };

   const hasChange = ItineraryValidationPresenter.hasMeaningfulVisibilityChange(
      animal,
      threshold
   );

   assert.equal(hasChange, false);
});


test('Test_BuildRemovedAnimals_TestBelowMin_ExpectVisibilityFields', () => {
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const likelihood = 5;
   const oldLikelihood = 40;
   const minLikelihood = 10;
   const animals = [
      { species, exhibit, likelihood, old_likelihood: oldLikelihood },
      { species: 'Amur Tiger', exhibit: 'Tundra Trek', likelihood: 50, old_likelihood: oldLikelihood },
      { species: 'Grizzly Bear', exhibit: 'Canadian Domain', likelihood },
   ];

   const removed = ItineraryValidationPresenter.buildRemovedAnimals(animals, minLikelihood);

   assert.deepEqual(removed, [{
      species,
      exhibit,
      likelihood,
      old_likelihood: oldLikelihood,
      likelihoodBefore: oldLikelihood,
      likelihoodAfter: likelihood,
   }]);
});


test('Test_BuildReducedAndImprovedVisibilityAnimals_TestDirection_ExpectBuckets', () => {
   const reducedAnimal = {
      species: 'African Lion',
      exhibit: 'Africa Savanna',
      likelihood: 20,
      old_likelihood: 80,
      is_added: false,
   };
   const improvedAnimal = {
      species: 'Amur Tiger',
      exhibit: 'Tundra Trek',
      likelihood: 90,
      old_likelihood: 40,
      is_added: false,
   };
   const threshold = 20;
   const minLikelihood = 10;
   const animals = [
      reducedAnimal,
      improvedAnimal,
      {
         species: 'Snow Leopard',
         exhibit: 'Eurasia Wilds',
         likelihood: 5,
         old_likelihood: 80,
         is_added: false,
      },
      {
         species: 'Masai Giraffe',
         exhibit: 'Africa Savanna',
         likelihood: 70,
         old_likelihood: 40,
         is_added: true,
      },
   ];

   const reduced = ItineraryValidationPresenter.buildReducedVisibilityAnimals(
      animals,
      threshold,
      minLikelihood
   );
   const improved = ItineraryValidationPresenter.buildImprovedVisibilityAnimals(
      animals,
      threshold
   );

   assert.equal(reduced.length, 1);
   assert.equal(reduced[Position.FIRST].species, reducedAnimal.species);
   assert.equal(improved.length, 1);
   assert.equal(improved[Position.FIRST].species, improvedAnimal.species);
});


test('Test_BuildAddedAnimals_TestFlag_ExpectAddedOnly', () => {
   const added = { species: 'African Lion', is_added: true, likelihood: 50 };
   const existing = { species: 'Amur Tiger', is_added: false, likelihood: 50 };
   const animals = [added, existing];

   const addedAnimals = ItineraryValidationPresenter.buildAddedAnimals(animals);

   assert.deepEqual(addedAnimals, [{
      ...added,
      likelihoodBefore: undefined,
      likelihoodAfter: added.likelihood,
   }]);
});


test('Test_BuildRemovedAttractions_TestBelowMin_ExpectRemoved', () => {
   const minLikelihood = 10;
   const attractions = [
      { name: 'Conservation Carousel', likelihood: 2, old_likelihood: 40 },
   ];

   const removed = ItineraryValidationPresenter.buildRemovedAttractions(
      attractions,
      minLikelihood
   );

   assert.equal(removed.length, 1);
});


test('Test_BuildRemovedScheduledItems_TestDeletedFlag_ExpectFiltered', () => {
   const deleted = { name: 'Lion Talk', is_deleted: true };
   const kept = { name: 'Zoomobile', is_deleted: false };
   const items = [deleted, kept];

   const removed = ItineraryValidationPresenter.buildRemovedScheduledItems(items);

   assert.deepEqual(removed, [deleted]);
});
