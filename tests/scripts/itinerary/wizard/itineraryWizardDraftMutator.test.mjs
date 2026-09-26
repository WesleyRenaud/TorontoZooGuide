import assert from 'node:assert/strict';
import test from 'node:test';

import { DraftStore } from '../../../../scripts/itinerary/draftStore.js';
import { ItineraryShape } from '../../../../scripts/itinerary/itineraryShape.js';
import { ItineraryWizardDraftMutator } from '../../../../scripts/itinerary/wizard/itineraryWizardDraftMutator.js';
import { WizardDiffPresenter } from '../../../../scripts/itinerary/wizard/diff/wizardDiffPresenter.js';

const _animalsKey = 'animals';


test('Test_CreatePendingValidationState_TestDefaults_ExpectNullFlags', () => {
   const pending = ItineraryWizardDraftMutator.createPendingValidationState();

   assert.deepEqual(pending, {
      pendingRemovedItems: null,
      pendingUnscheduledItems: null,
      pendingReducedVisibility: null,
      pendingImprovedVisibility: null,
      pendingValidatedEmpty: false,
   });
});


test('Test_BuildWizardDraftSnapshot_TestClone_ExpectShapeClone', () => {
   const original = ItineraryShape.cloneItineraryDraft;
   const date = '2026-06-15';
   const state = { date };
   ItineraryShape.cloneItineraryDraft = (value) => ({ ...value, cloned: true });

   try {
      const snapshot = ItineraryWizardDraftMutator.buildWizardDraftSnapshot(state);

      assert.deepEqual(snapshot, { date, cloned: true });
   } finally {
      ItineraryShape.cloneItineraryDraft = original;
   }
});


test('Test_WriteDraftState_TestDelegates_ExpectDraftStore', () => {
   const original = DraftStore.writeStoredItineraryDraft;
   const drafts = [];
   const date = '2026-06-15';
   const draft = { date };
   DraftStore.writeStoredItineraryDraft = (value) => { drafts.push(value); };

   try {
      ItineraryWizardDraftMutator.writeDraftState(draft);

      assert.deepEqual(drafts, [draft]);
   } finally {
      DraftStore.writeStoredItineraryDraft = original;
   }
});


test('Test_AssignWizardDraft_TestNormalized_ExpectCopiedArrays', () => {
   const original = ItineraryShape.normalizeItineraryDraft;
   const date = '2026-06-15';
   const animal = { species: 'Lion' };
   const attraction = 'Carousel';
   const talk = { name: 'Talk' };
   const encounter = { name: 'Encounter' };
   const transportation = { name: 'Zoomobile' };
   const station = { name: 'Station' };
   const normalized = {
      date,
      animals: [animal],
      attractions: [attraction],
      guardiansTalks: [talk],
      wildEncounters: [encounter],
      transportations: [transportation],
      transportationStations: [station],
   };
   ItineraryShape.normalizeItineraryDraft = () => normalized;
   const state = {};

   try {
      ItineraryWizardDraftMutator.assignWizardDraft(state, {});

      assert.equal(state.date, date);
      assert.deepEqual(state.animals, [animal]);
      assert.deepEqual(state.attractions, [attraction]);
      assert.notEqual(state.animals, normalized.animals);
   } finally {
      ItineraryShape.normalizeItineraryDraft = original;
   }
});


test('Test_ConsumePendingValidationState_TestResets_ExpectSnapshot', () => {
   const removed = { animals: [1] };
   const unscheduled = { animals: [2] };
   const reduced = { animals: [3] };
   const improved = { animals: [4] };
   const state = {
      pendingRemovedItems: removed,
      pendingUnscheduledItems: unscheduled,
      pendingReducedVisibility: reduced,
      pendingImprovedVisibility: improved,
      pendingValidatedEmpty: true,
   };

   const pending = ItineraryWizardDraftMutator.consumePendingValidationState(state);

   assert.deepEqual(pending, {
      removed,
      unscheduled,
      reducedVisibility: reduced,
      improvedVisibility: improved,
      isEmptyItinerary: true,
   });
   assert.equal(state.pendingRemovedItems, null);
   assert.equal(state.pendingValidatedEmpty, false);
});


test('Test_ApplySelectionUpdate_TestNullPreserveOnInvalid_ExpectUnchanged', () => {
   const animal = { species: 'Old' };
   const state = { animals: [animal] };

   const updated = ItineraryWizardDraftMutator.applySelectionUpdate(state, _animalsKey, null, {
      preserveOnInvalid: true,
   });

   assert.equal(updated, false);
   assert.deepEqual(state.animals, [animal]);
});


test('Test_ApplySelectionUpdate_TestNull_ExpectCleared', () => {
   const animal = { species: 'Old' };
   const state = { animals: [animal] };

   const updated = ItineraryWizardDraftMutator.applySelectionUpdate(state, _animalsKey, null);

   assert.equal(updated, true);
   assert.deepEqual(state.animals, []);
});


