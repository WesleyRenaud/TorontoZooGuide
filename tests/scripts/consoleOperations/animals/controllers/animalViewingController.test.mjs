import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { AnimalExhibitAutofillController } from '../../../../../scripts/consoleOperations/animals/controllers/animalExhibitAutofillController.js';
import { AnimalViewingController } from '../../../../../scripts/consoleOperations/animals/controllers/animalViewingController.js';
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
   ControllerHelper.validateOptionalDateRange = originals.validate;
   ControllerHelper.hideConsolePanel = originals.hide;
   ConsoleStatusPresenter.setStatus = originals.status;
   AnimalExhibitAutofillController.createAnimalExhibitAutofillController = originals.autofill;
   ConsoleOperationsClient.setAnimalViewingAlert = originals.set;
   ApiErrorMessageResolver.resolveConsoleMutationError = originals.resolve;
}

function _installBaseStubs({
   statuses = [],
   activations = [],
   hides = [],
   autofillArgs = [],
} = {}) {
   const originals = {
      load: ControllerHelper.loadOptionsAndShowPanel,
      reload: ControllerHelper.reloadOptions,
      get: ControllerHelper.getFieldValue,
      reset: ControllerHelper.resetFormFields,
      bind: ControllerHelper.bindResetValueOnChange,
      validate: ControllerHelper.validateOptionalDateRange,
      hide: ControllerHelper.hideConsolePanel,
      status: ConsoleStatusPresenter.setStatus,
      autofill: AnimalExhibitAutofillController.createAnimalExhibitAutofillController,
      set: ConsoleOperationsClient.setAnimalViewingAlert,
      resolve: ApiErrorMessageResolver.resolveConsoleMutationError,
   };

   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      activations.push(options.panelEl);
      assert.equal(options.loadOptions, ConsoleOptionsLoader.loadExhibits);
      assert.equal(options.populateOptions, ConsoleDropdownPopulator.populateExhibitDropdown);
   };
   ControllerHelper.reloadOptions = async () => {};
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
   AnimalExhibitAutofillController.createAnimalExhibitAutofillController = (args) => {
      autofillArgs.push(args);
      return originals.autofill(args);
   };

   return originals;
}

function _createController({
   panelEl = { id: 'viewing-alert' },
   species = 'Lion',
   exhibit = 'Savanna',
   startDate = '2026-06-01',
   message = 'Behind glass',
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

   const controller = AnimalViewingController.createAnimalViewingAlertController({
      showButtonEl: document.createElement('button'),
      submitButtonEl,
      cancelButtonEl,
      panelEl,
      statusEl: {},
      speciesEl,
      exhibitEl,
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
      messageEl,
      panelEl,
   };
}


test('Test_CreateAnimalViewingAlertController_TestShow_ExpectPanelActivated', async () => {
   const activations = [];
   const autofillArgs = [];
   const originals = _installBaseStubs({ activations, autofillArgs });
   const panelEl = { id: 'viewing-alert' };

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


test('Test_CreateAnimalViewingAlertController_TestSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const species = 'Lion';
   const exhibit = 'Savanna';
   const startDate = '2026-06-01';
   const message = 'Behind glass';
   const originals = _installBaseStubs({ statuses });

   ConsoleOperationsClient.setAnimalViewingAlert = async (payload) => {
      assert.deepEqual(payload, {
         species,
         exhibit,
         alertStartDate: startDate,
         alertEndDate: null,
         message,
      });
      return { success: true, species, exhibit };
   };

   try {
      const { submitButtonEl } = _createController({ species, exhibit, startDate, message });

      await submitButtonEl.listeners.click();

      assert.ok(
         statuses.some((entry) => (
            entry[Position.SECOND] === Strings.status.animalViewingAlertSaved({ species, exhibit })
            && entry[Position.THIRD] === 'is-success'
         ))
      );
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalViewingAlertController_TestMissingSpecies_ExpectErrorStatus', async () => {
   const statuses = [];
   const originals = _installBaseStubs({ statuses });

   try {
      const { submitButtonEl } = _createController({ species: '', exhibit: '', message: '' });
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


test('Test_CreateAnimalViewingAlertController_TestMissingExhibit_ExpectErrorStatus', async () => {
   const statuses = [];
   const species = 'Lion';
   const originals = _installBaseStubs({ statuses });

   try {
      const { submitButtonEl, speciesEl } = _createController({ species, exhibit: '', message: '' });
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


test('Test_CreateAnimalViewingAlertController_TestMissingMessage_ExpectErrorStatus', async () => {
   const statuses = [];
   const species = 'Lion';
   const exhibit = 'Savanna';
   const originals = _installBaseStubs({ statuses });

   try {
      const { submitButtonEl, speciesEl, exhibitEl } = _createController({
         species,
         exhibit,
         message: '',
      });
      ControllerHelper.getFieldValue = (el) => {
         if (el === speciesEl) return species;
         if (el === exhibitEl) return exhibit;
         return '';
      };

      await submitButtonEl.listeners.click();

      assert.ok(
         statuses.some((entry) => (
            entry[Position.SECOND] === Strings.validation.entityRequired(Strings.labels.alertMessage)
         ))
      );
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalViewingAlertController_TestInvalidDateRange_ExpectErrorStatus', async () => {
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


test('Test_CreateAnimalViewingAlertController_TestMutationFailure_ExpectErrorStatus', async () => {
   const statuses = [];
   const mutationFailed = 'mutation failed';
   const originals = _installBaseStubs({ statuses });
   ApiErrorMessageResolver.resolveConsoleMutationError = () => mutationFailed;
   ConsoleOperationsClient.setAnimalViewingAlert = async () => ({ success: false });

   try {
      const { submitButtonEl } = _createController();

      await submitButtonEl.listeners.click();

      assert.ok(statuses.some((entry) => entry[Position.SECOND] === mutationFailed));
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalViewingAlertController_TestNetworkError_ExpectRequestFailed', async () => {
   const statuses = [];
   const originals = _installBaseStubs({ statuses });
   ConsoleOperationsClient.setAnimalViewingAlert = async () => {
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


test('Test_CreateAnimalViewingAlertController_TestHideAndCancel_ExpectPanelHidden', () => {
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
