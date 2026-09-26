import assert from 'node:assert/strict';
import test from 'node:test';

import { GlobalAmenityStatusFormController } from '../../../../scripts/consoleOperations/forms/globalAmenityStatusFormController.js';
import { ApiErrorMessageResolver } from '../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { ControllerHelper } from '../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateGlobalAmenityStatusFormController_TestOpenPath_ExpectShowAndSubmitSuccess', async () => {
   const statuses = [];
   const activations = [];
   const submitted = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalReset = ControllerHelper.resetFormFields;
   const originalGet = ControllerHelper.getFieldValue;

   ConsoleStatusPresenter.setStatus = (...args) => { statuses.push(args); };
   ControllerHelper.validateOptionalDateRange = () => null;
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';

   try {
      const startDate = '2026-06-01';
      const panelEl = { id: 'open-panel' };
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const startDateEl = document.createElement('input');
      const endDateEl = document.createElement('input');
      startDateEl.value = startDate;

      const controller = GlobalAmenityStatusFormController.createGlobalAmenityStatusFormController({
         showButtonEl,
         submitButtonEl,
         panelEl,
         statusEl: {},
         startDateEl,
         endDateEl,
         activatePanel: (panel) => { activations.push(panel); },
         submitStatus: async (payload) => {
            submitted.push(payload);
            return { success: true };
         },
         successMessage: Strings.status.drinkingFountainsOpen,
      });

      controller.show();
      await submitButtonEl.listeners.click();

      assert.deepEqual(activations, [panelEl]);
      assert.deepEqual(submitted, [{ startDate, endDate: '', message: '' }]);
      assert.ok(statuses.some((entry) => entry[1] === Strings.status.drinkingFountainsOpen));
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.validateOptionalDateRange = originalValidate;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.getFieldValue = originalGet;
   }
});


test('Test_CreateGlobalAmenityStatusFormController_TestClosedPath_ExpectMessageAndFnSuccess', async () => {
   const statuses = [];
   const submitted = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalReset = ControllerHelper.resetFormFields;
   const originalGet = ControllerHelper.getFieldValue;

   ConsoleStatusPresenter.setStatus = (...args) => { statuses.push(args); };
   ControllerHelper.validateOptionalDateRange = () => null;
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';

   try {
      const message = 'Closed for repair';
      const submitButtonEl = document.createElement('button');
      const messageEl = document.createElement('input');
      messageEl.value = message;

      GlobalAmenityStatusFormController.createGlobalAmenityStatusFormController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         panelEl: {},
         statusEl: {},
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         messageEl,
         activatePanel: () => {},
         submitStatus: async (payload) => {
            submitted.push(payload);
            return { success: true };
         },
         successMessage: () => Strings.status.drinkingFountainsClosed,
      });

      await submitButtonEl.listeners.click();

      assert.equal(submitted[Position.FIRST].message, message);
      assert.ok(statuses.some((entry) => entry[1] === Strings.status.drinkingFountainsClosed));
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.validateOptionalDateRange = originalValidate;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.getFieldValue = originalGet;
   }
});


test('Test_CreateGlobalAmenityStatusFormController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalReset = ControllerHelper.resetFormFields;
   const originalGet = ControllerHelper.getFieldValue;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;

   ConsoleStatusPresenter.setStatus = (...args) => { statuses.push(args); };
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.getFieldValue = () => '';
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'mutation failed';

   try {
      const submitButtonEl = document.createElement('button');
      let submitStatus = async () => ({ success: false });

      GlobalAmenityStatusFormController.createGlobalAmenityStatusFormController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         panelEl: {},
         statusEl: {},
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         messageEl: document.createElement('input'),
         activatePanel: () => {},
         submitStatus: (...args) => submitStatus(...args),
         successMessage: Strings.status.drinkingFountainsClosed,
         requireMessage: true,
      });

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.message)
            && entry[2] === 'is-error'
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = () => 'value';
      ControllerHelper.validateOptionalDateRange = () => 'bad range';
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'bad range' && entry[2] === 'is-error'));

      statuses.length = 0;
      ControllerHelper.validateOptionalDateRange = () => null;
      submitStatus = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      submitStatus = async () => { throw new Error('network'); };
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.common.requestFailed));
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.validateOptionalDateRange = originalValidate;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.getFieldValue = originalGet;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