test('Test_ApplySelectionUpdate_TestValue_ExpectCopied', () => {
   const animal = { species: 'Lion' };
   const animals = [animal];
   const state = { animals: [{ species: 'Old' }] };

   const updated = ItineraryWizardDraftMutator.applySelectionUpdate(state, _animalsKey, animals);

   assert.equal(updated, true);
   assert.deepEqual(state.animals, animals);
});


test('Test_ApplyPendingValidation_TestValidatedAndFlags_ExpectState', () => {
   const originals = {
      hasRemovedItems: WizardDiffPresenter.hasRemovedItems,
      hasUnscheduledItems: WizardDiffPresenter.hasUnscheduledItems,
      hasReducedVisibility: WizardDiffPresenter.hasReducedVisibility,
      hasImprovedVisibility: WizardDiffPresenter.hasImprovedVisibility,
      isValidatedItineraryEmpty: WizardDiffPresenter.isValidatedItineraryEmpty,
      assignWizardDraft: ItineraryWizardDraftMutator.assignWizardDraft,
      buildWizardDraftSnapshot: ItineraryWizardDraftMutator.buildWizardDraftSnapshot,
   };
   const assigns = [];
   const removed = { animals: [1] };
   const reducedVisibility = { animals: [] };
   const validated = { animals: [] };

   WizardDiffPresenter.hasRemovedItems = (value) => Boolean(value);
   WizardDiffPresenter.hasUnscheduledItems = (value) => Boolean(value);
   WizardDiffPresenter.hasReducedVisibility = () => false;
   WizardDiffPresenter.hasImprovedVisibility = () => false;
   WizardDiffPresenter.isValidatedItineraryEmpty = () => true;
   ItineraryWizardDraftMutator.buildWizardDraftSnapshot = () => ({ date: 'old' });
   ItineraryWizardDraftMutator.assignWizardDraft = (...args) => { assigns.push(args); };

   try {
      const state = ItineraryWizardDraftMutator.createPendingValidationState();

      ItineraryWizardDraftMutator.applyPendingValidation(state, {
         removed,
         unscheduled: null,
         reducedVisibility,
         improvedVisibility: null,
         validated,
      });

      assert.equal(assigns.length, 1);
      assert.deepEqual(state.pendingRemovedItems, removed);
      assert.equal(state.pendingUnscheduledItems, null);
      assert.equal(state.pendingReducedVisibility, null);
      assert.equal(state.pendingValidatedEmpty, true);
   } finally {
      Object.assign(WizardDiffPresenter, {
         hasRemovedItems: originals.hasRemovedItems,
         hasUnscheduledItems: originals.hasUnscheduledItems,
         hasReducedVisibility: originals.hasReducedVisibility,
         hasImprovedVisibility: originals.hasImprovedVisibility,
         isValidatedItineraryEmpty: originals.isValidatedItineraryEmpty,
      });
      ItineraryWizardDraftMutator.assignWizardDraft = originals.assignWizardDraft;
      ItineraryWizardDraftMutator.buildWizardDraftSnapshot = originals.buildWizardDraftSnapshot;
   }
});


test('Test_ApplyPendingValidation_TestEmptyPayload_ExpectFlagsCleared', () => {
   const originals = {
      hasRemovedItems: WizardDiffPresenter.hasRemovedItems,
      hasUnscheduledItems: WizardDiffPresenter.hasUnscheduledItems,
      hasReducedVisibility: WizardDiffPresenter.hasReducedVisibility,
      hasImprovedVisibility: WizardDiffPresenter.hasImprovedVisibility,
      isValidatedItineraryEmpty: WizardDiffPresenter.isValidatedItineraryEmpty,
      assignWizardDraft: ItineraryWizardDraftMutator.assignWizardDraft,
      buildWizardDraftSnapshot: ItineraryWizardDraftMutator.buildWizardDraftSnapshot,
   };

   WizardDiffPresenter.hasRemovedItems = (value) => Boolean(value);
   WizardDiffPresenter.hasUnscheduledItems = (value) => Boolean(value);
   WizardDiffPresenter.hasReducedVisibility = () => false;
   WizardDiffPresenter.hasImprovedVisibility = () => false;
   WizardDiffPresenter.isValidatedItineraryEmpty = () => true;
   ItineraryWizardDraftMutator.buildWizardDraftSnapshot = () => ({ date: 'old' });
   ItineraryWizardDraftMutator.assignWizardDraft = () => {};

   try {
      const state = ItineraryWizardDraftMutator.createPendingValidationState();
      state.pendingValidatedEmpty = true;

      ItineraryWizardDraftMutator.applyPendingValidation(state, {});

      assert.equal(state.pendingValidatedEmpty, false);
   } finally {
      Object.assign(WizardDiffPresenter, {
         hasRemovedItems: originals.hasRemovedItems,
         hasUnscheduledItems: originals.hasUnscheduledItems,
         hasReducedVisibility: originals.hasReducedVisibility,
         hasImprovedVisibility: originals.hasImprovedVisibility,
         isValidatedItineraryEmpty: originals.isValidatedItineraryEmpty,
      });
      ItineraryWizardDraftMutator.assignWizardDraft = originals.assignWizardDraft;
      ItineraryWizardDraftMutator.buildWizardDraftSnapshot = originals.buildWizardDraftSnapshot;
   }
});
