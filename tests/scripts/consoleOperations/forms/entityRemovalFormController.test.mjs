import assert from 'node:assert/strict';
import test from 'node:test';

import { EntityRemovalFormController } from '../../../../scripts/consoleOperations/forms/entityRemovalFormController.js';
import { AnimalExhibitAutofillController } from '../../../../scripts/consoleOperations/animals/controllers/animalExhibitAutofillController.js';
import { ApiErrorMessageResolver } from '../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { ControllerHelper } from '../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateEntityRemovalFormController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const originalLoad = ControllerHelper.loadOptionsAndShowPanel;
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalReset = ControllerHelper.resetFormFields;
   const originalHide = ControllerHelper.hideConsolePanel;

   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      activations.push(options.panelEl);
      assert.equal(options.errorMessage, 'load failed');
   };
   ConsoleStatusPresenter.setStatus = (...args) => { statuses.push(args); };
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.hideConsolePanel = () => {};

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const cancelButtonEl = document.createElement('button');
      const speciesEl = { id: 'species' };
      const exhibitEl = { id: 'exhibit' };

      const controller = EntityRemovalFormController.createEntityRemovalFormController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl,
         panelEl: { id: 'remove-panel' },
         statusEl: {},
         formFieldEls: [speciesEl, exhibitEl],
         activatePanel: () => {},
         loadOptions: async () => [],
         populateOptions: () => {},
         targetEl: exhibitEl,
         loadErrorMessage: 'load failed',
         getFormValues: () => ({ species: 'Lion', exhibit: 'Savanna' }),
         validateForm: () => null,
         submitRemoval: async (payload) => {
            assert.deepEqual(payload, { species: 'Lion', exhibit: 'Savanna' });
            return { success: true, species: 'Lion', exhibit: 'Savanna' };
         },
         successMessage: result => `Removed ${result.species}`,
      });

      await controller.show();
      assert.deepEqual(activations, [{ id: 'remove-panel' }]);

      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'Removed Lion' && entry[2] === 'is-success'));
   } finally {
      ControllerHelper.loadOptionsAndShowPanel = originalLoad;
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.hideConsolePanel = originalHide;
   }
});

test('Test_CreateEntityRemovalFormController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalReset = ControllerHelper.resetFormFields;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;

   ConsoleStatusPresenter.setStatus = (...args) => { statuses.push(args); };
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.hideConsolePanel = (args) => { hides.push(args); };
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'mutation failed';

   try {
      const submitButtonEl = document.createElement('button');
      const cancelButtonEl = document.createElement('button');
      let formValues = { restroom: '' };
      let submitRemoval = async () => ({ success: false });

      const controller = EntityRemovalFormController.createEntityRemovalFormController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         cancelButtonEl,
         panelEl: {},
         statusEl: {},
         formFieldEls: [],
         activatePanel: () => {},
         loadOptions: async () => [],
         populateOptions: () => {},
         targetEl: {},
         loadErrorMessage: Strings.loadErrors.restrooms,
         getFormValues: () => formValues,
         validateForm: ({ restroom }) => (
            restroom
               ? null
               : Strings.validation.entityRequired(Strings.entityLabels.restroom)
         ),
         submitRemoval: (...args) => submitRemoval(...args),
         successMessage: 'done',
      });

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.entityLabels.restroom)
            && entry[2] === 'is-error'
         ))
      );

      statuses.length = 0;
      formValues = { restroom: 'Near Cafe' };
      submitRemoval = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      submitRemoval = async () => { throw new Error('network'); };
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.common.requestFailed));

      controller.hide();
      cancelButtonEl.listeners.click();
      assert.equal(hides.length, 2);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.hideConsolePanel = originalHide;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});

test('Test_CreateEntityRemovalFormController_TestReloadOptionsThrows_ExpectClearsFields', async () => {
   const resets = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalReload = ControllerHelper.reloadOptions;
   const originalReset = ControllerHelper.resetFormFields;

   ConsoleStatusPresenter.setStatus = () => {};
   ControllerHelper.reloadOptions = async () => {
      throw new Error('reload failed');
   };
   ControllerHelper.resetFormFields = (...args) => {
      resets.push(args);
   };

   try {
      const submitButtonEl = document.createElement('button');
      const exhibitEl = { id: 'exhibit' };

      EntityRemovalFormController.createEntityRemovalFormController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         panelEl: {},
         statusEl: {},
         formFieldEls: [exhibitEl],
         activatePanel: () => {},
         loadOptions: async () => [],
         populateOptions: () => {},
         targetEl: exhibitEl,
         loadErrorMessage: 'load failed',
         getFormValues: () => ({ exhibit: 'Savanna' }),
         validateForm: () => null,
         submitRemoval: async () => ({ success: true, exhibit: 'Savanna' }),
         successMessage: 'done',
      });

      await submitButtonEl.listeners.click();
      assert.equal(resets.length, 1);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.reloadOptions = originalReload;
      ControllerHelper.resetFormFields = originalReset;
   }
});

test('Test_CreateEntityRemovalFormController_TestSpeciesLoaders_ExpectAutofillWired', () => {
   const originalAutofill = AnimalExhibitAutofillController.createAnimalExhibitAutofillController;
   const autofillArgs = [];
   const speciesEl = document.createElement('input');
   const exhibitEl = document.createElement('select');
   const loadOptions = async () => ['Africa Savanna'];
   const loadOptionsForSpecies = async () => ['Africa Savanna'];

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController = (args) => {
      autofillArgs.push(args);
      return originalAutofill(args);
   };

   try {
      EntityRemovalFormController.createEntityRemovalFormController({
         showButtonEl: document.createElement('button'),
         panelEl: {},
         statusEl: {},
         formFieldEls: [speciesEl, exhibitEl],
         activatePanel: () => {},
         loadOptions,
         populateOptions: () => {},
         targetEl: exhibitEl,
         loadErrorMessage: 'load failed',
         getFormValues: () => ({}),
         validateForm: () => null,
         submitRemoval: async () => ({ success: true }),
         successMessage: 'done',
         speciesEl,
         loadOptionsForSpecies,
      });

      assert.equal(autofillArgs.length, 1);
      assert.equal(autofillArgs[Position.FIRST].loadExhibits, loadOptions);
      assert.equal(autofillArgs[Position.FIRST].loadExhibitsForSpecies, loadOptionsForSpecies);

      autofillArgs.length = 0;
      EntityRemovalFormController.createEntityRemovalFormController({
         showButtonEl: document.createElement('button'),
         panelEl: {},
         statusEl: {},
         formFieldEls: [],
         activatePanel: () => {},
         loadOptions,
         populateOptions: () => {},
         targetEl: exhibitEl,
         loadErrorMessage: 'load failed',
         getFormValues: () => ({}),
         validateForm: () => null,
         submitRemoval: async () => ({ success: true }),
         successMessage: 'done',
      });
      assert.equal(autofillArgs.length, 0);
   } finally {
      AnimalExhibitAutofillController.createAnimalExhibitAutofillController = originalAutofill;
   }
});
