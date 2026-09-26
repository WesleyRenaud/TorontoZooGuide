import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardDiffPresenter } from '../../../../../scripts/itinerary/wizard/diff/wizardDiffPresenter.js';


test('Test_HasRemovedItems_TestNull_ExpectFalse', () => {
   const collections = null;

   const hasRemoved = WizardDiffPresenter.hasRemovedItems(collections);

   assert.equal(hasRemoved, false);
});


test('Test_HasRemovedItems_TestEmptyAnimals_ExpectFalse', () => {
   const collections = { animals: [] };

   const hasRemoved = WizardDiffPresenter.hasRemovedItems(collections);

   assert.equal(hasRemoved, false);
});


test('Test_HasRemovedItems_TestAnimals_ExpectTrue', () => {
   const collections = { animals: [{ species: 'African Lion' }] };

   const hasRemoved = WizardDiffPresenter.hasRemovedItems(collections);

   assert.equal(hasRemoved, true);
});


test('Test_HasRemovedItems_TestAttractions_ExpectTrue', () => {
   const collections = { attractions: [{ name: 'Conservation Carousel' }] };

   const hasRemoved = WizardDiffPresenter.hasRemovedItems(collections);

   assert.equal(hasRemoved, true);
});


test('Test_HasAddedItems_TestEmptyAnimals_ExpectFalse', () => {
   const collections = { animals: [] };

   const hasAdded = WizardDiffPresenter.hasAddedItems(collections);

   assert.equal(hasAdded, false);
});


test('Test_HasAddedItems_TestAnimals_ExpectTrue', () => {
   const collections = { animals: [{ species: 'Amur Tiger' }] };

   const hasAdded = WizardDiffPresenter.hasAddedItems(collections);

   assert.equal(hasAdded, true);
});


test('Test_HasReducedVisibility_TestAnimals_ExpectTrue', () => {
   const collections = { animals: [{ species: 'African Lion' }] };

   const hasReduced = WizardDiffPresenter.hasReducedVisibility(collections);

   assert.equal(hasReduced, true);
});


test('Test_HasImprovedVisibility_TestEmptyAnimals_ExpectFalse', () => {
   const collections = { animals: [] };

   const hasImproved = WizardDiffPresenter.hasImprovedVisibility(collections);

   assert.equal(hasImproved, false);
});


test('Test_HasImprovedVisibility_TestAnimals_ExpectTrue', () => {
   const collections = { animals: [{ species: 'African Lion' }] };

   const hasImproved = WizardDiffPresenter.hasImprovedVisibility(collections);

   assert.equal(hasImproved, true);
});


test('Test_HasUnscheduledItems_TestAnimals_ExpectTrue', () => {
   const collections = { animals: [{ species: 'African Lion' }] };

   const hasUnscheduled = WizardDiffPresenter.hasUnscheduledItems(collections);

   assert.equal(hasUnscheduled, true);
});


test('Test_HasUnscheduledItems_TestAttractions_ExpectTrue', () => {
   const collections = { attractions: [{ name: 'Conservation Carousel' }] };

   const hasUnscheduled = WizardDiffPresenter.hasUnscheduledItems(collections);

   assert.equal(hasUnscheduled, true);
});


test('Test_HasUnscheduledItems_TestEmptyCollections_ExpectFalse', () => {
   const collections = { animals: [], attractions: [] };

   const hasUnscheduled = WizardDiffPresenter.hasUnscheduledItems(collections);

   assert.equal(hasUnscheduled, false);
});


test('Test_IsValidatedItineraryEmpty_TestNull_ExpectTrue', () => {
   const itinerary = null;

   const isEmpty = WizardDiffPresenter.isValidatedItineraryEmpty(itinerary);

   assert.equal(isEmpty, true);
});


test('Test_IsValidatedItineraryEmpty_TestEmptyCollections_ExpectTrue', () => {
   const itinerary = {
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [],
   };

   const isEmpty = WizardDiffPresenter.isValidatedItineraryEmpty(itinerary);

   assert.equal(isEmpty, true);
});


test('Test_IsValidatedItineraryEmpty_TestAnimals_ExpectFalse', () => {
   const itinerary = {
      animals: [{ species: 'African Lion' }],
   };

   const isEmpty = WizardDiffPresenter.isValidatedItineraryEmpty(itinerary);

   assert.equal(isEmpty, false);
});
