import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { AnimalExhibitAutofillController } from '../../../../../scripts/consoleOperations/animals/controllers/animalExhibitAutofillController.js';
import { AnimalOffController } from '../../../../../scripts/consoleOperations/animals/controllers/animalOffController.js';
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
   ControllerHelper.getFieldValue = originals.get;
   ControllerHelper.resetFormFields = originals.reset;
   ControllerHelper.bindResetValueOnChange = originals.bind;
   ControllerHelper.validateOptionalDateRange = originals.validate;
   ControllerHelper.hideConsolePanel = originals.hide;
   ConsoleStatusPresenter.setStatus = originals.status;
   AnimalViewingScopeController.createAnimalViewingScopeControl = originals.scope;
   AnimalExhibitAutofillController.createAnimalExhibitAutofillController = originals.autofill;
   ConsoleOperationsClient.setAnimalOffDisplay = originals.set;
   ApiErrorMessageResolver.resolveConsoleMutationError = originals.resolve;
}

function _installBaseStubs({
   statuses = [],
   activations = [],
   hides = [],
   resets = [],
   autofillArgs = [],
   viewingScopes = ['Male Herd'],
} = {}) {
   const originals = {
      load: ControllerHelper.loadOptionsAndShowPanel,
      get: ControllerHelper.getFieldValue,
      reset: ControllerHelper.resetFormFields,
      bind: ControllerHelper.bindResetValueOnChange,
      validate: ControllerHelper.validateOptionalDateRange,
      hide: ControllerHelper.hideConsolePanel,
      status: ConsoleStatusPresenter.setStatus,
      scope: AnimalViewingScopeController.createAnimalViewingScopeControl,
      autofill: AnimalExhibitAutofillController.createAnimalExhibitAutofillController,
      set: ConsoleOperationsClient.setAnimalOffDisplay,
      resolve: ApiErrorMessageResolver.resolveConsoleMutationError,
   };

   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      activations.push(options.panelEl);
      assert.equal(options.loadOptions, ConsoleOptionsLoader.loadExhibits);
      assert.equal(options.populateOptions, ConsoleDropdownPopulator.populateExhibitDropdown);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.bindResetValueOnChange = () => {};
   ControllerHelper.validateOptionalDateRange = () => null;
   ControllerHelper.hideConsolePanel = (args) => {
      hides.push(args);
   };
   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   AnimalViewingScopeController.createAnimalViewingScopeControl = () => ({
      reset: () => {
         resets.push(true);
      },
      refresh: async () => {},
      selectedEnclosureNames: () => viewingScopes,
   });
   AnimalExhibitAutofillController.createAnimalExhibitAutofillController = (args) => {
      autofillArgs.push(args);
      return originals.autofill(args);
   };

   return originals;
}

function _createController({
   panelEl = { id: 'animal-off' },
   species = 'Lion',
   exhibit = 'Savanna',
   startDate = '2026-06-01',
   message = 'Vet care',
} = {}) {
   const submitButtonEl = document.createElement('button');
   const cancelButtonEl = document.createElement('button');
   const speciesEl = document.createElement('input');
   const exhibitEl = document.createElement('select');
   const startDateEl = document.createElement('input');
   const messageEl = document.createElement('input');
   speciesEl.value = species;
   exhibitEl.value = exhibit;
   startDateEl.value = startDate;
   messageEl.value = message;

   const controller = AnimalOffController.createAnimalOffDisplayController({
      showButtonEl: document.createElement('button'),
      submitButtonEl,
      cancelButtonEl,
      panelEl,
      statusEl: {},
      speciesEl,
      exhibitEl,
      viewingScopeEl: document.createElement('select'),
      startDateEl,
      endDateEl: document.createElement('input'),
      messageEl,
      activatePanel: () => {},
   });

   return {
      controller,
      submitButtonEl,
      cancelButtonEl,
      speciesEl,
      exhibitEl,
      panelEl,
   };
}


test('Test_CreateAnimalOffDisplayController_TestShow_ExpectPanelActivated', async () => {
   const activations = [];
   const autofillArgs = [];
   const originals = _installBaseStubs({ activations, autofillArgs });
   const panelEl = { id: 'animal-off' };

   try {
      const { controller } = _createController({ panelEl });

      await controller.show();

      assert.deepEqual(activations, [panelEl]);
      assert.equal(autofillArgs[Position.FIRST].loadExhibits, ConsoleOptionsLoader.loadExhibits);
      assert.equal(autofillArgs[Position.FIRST].loadExhibitsForSpecies, ConsoleOptionsLoader.loadExhibitsForSpecies);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalOffDisplayController_TestSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const resets = [];
   const species = 'Lion';
   const exhibit = 'Savanna';
   const viewingScopes = ['Male Herd'];
   const startDate = '2026-06-01';
   const message = 'Vet care';
   const originals = _installBaseStubs({ statuses, resets, viewingScopes });

   ConsoleOperationsClient.setAnimalOffDisplay = async (payload) => {
      assert.deepEqual(payload, {
         species,
         exhibit,
         viewingScopes,
         startDate,
         endDate: null,
         message,
      });
      return { success: true, species, exhibit };
   };

   try {
      const { submitButtonEl } = _createController({ species, exhibit, startDate, message });

      await submitButtonEl.listeners.click();

      assert.ok(
         statuses.some((entry) => (
            entry[Position.SECOND] === Strings.status.animalOffDisplay({ species, exhibit })
            && entry[Position.THIRD] === 'is-success'
         ))
      );
      assert.ok(resets.length >= 1);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalOffDisplayController_TestMissingSpecies_ExpectErrorStatus', async () => {
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


test('Test_CreateAnimalOffDisplayController_TestMissingExhibit_ExpectErrorStatus', async () => {
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


test('Test_CreateAnimalOffDisplayController_TestInvalidDateRange_ExpectErrorStatus', async () => {
   const statuses = [];
   const badRange = 'bad range';
   const originals = _installBaseStubs({ statuses });
   ControllerHelper.validateOptionalDateRange = () => badRange;

   try {
      const { submitButtonEl } = _createController();

      await submitButtonEl.listeners.click();

      assert.ok(statuses.some((entry) => entry[Position.SECOND] === badRange));
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalOffDisplayController_TestMutationFailure_ExpectErrorStatus', async () => {
   const statuses = [];
   const mutationFailed = 'mutation failed';
   const originals = _installBaseStubs({ statuses });
   ApiErrorMessageResolver.resolveConsoleMutationError = () => mutationFailed;
   ConsoleOperationsClient.setAnimalOffDisplay = async () => ({ success: false });

   try {
      const { submitButtonEl } = _createController();

      await submitButtonEl.listeners.click();

      assert.ok(statuses.some((entry) => entry[Position.SECOND] === mutationFailed));
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalOffDisplayController_TestNetworkError_ExpectRequestFailed', async () => {
   const statuses = [];
   const originals = _installBaseStubs({ statuses });
   ConsoleOperationsClient.setAnimalOffDisplay = async () => {
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


test('Test_CreateAnimalOffDisplayController_TestHideAndCancel_ExpectPanelHidden', () => {
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
