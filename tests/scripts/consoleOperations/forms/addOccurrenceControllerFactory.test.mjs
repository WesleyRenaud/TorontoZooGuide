import assert from 'node:assert/strict';
import test from 'node:test';

import { AddOccurrenceControllerFactory } from '../../../../scripts/consoleOperations/forms/addOccurrenceControllerFactory.js';
import { ConsoleStatusPresenter } from '../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { ControllerHelper } from '../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ApiErrorMessageResolver } from '../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateAddOccurrenceController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const resets = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalReset = ControllerHelper.resetFormFields;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.resetFormFields = () => {
      resets.push(true);
   };

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');

      const controller = AddOccurrenceControllerFactory.createAddOccurrenceController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: { id: 'add-occurrence' },
         statusEl: {},
         formFieldEls: [document.createElement('input')],
         activatePanel: (panel) => {
            activations.push(panel);
         },
         resetSelection: () => {
            resets.push('selection');
         },
         getFormValues: () => ({
            talk: 'Keeper Talk',
            location: 'Africa',
            date: '2026-07-01',
            times: ['11:00 AM'],
         }),
         validateForm: () => null,
         prepareForm: async () => {},
         submitOccurrence: async (values) => ({ success: true, ...values }),
         successMessage: (result) => (
            `${result.talk} in ${result.location} on ${result.date} at ${result.times.join(', ')} was added.`
         ),
      });

      await showButtonEl.listeners.click();
      assert.deepEqual(activations, [{ id: 'add-occurrence' }]);
      assert.ok(resets.includes(true));
      assert.ok(resets.includes('selection'));

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === 'Keeper Talk in Africa on 2026-07-01 at 11:00 AM was added.'
            && entry[2] === 'is-success'
         ))
      );

      controller.show();
      assert.equal(activations.length, 2);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.resetFormFields = originalReset;
   }
});

test('Test_CreateAddOccurrenceController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalReset = ControllerHelper.resetFormFields;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.hideConsolePanel = (args) => {
      hides.push(args);
   };
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'mutation failed';

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const cancelButtonEl = document.createElement('button');

      const controller = AddOccurrenceControllerFactory.createAddOccurrenceController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl,
         panelEl: {},
         statusEl: {},
         formFieldEls: [],
         activatePanel: () => {},
         getFormValues: () => ({ talk: '' }),
         validateForm: ({ talk }) => (
            talk ? null : Strings.validation.entityRequired('Talk')
         ),
         prepareForm: async () => {
            throw new Error('load failed');
         },
         loadErrorMessage: 'could not load',
         submitOccurrence: async () => ({ success: false }),
         successMessage: () => 'ok',
      });

      await showButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'could not load' && entry[2] === 'is-error'));

      statuses.length = 0;
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired('Talk') && entry[2] === 'is-error'
         ))
      );

      statuses.length = 0;
      const mutationSubmitEl = document.createElement('button');
      AddOccurrenceControllerFactory.createAddOccurrenceController({
         showButtonEl: document.createElement('button'),
         submitButtonEl: mutationSubmitEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: {},
         statusEl: {},
         activatePanel: () => {},
         getFormValues: () => ({ talk: 'Ok' }),
         validateForm: () => null,
         submitOccurrence: async () => ({ success: false }),
         successMessage: () => 'ok',
      });
      await mutationSubmitEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      const networkSubmitEl = document.createElement('button');
      AddOccurrenceControllerFactory.createAddOccurrenceController({
         showButtonEl: document.createElement('button'),
         submitButtonEl: networkSubmitEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: {},
         statusEl: {},
         activatePanel: () => {},
         getFormValues: () => ({ talk: 'Ok' }),
         validateForm: () => null,
         submitOccurrence: async () => {
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
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.hideConsolePanel = originalHide;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
