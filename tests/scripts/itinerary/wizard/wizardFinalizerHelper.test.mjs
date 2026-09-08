import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryShape } from '../../../../scripts/itinerary/itineraryShape.js';
import { RegionStorageStore } from '../../../../scripts/itinerary/selectors/regionSelector/regionStorageStore.js';
import { WizardFinalizerHelper } from '../../../../scripts/itinerary/wizard/wizardFinalizerHelper.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ClearWizardMount_TestChildren_ExpectCleared', () => {
   const mountEl = document.createElement('div');
   mountEl.appendChild(document.createElement('span'));
   WizardFinalizerHelper.clearWizardMount(mountEl);
   assert.equal(mountEl.children.length, 0);
   WizardFinalizerHelper.clearWizardMount(null);
});

test('Test_CreateFinalItineraryDraft_TestNormalize_ExpectNormalized', () => {
   const draft = WizardFinalizerHelper.createFinalItineraryDraft(
      { animals: [{ species: 'African Lion' }] },
      (value) => ({ ...value, normalized: true })
   );
   assert.deepEqual(draft, {
      animals: [{ species: 'African Lion' }],
      normalized: true,
   });

   const original = ItineraryShape.normalizeItineraryDraft;
   ItineraryShape.normalizeItineraryDraft = (value) => ({ ...value, viaDefault: true });
   try {
      assert.deepEqual(
         WizardFinalizerHelper.createFinalItineraryDraft({ date: '2026-06-15' }),
         { date: '2026-06-15', viaDefault: true }
      );
   } finally {
      ItineraryShape.normalizeItineraryDraft = original;
   }
});

test('Test_ShowEmptySelectionPopup_TestConfig_ExpectPopupArgs', () => {
   const calls = [];
   const mountEl = document.createElement('div');

   WizardFinalizerHelper.showEmptySelectionPopup(mountEl, (args) => {
      calls.push(args);
   });

   assert.deepEqual(calls, [{
      mountEl,
      title: Strings.itinerary.noItemsSelected.title,
      message: Strings.itinerary.noItemsSelected.message,
      buttonText: Strings.itinerary.noItemsSelected.button,
   }]);
});

test('Test_SaveFinalItinerary_TestOptions_ExpectSaverCalled', () => {
   const calls = [];
   const finalItinerary = { date: '2026-06-15' };
   const originalLoad = RegionStorageStore.loadSelectedNames;
   RegionStorageStore.loadSelectedNames = () => ['African Rainforest'];

   try {
      const result = WizardFinalizerHelper.saveFinalItinerary(
         finalItinerary,
         { overridingConflictingGuardiansTalks: true },
         (itinerary, options) => {
            calls.push({ itinerary, options });
            return 'saved';
         }
      );

      assert.equal(result, 'saved');
      assert.equal(calls.length, 1);
      assert.equal(calls[0].itinerary, finalItinerary);
      assert.equal(calls[0].options.overridingConflictingGuardiansTalks, true);
      assert.deepEqual(calls[0].options.selectedExhibits, ['African Rainforest']);
   } finally {
      RegionStorageStore.loadSelectedNames = originalLoad;
   }
});
