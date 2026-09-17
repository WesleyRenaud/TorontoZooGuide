import assert from 'node:assert/strict';
import test from 'node:test';

import { UpdateEndController } from '../../../../../scripts/consoleOperations/updates/controllers/updateEndController.js';
import { UpdateOptions } from '../../../../../scripts/consoleOperations/updates/controllers/updateOptions.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateEndUpdateController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const originalLoad = ControllerHelper.loadOptionsAndShowPanel;
   const originalReload = ControllerHelper.reloadOptions;
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalIdentity = UpdateOptions.getSelectedUpdateIdentity;
   const originalGetField = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalEnd = ConsoleOperationsClient.endUpdate;

   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      activations.push(options.panelEl);
      assert.equal(options.loadOptions, UpdateOptions.loadActiveUpdates);
      assert.equal(options.populateOptions, UpdateOptions.populateUpdateDropdown);
   };
   ControllerHelper.reloadOptions = async (options) => {
      options.resetForm?.();
   };
   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   UpdateOptions.getSelectedUpdateIdentity = () => ({
      title: 'Notice',
      startDate: '2026-01-01',
   });
   ControllerHelper.getFieldValue = () => '2026-02-01';
   ControllerHelper.resetFormFields = () => {};
   ConsoleOperationsClient.endUpdate = async (values) => {
      assert.deepEqual(values, {
         title: 'Notice',
         startDate: '2026-01-01',
         endDate: '2026-02-01',
      });
      return { success: true };
   };

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const controller = UpdateEndController.createEndUpdateController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: { id: 'end-update' },
         statusEl: {},
         updateEl: document.createElement('select'),
         endDateEl: document.createElement('input'),
         activatePanel: () => {},
      });

      await controller.show();
      assert.deepEqual(activations, [{ id: 'end-update' }]);

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.status.updateEnded && entry[2] === 'is-success'
         ))
      );
   } finally {
      ControllerHelper.loadOptionsAndShowPanel = originalLoad;
      ControllerHelper.reloadOptions = originalReload;
      ConsoleStatusPresenter.setStatus = originalStatus;
      UpdateOptions.getSelectedUpdateIdentity = originalIdentity;
      ControllerHelper.getFieldValue = originalGetField;
      ControllerHelper.resetFormFields = originalReset;
      ConsoleOperationsClient.endUpdate = originalEnd;
   }
});

test('Test_CreateEndUpdateController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalIdentity = UpdateOptions.getSelectedUpdateIdentity;
   const originalGetField = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalEnd = ConsoleOperationsClient.endUpdate;
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
      const controller = UpdateEndController.createEndUpdateController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         cancelButtonEl,
         panelEl: {},
         statusEl: {},
         updateEl: document.createElement('select'),
         endDateEl: document.createElement('input'),
         activatePanel: () => {},
      });

      UpdateOptions.getSelectedUpdateIdentity = () => ({ title: '', startDate: '' });
      ControllerHelper.getFieldValue = () => '';
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.update)
            && entry[2] === 'is-error'
         ))
      );

      statuses.length = 0;
      UpdateOptions.getSelectedUpdateIdentity = () => ({
         title: 'Notice',
         startDate: '2026-01-01',
      });
      ControllerHelper.getFieldValue = () => '2026-02-01';
      ConsoleOperationsClient.endUpdate = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      ConsoleOperationsClient.endUpdate = async () => {
         throw new Error('network');
      };
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.common.requestFailed));

      controller.hide();
      cancelButtonEl.listeners.click();
      assert.equal(hides.length, 2);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      UpdateOptions.getSelectedUpdateIdentity = originalIdentity;
      ControllerHelper.getFieldValue = originalGetField;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.hideConsolePanel = originalHide;
      ConsoleOperationsClient.endUpdate = originalEnd;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});

test('Test_CreateEndUpdateController_TestReloadOptionsThrows_ExpectClearsFields', async () => {
   const resets = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalIdentity = UpdateOptions.getSelectedUpdateIdentity;
   const originalGetField = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalReload = ControllerHelper.reloadOptions;
   const originalEnd = ConsoleOperationsClient.endUpdate;

   ConsoleStatusPresenter.setStatus = () => {};
   UpdateOptions.getSelectedUpdateIdentity = () => ({
      title: 'Notice',
      startDate: '2026-01-01',
   });
   ControllerHelper.getFieldValue = () => '2026-02-01';
   ControllerHelper.resetFormFields = (fields) => {
      resets.push(fields);
   };
   ControllerHelper.reloadOptions = async () => {
      throw new Error('reload failed');
   };
   ConsoleOperationsClient.endUpdate = async () => ({ success: true });

   try {
      const submitButtonEl = document.createElement('button');
      UpdateEndController.createEndUpdateController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         panelEl: {},
         statusEl: {},
         updateEl: document.createElement('select'),
         endDateEl: document.createElement('input'),
         activatePanel: () => {},
      });

      await submitButtonEl.listeners.click();
      assert.equal(resets.length, 1);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      UpdateOptions.getSelectedUpdateIdentity = originalIdentity;
      ControllerHelper.getFieldValue = originalGetField;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.reloadOptions = originalReload;
      ConsoleOperationsClient.endUpdate = originalEnd;
   }
});
