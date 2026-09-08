import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalOffController } from '../../../../../scripts/consoleOperations/animals/controllers/animalOffController.js';
import { AnimalViewingScopeController } from '../../../../../scripts/consoleOperations/animals/controllers/animalViewingScopeController.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { AnimalViewingModel } from '../../../../../scripts/shared/enums/animalViewingModel.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateAnimalOffDisplayController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const resets = [];
   const originalLoad = ControllerHelper.loadOptionsAndShowPanel;
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalScope = AnimalViewingScopeController.createAnimalViewingScopeControl;
   const originalSet = ConsoleOperationsClient.setAnimalOffDisplay;

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
   AnimalViewingScopeController.createAnimalViewingScopeControl = () => ({
      reset: () => {
         resets.push(true);
      },
   });
   ConsoleOperationsClient.setAnimalOffDisplay = async (payload) => {
      assert.deepEqual(payload, {
         species: 'Lion',
         exhibit: 'Savanna',
         viewingScope: AnimalViewingModel.ALL,
         startDate: '2026-06-01',
         endDate: null,
         message: 'Vet care',
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
      messageEl.value = 'Vet care';

      const controller = AnimalOffController.createAnimalOffDisplayController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: { id: 'animal-off' },
         statusEl: {},
         speciesEl,
         exhibitEl,
         viewingScopeEl: document.createElement('select'),
         startDateEl,
         endDateEl: document.createElement('input'),
         messageEl,
         activatePanel: () => {},
      });

      await controller.show();
      assert.deepEqual(activations, [{ id: 'animal-off' }]);

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.status.animalOffDisplay({ species: 'Lion', exhibit: 'Savanna' })
            && entry[2] === 'is-success'
         ))
      );
      assert.ok(resets.length >= 1);
   } finally {
      ControllerHelper.loadOptionsAndShowPanel = originalLoad;
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.bindResetValueOnChange = originalBind;
      ControllerHelper.validateOptionalDateRange = originalValidate;
      AnimalViewingScopeController.createAnimalViewingScopeControl = originalScope;
      ConsoleOperationsClient.setAnimalOffDisplay = originalSet;
   }
});

test('Test_CreateAnimalOffDisplayController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalScope = AnimalViewingScopeController.createAnimalViewingScopeControl;
   const originalSet = ConsoleOperationsClient.setAnimalOffDisplay;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.bindResetValueOnChange = () => {};
   ControllerHelper.hideConsolePanel = (args) => {
      hides.push(args);
   };
   AnimalViewingScopeController.createAnimalViewingScopeControl = () => ({
      reset: () => {},
   });
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'mutation failed';

   try {
      const submitButtonEl = document.createElement('button');
      const cancelButtonEl = document.createElement('button');
      const speciesEl = document.createElement('input');
      const exhibitEl = document.createElement('select');
      const controller = AnimalOffController.createAnimalOffDisplayController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         cancelButtonEl,
         panelEl: {},
         statusEl: {},
         speciesEl,
         exhibitEl,
         viewingScopeEl: document.createElement('select'),
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         messageEl: document.createElement('input'),
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
      ControllerHelper.validateOptionalDateRange = () => 'bad range';
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'bad range'));

      statuses.length = 0;
      ControllerHelper.validateOptionalDateRange = () => null;
      ConsoleOperationsClient.setAnimalOffDisplay = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      ConsoleOperationsClient.setAnimalOffDisplay = async () => {
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
      AnimalViewingScopeController.createAnimalViewingScopeControl = originalScope;
      ConsoleOperationsClient.setAnimalOffDisplay = originalSet;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
