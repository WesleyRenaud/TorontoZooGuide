import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { ItineraryWizardStore } from '../../../../scripts/itinerary/wizard/itineraryWizardStore.js';
import { ScheduleItemKeySeparator } from '../../../../scripts/itinerary/scheduleItemKeySeparator.js';
import { StorageKeys } from '../../../../scripts/itinerary/storageKeys.js';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';

const _animalsKey = 'animals';

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
});


test('Test_HasUnsavedChanges_TestFreshState_ExpectFalse', () => {
   const wizard = ItineraryWizardStore.createItineraryWizardState({
      date: '',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   const hasChanges = wizard.hasUnsavedChanges();

   assert.equal(hasChanges, false);
});


test('Test_HasUnsavedChanges_TestHasUnsavedChangesIsTrueAfterSelectingOnlyAVisit_ExpectOk', () => {
   const wizard = ItineraryWizardStore.createItineraryWizardState({
      date: '',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });
   const visitDate = '2026-06-15';
   wizard.applyValidationResult(visitDate, null);

   const hasChanges = wizard.hasUnsavedChanges();

   assert.equal(hasChanges, true);
});


test('Test_HasUnsavedChanges_TestHasUnsavedChangesIsTrueWhenSelectionsDifferFromInitial_ExpectOk', () => {
   const wizard = ItineraryWizardStore.createItineraryWizardState({
      date: '',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });
   const animal = { species: 'African Lion', exhibit: 'Africa Savanna' };
   wizard.updateSelection(_animalsKey, [animal]);

   const hasChanges = wizard.hasUnsavedChanges();

   assert.equal(hasChanges, true);
});


test('Test_HasUnsavedChanges_TestHasUnsavedChangesIsFalseWhenAnimalsMatchSemanticallyAfter_ExpectOk', () => {
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const wizard = ItineraryWizardStore.createItineraryWizardState({
      date: '2026-06-15',
      animals: [{ species, exhibit }],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });
   wizard.updateSelection(_animalsKey, [
      {
         species,
         exhibit,
         likelihood: 88,
         imageSrc: 'https://example.test/lion.png',
         id: [species, exhibit].join(ScheduleItemKeySeparator.VALUE),
      },
   ]);

   const hasChanges = wizard.hasUnsavedChanges();

   assert.equal(hasChanges, false);
});


test('Test_HasUnsavedChanges_TestHasUnsavedChangesIgnoresRevisitingTheSameVisitDateOn_ExpectOk', () => {
   const visitDate = '2026-06-15';
   const wizard = ItineraryWizardStore.createItineraryWizardState({
      date: visitDate,
      animals: [{ species: 'Red Panda', exhibit: 'Eurasia Wilds' }],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });
   wizard.applyValidationResult(visitDate, null);

   const hasChanges = wizard.hasUnsavedChanges();

   assert.equal(hasChanges, false);
});


test('Test_HasUnsavedChanges_TestHasUnsavedChangesIsTrueWhenOnlyTheVisitDate_ExpectOk', () => {
   const wizard = ItineraryWizardStore.createItineraryWizardState({
      date: '2026-06-15',
      animals: [{ species: 'Red Panda', exhibit: 'Eurasia Wilds' }],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });
   const nextDate = '2026-06-20';
   wizard.applyValidationResult(nextDate, null);

   const hasChanges = wizard.hasUnsavedChanges();

   assert.equal(hasChanges, true);
});


test('Test_HasUnsavedChanges_TestHasUnsavedChangesStaysFalseAfterRevisitingDateAndAnimals_ExpectOk', () => {
   const visitDate = '2026-06-15';
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const wizard = ItineraryWizardStore.createItineraryWizardState({
      date: visitDate,
      animals: [{ species, exhibit }],
      attractions: [{ name: 'Carousel' }],
      guardiansTalks: [],
      wildEncounters: [],
   });
   wizard.applyValidationResult(visitDate, null);
   wizard.updateSelection(_animalsKey, [
      {
         species,
         exhibit,
         likelihood: 91,
         id: [species, exhibit].join(ScheduleItemKeySeparator.VALUE),
      },
   ]);

   const hasChanges = wizard.hasUnsavedChanges();

   assert.equal(hasChanges, false);
});


test('Test_ApplyValidationResult_TestApplyValidationResultWithNullValidatedDoesNotMarkItinerary_ExpectOk', () => {
   const wizard = ItineraryWizardStore.createItineraryWizardState({
      date: '2026-06-15',
      animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });
   wizard.applyValidationResult('2026-06-20', null);

   const pending = wizard.consumePendingValidation();

   assert.equal(pending.isEmptyItinerary, false);
});


test('Test_HasUnsavedChanges_TestHasUnsavedChangesIsTrueWhenClearingANonEmpty_ExpectOk', () => {
   const wizard = ItineraryWizardStore.createItineraryWizardState({
      date: '2026-06-15',
      animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });
   wizard.updateSelection(_animalsKey, []);

   const hasChanges = wizard.hasUnsavedChanges();

   assert.equal(hasChanges, true);
});


test('Test_Hydrates_TestHydratesAlsoTransportationAttractionsWhenOpeningWizardState_ExpectOk', () => {
   const transportationName = 'Zoomobile';
   const transportation = { name: transportationName, added_as_attraction: true };
   const attraction = {
      name: transportationName,
      addedAsAttraction: true,
   };
   const wizard = ItineraryWizardStore.createItineraryWizardState({
      date: '2026-08-17',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [transportation],
   });

   assert.deepEqual(wizard.state.attractions, [attraction]);
   assert.deepEqual(wizard.state.transportations, []);
   assert.deepEqual(JSON.parse(localStorage.getItem(StorageKeys.ATTRACTIONS_KEY)), [attraction]);
});


test('Test_UpdateSelection_TestPreserveOnInvalidRejected_ExpectNoPersist', () => {
   const animal = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const wizard = ItineraryWizardStore.createItineraryWizardState({
      date: '2026-06-15',
      animals: [animal],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   wizard.updateSelection(_animalsKey, null, { preserveOnInvalid: true });

   assert.deepEqual(wizard.state.animals, [animal]);
});


test('Test_DiscardChanges_TestRestoresInitialDraft_ExpectOk', () => {
   const animal = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const wizard = ItineraryWizardStore.createItineraryWizardState({
      date: '2026-06-15',
      animals: [animal],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });
   wizard.updateSelection(_animalsKey, []);

   wizard.discardChanges();

   assert.equal(wizard.hasUnsavedChanges(), false);
   assert.deepEqual(wizard.state.animals, [animal]);
});


test('Test_UpdateVisitTimes_TestChangedTimes_ExpectUnsaved', () => {
   const visitDate = '2026-06-15';
   const arrivalTime = '10:00 AM';
   const departureTime = '4:00 PM';
   const wizard = ItineraryWizardStore.createItineraryWizardState({
      date: visitDate,
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   wizard.updateVisitTimes({ arrivalTime, departureTime });

   assert.equal(wizard.state.arrivalTime, arrivalTime);
   assert.equal(wizard.state.departureTime, departureTime);
   assert.equal(wizard.hasUnsavedChanges(), true);
});
