import assert from 'node:assert/strict';
import test from 'node:test';

import { ValidationFragment } from '../../../../scripts/itinerary/wizard/validationFragment.js';
import { RemovedItemsFragment } from '../../../../scripts/itinerary/panel/components/removedItemsFragment.js';
import { ItineraryService } from '../../../../scripts/itinerary/itineraryService.js';

test('Test_ShowWizardValidationPopupIfNeeded_TestEmpty_ExpectNoPopup', () => {
   const original = RemovedItemsFragment.showRemovedItemsPopup;
   const calls = [];
   RemovedItemsFragment.showRemovedItemsPopup = (args) => { calls.push(args); };

   try {
      ValidationFragment.showWizardValidationPopupIfNeeded({
         mountEl: {},
         pendingValidation: {},
      });
      assert.deepEqual(calls, []);
   } finally {
      RemovedItemsFragment.showRemovedItemsPopup = original;
   }
});

test('Test_ShowWizardValidationPopupIfNeeded_TestRemoved_ExpectPopupAndAccept', () => {
   const originalShow = RemovedItemsFragment.showRemovedItemsPopup;
   const originalAccept = ItineraryService.acceptItinerary;
   const calls = [];
   const accepts = [];

   RemovedItemsFragment.showRemovedItemsPopup = (args) => { calls.push(args); };
   ItineraryService.acceptItinerary = async (payload) => { accepts.push(payload); };

   try {
      const onViewAlternatives = () => {};
      ValidationFragment.showWizardValidationPopupIfNeeded({
         mountEl: { id: 'mount' },
         pendingValidation: {
            removed: { animals: [{ species: 'Lion' }] },
            adjustments: [],
         },
         onViewAlternatives,
      });

      assert.equal(calls.length, 1);
      assert.equal(calls[0].mountEl.id, 'mount');
      assert.equal(calls[0].onViewAlternatives, onViewAlternatives);
      calls[0].onAccept({ animalsToKeep: ['Lion'], attractionsToKeep: [] });
      assert.deepEqual(accepts, [{ animalsToKeep: ['Lion'], attractionsToKeep: [] }]);
      calls[0].onDismiss();
   } finally {
      RemovedItemsFragment.showRemovedItemsPopup = originalShow;
      ItineraryService.acceptItinerary = originalAccept;
   }
});
