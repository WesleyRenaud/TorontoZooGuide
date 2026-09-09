import assert from 'node:assert/strict';
import test from 'node:test';

import { CancelOccurrenceControllerFactory } from '../../../../scripts/consoleOperations/forms/cancelOccurrenceControllerFactory.js';
import { ScheduleTimesCheckboxField } from '../../../../scripts/consoleOperations/forms/scheduleTimesCheckboxField.js';
import { ConsoleStatusPresenter } from '../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { ControllerHelper } from '../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ApiErrorMessageResolver } from '../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateCancelOccurrenceController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const resets = [];
   const filterCalls = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalGetTimes = ScheduleTimesCheckboxField.getSelectedScheduleTimes;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {
      resets.push(true);
   };
   ScheduleTimesCheckboxField.getSelectedScheduleTimes = () => ['11:00 AM'];

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const dateEl = document.createElement('input');
      dateEl.value = '2026-07-01';

      const occurrenceFilterController = {
         clear: () => {
            filterCalls.push('clear');
         },
         refreshTimes: () => {
            filterCalls.push('refreshTimes');
         },
      };

      const controller = CancelOccurrenceControllerFactory.createCancelOccurrenceController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: { id: 'cancel-occurrence' },
         statusEl: {},
         dateEl,
         timesEl: {},
         activatePanel: (panel) => {
            activations.push(panel);
         },
         occurrenceFilterController,
         resetSelection: () => {
            resets.push('selection');
         },
         getSelectionValues: () => ({ entity: 'Giraffe' }),
         validateSelection: () => null,
         prepareForm: async () => {},
         submitOccurrenceCancellation: async (values) => ({ success: true, ...values }),
         successMessage: (result) => (
            `${result.entity} on ${result.date} at ${result.times.join(', ')} was cancelled.`
         ),
      });

      await showButtonEl.listeners.click();
      assert.deepEqual(activations, [{ id: 'cancel-occurrence' }]);
      assert.ok(resets.includes(true));
      assert.ok(resets.includes('selection'));
      assert.ok(filterCalls.includes('clear'));

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === 'Giraffe on 2026-07-01 at 11:00 AM was cancelled.'
            && entry[2] === 'is-success'
         ))
      );

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
   }
});

test('Test_CreateCancelOccurrenceController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalGetTimes = ScheduleTimesCheckboxField.getSelectedScheduleTimes;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = () => '';
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

      const controller = CancelOccurrenceControllerFactory.createCancelOccurrenceController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl,
         panelEl: {},
         statusEl: {},
         dateEl: document.createElement('input'),
         timesEl: {},
         activatePanel: () => {},
         getSelectionValues: () => ({ entity: '' }),
         validateSelection: ({ entity }) => (
            entity ? null : Strings.validation.entityRequired('Entity')
         ),
         prepareForm: async () => {
            throw new Error('load failed');
         },
         loadErrorMessage: 'could not load',
         submitOccurrenceCancellation: async () => ({ success: false }),
         successMessage: () => 'ok',
      });

      await showButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'could not load' && entry[2] === 'is-error'));

      statuses.length = 0;
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired('Entity') && entry[2] === 'is-error'
         ))
      );

      statuses.length = 0;
      ScheduleTimesCheckboxField.getSelectedScheduleTimes = () => ['11:00 AM'];
      const mutationSubmitEl = document.createElement('button');
      CancelOccurrenceControllerFactory.createCancelOccurrenceController({
         showButtonEl: document.createElement('button'),
         submitButtonEl: mutationSubmitEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: {},
         statusEl: {},
         dateEl: document.createElement('input'),
         timesEl: {},
         activatePanel: () => {},
         getSelectionValues: () => ({ entity: 'Ok' }),
         validateSelection: () => null,
         submitOccurrenceCancellation: async () => ({ success: false }),
         successMessage: () => 'ok',
      });
      await mutationSubmitEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      const networkSubmitEl = document.createElement('button');
      CancelOccurrenceControllerFactory.createCancelOccurrenceController({
         showButtonEl: document.createElement('button'),
         submitButtonEl: networkSubmitEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: {},
         statusEl: {},
         dateEl: document.createElement('input'),
         timesEl: {},
         activatePanel: () => {},
         getSelectionValues: () => ({ entity: 'Ok' }),
         validateSelection: () => null,
         submitOccurrenceCancellation: async () => {
            throw new Error('network');
         },
         successMessage: () => 'ok',
      });
      await networkSubmitEl.listeners.click();
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
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
