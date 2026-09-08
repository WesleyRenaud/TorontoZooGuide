import assert from 'node:assert/strict';
import test from 'node:test';

import { EndGuardiansTalkController } from '../../../../../scripts/consoleOperations/guardiansTalks/controllers/endGuardiansTalkController.js';
import { EndRecurringScheduleFormController } from '../../../../../scripts/consoleOperations/forms/endRecurringScheduleFormController.js';
import { ScheduleTimesCheckboxField } from '../../../../../scripts/consoleOperations/forms/scheduleTimesCheckboxField.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateEndGuardiansTalkScheduleController_TestWiring_ExpectFormCallbacks', async () => {
   const originalCreate = EndRecurringScheduleFormController.createEndRecurringScheduleFormController;
   const originalGetTimes = ScheduleTimesCheckboxField.getSelectedScheduleTimes;
   const originalGetField = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalPopulate = ConsoleDropdownPopulator.populateGuardiansTalkDropdown;
   const originalEnd = ConsoleOperationsClient.endGuardiansTalkSchedule;
   let captured;
   const filterCalls = [];

   EndRecurringScheduleFormController.createEndRecurringScheduleFormController = (options) => {
      captured = options;
      return { controller: true };
   };
   ScheduleTimesCheckboxField.getSelectedScheduleTimes = () => ['11:00 AM'];
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = (...args) => { filterCalls.push(['reset', ...args]); };
   ConsoleDropdownPopulator.populateGuardiansTalkDropdown = (...args) => { filterCalls.push(['populate', ...args]); };
   ConsoleOperationsClient.endGuardiansTalkSchedule = async (payload) => payload;

   const talkNameEl = document.createElement('select');
   talkNameEl.value = 'Tiger Talk';
   const locationEl = document.createElement('select');
   locationEl.value = 'Eurasia';
   const talkLocationFilterController = {
      refreshLocations: async () => { filterCalls.push('refreshLocations'); },
      clear: () => { filterCalls.push('clearTalk'); },
   };
   const scheduleTimesFilterController = {
      refresh: async () => { filterCalls.push('refreshTimes'); },
      clear: () => { filterCalls.push('clearTimes'); },
   };

   try {
      const result = EndGuardiansTalkController.createEndGuardiansTalkScheduleController({
         talkNameEl,
         locationEl,
         timesEl: {},
         endDateEl: {},
         talkLocationFilterController,
         scheduleTimesFilterController,
      });

      assert.deepEqual(result, { controller: true });
      assert.equal(captured.loadErrorMessage, Strings.loadErrors.locations);
      assert.deepEqual(captured.getSelectionValues(), {
         talk: 'Tiger Talk',
         location: 'Eurasia',
         times: ['11:00 AM'],
      });
      assert.equal(
         captured.validateSelection({ talk: '', location: '', times: [] }),
         Strings.validation.entityRequired(Strings.labels.location)
      );
      assert.equal(
         captured.validateSelection({ talk: '', location: 'Eurasia', times: [] }),
         Strings.validation.entityRequired(Strings.labels.talkName)
      );
      assert.equal(
         captured.validateSelection({ talk: 'Tiger', location: 'Eurasia', times: [] }),
         Strings.validation.entityRequired(Strings.labels.talkTimes)
      );
      assert.equal(
         captured.validateSelection({ talk: 'Tiger', location: 'Eurasia', times: ['11:00 AM'] }),
         null
      );

      await captured.prepareForm();
      assert.ok(filterCalls.includes('refreshLocations'));
      assert.ok(filterCalls.includes('refreshTimes'));

      captured.resetSelection();
      assert.ok(filterCalls.includes('clearTalk'));
      assert.ok(filterCalls.includes('clearTimes'));

      assert.deepEqual(
         await captured.submitEndSchedule({
            talk: 'Tiger',
            location: 'Eurasia',
            times: ['11:00 AM'],
            endDate: '',
         }),
         {
            talk: 'Tiger',
            location: 'Eurasia',
            times: ['11:00 AM'],
            endDate: null,
         }
      );

      filterCalls.length = 0;
      await locationEl.listeners.change();
      assert.deepEqual(filterCalls, ['clearTimes']);

      filterCalls.length = 0;
      await talkNameEl.listeners.change();
      assert.deepEqual(filterCalls, ['clearTimes', 'refreshTimes']);

      assert.equal(
         captured.successMessage({ talk: 'Tiger', location: 'Eurasia' }),
         Strings.status.guardiansTalkScheduleEnded({ talk: 'Tiger', location: 'Eurasia' })
      );
   } finally {
      EndRecurringScheduleFormController.createEndRecurringScheduleFormController = originalCreate;
      ScheduleTimesCheckboxField.getSelectedScheduleTimes = originalGetTimes;
      ControllerHelper.getFieldValue = originalGetField;
      ControllerHelper.resetFormFields = originalReset;
      ConsoleDropdownPopulator.populateGuardiansTalkDropdown = originalPopulate;
      ConsoleOperationsClient.endGuardiansTalkSchedule = originalEnd;
   }
});

test('Test_CreateEndGuardiansTalkScheduleController_TestResetWithoutFilter_ExpectPopulate', () => {
   const originalCreate = EndRecurringScheduleFormController.createEndRecurringScheduleFormController;
   const originalPopulate = ConsoleDropdownPopulator.populateGuardiansTalkDropdown;
   const originalGetTimes = ScheduleTimesCheckboxField.getSelectedScheduleTimes;
   const originalGetField = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   let captured;
   const populateCalls = [];

   EndRecurringScheduleFormController.createEndRecurringScheduleFormController = (options) => {
      captured = options;
      return {};
   };
   ScheduleTimesCheckboxField.getSelectedScheduleTimes = () => [];
   ConsoleDropdownPopulator.populateGuardiansTalkDropdown = (...args) => {
      populateCalls.push(args);
   };
   ControllerHelper.getFieldValue = () => '';
   ControllerHelper.resetFormFields = () => {};

   try {
      const talkNameEl = document.createElement('select');
      EndGuardiansTalkController.createEndGuardiansTalkScheduleController({
         talkNameEl,
         locationEl: document.createElement('select'),
         timesEl: {},
         endDateEl: {},
      });

      captured.resetSelection();
      assert.equal(populateCalls.length, 1);
      assert.deepEqual(populateCalls[0][1], []);
   } finally {
      EndRecurringScheduleFormController.createEndRecurringScheduleFormController = originalCreate;
      ConsoleDropdownPopulator.populateGuardiansTalkDropdown = originalPopulate;
      ScheduleTimesCheckboxField.getSelectedScheduleTimes = originalGetTimes;
      ControllerHelper.getFieldValue = originalGetField;
      ControllerHelper.resetFormFields = originalReset;
   }
});
