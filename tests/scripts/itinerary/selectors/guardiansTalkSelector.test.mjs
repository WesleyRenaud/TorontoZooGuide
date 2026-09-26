import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkSelector } from '../../../../scripts/itinerary/selectors/guardiansTalkSelector.js';
import { CreateScheduledOccurrenceSelector } from '../../../../scripts/itinerary/selectors/createScheduledOccurrenceSelector.js';
import { GuardiansTalkSelectorModel } from '../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { StorageKeys } from '../../../../scripts/itinerary/storageKeys.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_CreateItineraryGuardiansTalkSelectorController_TestWiring_ExpectFactoryOptions', () => {
   const original = CreateScheduledOccurrenceSelector.createScheduledOccurrenceSelectorController;
   let captured;
   const controllerResult = { selector: true };
   const callbacks = {
      mountEl: { id: 'mount' },
      onNext: () => {},
      onPrev: () => {},
      onFinish: () => {},
      onClose: () => {},
   };
   CreateScheduledOccurrenceSelector.createScheduledOccurrenceSelectorController = (options) => {
      captured = options;
      return controllerResult;
   };

   try {
      const controller = GuardiansTalkSelector.createItineraryGuardiansTalkSelectorController(callbacks);

      assert.deepEqual(controller, controllerResult);
      assert.equal(GuardiansTalkSelector.STORAGE_KEY, StorageKeys.GUARDIANS_KEY);
      assert.equal(captured.mountEl, callbacks.mountEl);
      assert.equal(captured.storageKey, GuardiansTalkSelector.STORAGE_KEY);
      assert.equal(captured.responseKey, 'guardians_talks');
      assert.equal(captured.searchFlag, 'includeGuardiansTalks');
      assert.equal(captured.imageDirectory, 'guardians-talks');
      assert.equal(captured.defaultTitle, Strings.itinerary.selectors.talkFallback);
      assert.equal(captured.heading, Strings.site.nav.meetTheGuardians);
      assert.equal(captured.getName, GuardiansTalkSelectorModel.getGuardiansTalkName);
      assert.equal(captured.getId, GuardiansTalkSelectorModel.getGuardiansTalkId);
      assert.equal(captured.getPrimaryValue, GuardiansTalkSelectorModel.getGuardiansTalkLocation);
      assert.equal(captured.getTimeOfDay, GuardiansTalkSelectorModel.getGuardiansTalkScheduleStart);
      assert.equal(captured.readStoredFields, GuardiansTalkSelectorModel.readGuardiansTalkStoredFields);
      assert.equal(captured.buildSelectionFields, GuardiansTalkSelectorModel.buildGuardiansTalkSelectionFields);
      assert.deepEqual(captured.emptyStoredFields, {
         location: '',
         start_time: '',
         end_time: '',
      });
   } finally {
      CreateScheduledOccurrenceSelector.createScheduledOccurrenceSelectorController = original;
   }
});
