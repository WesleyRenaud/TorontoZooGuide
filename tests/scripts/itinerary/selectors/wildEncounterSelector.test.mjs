import assert from 'node:assert/strict';
import test from 'node:test';

import { WildEncounterSelector } from '../../../../scripts/itinerary/selectors/wildEncounterSelector.js';
import { CreateScheduledOccurrenceSelector } from '../../../../scripts/itinerary/selectors/createScheduledOccurrenceSelector.js';
import { WildEncounterSelectorModel } from '../../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterSelectorModel.js';
import { StorageKeys } from '../../../../scripts/itinerary/storageKeys.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_CreateItineraryWildEncounterSelectorController_TestWiring_ExpectFactoryOptions', () => {
   const original = CreateScheduledOccurrenceSelector.createScheduledOccurrenceSelectorController;
   let captured;
   const controllerResult = { selector: true };
   const mountEl = { id: 'mount' };
   CreateScheduledOccurrenceSelector.createScheduledOccurrenceSelectorController = (options) => {
      captured = options;
      return controllerResult;
   };

   try {
      const controller = WildEncounterSelector.createItineraryWildEncounterSelectorController({
         mountEl,
      });

      assert.deepEqual(controller, controllerResult);
      assert.equal(WildEncounterSelector.STORAGE_KEY, StorageKeys.WILD_KEY);
      assert.equal(captured.storageKey, WildEncounterSelector.STORAGE_KEY);
      assert.equal(captured.responseKey, 'wild_encounters');
      assert.equal(captured.searchFlag, 'includeWildEncounters');
      assert.equal(captured.imageDirectory, 'wild-encounters');
      assert.equal(captured.defaultTitle, Strings.entityLabels.wildEncounter);
      assert.equal(captured.heading, Strings.site.nav.wildEncounters);
      assert.equal(captured.getName, WildEncounterSelectorModel.getWildEncounterName);
      assert.equal(captured.getId, WildEncounterSelectorModel.getWildEncounterId);
      assert.equal(captured.getPrimaryValue, WildEncounterSelectorModel.getWildEncounterMeetingSpot);
      assert.equal(captured.getTimeOfDay, WildEncounterSelectorModel.getWildEncounterScheduleStart);
      assert.equal(captured.getLink, WildEncounterSelectorModel.getWildEncounterLink);
      assert.equal(captured.readStoredFields, WildEncounterSelectorModel.readWildEncounterStoredFields);
      assert.equal(captured.buildSelectionFields, WildEncounterSelectorModel.buildWildEncounterSelectionFields);
      assert.deepEqual(captured.emptyStoredFields, {
         meeting_spot: '',
         start_time: '',
         end_time: '',
      });
   } finally {
      CreateScheduledOccurrenceSelector.createScheduledOccurrenceSelectorController = original;
   }
});
