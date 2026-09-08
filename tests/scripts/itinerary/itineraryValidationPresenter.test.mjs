import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryValidationPresenter } from '../../../scripts/itinerary/itineraryValidationPresenter.js';

test('Test_MaxStoredLikelihood_TestValues_ExpectMaxOrNull', () => {
   assert.equal(ItineraryValidationPresenter.maxStoredLikelihood(null, '', 10, 40), 40);
   assert.equal(ItineraryValidationPresenter.maxStoredLikelihood(null, ''), null);
});

test('Test_AggregateAnimalsForVisibilityComparison_TestSameKey_ExpectMaxLikelihood', () => {
   const aggregated = ItineraryValidationPresenter.aggregateAnimalsForVisibilityComparison([
      { species: 'Lion', exhibit: 'Savanna', likelihood: 20, old_likelihood: 10 },
      { species: 'Lion', exhibit: 'Savanna', likelihood: 50, old_likelihood: 5 },
      { species: 'Tiger', exhibit: 'Indo', likelihood: 30, old_likelihood: 40 },
      { species: '', exhibit: 'Savanna', likelihood: 99 },
   ]);

   assert.equal(aggregated.length, 2);
   assert.equal(
      aggregated.find((row) => row.species === 'Lion').likelihood,
      50
   );
   assert.equal(
      aggregated.find((row) => row.species === 'Lion').old_likelihood,
      10
   );
});

test('Test_HasMeaningfulVisibilityChange_TestThreshold_ExpectBoolean', () => {
   assert.equal(
      ItineraryValidationPresenter.hasMeaningfulVisibilityChange(
         { old_likelihood: 80, likelihood: 40 },
         20
      ),
      true
   );
   assert.equal(
      ItineraryValidationPresenter.hasMeaningfulVisibilityChange(
         { old_likelihood: 50, likelihood: 45 },
         20
      ),
      false
   );
   assert.equal(
      ItineraryValidationPresenter.hasMeaningfulVisibilityChange(
         { old_likelihood: null, likelihood: 40 },
         20
      ),
      false
   );
});

test('Test_BuildRemovedAnimals_TestBelowMin_ExpectVisibilityFields', () => {
   const removed = ItineraryValidationPresenter.buildRemovedAnimals([
      { species: 'Lion', exhibit: 'Savanna', likelihood: 5, old_likelihood: 40 },
      { species: 'Tiger', exhibit: 'Indo', likelihood: 50, old_likelihood: 40 },
      { species: 'Bear', exhibit: 'Americas', likelihood: 5 },
   ], 10);

   assert.deepEqual(removed, [{
      species: 'Lion',
      exhibit: 'Savanna',
      likelihood: 5,
      old_likelihood: 40,
      likelihoodBefore: 40,
      likelihoodAfter: 5,
   }]);
});

test('Test_BuildReducedAndImprovedVisibilityAnimals_TestDirection_ExpectBuckets', () => {
   const animals = [
      { species: 'A', exhibit: 'E', likelihood: 20, old_likelihood: 80, is_added: false },
      { species: 'B', exhibit: 'E', likelihood: 90, old_likelihood: 40, is_added: false },
      { species: 'C', exhibit: 'E', likelihood: 5, old_likelihood: 80, is_added: false },
      { species: 'D', exhibit: 'E', likelihood: 70, old_likelihood: 40, is_added: true },
   ];

   const reduced = ItineraryValidationPresenter.buildReducedVisibilityAnimals(animals, 20, 10);
   const improved = ItineraryValidationPresenter.buildImprovedVisibilityAnimals(animals, 20);

   assert.equal(reduced.length, 1);
   assert.equal(reduced[0].species, 'A');
   assert.equal(improved.length, 1);
   assert.equal(improved[0].species, 'B');
});

test('Test_BuildAddedAnimals_TestFlag_ExpectAddedOnly', () => {
   assert.deepEqual(
      ItineraryValidationPresenter.buildAddedAnimals([
         { species: 'A', is_added: true, likelihood: 50 },
         { species: 'B', is_added: false, likelihood: 50 },
      ]),
      [{ species: 'A', is_added: true, likelihood: 50, likelihoodBefore: undefined, likelihoodAfter: 50 }]
   );
});

test('Test_BuildRemovedAttractions_TestBelowMin_ExpectRemoved', () => {
   assert.equal(
      ItineraryValidationPresenter.buildRemovedAttractions([
         { name: 'Carousel', likelihood: 2, old_likelihood: 40 },
      ], 10).length,
      1
   );
});

test('Test_BuildRemovedScheduledItems_TestDeletedFlag_ExpectFiltered', () => {
   assert.deepEqual(
      ItineraryValidationPresenter.buildRemovedScheduledItems([
         { name: 'Talk', is_deleted: true },
         { name: 'Keep', is_deleted: false },
      ]),
      [{ name: 'Talk', is_deleted: true }]
   );
});
