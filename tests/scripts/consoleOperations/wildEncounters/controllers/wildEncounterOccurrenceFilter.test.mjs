import assert from 'node:assert/strict';
import test from 'node:test';

import { WildEncounterOccurrenceFilter } from '../../../../../scripts/consoleOperations/wildEncounters/controllers/wildEncounterOccurrenceFilter.js';
import { OccurrenceFilterController } from '../../../../../scripts/consoleOperations/helpers/occurrenceFilterController.js';
import { ScheduleTimesCheckboxField } from '../../../../../scripts/consoleOperations/forms/scheduleTimesCheckboxField.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';

test('Test_CreateWildEncounterOccurrenceFilterController_TestWiring_ExpectFilter', async () => {
   const originalCreate = OccurrenceFilterController.createOccurrenceFilterController;
   const originalResolve = ScheduleTimesCheckboxField.resolveScheduleTimesListEl;
   const originalUpdate = ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList;
   let captured;
   const updates = [];

   OccurrenceFilterController.createOccurrenceFilterController = (options) => {
      captured = options;
      return { filter: true };
   };
   ScheduleTimesCheckboxField.resolveScheduleTimesListEl = () => ({ id: 'list' });
   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = (...args) => { updates.push(args); };

   try {
      assert.deepEqual(
         WildEncounterOccurrenceFilter.createWildEncounterOccurrenceFilterController({
            wildEncounterEl: { value: 'Giraffe' },
            dateEl: { value: '2026-06-15' },
            timesEl: {},
         }),
         { filter: true }
      );

      captured.populateTimes(['11:00 AM']);
      assert.equal(updates.length, 1);
      assert.deepEqual(captured.getSelectionValues(), { wildEncounter: 'Giraffe' });
      assert.equal(captured.isSelectionReady({ wildEncounter: 'Giraffe' }), true);

      const originalGet = ConsoleOperationsClient.getWildEncounterOccurrences;
      ConsoleOperationsClient.getWildEncounterOccurrences = async () => ({
         occurrences: [{ time: '1:00 PM' }],
      });
      try {
         assert.deepEqual(
            await captured.loadOccurrences({ wildEncounter: 'Giraffe' }),
            [{ time: '1:00 PM' }]
         );
      } finally {
         ConsoleOperationsClient.getWildEncounterOccurrences = originalGet;
      }
   } finally {
      OccurrenceFilterController.createOccurrenceFilterController = originalCreate;
      ScheduleTimesCheckboxField.resolveScheduleTimesListEl = originalResolve;
      ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = originalUpdate;
   }
});
