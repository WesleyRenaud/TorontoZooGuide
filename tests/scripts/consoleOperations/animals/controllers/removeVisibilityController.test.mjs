import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { AnimalExhibitAutofillController } from '../../../../../scripts/consoleOperations/animals/controllers/animalExhibitAutofillController.js';
import { RemoveVisibilityController } from '../../../../../scripts/consoleOperations/animals/controllers/removeVisibilityController.js';
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
   AnimalExhibitAutofillController.createAnimalExhibitAutofillController = originals.autofill;
   ConsoleOperationsClient.removeAnimalVisibilitySchedule = originals.remove;
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
      hide: ControllerHelper.hideConsolePanel,
      status: ConsoleStatusPresenter.setStatus,
      autofill: AnimalExhibitAutofillController.createAnimalExhibitAutofillController,
      remove: ConsoleOperationsClient.removeAnimalVisibilitySchedule,
      resolve: ApiErrorMessageResolver.resolveConsoleMutationError,
   };

   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      activations.push(options.panelEl);
      assert.equal(options.loadOptions, ConsoleOptionsLoader.loadVisibilityScheduleExhibits);
      assert.equal(options.populateOptions, ConsoleDropdownPopulator.populateExhibitDropdown);
   };
   ControllerHelper.reloadOptions = async () => {};
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.bindResetValueOnChange = () => {};
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
   panelEl = { id: 'remove-visibility' },
   species = 'Lion',
   exhibit = 'Savanna',
} = {}) {
   const submitButtonEl = document.createElement('button');
   const cancelButtonEl = document.createElement('button');
   const speciesEl = document.createElement('input');
   const exhibitEl = document.createElement('select');
   speciesEl.value = species;
   exhibitEl.value = exhibit;

   const controller = RemoveVisibilityController.createRemoveVisibilityScheduleController({
      showButtonEl: document.createElement('button'),
      submitButtonEl,
      cancelButtonEl,
      panelEl,
      statusEl: {},
      speciesEl,
      exhibitEl,
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


test('Test_CreateRemoveVisibilityScheduleController_TestShow_ExpectPanelActivated', async () => {
   const activations = [];
   const autofillArgs = [];
   const originals = _installBaseStubs({ activations, autofillArgs });
   const panelEl = { id: 'remove-visibility' };

   try {
      const { controller } = _createController({ panelEl });

      await controller.show();

      assert.deepEqual(activations, [panelEl]);
      assert.equal(
         autofillArgs[Position.FIRST].loadExhibits,
         ConsoleOptionsLoader.loadVisibilityScheduleExhibits
      );
      assert.equal(
         autofillArgs[Position.FIRST].loadExhibitsForSpecies,
         ConsoleOptionsLoader.loadVisibilityScheduleExhibits
      );
   } finally {
      _restore(originals);
   }
});


test('Test_CreateRemoveVisibilityScheduleController_TestSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const species = 'Lion';
   const exhibit = 'Savanna';
   const originals = _installBaseStubs({ statuses });

   ConsoleOperationsClient.removeAnimalVisibilitySchedule = async (payload) => {
      assert.deepEqual(payload, { species, exhibit });
      return { success: true, species, exhibit };
   };

   try {
      const { submitButtonEl } = _createController({ species, exhibit });

      await submitButtonEl.listeners.click();

      assert.ok(
         statuses.some((entry) => (
            entry[Position.SECOND] === Strings.status.animalVisibilityScheduleRemoved({ species, exhibit })
            && entry[Position.THIRD] === 'is-success'
         ))
      );
   } finally {
      _restore(originals);
   }
});


test('Test_CreateRemoveVisibilityScheduleController_TestMissingSpecies_ExpectErrorStatus', async () => {
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


test('Test_CreateRemoveVisibilityScheduleController_TestMissingExhibit_ExpectErrorStatus', async () => {
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


test('Test_CreateRemoveVisibilityScheduleController_TestMutationFailure_ExpectErrorStatus', async () => {
   const statuses = [];
   const mutationFailed = 'mutation failed';
   const originals = _installBaseStubs({ statuses });
   ApiErrorMessageResolver.resolveConsoleMutationError = () => mutationFailed;
   ConsoleOperationsClient.removeAnimalVisibilitySchedule = async () => ({ success: false });

   try {
      const { submitButtonEl } = _createController();

      await submitButtonEl.listeners.click();

      assert.ok(statuses.some((entry) => entry[Position.SECOND] === mutationFailed));
   } finally {
      _restore(originals);
   }
});


test('Test_CreateRemoveVisibilityScheduleController_TestNetworkError_ExpectRequestFailed', async () => {
   const statuses = [];
   const originals = _installBaseStubs({ statuses });
   ConsoleOperationsClient.removeAnimalVisibilitySchedule = async () => {
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


test('Test_CreateRemoveVisibilityScheduleController_TestHideAndCancel_ExpectPanelHidden', () => {
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
