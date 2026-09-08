import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkOccurrenceFilter } from '../../../../../scripts/consoleOperations/guardiansTalks/controllers/guardiansTalkOccurrenceFilter.js';
import { OccurrenceFilterController } from '../../../../../scripts/consoleOperations/helpers/occurrenceFilterController.js';
import { ScheduleTimesCheckboxField } from '../../../../../scripts/consoleOperations/forms/scheduleTimesCheckboxField.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';

test('Test_CreateGuardiansTalkOccurrenceFilterController_TestWiring_ExpectFilter', async () => {
   const originalCreate = OccurrenceFilterController.createOccurrenceFilterController;
   let captured;
   OccurrenceFilterController.createOccurrenceFilterController = (options) => {
      captured = options;
      return { filter: true };
   };
   const originalResolve = ScheduleTimesCheckboxField.resolveScheduleTimesListEl;
   const originalUpdate = ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList;
   ScheduleTimesCheckboxField.resolveScheduleTimesListEl = () => ({});
   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = () => {};

   try {
      GuardiansTalkOccurrenceFilter.createGuardiansTalkOccurrenceFilterController({
         talkNameEl: { value: 'Tiger' },
         locationEl: { value: 'Eurasia' },
         dateEl: { value: '2026-06-15' },
         timesEl: {},
      });

      assert.deepEqual(captured.getSelectionValues(), {
         talk: 'Tiger',
         location: 'Eurasia',
      });
      assert.equal(captured.isSelectionReady({ talk: 'Tiger', location: 'Eurasia' }), true);
      captured.populateTimes(['11:00 AM']);

      const originalGet = ConsoleOperationsClient.getGuardiansTalkOccurrences;
      ConsoleOperationsClient.getGuardiansTalkOccurrences = async () => ({
         occurrences: [{ time: '11:00 AM' }],
      });
      try {
         assert.deepEqual(
            await captured.loadOccurrences({ talk: 'Tiger', location: 'Eurasia' }),
            [{ time: '11:00 AM' }]
         );
      } finally {
         ConsoleOperationsClient.getGuardiansTalkOccurrences = originalGet;
      }
   } finally {
      OccurrenceFilterController.createOccurrenceFilterController = originalCreate;
      ScheduleTimesCheckboxField.resolveScheduleTimesListEl = originalResolve;
      ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = originalUpdate;
   }
});
