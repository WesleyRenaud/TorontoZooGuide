import assert from 'node:assert/strict';
import test from 'node:test';

import { CancelGuardiansTalkController } from '../../../../../scripts/consoleOperations/guardiansTalks/controllers/cancelGuardiansTalkController.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { ScheduleTimesCheckboxField } from '../../../../../scripts/consoleOperations/forms/scheduleTimesCheckboxField.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateCancelGuardiansTalkOccurrenceController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const filterCalls = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalGetTimes = ScheduleTimesCheckboxField.getSelectedScheduleTimes;
   const originalCancel = ConsoleOperationsClient.cancelGuardiansTalkOccurrence;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {};
   ScheduleTimesCheckboxField.getSelectedScheduleTimes = () => ['11:00 AM'];
   ConsoleOperationsClient.cancelGuardiansTalkOccurrence = async (payload) => {
      assert.deepEqual(payload, {
         talk: 'Tiger Talk',
         location: 'Eurasia',
         date: '2026-07-01',
         times: ['11:00 AM'],
      });
      return {
         success: true,
         talk: 'Tiger Talk',
         location: 'Eurasia',
         date: '2026-07-01',
         times: ['11:00 AM'],
      };
   };

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const talkNameEl = document.createElement('select');
      const locationEl = document.createElement('select');
      const dateEl = document.createElement('input');
      talkNameEl.value = 'Tiger Talk';
      locationEl.value = 'Eurasia';
      dateEl.value = '2026-07-01';

      const talkLocationFilterController = {
         clear: () => {
            filterCalls.push('clearTalk');
         },
         refreshLocations: async () => {
            filterCalls.push('refreshLocations');
         },
      };
      const occurrenceFilterController = {
         clear: () => {
            filterCalls.push('clearOccurrence');
         },
         refresh: async () => {
            filterCalls.push('refreshOccurrence');
         },
         refreshTimes: () => {
            filterCalls.push('refreshTimes');
         },
      };

      const controller = CancelGuardiansTalkController.createCancelGuardiansTalkOccurrenceController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: { id: 'cancel-talk' },
         statusEl: {},
         talkNameEl,
         locationEl,
         dateEl,
         timesEl: {},
         activatePanel: (panel) => {
            activations.push(panel);
         },
         talkLocationFilterController,
         occurrenceFilterController,
      });

      await showButtonEl.listeners.click();
      assert.deepEqual(activations, [{ id: 'cancel-talk' }]);
      assert.ok(filterCalls.includes('refreshLocations'));
      assert.ok(filterCalls.includes('clearTalk'));
      assert.ok(filterCalls.includes('clearOccurrence'));

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === 'Tiger Talk in Eurasia on 2026-07-01 at 11:00 AM was cancelled.'
            && entry[2] === 'is-success'
         ))
      );

      filterCalls.length = 0;
      locationEl.listeners.change();
      assert.deepEqual(filterCalls, ['clearOccurrence']);

      filterCalls.length = 0;
      await talkNameEl.listeners.change();
      assert.deepEqual(filterCalls, ['refreshOccurrence']);

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
      ConsoleOperationsClient.cancelGuardiansTalkOccurrence = originalCancel;
   }
});

