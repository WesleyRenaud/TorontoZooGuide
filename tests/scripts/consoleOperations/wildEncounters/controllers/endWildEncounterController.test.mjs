import assert from 'node:assert/strict';
import test from 'node:test';

import { EndWildEncounterController } from '../../../../../scripts/consoleOperations/wildEncounters/controllers/endWildEncounterController.js';
import { EndRecurringScheduleFormController } from '../../../../../scripts/consoleOperations/forms/endRecurringScheduleFormController.js';
import { ScheduleTimesCheckboxField } from '../../../../../scripts/consoleOperations/forms/scheduleTimesCheckboxField.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateEndWildEncounterScheduleController_TestWiring_ExpectFormCallbacks', async () => {
   const originalCreate = EndRecurringScheduleFormController.createEndRecurringScheduleFormController;
   const originalGetTimes = ScheduleTimesCheckboxField.getSelectedScheduleTimes;
   const originalLoad = ConsoleOptionsLoader.loadWildEncounters;
   const originalPopulate = ConsoleDropdownPopulator.populateWildEncounterDropdown;
   const originalGetField = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalEnd = ConsoleOperationsClient.endWildEncounterSchedule;
   let captured;
   const filterCalls = [];

   EndRecurringScheduleFormController.createEndRecurringScheduleFormController = (options) => {
      captured = options;
      return { controller: true };
   };
   ScheduleTimesCheckboxField.getSelectedScheduleTimes = () => ['11:00 AM'];
   ConsoleOptionsLoader.loadWildEncounters = async () => [{ name: 'Giraffe' }];
   ConsoleDropdownPopulator.populateWildEncounterDropdown = (...args) => {
      filterCalls.push(['populate', ...args]);
   };
   ControllerHelper.getFieldValue = () => 'Giraffe Encounter';
   ControllerHelper.resetFormFields = (...args) => {
      filterCalls.push(['reset', ...args]);
   };
   ConsoleOperationsClient.endWildEncounterSchedule = async (payload) => payload;

   const wildEncounterEl = document.createElement('select');
   const scheduleTimesFilterController = {
      refresh: async () => {
         filterCalls.push('refresh');
      },
      clear: () => {
         filterCalls.push('clear');
      },
   };

   try {
      const result = EndWildEncounterController.createEndWildEncounterScheduleController({
         wildEncounterEl,
         timesEl: {},
         endDateEl: {},
         scheduleTimesFilterController,
         statusEl: {},
      });

      assert.deepEqual(result, { controller: true });
      assert.equal(captured.loadErrorMessage, Strings.loadErrors.wildEncounters);
      assert.deepEqual(captured.getSelectionValues(), {
         wildEncounter: 'Giraffe Encounter',
         times: ['11:00 AM'],
      });
      assert.equal(
         captured.validateSelection({ wildEncounter: '', times: [] }),
         Strings.validation.entityRequired(Strings.entityLabels.wildEncounter)
      );
      assert.equal(
         captured.validateSelection({ wildEncounter: 'Giraffe', times: [] }),
         Strings.validation.entityRequired(Strings.labels.encounterTimes)
      );
      assert.equal(
         captured.validateSelection({ wildEncounter: 'Giraffe', times: ['11:00 AM'] }),
         null
      );
      assert.equal(
         captured.successMessage({ wildEncounter: 'Giraffe' }),
         Strings.status.scheduleEnded('Giraffe')
      );

      await captured.prepareForm();
      assert.ok(filterCalls.some((call) => call === 'refresh'));
      assert.ok(filterCalls.some((call) => Array.isArray(call) && call[0] === 'populate'));

      captured.resetSelection();
      assert.ok(filterCalls.includes('clear'));

      assert.deepEqual(
         await captured.submitEndSchedule({
            wildEncounter: 'Giraffe',
            times: ['11:00 AM'],
            endDate: '',
         }),
         {
            wildEncounter: 'Giraffe',
            times: ['11:00 AM'],
            endDate: null,
         }
      );

      filterCalls.length = 0;
      await wildEncounterEl.listeners.change();
      assert.deepEqual(filterCalls, ['clear', 'refresh']);
   } finally {
      EndRecurringScheduleFormController.createEndRecurringScheduleFormController = originalCreate;
      ScheduleTimesCheckboxField.getSelectedScheduleTimes = originalGetTimes;
      ConsoleOptionsLoader.loadWildEncounters = originalLoad;
      ConsoleDropdownPopulator.populateWildEncounterDropdown = originalPopulate;
      ControllerHelper.getFieldValue = originalGetField;
      ControllerHelper.resetFormFields = originalReset;
      ConsoleOperationsClient.endWildEncounterSchedule = originalEnd;
   }
});
