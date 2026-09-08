import assert from 'node:assert/strict';
import test from 'node:test';

import { UpdateCreateController } from '../../../../../scripts/consoleOperations/updates/controllers/updateCreateController.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateCreateUpdateController_TestShowHideAndSubmit_ExpectFlows', async () => {
   const statuses = [];
   const activations = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalReset = ControllerHelper.resetFormFields;
   const originalGet = ControllerHelper.getFieldValue;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalCreate = ConsoleOperationsClient.createUpdate;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;
   let hideCalls = 0;

   ConsoleStatusPresenter.setStatus = (...args) => { statuses.push(args); };
   ControllerHelper.hideConsolePanel = () => { hideCalls += 1; };
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.validateOptionalDateRange = () => null;
   ConsoleOperationsClient.createUpdate = async () => ({ success: true, title: 'Notice' });
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'mutation failed';

   try {
      const showButtonEl = document.createElement('button');
      const cancelButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const titleEl = document.createElement('input');
      const descriptionEl = document.createElement('input');
      const typeEl = document.createElement('input');
      titleEl.value = 'Notice';
      descriptionEl.value = 'Details';
      typeEl.value = 'info';

      const controller = UpdateCreateController.createCreateUpdateController({
         showButtonEl,
         cancelButtonEl,
         submitButtonEl,
         panelEl: { id: 'create-update' },
         statusEl: {},
         titleEl,
         descriptionEl,
         typeEl,
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         activatePanel: (panel) => { activations.push(panel); },
      });

      controller.show();
      assert.deepEqual(activations, [{ id: 'create-update' }]);

      controller.hide();
      assert.equal(hideCalls, 1);

      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.status.updateCreated({ title: 'Notice' })));

      statuses.length = 0;
      titleEl.value = '';
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[2] === 'is-error'));

      statuses.length = 0;
      titleEl.value = 'Notice';
      ConsoleOperationsClient.createUpdate = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      ConsoleOperationsClient.createUpdate = async () => { throw new Error('network'); };
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.common.requestFailed));
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.hideConsolePanel = originalHide;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.validateOptionalDateRange = originalValidate;
      ConsoleOperationsClient.createUpdate = originalCreate;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
