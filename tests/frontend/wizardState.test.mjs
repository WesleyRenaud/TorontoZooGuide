import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { createItineraryWizardState } from '../../scripts/itinerary/wizard/state.js';

function createLocalStorageMock() {
   const values = new Map();

   return {
      getItem: (key) => values.get(key) ?? null,
      setItem: (key, value) => {
         values.set(key, String(value));
      },
      removeItem: (key) => {
         values.delete(key);
      },
   };
}

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
});

test('hasUnsavedChanges is false when both drafts are itinerary-empty (date-only drift)', () => {
   const wizard = createItineraryWizardState({
      date: '',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   assert.equal(wizard.hasUnsavedChanges(), false);

   wizard.applyValidationResult('2026-06-15', null);

   assert.equal(wizard.hasUnsavedChanges(), false);
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
