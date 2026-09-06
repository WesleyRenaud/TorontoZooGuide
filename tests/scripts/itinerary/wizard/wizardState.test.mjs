import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { State } from '../../../../scripts/itinerary/wizard/state.js';
import { StorageKeys } from '../../../../scripts/itinerary/storageKeys.js';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
});

test('Test_HasUnsavedChanges_TestHasUnsavedChangesIsTrueAfterSelectingOnlyAVisit_ExpectOk', () => {
   const wizard = State.createItineraryWizardState({
      date: '',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   assert.equal(wizard.hasUnsavedChanges(), false);

   wizard.applyValidationResult('2026-06-15', null);

   assert.equal(wizard.hasUnsavedChanges(), true);
});

test('Test_HasUnsavedChanges_TestHasUnsavedChangesIsTrueWhenSelectionsDifferFromInitial_ExpectOk', () => {
   const wizard = State.createItineraryWizardState({
      date: '',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   wizard.updateSelection('animals', [
      { species: 'African Lion', exhibit: 'Africa Savanna' },
   ]);

   assert.equal(wizard.hasUnsavedChanges(), true);
});

test('Test_HasUnsavedChanges_TestHasUnsavedChangesIsFalseWhenAnimalsMatchSemanticallyAfter_ExpectOk', () => {
   const wizard = State.createItineraryWizardState({
      date: '2026-06-15',
      animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   wizard.updateSelection('animals', [
      {
         species: 'African Lion',
         exhibit: 'Africa Savanna',
         likelihood: 88,
         imageSrc: 'https://example.test/lion.png',
         id: 'African Lion||Africa Savanna',
      },
   ]);

   assert.equal(wizard.hasUnsavedChanges(), false);
});

test('Test_HasUnsavedChanges_TestHasUnsavedChangesIgnoresRevisitingTheSameVisitDateOn_ExpectOk', () => {
   const wizard = State.createItineraryWizardState({
      date: '2026-06-15',
      animals: [{ species: 'Red Panda', exhibit: 'Eurasia Wilds' }],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   wizard.applyValidationResult('2026-06-15', null);

   assert.equal(wizard.hasUnsavedChanges(), false);
});

test('Test_HasUnsavedChanges_TestHasUnsavedChangesIsTrueWhenOnlyTheVisitDate_ExpectOk', () => {
   const wizard = State.createItineraryWizardState({
      date: '2026-06-15',
      animals: [{ species: 'Red Panda', exhibit: 'Eurasia Wilds' }],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   wizard.applyValidationResult('2026-06-20', null);

   assert.equal(wizard.hasUnsavedChanges(), true);
});

test('Test_HasUnsavedChanges_TestHasUnsavedChangesStaysFalseAfterRevisitingDateAndAnimals_ExpectOk', () => {
   const wizard = State.createItineraryWizardState({
      date: '2026-06-15',
      animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
      attractions: [{ name: 'Carousel' }],
      guardiansTalks: [],
      wildEncounters: [],
   });

   wizard.applyValidationResult('2026-06-15', null);
   wizard.updateSelection('animals', [
      {
         species: 'African Lion',
         exhibit: 'Africa Savanna',
         likelihood: 91,
         id: 'African Lion||Africa Savanna',
      },
   ]);

   assert.equal(wizard.hasUnsavedChanges(), false);
});

test('Test_ApplyValidationResult_TestApplyValidationResultWithNullValidatedDoesNotMarkItinerary_ExpectOk', () => {
   const wizard = State.createItineraryWizardState({
      date: '2026-06-15',
      animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   wizard.applyValidationResult('2026-06-20', null);

   assert.equal(wizard.consumePendingValidation().isEmptyItinerary, false);
});

test('Test_HasUnsavedChanges_TestHasUnsavedChangesIsTrueWhenClearingANonEmpty_ExpectOk', () => {
   const wizard = State.createItineraryWizardState({
      date: '2026-06-15',
      animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   wizard.updateSelection('animals', []);

   assert.equal(wizard.hasUnsavedChanges(), true);
});

test('Test_Hydrates_TestHydratesAlsoTransportationAttractionsWhenOpeningWizardState_ExpectOk', () => {
   const wizard = State.createItineraryWizardState({
      date: '2026-08-17',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [{ name: 'Zoomobile', added_as_attraction: true }],
   });

   assert.deepEqual(wizard.state.attractions, [{
      name: 'Zoomobile',
      addedAsAttraction: true,
   }]);
   assert.deepEqual(wizard.state.transportations, []);
   assert.deepEqual(JSON.parse(localStorage.getItem(StorageKeys.ATTRACTIONS_KEY)), [{
      name: 'Zoomobile',
      addedAsAttraction: true,
   }]);
});
