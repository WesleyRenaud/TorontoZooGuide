import assert from 'node:assert/strict';
import test from 'node:test';

import { RemoveVisibilityController } from '../../../../../scripts/consoleOperations/animals/controllers/removeVisibilityController.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateRemoveVisibilityScheduleController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const originalLoad = ControllerHelper.loadOptionsAndShowPanel;
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalRemove = ConsoleOperationsClient.removeAnimalVisibilitySchedule;

   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      activations.push(options.panelEl);
      assert.equal(options.loadOptions, ConsoleOptionsLoader.loadExhibits);
      assert.equal(options.populateOptions, ConsoleDropdownPopulator.populateExhibitDropdown);
   };
   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.bindResetValueOnChange = () => {};
   ConsoleOperationsClient.removeAnimalVisibilitySchedule = async (payload) => {
      assert.deepEqual(payload, { species: 'Lion', exhibit: 'Savanna' });
      return { success: true, species: 'Lion', exhibit: 'Savanna' };
   };

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const speciesEl = document.createElement('input');
      const exhibitEl = document.createElement('select');
      speciesEl.value = 'Lion';
      exhibitEl.value = 'Savanna';

      const controller = RemoveVisibilityController.createRemoveVisibilityScheduleController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: { id: 'remove-visibility' },
         statusEl: {},
         speciesEl,
         exhibitEl,
         activatePanel: () => {},
      });

      await controller.show();
      assert.deepEqual(activations, [{ id: 'remove-visibility' }]);

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === 'Lion in Savanna no longer has a visibility schedule.'
            && entry[2] === 'is-success'
         ))
      );
   } finally {
      ControllerHelper.loadOptionsAndShowPanel = originalLoad;
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.bindResetValueOnChange = originalBind;
      ConsoleOperationsClient.removeAnimalVisibilitySchedule = originalRemove;
   }
});

test('Test_CreateRemoveVisibilityScheduleController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalRemove = ConsoleOperationsClient.removeAnimalVisibilitySchedule;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.bindResetValueOnChange = () => {};
   ControllerHelper.hideConsolePanel = (args) => {
      hides.push(args);
   };
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'mutation failed';

   try {
      const submitButtonEl = document.createElement('button');
      const cancelButtonEl = document.createElement('button');
      const speciesEl = document.createElement('input');
      const exhibitEl = document.createElement('select');
      const controller = RemoveVisibilityController.createRemoveVisibilityScheduleController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         cancelButtonEl,
         panelEl: {},
         statusEl: {},
         speciesEl,
         exhibitEl,
         activatePanel: () => {},
      });

      ControllerHelper.getFieldValue = () => '';
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.species)
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = (el) => (el === speciesEl ? 'Lion' : '');
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.entityLabels.exhibit)
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = (el) => (el === speciesEl ? 'Lion' : 'Savanna');
      ConsoleOperationsClient.removeAnimalVisibilitySchedule = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      ConsoleOperationsClient.removeAnimalVisibilitySchedule = async () => {
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
      ControllerHelper.bindResetValueOnChange = originalBind;
      ControllerHelper.hideConsolePanel = originalHide;
      ConsoleOperationsClient.removeAnimalVisibilitySchedule = originalRemove;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
