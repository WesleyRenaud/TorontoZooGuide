import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { createItineraryWizardState } from '../../scripts/itinerary/wizard/state.js';
import { StorageKeys } from '../../scripts/itinerary/storageKeys.js';
import { createLocalStorageMock } from './helpers/localStorageMock.mjs';

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
});

test('hasUnsavedChanges is true after selecting only a visit date', () => {
   const wizard = createItineraryWizardState({
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

test('hasUnsavedChanges is true when selections differ from initial', () => {
   const wizard = createItineraryWizardState({
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

test('hasUnsavedChanges is false when animals match semantically after refetch-style metadata', () => {
   const wizard = createItineraryWizardState({
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

test('hasUnsavedChanges ignores revisiting the same visit date on a saved itinerary', () => {
   const wizard = createItineraryWizardState({
      date: '2026-06-15',
      animals: [{ species: 'Red Panda', exhibit: 'Eurasia Wilds' }],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   wizard.applyValidationResult('2026-06-15', null);

   assert.equal(wizard.hasUnsavedChanges(), false);
});

test('hasUnsavedChanges is true when only the visit date changes on a saved itinerary', () => {
   const wizard = createItineraryWizardState({
      date: '2026-06-15',
      animals: [{ species: 'Red Panda', exhibit: 'Eurasia Wilds' }],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   wizard.applyValidationResult('2026-06-20', null);

   assert.equal(wizard.hasUnsavedChanges(), true);
});

test('hasUnsavedChanges stays false after revisiting date and animals without edits', () => {
   const wizard = createItineraryWizardState({
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

test('applyValidationResult with null validated does not mark itinerary as empty', () => {
   const wizard = createItineraryWizardState({
      date: '2026-06-15',
      animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   wizard.applyValidationResult('2026-06-20', null);

   assert.equal(wizard.consumePendingValidation().isEmptyItinerary, false);
});

test('hasUnsavedChanges is true when clearing a non-empty initial itinerary', () => {
   const wizard = createItineraryWizardState({
      date: '2026-06-15',
      animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   wizard.updateSelection('animals', []);

   assert.equal(wizard.hasUnsavedChanges(), true);
});

test('hydrates also-transportation attractions when opening wizard state', () => {
   const wizard = createItineraryWizardState({
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
