import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleTimesCheckboxField } from '../../../../../scripts/consoleOperations/forms/scheduleTimesCheckboxField.js';
import { WildEncounterScheduleTimesFilter } from '../../../../../scripts/consoleOperations/wildEncounters/controllers/wildEncounterScheduleTimesFilter.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';
import { ConsoleScheduleTimesCheckboxFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleScheduleTimesCheckboxFieldBuilder.js';

installDomTestHooks();

test('Test_CreateWildEncounterScheduleTimesFilterController_TestSelectedEncounter_ExpectTimesLoaded', async () => {
   const wildEncounterEl = document.createElement('select');
   const fieldEl = ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
      label: 'Encounter times',
      inputId: 'testWildEncounterScheduleTimes',
   });
   const timesEl = fieldEl.querySelector('.console-operations-schedule-times-list');
   wildEncounterEl.value = 'African Rainforest';

   const controller = WildEncounterScheduleTimesFilter.createWildEncounterScheduleTimesFilterController({
      wildEncounterEl,
      timesEl,
      loadScheduleTimes: async ({ wildEncounter }) => {
         assert.equal(wildEncounter, 'African Rainforest');
         return [ '2:00 PM', '3:30 PM' ];
      },
   });

   await controller.refresh();

   const checkboxes = [
      ...timesEl.children ?? [],
   ].flatMap((optionEl) =>
      (optionEl.children ?? []).filter((child) => child.type === 'checkbox')
   );

   assert.equal(timesEl.hidden, false);
   assert.equal(checkboxes.length, 2);
   assert.equal(checkboxes[0].value, '2:00 PM');
   assert.equal(checkboxes[1].value, '3:30 PM');
   assert.equal(checkboxes[0].checked, false);
});

test('Test_CreateWildEncounterScheduleTimesFilterController_TestSingleTime_ExpectAutoSelect', async () => {
   const wildEncounterEl = document.createElement('select');
   const fieldEl = ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
      label: 'Encounter times',
      inputId: 'testWildEncounterScheduleTimesSingle',
   });
   const timesEl = fieldEl.querySelector('.console-operations-schedule-times-list');
   wildEncounterEl.value = 'African Rainforest';

   const controller = WildEncounterScheduleTimesFilter.createWildEncounterScheduleTimesFilterController({
      wildEncounterEl,
      timesEl,
      loadScheduleTimes: async () => [ '1:30 AM' ],
   });

   await controller.refresh();

   assert.equal(
      timesEl.querySelector('.console-operations-schedule-times-single')?.textContent,
      '1:30 AM'
   );
   assert.deepEqual(ScheduleTimesCheckboxField.getSelectedScheduleTimes(timesEl), [ '1:30 AM' ]);
});

test('Test_CreateWildEncounterScheduleTimesFilterController_TestDefaultLoaderClearAndError_ExpectHandled', async () => {
   const wildEncounterEl = document.createElement('select');
   const fieldEl = ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
      label: 'Encounter times',
      inputId: 'testWildEncounterScheduleTimesDefault',
   });
   const timesEl = fieldEl.querySelector('.console-operations-schedule-times-list');
   const { ConsoleOperationsClient } = await import(
      '../../../../../scripts/api/consoleOperationsClient.js'
   );
   const originalGet = ConsoleOperationsClient.getWildEncounterScheduleTimes;
   ConsoleOperationsClient.getWildEncounterScheduleTimes = async ({ wildEncounter }) => {
      assert.equal(wildEncounter, 'Giraffe');
      return { times: [ '4:00 PM' ] };
   };

   try {
      const controller = WildEncounterScheduleTimesFilter.createWildEncounterScheduleTimesFilterController({
         wildEncounterEl,
         timesEl,
      });

      wildEncounterEl.value = 'Giraffe';
      await controller.refresh();
      assert.deepEqual(ScheduleTimesCheckboxField.getSelectedScheduleTimes(timesEl), [ '4:00 PM' ]);

      controller.clear();
      assert.deepEqual(ScheduleTimesCheckboxField.getSelectedScheduleTimes(timesEl), []);

      wildEncounterEl.value = '';
      await controller.refresh();
      assert.deepEqual(ScheduleTimesCheckboxField.getSelectedScheduleTimes(timesEl), []);

      const failing = WildEncounterScheduleTimesFilter.createWildEncounterScheduleTimesFilterController({
         wildEncounterEl,
         timesEl,
         loadScheduleTimes: async () => {
            throw new Error('load failed');
         },
      });
      wildEncounterEl.value = 'Giraffe';
      await failing.refresh();
      assert.deepEqual(ScheduleTimesCheckboxField.getSelectedScheduleTimes(timesEl), []);
   } finally {
      ConsoleOperationsClient.getWildEncounterScheduleTimes = originalGet;
   }
});
