import assert from 'node:assert/strict';
import test from 'node:test';

import { CancelWildEncounterController } from '../../../../../scripts/consoleOperations/wildEncounters/controllers/cancelWildEncounterController.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { ScheduleTimesCheckboxField } from '../../../../../scripts/consoleOperations/forms/scheduleTimesCheckboxField.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateCancelWildEncounterOccurrenceController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const filterCalls = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalGetTimes = ScheduleTimesCheckboxField.getSelectedScheduleTimes;
   const originalLoad = ConsoleOptionsLoader.loadWildEncounters;
   const originalPopulate = ConsoleDropdownPopulator.populateWildEncounterDropdown;
   const originalCancel = ConsoleOperationsClient.cancelWildEncounterOccurrence;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {};
   ScheduleTimesCheckboxField.getSelectedScheduleTimes = () => ['11:00 AM'];
   ConsoleOptionsLoader.loadWildEncounters = async () => [{ name: 'Giraffe' }];
   ConsoleDropdownPopulator.populateWildEncounterDropdown = (...args) => {
      filterCalls.push(['populate', args[1]]);
   };
   ConsoleOperationsClient.cancelWildEncounterOccurrence = async (payload) => {
      assert.deepEqual(payload, {
         wildEncounter: 'Giraffe Encounter',
         date: '2026-07-01',
         times: ['11:00 AM'],
      });
      return {
         success: true,
         wildEncounter: 'Giraffe Encounter',
         date: '2026-07-01',
         times: ['11:00 AM'],
      };
   };

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const wildEncounterEl = document.createElement('select');
      const dateEl = document.createElement('input');
      wildEncounterEl.value = 'Giraffe Encounter';
      dateEl.value = '2026-07-01';

      const occurrenceFilterController = {
         clear: () => {
            filterCalls.push('clear');
         },
         refresh: async () => {
            filterCalls.push('refresh');
         },
         refreshTimes: () => {
            filterCalls.push('refreshTimes');
         },
      };

      const controller = CancelWildEncounterController.createCancelWildEncounterOccurrenceController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: { id: 'cancel-encounter' },
         statusEl: {},
         wildEncounterEl,
         dateEl,
         timesEl: {},
         activatePanel: (panel) => {
            activations.push(panel);
         },
         occurrenceFilterController,
      });

      await showButtonEl.listeners.click();
      assert.deepEqual(activations, [{ id: 'cancel-encounter' }]);
      assert.ok(filterCalls.some((call) => Array.isArray(call) && call[0] === 'populate'));
      assert.ok(filterCalls.includes('clear'));

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === 'Giraffe Encounter on 2026-07-01 at 11:00 AM was cancelled.'
            && entry[2] === 'is-success'
         ))
      );

      filterCalls.length = 0;
      await wildEncounterEl.listeners.change();
      assert.ok(filterCalls.includes('clear'));
      assert.ok(filterCalls.includes('refresh'));

      filterCalls.length = 0;
      dateEl.listeners.change();
      assert.deepEqual(filterCalls, ['refreshTimes']);

      controller.show();
      assert.equal(activations.length, 2);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ScheduleTimesCheckboxField.getSelectedScheduleTimes = originalGetTimes;
      ConsoleOptionsLoader.loadWildEncounters = originalLoad;
      ConsoleDropdownPopulator.populateWildEncounterDropdown = originalPopulate;
      ConsoleOperationsClient.cancelWildEncounterOccurrence = originalCancel;
   }
});

test('Test_CreateCancelWildEncounterOccurrenceController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalGetTimes = ScheduleTimesCheckboxField.getSelectedScheduleTimes;
   const originalLoad = ConsoleOptionsLoader.loadWildEncounters;
   const originalCancel = ConsoleOperationsClient.cancelWildEncounterOccurrence;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.hideConsolePanel = (args) => {
      hides.push(args);
   };
   ScheduleTimesCheckboxField.getSelectedScheduleTimes = () => [];
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'mutation failed';

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const cancelButtonEl = document.createElement('button');
      const wildEncounterEl = document.createElement('select');
      const dateEl = document.createElement('input');

      const controller = CancelWildEncounterController.createCancelWildEncounterOccurrenceController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl,
         panelEl: {},
         statusEl: {},
         wildEncounterEl,
         dateEl,
         timesEl: {},
         activatePanel: () => {},
      });

      ConsoleOptionsLoader.loadWildEncounters = async () => {
         throw new Error('load failed');
      };
      await showButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.loadErrors.wildEncounters && entry[2] === 'is-error'
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = () => '';
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.entityLabels.wildEncounter)
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = (el) => (el === wildEncounterEl ? 'Giraffe' : '');
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.date)
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = (el) => {
         if (el === wildEncounterEl) return 'Giraffe';
         if (el === dateEl) return '2026-07-01';
         return '';
      };
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.encounterTimes)
         ))
      );

      statuses.length = 0;
      ScheduleTimesCheckboxField.getSelectedScheduleTimes = () => ['11:00 AM'];
      ConsoleOperationsClient.cancelWildEncounterOccurrence = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      ConsoleOperationsClient.cancelWildEncounterOccurrence = async () => {
         throw new Error('network');
      };
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.common.requestFailed));

      controller.hide();
      cancelButtonEl.listeners.click();
      assert.equal(hides.length, 2);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.hideConsolePanel = originalHide;
      ScheduleTimesCheckboxField.getSelectedScheduleTimes = originalGetTimes;
      ConsoleOptionsLoader.loadWildEncounters = originalLoad;
      ConsoleOperationsClient.cancelWildEncounterOccurrence = originalCancel;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
