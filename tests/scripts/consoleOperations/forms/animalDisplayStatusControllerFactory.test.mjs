import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalDisplayStatusControllerFactory } from '../../../../scripts/consoleOperations/forms/animalDisplayStatusControllerFactory.js';
import { AnimalViewingScopeController } from '../../../../scripts/consoleOperations/animals/controllers/animalViewingScopeController.js';
import { ApiErrorMessageResolver } from '../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { ControllerHelper } from '../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ConsoleOptionsLoader } from '../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleDropdownPopulator } from '../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { ConsoleStatusPresenter } from '../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateAnimalDisplayStatusController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const resets = [];
   const originalLoad = ControllerHelper.loadOptionsAndShowPanel;
   const originalReload = ControllerHelper.reloadOptions;
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalScope = AnimalViewingScopeController.createAnimalViewingScopeControl;

   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      activations.push(options.panelEl);
      assert.equal(options.loadOptions, ConsoleOptionsLoader.loadExhibits);
      assert.equal(options.populateOptions, ConsoleDropdownPopulator.populateExhibitDropdown);
      assert.equal(options.errorMessage, Strings.loadErrors.exhibits);
   };
   ControllerHelper.reloadOptions = async (options) => {
      options.resetForm?.();
   };
   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {};
   AnimalViewingScopeController.createAnimalViewingScopeControl = () => ({
      reset: () => {
         resets.push(true);
      },
      refresh: async () => {},
      selectedEnclosureNames: () => [ 'Male Herd' ],
   });

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const speciesEl = document.createElement('input');
      const exhibitEl = document.createElement('select');
      speciesEl.value = 'Lion';
      exhibitEl.value = 'Savanna';

      const controller = AnimalDisplayStatusControllerFactory.createAnimalDisplayStatusController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: { id: 'animal-display' },
         statusEl: {},
         speciesEl,
         exhibitEl,
         viewingScopeEl: document.createElement('select'),
         activatePanel: () => {},
         submitDisplayStatus: async (payload) => {
            assert.deepEqual(payload, {
               species: 'Lion',
               exhibit: 'Savanna',
               viewingScopes: [ 'Male Herd' ],
               startDate: '',
               endDate: '',
               message: '',
            });
            return { success: true, species: 'Lion', exhibit: 'Savanna' };
         },
         successMessage: result => `On display: ${result.species}`,
      });

      await controller.show();
      assert.deepEqual(activations, [{ id: 'animal-display' }]);

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === 'On display: Lion'
            && entry[2] === 'is-success'
         ))
      );
      assert.ok(resets.length >= 1);
   } finally {
      ControllerHelper.loadOptionsAndShowPanel = originalLoad;
      ControllerHelper.reloadOptions = originalReload;
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.bindResetValueOnChange = originalBind;
      AnimalViewingScopeController.createAnimalViewingScopeControl = originalScope;
   }
});

test('Test_CreateAnimalDisplayStatusController_TestDateRangeAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalScope = AnimalViewingScopeController.createAnimalViewingScopeControl;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.bindResetValueOnChange = () => {};
   ControllerHelper.validateOptionalDateRange = () => 'bad dates';
   ControllerHelper.hideConsolePanel = (args) => {
      hides.push(args);
   };
   AnimalViewingScopeController.createAnimalViewingScopeControl = () => ({
      reset: () => {},
      refresh: async () => {},
      selectedEnclosureNames: () => [ 'Male Herd' ],
   });
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'mutation failed';

   try {
      const submitButtonEl = document.createElement('button');
      const cancelButtonEl = document.createElement('button');
      const speciesEl = document.createElement('input');
      const exhibitEl = document.createElement('select');
      const startDateEl = document.createElement('input');
      const endDateEl = document.createElement('input');
      speciesEl.value = 'Lion';
      exhibitEl.value = 'Savanna';
      startDateEl.value = '2026-07-02';
      endDateEl.value = '2026-07-01';

      const controller = AnimalDisplayStatusControllerFactory.createAnimalDisplayStatusController({
         submitButtonEl,
         cancelButtonEl,
         panelEl: { id: 'animal-off' },
         statusEl: {},
         speciesEl,
         exhibitEl,
         viewingScopeEl: document.createElement('select'),
         startDateEl,
         endDateEl,
         messageEl: document.createElement('textarea'),
         activatePanel: () => {},
         submitDisplayStatus: async () => ({ success: false }),
         successMessage: () => 'ok',
      });

      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'bad dates' && entry[2] === 'is-error'));

      ControllerHelper.validateOptionalDateRange = () => null;
      statuses.length = 0;
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed' && entry[2] === 'is-error'));

      await cancelButtonEl.listeners.click();
      assert.equal(hides.length, 1);
      assert.equal(hides[0].panelEl.id, 'animal-off');
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.bindResetValueOnChange = originalBind;
      ControllerHelper.validateOptionalDateRange = originalValidate;
      ControllerHelper.hideConsolePanel = originalHide;
      AnimalViewingScopeController.createAnimalViewingScopeControl = originalScope;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});