test('Test_CreateCancelGuardiansTalkOccurrenceController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const populateCalls = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalGetTimes = ScheduleTimesCheckboxField.getSelectedScheduleTimes;
   const originalPopulate = ConsoleDropdownPopulator.populateGuardiansTalkDropdown;
   const originalCancel = ConsoleOperationsClient.cancelGuardiansTalkOccurrence;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.hideConsolePanel = (args) => {
      hides.push(args);
   };
   ScheduleTimesCheckboxField.getSelectedScheduleTimes = () => [];
   ConsoleDropdownPopulator.populateGuardiansTalkDropdown = (...args) => {
      populateCalls.push(args);
   };
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'mutation failed';

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const cancelButtonEl = document.createElement('button');
      const talkNameEl = document.createElement('select');
      const locationEl = document.createElement('select');
      const dateEl = document.createElement('input');

      const controller = CancelGuardiansTalkController.createCancelGuardiansTalkOccurrenceController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl,
         panelEl: {},
         statusEl: {},
         talkNameEl,
         locationEl,
         dateEl,
         timesEl: {},
         activatePanel: () => {},
         talkLocationFilterController: {
            refreshLocations: async () => {
               throw new Error('load failed');
            },
            clear: () => {},
         },
      });

      await showButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.loadErrors.locations && entry[2] === 'is-error'
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = () => '';
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.location)
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = (el) => (el === locationEl ? 'Eurasia' : '');
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.talkName)
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = (el) => {
         if (el === locationEl) return 'Eurasia';
         if (el === talkNameEl) return 'Tiger';
         return '';
      };
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.date)
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = (el) => {
         if (el === locationEl) return 'Eurasia';
         if (el === talkNameEl) return 'Tiger';
         if (el === dateEl) return '2026-07-01';
         return '';
      };
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.talkTimes)
         ))
      );

      statuses.length = 0;
      ScheduleTimesCheckboxField.getSelectedScheduleTimes = () => ['11:00 AM'];
      ConsoleOperationsClient.cancelGuardiansTalkOccurrence = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      ConsoleOperationsClient.cancelGuardiansTalkOccurrence = async () => {
         throw new Error('network');
      };
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.common.requestFailed));

      const resetShowButtonEl = document.createElement('button');
      CancelGuardiansTalkController.createCancelGuardiansTalkOccurrenceController({
         talkNameEl: document.createElement('select'),
         locationEl: document.createElement('select'),
         dateEl: document.createElement('input'),
         timesEl: {},
         panelEl: {},
         statusEl: {},
         showButtonEl: resetShowButtonEl,
         submitButtonEl: document.createElement('button'),
         cancelButtonEl: document.createElement('button'),
         activatePanel: () => {},
      });
      await resetShowButtonEl.listeners.click();
      assert.equal(populateCalls.length, 1);
      assert.deepEqual(populateCalls[0][1], []);

      const talkInputEl = document.createElement('input');
      talkInputEl.value = 'Old Talk';
      const inputShowButtonEl = document.createElement('button');
      CancelGuardiansTalkController.createCancelGuardiansTalkOccurrenceController({
         talkNameEl: talkInputEl,
         locationEl: document.createElement('select'),
         dateEl: document.createElement('input'),
         timesEl: {},
         panelEl: {},
         statusEl: {},
         showButtonEl: inputShowButtonEl,
         submitButtonEl: document.createElement('button'),
         cancelButtonEl: document.createElement('button'),
         activatePanel: () => {},
      });
      await inputShowButtonEl.listeners.click();
      assert.equal(talkInputEl.value, '');

      const talkNameForChange = document.createElement('select');
      CancelGuardiansTalkController.createCancelGuardiansTalkOccurrenceController({
         talkNameEl: talkNameForChange,
         locationEl: document.createElement('select'),
         dateEl: document.createElement('input'),
         timesEl: {},
         panelEl: {},
         statusEl: {},
         showButtonEl: document.createElement('button'),
         submitButtonEl: document.createElement('button'),
         cancelButtonEl: document.createElement('button'),
         activatePanel: () => {},
      });
      ScheduleTimesCheckboxField.getSelectedScheduleTimes = () => ['11:00 AM'];
      talkNameForChange.value = 'Tiger';
      await talkNameForChange.listeners.change();

      controller.hide();
      cancelButtonEl.listeners.click();
      assert.equal(hides.length, 2);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.hideConsolePanel = originalHide;
      ScheduleTimesCheckboxField.getSelectedScheduleTimes = originalGetTimes;
      ConsoleDropdownPopulator.populateGuardiansTalkDropdown = originalPopulate;
      ConsoleOperationsClient.cancelGuardiansTalkOccurrence = originalCancel;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
