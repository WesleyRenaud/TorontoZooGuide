import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalViewingController } from '../../../../../scripts/consoleOperations/animals/controllers/animalViewingController.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateAnimalViewingAlertController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const originalLoad = ControllerHelper.loadOptionsAndShowPanel;
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalSet = ConsoleOperationsClient.setAnimalViewingAlert;

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
   ControllerHelper.validateOptionalDateRange = () => null;
   ConsoleOperationsClient.setAnimalViewingAlert = async (payload) => {
      assert.deepEqual(payload, {
         species: 'Lion',
         exhibit: 'Savanna',
         alertStartDate: '2026-06-01',
         alertEndDate: null,
         message: 'Behind glass',
      });
      return { success: true, species: 'Lion', exhibit: 'Savanna' };
   };

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const speciesEl = document.createElement('input');
      const exhibitEl = document.createElement('select');
      const startDateEl = document.createElement('input');
      const messageEl = document.createElement('input');
      speciesEl.value = 'Lion';
      exhibitEl.value = 'Savanna';
      startDateEl.value = '2026-06-01';
      messageEl.value = 'Behind glass';

      const controller = AnimalViewingController.createAnimalViewingAlertController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: { id: 'viewing-alert' },
         statusEl: {},
         speciesEl,
         exhibitEl,
         startDateEl,
         endDateEl: document.createElement('input'),
         messageEl,
         activatePanel: () => {},
      });

      await controller.show();
      assert.deepEqual(activations, [{ id: 'viewing-alert' }]);

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === 'Lion in Savanna was given a viewing alert.'
            && entry[2] === 'is-success'
         ))
      );
   } finally {
      ControllerHelper.loadOptionsAndShowPanel = originalLoad;
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.bindResetValueOnChange = originalBind;
      ControllerHelper.validateOptionalDateRange = originalValidate;
      ConsoleOperationsClient.setAnimalViewingAlert = originalSet;
   }
});

test('Test_CreateAnimalViewingAlertController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalSet = ConsoleOperationsClient.setAnimalViewingAlert;
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
      const messageEl = document.createElement('input');
      const controller = AnimalViewingController.createAnimalViewingAlertController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         cancelButtonEl,
         panelEl: {},
         statusEl: {},
         speciesEl,
         exhibitEl,
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         messageEl,
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
      ControllerHelper.getFieldValue = (el) => {
         if (el === speciesEl) return 'Lion';
         if (el === exhibitEl) return 'Savanna';
         return '';
      };
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.alertMessage)
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = (el) => {
         if (el === speciesEl) return 'Lion';
         if (el === exhibitEl) return 'Savanna';
         if (el === messageEl) return 'Behind glass';
         return '';
      };
      ControllerHelper.validateOptionalDateRange = () => 'bad range';
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'bad range'));

      statuses.length = 0;
      ControllerHelper.validateOptionalDateRange = () => null;
      ConsoleOperationsClient.setAnimalViewingAlert = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      ConsoleOperationsClient.setAnimalViewingAlert = async () => {
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
      ControllerHelper.validateOptionalDateRange = originalValidate;
      ControllerHelper.hideConsolePanel = originalHide;
      ConsoleOperationsClient.setAnimalViewingAlert = originalSet;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