test('Test_CreateAnimalDisplayStatusController_TestMissingSpecies_ExpectValidationError', async () => {
   const statuses = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalScope = AnimalViewingScopeController.createAnimalViewingScopeControl;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.bindResetValueOnChange = () => {};
   AnimalViewingScopeController.createAnimalViewingScopeControl = () => ({
      reset: () => {},
      refresh: async () => {},
      selectedEnclosureNames: () => [ 'Male Herd' ],
   });

   try {
      const submitButtonEl = document.createElement('button');
      const speciesEl = document.createElement('input');
      const exhibitEl = document.createElement('select');
      exhibitEl.value = 'Savanna';

      AnimalDisplayStatusControllerFactory.createAnimalDisplayStatusController({
         submitButtonEl,
         panelEl: {},
         statusEl: {},
         speciesEl,
         exhibitEl,
         viewingScopeEl: document.createElement('select'),
         submitDisplayStatus: async () => ({ success: true }),
         successMessage: () => 'ok',
      });

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.species)
            && entry[2] === 'is-error'
         ))
      );
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.bindResetValueOnChange = originalBind;
      AnimalViewingScopeController.createAnimalViewingScopeControl = originalScope;
   }
});

test('Test_CreateAnimalDisplayStatusController_TestMissingViewingScope_ExpectValidationError', async () => {
   const statuses = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalScope = AnimalViewingScopeController.createAnimalViewingScopeControl;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.bindResetValueOnChange = () => {};
   AnimalViewingScopeController.createAnimalViewingScopeControl = () => ({
      reset: () => {},
      refresh: async () => {},
      selectedEnclosureNames: () => [],
   });

   try {
      const submitButtonEl = document.createElement('button');
      const speciesEl = document.createElement('input');
      const exhibitEl = document.createElement('select');
      speciesEl.value = 'Lion';
      exhibitEl.value = 'Savanna';

      AnimalDisplayStatusControllerFactory.createAnimalDisplayStatusController({
         submitButtonEl,
         panelEl: {},
         statusEl: {},
         speciesEl,
         exhibitEl,
         viewingScopeEl: document.createElement('div'),
         submitDisplayStatus: async () => ({ success: true }),
         successMessage: () => 'ok',
      });

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.viewingScope)
            && entry[2] === 'is-error'
         ))
      );
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.bindResetValueOnChange = originalBind;
      AnimalViewingScopeController.createAnimalViewingScopeControl = originalScope;
   }
});

