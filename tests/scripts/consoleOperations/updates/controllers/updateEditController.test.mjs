import assert from 'node:assert/strict';
import test from 'node:test';

import { UpdateEditController } from '../../../../../scripts/consoleOperations/updates/controllers/updateEditController.js';
import { UpdateOptions } from '../../../../../scripts/consoleOperations/updates/controllers/updateOptions.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateEditUpdateController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const originalLoad = ControllerHelper.loadOptionsAndShowPanel;
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalIdentity = UpdateOptions.getSelectedUpdateData;
   const originalGetField = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalEdit = ConsoleOperationsClient.editUpdate;

   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      activations.push(options.panelEl);
      assert.equal(options.loadOptions, UpdateOptions.loadActiveUpdates);
      assert.equal(options.populateOptions, UpdateOptions.populateUpdateDropdown);
   };
   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   UpdateOptions.getSelectedUpdateData = () => ({
      title: 'Notice',
      startDate: '2026-01-01',
      description: 'Details',
      type: 'info',
      endDate: '2026-02-01',
   });
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {};
   ConsoleOperationsClient.editUpdate = async (values) => {
      assert.deepEqual(values, {
         title: 'Notice',
         startDate: '2026-01-01',
         description: 'Updated details',
         type: 'warning',
         endDate: '2026-03-01',
      });
      return { success: true };
   };

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const updateEl = document.createElement('select');
      const descriptionEl = document.createElement('input');
      const typeEl = document.createElement('input');
      const endDateEl = document.createElement('input');
      descriptionEl.value = 'Updated details';
      typeEl.value = 'warning';
      endDateEl.value = '2026-03-01';

      const controller = UpdateEditController.createEditUpdateController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: { id: 'edit-update' },
         statusEl: {},
         updateEl,
         descriptionEl,
         typeEl,
         endDateEl,
         activatePanel: () => {},
      });

      await controller.show();
      assert.deepEqual(activations, [{ id: 'edit-update' }]);

      await updateEl.listeners.change();
      assert.equal(descriptionEl.value, 'Details');
      assert.equal(typeEl.value, 'info');
      assert.equal(endDateEl.value, '2026-02-01');

      descriptionEl.value = 'Updated details';
      typeEl.value = 'warning';
      endDateEl.value = '2026-03-01';
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.status.updateEdited && entry[2] === 'is-success'
         ))
      );
   } finally {
      ControllerHelper.loadOptionsAndShowPanel = originalLoad;
      ConsoleStatusPresenter.setStatus = originalStatus;
      UpdateOptions.getSelectedUpdateData = originalIdentity;
      ControllerHelper.getFieldValue = originalGetField;
      ControllerHelper.resetFormFields = originalReset;
      ConsoleOperationsClient.editUpdate = originalEdit;
   }
});

test('Test_CreateEditUpdateController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalIdentity = UpdateOptions.getSelectedUpdateData;
   const originalGetField = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalEdit = ConsoleOperationsClient.editUpdate;
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
      const descriptionEl = document.createElement('input');
      const typeEl = document.createElement('input');
      const endDateEl = document.createElement('input');
      const controller = UpdateEditController.createEditUpdateController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         cancelButtonEl,
         panelEl: {},
         statusEl: {},
         updateEl: document.createElement('select'),
         descriptionEl,
         typeEl,
         endDateEl,
         activatePanel: () => {},
      });

      UpdateOptions.getSelectedUpdateData = () => ({ title: '', startDate: '' });
      ControllerHelper.getFieldValue = () => '';
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.update)
            && entry[2] === 'is-error'
         ))
      );

      statuses.length = 0;
      UpdateOptions.getSelectedUpdateData = () => ({
         title: 'Notice',
         startDate: '2026-01-01',
      });
      ControllerHelper.getFieldValue = (el) => {
         if (el === descriptionEl) return '';
         if (el === typeEl) return 'info';
         return '';
      };
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.description)
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = (el) => {
         if (el === descriptionEl) return 'Details';
         if (el === typeEl) return '';
         return '';
      };
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.type)
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = (el) => {
         if (el === descriptionEl) return 'Details';
         if (el === typeEl) return 'info';
         if (el === endDateEl) return '2025-01-01';
         return '';
      };
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.validation.endDateBeforeStartDate));

      statuses.length = 0;
      ControllerHelper.getFieldValue = (el) => {
         if (el === descriptionEl) return 'Details';
         if (el === typeEl) return 'info';
         if (el === endDateEl) return '2026-02-01';
         return '';
      };
      ConsoleOperationsClient.editUpdate = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      ConsoleOperationsClient.editUpdate = async () => {
         throw new Error('network');
      };
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.common.requestFailed));

      controller.hide();
      cancelButtonEl.listeners.click();
      assert.equal(hides.length, 2);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      UpdateOptions.getSelectedUpdateData = originalIdentity;
      ControllerHelper.getFieldValue = originalGetField;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.hideConsolePanel = originalHide;
      ConsoleOperationsClient.editUpdate = originalEdit;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
