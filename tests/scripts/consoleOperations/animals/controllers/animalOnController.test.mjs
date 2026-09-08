import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalOnController } from '../../../../../scripts/consoleOperations/animals/controllers/animalOnController.js';
import { AnimalViewingScopeController } from '../../../../../scripts/consoleOperations/animals/controllers/animalViewingScopeController.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { AnimalViewingScope } from '../../../../../scripts/shared/enums/animalViewingScope.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateAnimalOnDisplayController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const resets = [];
   const originalLoad = ControllerHelper.loadOptionsAndShowPanel;
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalScope = AnimalViewingScopeController.createAnimalViewingScopeControl;
   const originalSet = ConsoleOperationsClient.setAnimalOnDisplay;

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
   AnimalViewingScopeController.createAnimalViewingScopeControl = () => ({
      reset: () => {
         resets.push(true);
      },
   });
   ConsoleOperationsClient.setAnimalOnDisplay = async (payload) => {
      assert.deepEqual(payload, {
         species: 'Lion',
         exhibit: 'Savanna',
         viewingScope: AnimalViewingScope.ALL,
      });
      return { success: true, species: 'Lion', exhibit: 'Savanna' };
   };

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const speciesEl = document.createElement('input');
      const exhibitEl = document.createElement('select');
      speciesEl.value = 'Lion';
      exhibitEl.value = 'Savanna';

      const controller = AnimalOnController.createAnimalOnDisplayController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: { id: 'animal-on' },
         statusEl: {},
         speciesEl,
         exhibitEl,
         viewingScopeEl: document.createElement('select'),
         activatePanel: () => {},
      });

      await controller.show();
      assert.deepEqual(activations, [{ id: 'animal-on' }]);

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.status.animalOnDisplay({ species: 'Lion', exhibit: 'Savanna' })
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
      AnimalViewingScopeController.createAnimalViewingScopeControl = originalScope;
      ConsoleOperationsClient.setAnimalOnDisplay = originalSet;
   }
});

test('Test_CreateAnimalOnDisplayController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalScope = AnimalViewingScopeController.createAnimalViewingScopeControl;
   const originalSet = ConsoleOperationsClient.setAnimalOnDisplay;
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
      const controller = AnimalOnController.createAnimalOnDisplayController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         cancelButtonEl,
         panelEl: {},
         statusEl: {},
         speciesEl,
         exhibitEl,
         viewingScopeEl: document.createElement('select'),
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
         return AnimalViewingScope.INDOOR;
      };
      ConsoleOperationsClient.setAnimalOnDisplay = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      ConsoleOperationsClient.setAnimalOnDisplay = async () => {
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
      AnimalViewingScopeController.createAnimalViewingScopeControl = originalScope;
      ConsoleOperationsClient.setAnimalOnDisplay = originalSet;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
