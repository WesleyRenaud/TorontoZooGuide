import assert from 'node:assert/strict';
import test from 'node:test';

import { EntityClosedFormController } from '../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { ConsoleStatusPresenter } from '../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { ControllerHelper } from '../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ApiErrorMessageResolver } from '../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateEntityClosedFormController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const originalLoad = ControllerHelper.loadOptionsAndShowPanel;
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalValidate = ControllerHelper.validateOptionalDateRange;

   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      activations.push(options.panelEl);
      assert.equal(options.errorMessage, Strings.loadErrors.entityOptions('Items'));
   };
   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.validateOptionalDateRange = () => null;

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const entityEl = document.createElement('select');
      const messageEl = document.createElement('input');
      entityEl.value = 'Near Cafe';
      messageEl.value = 'Closed';

      const controller = EntityClosedFormController.createEntityClosedFormController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: { id: 'closed-form' },
         statusEl: {},
         entityEl,
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         messageEl,
         activatePanel: () => {},
         loadOptions: async () => [],
         populateOptions: () => {},
         submitClosedStatus: async (values) => ({ success: true, ...values }),
         successMessage: (result) => Strings.status.closed(result.entity),
         optionsLabel: 'Items',
      });

      await showButtonEl.listeners.click();
      assert.deepEqual(activations, [{ id: 'closed-form' }]);

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.status.closed('Near Cafe') && entry[2] === 'is-success'
         ))
      );

      controller.show();
   } finally {
      ControllerHelper.loadOptionsAndShowPanel = originalLoad;
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.validateOptionalDateRange = originalValidate;
   }
});

test('Test_CreateEntityClosedFormController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
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
      const submitButtonEl = document.createElement('button');
      const cancelButtonEl = document.createElement('button');
      const entityEl = document.createElement('select');
      let submitImpl = async () => ({ success: false });

      const controller = EntityClosedFormController.createEntityClosedFormController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         cancelButtonEl,
         panelEl: {},
         statusEl: {},
         entityEl,
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         messageEl: document.createElement('input'),
         activatePanel: () => {},
         loadOptions: async () => [],
         populateOptions: () => {},
         submitClosedStatus: async (values) => submitImpl(values),
         entityLabel: 'Restroom',
      });

      ControllerHelper.getFieldValue = () => '';
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired('Restroom')
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = (el) => (el === entityEl ? 'Near Cafe' : '');
      ControllerHelper.validateOptionalDateRange = () => 'bad range';
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'bad range'));

      statuses.length = 0;
      ControllerHelper.validateOptionalDateRange = () => null;
      submitImpl = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      submitImpl = async () => {
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
      ControllerHelper.validateOptionalDateRange = originalValidate;
      ControllerHelper.hideConsolePanel = originalHide;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});

test('Test_CreateEntityClosedFormController_TestNoDateRange_ExpectSkipsDateValidation', async () => {
   const statuses = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   let validated = false;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = () => 'Near Cafe';
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.validateOptionalDateRange = () => {
      validated = true;
      return 'should not run';
   };

   try {
      const submitButtonEl = document.createElement('button');
      EntityClosedFormController.createEntityClosedFormController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         panelEl: {},
         statusEl: {},
         entityEl: document.createElement('select'),
         activatePanel: () => {},
         loadOptions: async () => [],
         populateOptions: () => {},
         submitClosedStatus: async () => ({ success: true, entity: 'Near Cafe' }),
         successMessage: () => 'closed',
      });

      await submitButtonEl.listeners.click();
      assert.equal(validated, false);
      assert.ok(statuses.some((entry) => entry[1] === 'closed' && entry[2] === 'is-success'));
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.validateOptionalDateRange = originalValidate;
   }
});
