import assert from 'node:assert/strict';
import test from 'node:test';

import { DrinkingFountainsOpenController } from '../../../../../scripts/consoleOperations/drinkingFountains/controllers/drinkingFountainsOpenController.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateDrinkingFountainsOpenController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const originalSet = ConsoleOperationsClient.setDrinkingFountainsOpen;
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalReset = ControllerHelper.resetFormFields;

   ConsoleOperationsClient.setDrinkingFountainsOpen = async () => ({ success: true });
   ConsoleStatusPresenter.setStatus = (...args) => { statuses.push(args); };
   ControllerHelper.validateOptionalDateRange = () => null;
   ControllerHelper.resetFormFields = () => {};

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const startDateEl = document.createElement('input');
      const endDateEl = document.createElement('input');
      startDateEl.value = '2026-06-01';

      const controller = DrinkingFountainsOpenController.createDrinkingFountainsOpenController({
         showButtonEl,
         submitButtonEl,
         panelEl: { id: 'panel' },
         statusEl: {},
         startDateEl,
         endDateEl,
         activatePanel: (panel) => { activations.push(panel); },
      });

      controller.show();
      assert.deepEqual(activations, [{ id: 'panel' }]);

      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.status.drinkingFountainsOpen));
   } finally {
      ConsoleOperationsClient.setDrinkingFountainsOpen = originalSet;
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.validateOptionalDateRange = originalValidate;
      ControllerHelper.resetFormFields = originalReset;
   }
});

test('Test_CreateDrinkingFountainsOpenController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const originalSet = ConsoleOperationsClient.setDrinkingFountainsOpen;
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalReset = ControllerHelper.resetFormFields;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;

   ConsoleStatusPresenter.setStatus = (...args) => { statuses.push(args); };
   ControllerHelper.resetFormFields = () => {};
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'mutation failed';

   try {
      const submitButtonEl = document.createElement('button');
      DrinkingFountainsOpenController.createDrinkingFountainsOpenController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         panelEl: {},
         statusEl: {},
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         activatePanel: () => {},
      });

      ControllerHelper.validateOptionalDateRange = () => 'bad range';
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'bad range' && entry[2] === 'is-error'));

      statuses.length = 0;
      ControllerHelper.validateOptionalDateRange = () => null;
      ConsoleOperationsClient.setDrinkingFountainsOpen = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      ConsoleOperationsClient.setDrinkingFountainsOpen = async () => { throw new Error('network'); };
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.common.requestFailed));
   } finally {
      ConsoleOperationsClient.setDrinkingFountainsOpen = originalSet;
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.validateOptionalDateRange = originalValidate;
      ControllerHelper.resetFormFields = originalReset;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
