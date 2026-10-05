import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalsClient } from '../../../../../scripts/api/animalsClient.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { AnimalExhibitAutofillController } from '../../../../../scripts/consoleOperations/animals/controllers/animalExhibitAutofillController.js';
import { AnimalOnController } from '../../../../../scripts/consoleOperations/animals/controllers/animalOnController.js';
import { AnimalViewingScopeController } from '../../../../../scripts/consoleOperations/animals/controllers/animalViewingScopeController.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _restore(originals) {
   ControllerHelper.loadOptionsAndShowPanel = originals.load;
   ControllerHelper.reloadOptions = originals.reload;
   ControllerHelper.getFieldValue = originals.get;
   ControllerHelper.resetFormFields = originals.reset;
   ControllerHelper.bindResetValueOnChange = originals.bind;
   ControllerHelper.hideConsolePanel = originals.hide;
   ConsoleStatusPresenter.setStatus = originals.status;
   AnimalViewingScopeController.createAnimalViewingScopeControl = originals.scope;
   AnimalExhibitAutofillController.createAnimalExhibitAutofillController = originals.autofill;
   ConsoleOperationsClient.setAnimalOnDisplay = originals.set;
   ApiErrorMessageResolver.resolveConsoleMutationError = originals.resolve;
}

function _installBaseStubs({
   statuses = [],
   activations = [],
   hides = [],
   resets = [],
   autofillArgs = [],
   scopeArgs = [],
   viewingScopes = ['Male Herd'],
} = {}) {
   const originals = {
      load: ControllerHelper.loadOptionsAndShowPanel,
      reload: ControllerHelper.reloadOptions,
      get: ControllerHelper.getFieldValue,
      reset: ControllerHelper.resetFormFields,
      bind: ControllerHelper.bindResetValueOnChange,
      hide: ControllerHelper.hideConsolePanel,
      status: ConsoleStatusPresenter.setStatus,
      scope: AnimalViewingScopeController.createAnimalViewingScopeControl,
      autofill: AnimalExhibitAutofillController.createAnimalExhibitAutofillController,
      set: ConsoleOperationsClient.setAnimalOnDisplay,
      resolve: ApiErrorMessageResolver.resolveConsoleMutationError,
   };

   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      activations.push(options.panelEl);
      assert.equal(options.loadOptions, ConsoleOptionsLoader.loadOffDisplayExhibits);
      assert.equal(options.populateOptions, ConsoleDropdownPopulator.populateExhibitDropdown);
   };
   ControllerHelper.reloadOptions = async (options) => {
      options.resetForm?.();
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.bindResetValueOnChange = () => {};
   ControllerHelper.hideConsolePanel = (args) => {
      hides.push(args);
   };
   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   AnimalViewingScopeController.createAnimalViewingScopeControl = (args) => {
      scopeArgs.push(args);
      return {
         reset: () => {
            resets.push(true);
         },
         refresh: async () => {},
         selectedEnclosureNames: () => viewingScopes,
      };
   };
   AnimalExhibitAutofillController.createAnimalExhibitAutofillController = (args) => {
      autofillArgs.push(args);
      return originals.autofill(args);
   };

   return originals;
}

function _createController({
   panelEl = { id: 'animal-on' },
   species = 'Lion',
   exhibit = 'Savanna',
   createController = AnimalOnController.createAnimalOnDisplayController,
} = {}) {
   const showButtonEl = document.createElement('button');
   const submitButtonEl = document.createElement('button');
   const cancelButtonEl = document.createElement('button');
   const speciesEl = document.createElement('input');
   const exhibitEl = document.createElement('select');
   speciesEl.value = species;
   exhibitEl.value = exhibit;

   const controller = createController({
      showButtonEl,
      submitButtonEl,
      cancelButtonEl,
      panelEl,
      statusEl: {},
      speciesEl,
      exhibitEl,
      viewingScopeEl: document.createElement('select'),
      activatePanel: () => {},
   });

   return {
      controller,
      showButtonEl,
      submitButtonEl,
      cancelButtonEl,
      speciesEl,
      exhibitEl,
      panelEl,
   };
}