test('Test_CreateAnimalDisplayStatusController_TestInjectedLoadExhibits_ExpectUsed', async () => {
   const originalLoad = ControllerHelper.loadOptionsAndShowPanel;
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalReset = ControllerHelper.resetFormFields;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalScope = AnimalViewingScopeController.createAnimalViewingScopeControl;
   const loadExhibits = async () => ['Africa Savanna'];
   let usedLoader;

   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      usedLoader = options.loadOptions;
   };
   ConsoleStatusPresenter.setStatus = () => {};
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.bindResetValueOnChange = () => {};
   AnimalViewingScopeController.createAnimalViewingScopeControl = () => ({
      reset: () => {},
      refresh: async () => {},
      selectedEnclosureNames: () => [ 'Male Herd' ],
   });

   try {
      const controller = AnimalDisplayStatusControllerFactory.createAnimalDisplayStatusController({
         panelEl: {},
         statusEl: {},
         speciesEl: document.createElement('input'),
         exhibitEl: document.createElement('select'),
         viewingScopeEl: document.createElement('select'),
         activatePanel: () => {},
         submitDisplayStatus: async () => ({ success: true }),
         successMessage: () => 'ok',
         loadExhibits,
      });

      await controller.show();
      assert.equal(usedLoader, loadExhibits);
   } finally {
      ControllerHelper.loadOptionsAndShowPanel = originalLoad;
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.bindResetValueOnChange = originalBind;
      AnimalViewingScopeController.createAnimalViewingScopeControl = originalScope;
   }
});

test('Test_CreateAnimalDisplayStatusController_TestUniqueSpecies_ExpectFillsExhibitAndRefreshesScope', async () => {
   const refreshes = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalScope = AnimalViewingScopeController.createAnimalViewingScopeControl;

   ConsoleStatusPresenter.setStatus = () => {};
   AnimalViewingScopeController.createAnimalViewingScopeControl = () => ({
      reset: () => {},
      refresh: async () => {
         refreshes.push(true);
      },
   });

   try {
      const speciesEl = document.createElement('input');
      const exhibitEl = document.createElement('select');
      speciesEl.value = 'African Lion';

      AnimalDisplayStatusControllerFactory.createAnimalDisplayStatusController({
         panelEl: {},
         statusEl: {},
         speciesEl,
         exhibitEl,
         viewingScopeEl: document.createElement('select'),
         activatePanel: () => {},
         submitDisplayStatus: async () => ({ success: true }),
         successMessage: () => 'ok',
         loadExhibits: async () => ['Africa Savanna', 'Eurasia Wilds'],
         loadExhibitsForSpecies: async (species) => {
            assert.equal(species, 'African Lion');
            return ['Africa Savanna'];
         },
      });

      await speciesEl.listeners.change();
      assert.equal(exhibitEl.value, 'Africa Savanna');
      assert.equal(speciesEl.value, 'African Lion');
      assert.deepEqual(refreshes, [true]);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      AnimalViewingScopeController.createAnimalViewingScopeControl = originalScope;
   }
});

test('Test_CreateAnimalDisplayStatusController_TestReloadOptionsThrows_ExpectClearsFields', async () => {
   const resets = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalReload = ControllerHelper.reloadOptions;
   const originalReset = ControllerHelper.resetFormFields;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalScope = AnimalViewingScopeController.createAnimalViewingScopeControl;

   ConsoleStatusPresenter.setStatus = () => {};
   ControllerHelper.reloadOptions = async () => {
      throw new Error('reload failed');
   };
   ControllerHelper.resetFormFields = (...args) => {
      resets.push(args);
   };
   ControllerHelper.bindResetValueOnChange = () => {};
   AnimalViewingScopeController.createAnimalViewingScopeControl = () => ({
      reset: () => {},
      refresh: async () => {},
      selectedEnclosureNames: () => [ 'Male Herd' ],
   });

   try {
      const submitButtonEl = document.createElement('button');
      const speciesEl = document.createElement('input');
      const exhibitEl = document.createElement('select');
      speciesEl.value = 'Lion';
      exhibitEl.value = 'Savanna';

      AnimalDisplayStatusControllerFactory.createAnimalDisplayStatusController({
         submitButtonEl,
         panelEl: {},
         statusEl: {},
         speciesEl,
         exhibitEl,
         viewingScopeEl: document.createElement('select'),
         submitDisplayStatus: async () => ({ success: true, species: 'Lion' }),
         successMessage: () => 'ok',
      });

      await submitButtonEl.listeners.click();
      assert.equal(resets.length, 1);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.reloadOptions = originalReload;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.bindResetValueOnChange = originalBind;
      AnimalViewingScopeController.createAnimalViewingScopeControl = originalScope;
   }
});
