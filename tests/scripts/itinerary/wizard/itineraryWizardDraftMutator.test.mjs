import assert from 'node:assert/strict';
import test from 'node:test';

import { DraftStore } from '../../../../scripts/itinerary/draftStore.js';
import { ItineraryShape } from '../../../../scripts/itinerary/itineraryShape.js';
import { ItineraryWizardDraftMutator } from '../../../../scripts/itinerary/wizard/itineraryWizardDraftMutator.js';
import { WizardDiffPresenter } from '../../../../scripts/itinerary/wizard/diff/wizardDiffPresenter.js';

test('Test_CreatePendingValidationState_TestDefaults_ExpectNullFlags', () => {
   assert.deepEqual(ItineraryWizardDraftMutator.createPendingValidationState(), {
      pendingRemovedItems: null,
      pendingUnscheduledItems: null,
      pendingReducedVisibility: null,
      pendingImprovedVisibility: null,
      pendingValidatedEmpty: false,
   });
});

test('Test_BuildWizardDraftSnapshot_TestClone_ExpectShapeClone', () => {
   const original = ItineraryShape.cloneItineraryDraft;
   ItineraryShape.cloneItineraryDraft = (state) => ({ ...state, cloned: true });

   try {
      assert.deepEqual(
         ItineraryWizardDraftMutator.buildWizardDraftSnapshot({ date: '2026-06-15' }),
         { date: '2026-06-15', cloned: true }
      );
   } finally {
      ItineraryShape.cloneItineraryDraft = original;
   }
});

test('Test_WriteDraftState_TestDelegates_ExpectDraftStore', () => {
   const original = DraftStore.writeStoredItineraryDraft;
   const drafts = [];
   DraftStore.writeStoredItineraryDraft = (draft) => { drafts.push(draft); };

   try {
      ItineraryWizardDraftMutator.writeDraftState({ date: '2026-06-15' });
      assert.deepEqual(drafts, [{ date: '2026-06-15' }]);
   } finally {
      DraftStore.writeStoredItineraryDraft = original;
   }
});

test('Test_AssignWizardDraft_TestNormalized_ExpectCopiedArrays', () => {
   const original = ItineraryShape.normalizeItineraryDraft;
   ItineraryShape.normalizeItineraryDraft = () => ({
      date: '2026-06-15',
      animals: [{ species: 'Lion' }],
      attractions: ['Carousel'],
      guardiansTalks: [{ name: 'Talk' }],
      wildEncounters: [{ name: 'Encounter' }],
      transportations: [{ name: 'Zoomobile' }],
      transportationStations: [{ name: 'Station' }],
   });

   try {
      const state = {};
      ItineraryWizardDraftMutator.assignWizardDraft(state, {});
      assert.equal(state.date, '2026-06-15');
      assert.deepEqual(state.animals, [{ species: 'Lion' }]);
      assert.deepEqual(state.attractions, ['Carousel']);
      assert.notEqual(state.animals, ItineraryShape.normalizeItineraryDraft().animals);
   } finally {
      ItineraryShape.normalizeItineraryDraft = original;
   }
});

test('Test_ConsumePendingValidationState_TestResets_ExpectSnapshot', () => {
   const state = {
      pendingRemovedItems: { animals: [1] },
      pendingUnscheduledItems: { animals: [2] },
      pendingReducedVisibility: { animals: [3] },
      pendingImprovedVisibility: { animals: [4] },
      pendingValidatedEmpty: true,
   };

   assert.deepEqual(ItineraryWizardDraftMutator.consumePendingValidationState(state), {
      removed: { animals: [1] },
      unscheduled: { animals: [2] },
      reducedVisibility: { animals: [3] },
      improvedVisibility: { animals: [4] },
      isEmptyItinerary: true,
   });
   assert.equal(state.pendingRemovedItems, null);
   assert.equal(state.pendingValidatedEmpty, false);
});

test('Test_ApplySelectionUpdate_TestNullAndValue_ExpectFlags', () => {
   const state = { animals: [{ species: 'Old' }] };

   assert.equal(
      ItineraryWizardDraftMutator.applySelectionUpdate(state, 'animals', null, {
         preserveOnInvalid: true,
      }),
      false
   );
   assert.deepEqual(state.animals, [{ species: 'Old' }]);

   assert.equal(ItineraryWizardDraftMutator.applySelectionUpdate(state, 'animals', null), true);
   assert.deepEqual(state.animals, []);

   assert.equal(
      ItineraryWizardDraftMutator.applySelectionUpdate(state, 'animals', [{ species: 'Lion' }]),
      true
   );
   assert.deepEqual(state.animals, [{ species: 'Lion' }]);
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
         removed: { animals: [1] },
         unscheduled: null,
         reducedVisibility: { animals: [] },
         improvedVisibility: null,
         validated: { animals: [] },
      });

      assert.equal(assigns.length, 1);
      assert.deepEqual(state.pendingRemovedItems, { animals: [1] });
      assert.equal(state.pendingUnscheduledItems, null);
      assert.equal(state.pendingReducedVisibility, null);
      assert.equal(state.pendingValidatedEmpty, true);

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