test('Test_CreateAnimalOnDisplayController_TestShow_ExpectPanelActivated', async () => {
   const activations = [];
   const autofillArgs = [];
   const scopeArgs = [];
   const originals = _installBaseStubs({ activations, autofillArgs, scopeArgs });
   const panelEl = { id: 'animal-on' };

   try {
      const { controller } = _createController({ panelEl });

      await controller.show();

      assert.deepEqual(activations, [panelEl]);
      assert.equal(autofillArgs[Position.FIRST].loadExhibits, ConsoleOptionsLoader.loadOffDisplayExhibits);
      assert.equal(autofillArgs[Position.FIRST].loadExhibitsForSpecies, ConsoleOptionsLoader.loadOffDisplayExhibits);
      assert.equal(scopeArgs[Position.FIRST].loadViewingScopes, ConsoleOptionsLoader.loadOffDisplayViewingScopes);
      assert.equal(scopeArgs[Position.FIRST].loadAnimalViewingScopes, AnimalsClient.getAnimalViewingScopes);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalOnDisplayController_TestSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const resets = [];
   const species = 'Lion';
   const exhibit = 'Savanna';
   const viewingScopes = ['Male Herd'];
   const originals = _installBaseStubs({ statuses, resets, viewingScopes });

   ConsoleOperationsClient.setAnimalOnDisplay = async (payload) => {
      assert.deepEqual(payload, { species, exhibit, viewingScopes });
      return { success: true, species, exhibit };
   };

   try {
      const { submitButtonEl } = _createController({ species, exhibit });

      await submitButtonEl.listeners.click();

      assert.ok(
         statuses.some((entry) => (
            entry[Position.SECOND] === Strings.status.animalOnDisplay({ species, exhibit })
            && entry[Position.THIRD] === 'is-success'
         ))
      );
      assert.ok(resets.length >= 1);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalOnDisplayController_TestMissingSpecies_ExpectErrorStatus', async () => {
   const statuses = [];
   const originals = _installBaseStubs({ statuses });

   try {
      const { submitButtonEl } = _createController({ species: '', exhibit: '' });
      ControllerHelper.getFieldValue = () => '';

      await submitButtonEl.listeners.click();

      assert.ok(
         statuses.some((entry) => (
            entry[Position.SECOND] === Strings.validation.entityRequired(Strings.labels.species)
         ))
      );
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalOnDisplayController_TestMissingExhibit_ExpectErrorStatus', async () => {
   const statuses = [];
   const species = 'Lion';
   const originals = _installBaseStubs({ statuses });

   try {
      const { submitButtonEl, speciesEl } = _createController({ species, exhibit: '' });
      ControllerHelper.getFieldValue = (el) => (el === speciesEl ? species : '');

      await submitButtonEl.listeners.click();

      assert.ok(
         statuses.some((entry) => (
            entry[Position.SECOND] === Strings.validation.entityRequired(Strings.entityLabels.exhibit)
         ))
      );
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalOnDisplayController_TestMutationFailure_ExpectErrorStatus', async () => {
   const statuses = [];
   const mutationFailed = 'mutation failed';
   const originals = _installBaseStubs({ statuses });
   ApiErrorMessageResolver.resolveConsoleMutationError = () => mutationFailed;
   ConsoleOperationsClient.setAnimalOnDisplay = async () => ({ success: false });

   try {
      const { submitButtonEl } = _createController();

      await submitButtonEl.listeners.click();

      assert.ok(statuses.some((entry) => entry[Position.SECOND] === mutationFailed));
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalOnDisplayController_TestNetworkError_ExpectRequestFailed', async () => {
   const statuses = [];
   const originals = _installBaseStubs({ statuses });
   ConsoleOperationsClient.setAnimalOnDisplay = async () => {
      throw new Error('network');
   };

   try {
      const { submitButtonEl } = _createController();

      await submitButtonEl.listeners.click();

      assert.ok(statuses.some((entry) => entry[Position.SECOND] === Strings.common.requestFailed));
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalOnDisplayController_TestHideAndCancel_ExpectPanelHidden', () => {
   const hides = [];
   const originals = _installBaseStubs({ hides });

   try {
      const { controller, cancelButtonEl } = _createController();

      controller.hide();
      cancelButtonEl.listeners.click();

      assert.equal(hides.length, 2);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalOnDisplayForSeasonController_TestShow_ExpectSeasonLoaders', async (t) => {
   const activations = [];
   const autofillArgs = [];
   const scopeArgs = [];
   const originals = _installBaseStubs({ autofillArgs, scopeArgs });
   t.after(() => _restore(originals));
   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      activations.push(options.loadOptions);
   };
   const { controller } = _createController({
      createController: AnimalOnController.createAnimalOnDisplayForSeasonController,
   });

   await controller.show();

   assert.deepEqual(activations, [ConsoleOptionsLoader.loadOffDisplayForSeasonExhibits]);
   assert.equal(autofillArgs[Position.FIRST].loadExhibits, ConsoleOptionsLoader.loadOffDisplayForSeasonExhibits);
   assert.equal(autofillArgs[Position.FIRST].loadExhibitsForSpecies, ConsoleOptionsLoader.loadOffDisplayForSeasonExhibits);
   assert.equal(scopeArgs[Position.FIRST].loadViewingScopes, ConsoleOptionsLoader.loadOffDisplayForSeasonViewingScopes);
   assert.equal(scopeArgs[Position.FIRST].loadAnimalViewingScopes, AnimalsClient.getAnimalViewingScopes);
});


test('Test_CreateAnimalOnDisplayForSeasonController_TestSubmitSuccess_ExpectSeasonStatus', async (t) => {
   const statuses = [];
   const payloads = [];
   const species = 'Marabou Stork';
   const exhibit = 'Africa Savanna';
   const viewingScopes = ['White Rhino Viewing'];
   const originals = _installBaseStubs({ statuses, viewingScopes });
   t.after(() => _restore(originals));
   ConsoleOperationsClient.setAnimalOnDisplay = async (payload) => {
      payloads.push(payload);
      return { success: true, species, exhibit };
   };
   const { submitButtonEl } = _createController({
      species,
      exhibit,
      createController: AnimalOnController.createAnimalOnDisplayForSeasonController,
   });

   await submitButtonEl.listeners.click();

   assert.deepEqual(payloads, [{ species, exhibit, viewingScopes }]);
   assert.ok(
      statuses.some((entry) => (
         entry[Position.SECOND] === Strings.status.animalOnDisplayForSeason({ species, exhibit })
         && entry[Position.THIRD] === 'is-success'
      ))
   );
});
