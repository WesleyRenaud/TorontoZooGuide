import assert from 'node:assert/strict';
import test from 'node:test';

import { DrinkingFountainsController } from '../../../../../scripts/consoleOperations/drinkingFountains/controllers/drinkingFountainsController.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateDrinkingFountainsClosedController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const originalSet = ConsoleOperationsClient.setDrinkingFountainsClosed;
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalReset = ControllerHelper.resetFormFields;

   ConsoleOperationsClient.setDrinkingFountainsClosed = async () => ({ success: true });
   ConsoleStatusPresenter.setStatus = (...args) => { statuses.push(args); };
   ControllerHelper.validateOptionalDateRange = () => null;
   ControllerHelper.resetFormFields = () => {};

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const messageEl = document.createElement('input');
      messageEl.value = 'Closed for repair';

      const controller = DrinkingFountainsController.createDrinkingFountainsClosedController({
         showButtonEl,
         submitButtonEl,
         panelEl: { id: 'closed-panel' },
         statusEl: {},
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         messageEl,
         activatePanel: (panel) => { activations.push(panel); },
      });

      controller.show();
      assert.deepEqual(activations, [{ id: 'closed-panel' }]);

      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.status.drinkingFountainsClosed));
   } finally {
      ConsoleOperationsClient.setDrinkingFountainsClosed = originalSet;
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.validateOptionalDateRange = originalValidate;
      ControllerHelper.resetFormFields = originalReset;
   }
});

test('Test_CreateDrinkingFountainsClosedController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const originalSet = ConsoleOperationsClient.setDrinkingFountainsClosed;
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalReset = ControllerHelper.resetFormFields;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;

   ConsoleStatusPresenter.setStatus = (...args) => { statuses.push(args); };
   ControllerHelper.resetFormFields = () => {};
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'mutation failed';

   try {
      const submitButtonEl = document.createElement('button');
      DrinkingFountainsController.createDrinkingFountainsClosedController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         panelEl: {},
         statusEl: {},
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         messageEl: document.createElement('input'),
         activatePanel: () => {},
      });

      ControllerHelper.validateOptionalDateRange = () => 'bad range';
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'bad range' && entry[2] === 'is-error'));

      statuses.length = 0;
      ControllerHelper.validateOptionalDateRange = () => null;
      ConsoleOperationsClient.setDrinkingFountainsClosed = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      ConsoleOperationsClient.setDrinkingFountainsClosed = async () => { throw new Error('network'); };
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.common.requestFailed));
   } finally {
      ConsoleOperationsClient.setDrinkingFountainsClosed = originalSet;
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.validateOptionalDateRange = originalValidate;
      ControllerHelper.resetFormFields = originalReset;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
