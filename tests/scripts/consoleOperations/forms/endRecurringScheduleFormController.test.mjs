import assert from 'node:assert/strict';
import test from 'node:test';

import { EndRecurringScheduleFormController } from '../../../../scripts/consoleOperations/forms/endRecurringScheduleFormController.js';
import { ConsoleStatusPresenter } from '../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { ControllerHelper } from '../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ApiErrorMessageResolver } from '../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateEndRecurringScheduleFormController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const resets = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {
      resets.push(true);
   };

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const endDateEl = document.createElement('input');
      endDateEl.value = '2026-07-01';

      const controller = EndRecurringScheduleFormController.createEndRecurringScheduleFormController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: { id: 'end-schedule' },
         statusEl: {},
         endDateEl,
         activatePanel: (panel) => {
            activations.push(panel);
         },
         getSelectionValues: () => ({ entity: 'Giraffe' }),
         validateSelection: () => null,
         prepareForm: async () => {},
         submitEndSchedule: async (values) => ({ success: true, ...values }),
         successMessage: (result) => Strings.status.scheduleEnded(result.entity),
      });

      await showButtonEl.listeners.click();
      assert.deepEqual(activations, [{ id: 'end-schedule' }]);
      assert.ok(resets.length >= 1);

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.status.scheduleEnded('Giraffe') && entry[2] === 'is-success'
         ))
      );

      controller.show();
      assert.equal(activations.length, 2);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
   }
});

test('Test_CreateEndRecurringScheduleFormController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = () => '';
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.hideConsolePanel = (args) => {
      hides.push(args);
   };
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'mutation failed';

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const cancelButtonEl = document.createElement('button');

      const controller = EndRecurringScheduleFormController.createEndRecurringScheduleFormController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl,
         panelEl: {},
         statusEl: {},
         endDateEl: document.createElement('input'),
         activatePanel: () => {},
         getSelectionValues: () => ({ entity: '' }),
         validateSelection: ({ entity }) => (
            entity ? null : Strings.validation.entityRequired('Entity')
         ),
         prepareForm: async () => {
            throw new Error('load failed');
         },
         loadErrorMessage: 'could not load',
         submitEndSchedule: async () => ({ success: false }),
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
      const mutationSubmitEl = document.createElement('button');
      EndRecurringScheduleFormController.createEndRecurringScheduleFormController({
         showButtonEl: document.createElement('button'),
         submitButtonEl: mutationSubmitEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: {},
         statusEl: {},
         endDateEl: document.createElement('input'),
         activatePanel: () => {},
         getSelectionValues: () => ({ entity: 'Ok' }),
         validateSelection: () => null,
         submitEndSchedule: async () => ({ success: false }),
      });
      await mutationSubmitEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      const networkSubmitEl = document.createElement('button');
      EndRecurringScheduleFormController.createEndRecurringScheduleFormController({
         showButtonEl: document.createElement('button'),
         submitButtonEl: networkSubmitEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: {},
         statusEl: {},
         endDateEl: document.createElement('input'),
         activatePanel: () => {},
         getSelectionValues: () => ({ entity: 'Ok' }),
         validateSelection: () => null,
         submitEndSchedule: async () => {
            throw new Error('network');
         },
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
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
