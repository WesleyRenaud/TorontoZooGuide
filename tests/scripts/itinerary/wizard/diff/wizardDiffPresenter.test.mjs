import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardDiffPresenter } from '../../../../../scripts/itinerary/wizard/diff/wizardDiffPresenter.js';

test('Test_HasRemovedItems_TestCollections_ExpectBoolean', () => {
   assert.equal(WizardDiffPresenter.hasRemovedItems(null), false);
   assert.equal(WizardDiffPresenter.hasRemovedItems({ animals: [] }), false);
   assert.equal(WizardDiffPresenter.hasRemovedItems({ animals: [{ species: 'Lion' }] }), true);
   assert.equal(WizardDiffPresenter.hasRemovedItems({ attractions: [{ name: 'Carousel' }] }), true);
});

test('Test_HasAddedItems_TestAnimals_ExpectBoolean', () => {
   assert.equal(WizardDiffPresenter.hasAddedItems({ animals: [] }), false);
   assert.equal(WizardDiffPresenter.hasAddedItems({ animals: [{ species: 'Tiger' }] }), true);
});

test('Test_HasVisibilityBuckets_TestAnimals_ExpectBoolean', () => {
   assert.equal(WizardDiffPresenter.hasReducedVisibility({ animals: [{ species: 'Lion' }] }), true);
   assert.equal(WizardDiffPresenter.hasImprovedVisibility({ animals: [] }), false);
   assert.equal(WizardDiffPresenter.hasImprovedVisibility({ animals: [{ species: 'Lion' }] }), true);
});

test('Test_HasUnscheduledItems_TestCollections_ExpectBoolean', () => {
   assert.equal(WizardDiffPresenter.hasUnscheduledItems({ animals: [{ species: 'Lion' }] }), true);
   assert.equal(WizardDiffPresenter.hasUnscheduledItems({ attractions: [{ name: 'Carousel' }] }), true);
   assert.equal(WizardDiffPresenter.hasUnscheduledItems({ animals: [], attractions: [] }), false);
});

test('Test_IsValidatedItineraryEmpty_TestCollections_ExpectBoolean', () => {
   assert.equal(WizardDiffPresenter.isValidatedItineraryEmpty(null), true);
   assert.equal(WizardDiffPresenter.isValidatedItineraryEmpty({
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [],
   }), true);
   assert.equal(WizardDiffPresenter.isValidatedItineraryEmpty({
      animals: [{ species: 'Lion' }],
   }), false);
});
