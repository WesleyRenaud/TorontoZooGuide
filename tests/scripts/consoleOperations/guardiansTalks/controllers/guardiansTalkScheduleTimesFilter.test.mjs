import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkScheduleTimesFilter } from '../../../../../scripts/consoleOperations/guardiansTalks/controllers/guardiansTalkScheduleTimesFilter.js';
import { ScheduleTimesCheckboxField } from '../../../../../scripts/consoleOperations/forms/scheduleTimesCheckboxField.js';

test('Test_CreateGuardiansTalkScheduleTimesFilterController_TestRefreshAndClear_ExpectUpdates', async () => {
   const updates = [];
   const originalResolve = ScheduleTimesCheckboxField.resolveScheduleTimesListEl;
   const originalUpdate = ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList;
   ScheduleTimesCheckboxField.resolveScheduleTimesListEl = () => ({ id: 'times' });
   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = (...args) => { updates.push(args); };

   try {
      const controller = GuardiansTalkScheduleTimesFilter.createGuardiansTalkScheduleTimesFilterController({
         talkNameEl: { value: 'Tiger' },
         locationEl: { value: 'Eurasia' },
         timesEl: {},
         loadScheduleTimes: async () => ['11:00 AM', '2:00 PM'],
      });

      await controller.refresh();
      assert.equal(updates.at(-1)[1].times.length, 2);

      controller.clear();
      assert.deepEqual(updates.at(-1)[1].times, []);
      assert.equal(updates.at(-1)[1].hasWildEncounter, false);

      const emptyController = GuardiansTalkScheduleTimesFilter.createGuardiansTalkScheduleTimesFilterController({
         talkNameEl: { value: '' },
         locationEl: { value: '' },
         timesEl: {},
         loadScheduleTimes: async () => ['should-not-load'],
      });
      await emptyController.refresh();
      assert.deepEqual(updates.at(-1)[1].times, []);

      const failing = GuardiansTalkScheduleTimesFilter.createGuardiansTalkScheduleTimesFilterController({
         talkNameEl: { value: 'Tiger' },
         locationEl: { value: 'Eurasia' },
         timesEl: {},
         loadScheduleTimes: async () => { throw new Error('fail'); },
      });
      await failing.refresh();
      assert.deepEqual(updates.at(-1)[1].times, []);
   } finally {
      ScheduleTimesCheckboxField.resolveScheduleTimesListEl = originalResolve;
      ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = originalUpdate;
   }
});

test('Test_CreateGuardiansTalkScheduleTimesFilterController_TestDefaultLoader_ExpectClientTimes', async () => {
   const { ConsoleOperationsClient } = await import(
      '../../../../../scripts/api/consoleOperationsClient.js'
   );
   const originalGet = ConsoleOperationsClient.getGuardiansTalkScheduleTimes;
   const updates = [];
   const originalResolve = ScheduleTimesCheckboxField.resolveScheduleTimesListEl;
   const originalUpdate = ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList;
   ScheduleTimesCheckboxField.resolveScheduleTimesListEl = () => ({ id: 'times' });
   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = (...args) => { updates.push(args); };
   ConsoleOperationsClient.getGuardiansTalkScheduleTimes = async ({ talk, location }) => {
      assert.equal(talk, 'Tiger');
      assert.equal(location, 'Eurasia');
      return { times: ['10:00 AM'] };
   };

   try {
      const controller = GuardiansTalkScheduleTimesFilter.createGuardiansTalkScheduleTimesFilterController({
         talkNameEl: { value: 'Tiger' },
         locationEl: { value: 'Eurasia' },
         timesEl: {},
      });
      await controller.refresh();
      assert.deepEqual(updates.at(-1)[1].times, ['10:00 AM']);
   } finally {
      ConsoleOperationsClient.getGuardiansTalkScheduleTimes = originalGet;
      ScheduleTimesCheckboxField.resolveScheduleTimesListEl = originalResolve;
      ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = originalUpdate;
   }
});
