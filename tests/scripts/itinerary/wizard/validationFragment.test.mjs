import assert from 'node:assert/strict';
import test from 'node:test';

import { ValidationFragment } from '../../../../scripts/itinerary/wizard/validationFragment.js';
import { RemovedItemsFragment } from '../../../../scripts/itinerary/panel/components/removedItemsFragment.js';
import { ItineraryService } from '../../../../scripts/itinerary/itineraryService.js';
import { Position } from '../../../../scripts/shared/enums/position.js';


test('Test_ShowWizardValidationPopupIfNeeded_TestEmpty_ExpectNoPopup', () => {
   const original = RemovedItemsFragment.showRemovedItemsPopup;
   const calls = [];
   RemovedItemsFragment.showRemovedItemsPopup = (args) => { calls.push(args); };
   const mountEl = {};
   const pendingValidation = {};

   try {
      ValidationFragment.showWizardValidationPopupIfNeeded({
         mountEl,
         pendingValidation,
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
   const onViewAlternatives = () => {};
   const mountId = 'mount';
   const species = 'African Lion';
   const acceptPayload = { animalsToKeep: [species], attractionsToKeep: [] };

   try {
      ValidationFragment.showWizardValidationPopupIfNeeded({
         mountEl: { id: mountId },
         pendingValidation: {
            removed: { animals: [{ species }] },
            adjustments: [],
         },
         onViewAlternatives,
      });

      assert.equal(calls.length, 1);
      assert.equal(calls[Position.FIRST].mountEl.id, mountId);
      assert.equal(calls[Position.FIRST].onViewAlternatives, onViewAlternatives);

      calls[Position.FIRST].onAccept(acceptPayload);

      assert.deepEqual(accepts, [acceptPayload]);

      calls[Position.FIRST].onDismiss();
   } finally {
      RemovedItemsFragment.showRemovedItemsPopup = originalShow;
      ItineraryService.acceptItinerary = originalAccept;
   }
});
