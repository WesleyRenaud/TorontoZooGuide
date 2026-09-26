import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryShape } from '../../../../scripts/itinerary/itineraryShape.js';
import { RegionStorageStore } from '../../../../scripts/itinerary/selectors/regionSelector/regionStorageStore.js';
import { WizardFinalizerHelper } from '../../../../scripts/itinerary/wizard/wizardFinalizerHelper.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ClearWizardMount_TestChildren_ExpectCleared', () => {
   const mountEl = document.createElement('div');
   mountEl.appendChild(document.createElement('span'));

   WizardFinalizerHelper.clearWizardMount(mountEl);

   assert.equal(mountEl.children.length, 0);
});


test('Test_ClearWizardMount_TestNull_ExpectNoOp', () => {
   const mountEl = null;

   assert.doesNotThrow(() => {
      WizardFinalizerHelper.clearWizardMount(mountEl);
   });
});


test('Test_CreateFinalItineraryDraft_TestNormalize_ExpectNormalized', () => {
   const animal = { species: 'African Lion' };
   const source = { animals: [animal] };
   const normalize = (value) => ({ ...value, normalized: true });

   const draft = WizardFinalizerHelper.createFinalItineraryDraft(source, normalize);

   assert.deepEqual(draft, {
      animals: [animal],
      normalized: true,
   });
});


test('Test_CreateFinalItineraryDraft_TestDefaultNormalizer_ExpectNormalized', () => {
   const original = ItineraryShape.normalizeItineraryDraft;
   ItineraryShape.normalizeItineraryDraft = (value) => ({ ...value, viaDefault: true });
   const date = '2026-06-15';
   const source = { date };

   try {
      const draft = WizardFinalizerHelper.createFinalItineraryDraft(source);

      assert.deepEqual(draft, { date, viaDefault: true });
   } finally {
      ItineraryShape.normalizeItineraryDraft = original;
   }
});


test('Test_SaveFinalItinerary_TestOptions_ExpectSaverCalled', () => {
   const calls = [];
   const finalItinerary = { date: '2026-06-15' };
   const selectedExhibits = ['African Rainforest'];
   const originalLoad = RegionStorageStore.loadSelectedNames;
   RegionStorageStore.loadSelectedNames = () => selectedExhibits;
   const saved = 'saved';
   const options = { overridingConflictingGuardiansTalks: true };
   const saveItinerary = (itinerary, nextOptions) => {
      calls.push({ itinerary, options: nextOptions });
      return saved;
   };

   try {
      const result = WizardFinalizerHelper.saveFinalItinerary(
         finalItinerary,
         options,
         saveItinerary
      );

      assert.equal(result, saved);
      assert.equal(calls.length, 1);
      assert.equal(calls[Position.FIRST].itinerary, finalItinerary);
      assert.equal(
         calls[Position.FIRST].options.overridingConflictingGuardiansTalks,
         options.overridingConflictingGuardiansTalks
      );
      assert.deepEqual(calls[Position.FIRST].options.selectedExhibits, selectedExhibits);
   } finally {
      RegionStorageStore.loadSelectedNames = originalLoad;
   }
});
