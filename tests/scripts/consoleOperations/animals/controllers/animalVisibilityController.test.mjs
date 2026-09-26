import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { AnimalExhibitAutofillController } from '../../../../../scripts/consoleOperations/animals/controllers/animalExhibitAutofillController.js';
import { AnimalVisibilityController } from '../../../../../scripts/consoleOperations/animals/controllers/animalVisibilityController.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../../scripts/strings.js';

const SPECIES = 'Lion';
const EXHIBIT = 'Savanna';
const START_DATE = '2026-01-01';
const END_DATE = '2026-01-02';
const DAILY_START_TIME = '10:00 AM';
const DAILY_END_TIME = '4:00 PM';
const MESSAGE = 'note';

function _createField(value = '') {
   return {
      value,
      addEventListener() {},
   };
}

function _createButton() {
   const listeners = {};
   return {
      listeners,
      addEventListener(eventName, handler) {
         listeners[eventName] = handler;
      },
   };
}

function _createController(overrides = {}) {
   const showButtonEl = _createButton();
   const cancelButtonEl = _createButton();
   const submitButtonEl = _createButton();
   const statusEl = { id: 'status' };
   const speciesEl = _createField(overrides.species ?? SPECIES);
   const exhibitEl = _createField(overrides.exhibit ?? EXHIBIT);
   const startDateEl = _createField(overrides.startDate ?? START_DATE);
   const endDateEl = _createField(overrides.endDate ?? END_DATE);
   const dailyStartTimeEl = _createField(overrides.dailyStartTime ?? DAILY_START_TIME);
   const dailyEndTimeEl = _createField(overrides.dailyEndTime ?? DAILY_END_TIME);
   const messageEl = _createField(overrides.message ?? MESSAGE);
   const activateCalls = [];

   const controller = AnimalVisibilityController.createAnimalVisibilityScheduleController({
      showButtonEl,
      panelEl: { id: 'panel' },
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      speciesEl,
      exhibitEl,
      startDateEl,
      endDateEl,
      dailyStartTimeEl,
      dailyEndTimeEl,
      messageEl,
      activatePanel: (panel) => activateCalls.push(panel),
   });

   return {
      controller,
      showButtonEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      speciesEl,
      exhibitEl,
      dailyStartTimeEl,
      dailyEndTimeEl,
      activateCalls,
   };
}

function _restore(originals) {
   ControllerHelper.getFieldValue = originals.get;
   ControllerHelper.validateOptionalDateRange = originals.validate;
   ControllerHelper.resetFormFields = originals.reset;
   ControllerHelper.hideConsolePanel = originals.hide;
   ControllerHelper.loadOptionsAndShowPanel = originals.load;
   ControllerHelper.reloadOptions = originals.reload;
   ControllerHelper.bindResetValueOnChange = originals.bind;
   ConsoleStatusPresenter.setStatus = originals.status;
   ConsoleOperationsClient.setAnimalVisibilitySchedule = originals.client;
   ApiErrorMessageResolver.resolveConsoleMutationError = originals.resolve;
   AnimalExhibitAutofillController.createAnimalExhibitAutofillController = originals.autofill;
}

function _installBaseStubs({
   statusCalls = [],
   resets = [],
   hides = [],
   payloads = [],
} = {}) {
   const originals = {
      get: ControllerHelper.getFieldValue,
      validate: ControllerHelper.validateOptionalDateRange,
      reset: ControllerHelper.resetFormFields,
      hide: ControllerHelper.hideConsolePanel,
      load: ControllerHelper.loadOptionsAndShowPanel,
      reload: ControllerHelper.reloadOptions,
      bind: ControllerHelper.bindResetValueOnChange,
      status: ConsoleStatusPresenter.setStatus,
      client: ConsoleOperationsClient.setAnimalVisibilitySchedule,
      resolve: ApiErrorMessageResolver.resolveConsoleMutationError,
      autofill: AnimalExhibitAutofillController.createAnimalExhibitAutofillController,
   };

   ControllerHelper.getFieldValue = (el) => el.value;
   ControllerHelper.validateOptionalDateRange = () => '';
   ControllerHelper.resetFormFields = () => {
      resets.push(true);
   };
   ControllerHelper.hideConsolePanel = () => {
      hides.push(true);
   };
   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      options.resetForm();
      options.activatePanel?.(options.panelEl);
   };
   ControllerHelper.reloadOptions = async (options) => {
      options.resetForm?.();
   };
   ControllerHelper.bindResetValueOnChange = () => {};
   ConsoleStatusPresenter.setStatus = (_el, message, tone) => {
      statusCalls.push({ message, tone });
   };
   ConsoleOperationsClient.setAnimalVisibilitySchedule = async (payload) => {
      payloads.push(payload);
      return {
         success: true,
         species: payload.species,
         exhibit: payload.exhibit,
      };
   };
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'resolved-error';

   return originals;
}


test('Test_CreateAnimalVisibilityScheduleController_TestMissingSpecies_ExpectErrorStatus', async () => {
   const statusCalls = [];
   const originals = _installBaseStubs({ statusCalls });

   try {
      const missingSpecies = _createController({ species: '' });

      await missingSpecies.submitButtonEl.listeners.click();

      assert.equal(statusCalls.at(Position.LAST).tone, 'is-error');
      assert.equal(
         statusCalls.at(Position.LAST).message,
         Strings.validation.entityRequired(Strings.labels.species)
      );
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalVisibilityScheduleController_TestMissingExhibit_ExpectErrorStatus', async () => {
   const statusCalls = [];
   const originals = _installBaseStubs({ statusCalls });

   try {
      const missingExhibit = _createController({ exhibit: '' });

      await missingExhibit.submitButtonEl.listeners.click();

      assert.equal(
         statusCalls.at(Position.LAST).message,
         Strings.validation.entityRequired(Strings.entityLabels.exhibit)
      );
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalVisibilityScheduleController_TestMissingTimes_ExpectErrorStatus', async () => {
   const statusCalls = [];
   const originals = _installBaseStubs({ statusCalls });

   try {
      const missingTimes = _createController({ dailyStartTime: '', dailyEndTime: '' });

      await missingTimes.submitButtonEl.listeners.click();

      assert.equal(statusCalls.at(Position.LAST).message, Strings.validation.dailyViewingTimes);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalVisibilityScheduleController_TestShow_ExpectPanelActivated', async () => {
   const resets = [];
   const originals = _installBaseStubs({ resets });

   try {
      const ok = _createController();

      await ok.showButtonEl.listeners.click();

      assert.equal(ok.activateCalls[Position.FIRST].id, 'panel');
      assert.ok(resets.length >= 1);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalVisibilityScheduleController_TestSubmitSuccess_ExpectStatus', async () => {
   const statusCalls = [];
   const payloads = [];
   const originals = _installBaseStubs({ statusCalls, payloads });

   try {
      const ok = _createController();

      await ok.submitButtonEl.listeners.click();

      assert.deepEqual(payloads.at(Position.LAST), {
         species: SPECIES,
         exhibit: EXHIBIT,
         startDate: START_DATE,
         endDate: END_DATE,
         dailyStartTime: DAILY_START_TIME,
         dailyEndTime: DAILY_END_TIME,
         message: MESSAGE,
      });
      assert.equal(statusCalls.at(Position.LAST).tone, 'is-success');
      assert.equal(
         statusCalls.at(Position.LAST).message,
         Strings.status.animalVisibilityScheduleSaved({ species: SPECIES, exhibit: EXHIBIT })
      );
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalVisibilityScheduleController_TestMutationFailure_ExpectErrorStatus', async () => {
   const statusCalls = [];
   const resolvedError = 'resolved-error';
   const originals = _installBaseStubs({ statusCalls });
   ConsoleOperationsClient.setAnimalVisibilitySchedule = async () => ({ success: false });

   try {
      const ok = _createController();

      await ok.submitButtonEl.listeners.click();

      assert.equal(statusCalls.at(Position.LAST).message, resolvedError);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalVisibilityScheduleController_TestNetworkError_ExpectRequestFailed', async () => {
   const statusCalls = [];
   const originals = _installBaseStubs({ statusCalls });
   ConsoleOperationsClient.setAnimalVisibilitySchedule = async () => {
      throw new Error('network');
   };

   try {
      const ok = _createController();

      await ok.submitButtonEl.listeners.click();

      assert.equal(statusCalls.at(Position.LAST).message, Strings.common.requestFailed);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalVisibilityScheduleController_TestHideAndCancel_ExpectPanelHidden', () => {
   const hides = [];
   const originals = _installBaseStubs({ hides });

   try {
      const ok = _createController();

      ok.cancelButtonEl.listeners.click();
      ok.controller.hide();

      assert.ok(hides.length >= 1);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalVisibilityScheduleController_TestShow_ExpectExhibitLoaders', async () => {
   const originalLoad = ControllerHelper.loadOptionsAndShowPanel;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalAutofill = AnimalExhibitAutofillController.createAnimalExhibitAutofillController;
   const autofillArgs = [];
   let captured;

   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      captured = options;
   };
   ControllerHelper.bindResetValueOnChange = () => {};
   AnimalExhibitAutofillController.createAnimalExhibitAutofillController = (args) => {
      autofillArgs.push(args);
      return originalAutofill(args);
   };

   try {
      const { showButtonEl } = _createController();

      await showButtonEl.listeners.click();

      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadExhibits);
      assert.equal(captured.populateOptions, ConsoleDropdownPopulator.populateExhibitDropdown);
      assert.equal(captured.setStatus, ConsoleStatusPresenter.setStatus);
      assert.equal(captured.errorMessage, Strings.loadErrors.exhibits);
      assert.equal(autofillArgs.length, 1);
      assert.equal(autofillArgs[Position.FIRST].loadExhibits, ConsoleOptionsLoader.loadExhibits);
      assert.equal(autofillArgs[Position.FIRST].loadExhibitsForSpecies, ConsoleOptionsLoader.loadExhibitsForSpecies);
   } finally {
      ControllerHelper.loadOptionsAndShowPanel = originalLoad;
      ControllerHelper.bindResetValueOnChange = originalBind;
      AnimalExhibitAutofillController.createAnimalExhibitAutofillController = originalAutofill;
   }
});


test('Test_CreateAnimalVisibilityScheduleController_TestReloadOptionsThrows_ExpectClearsFields', async () => {
   const resets = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalReload = ControllerHelper.reloadOptions;
   const originalReset = ControllerHelper.resetFormFields;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalClient = ConsoleOperationsClient.setAnimalVisibilitySchedule;

   ConsoleStatusPresenter.setStatus = () => {};
   ControllerHelper.reloadOptions = async () => {
      throw new Error('reload failed');
   };
   ControllerHelper.resetFormFields = () => {
      resets.push(true);
   };
   ControllerHelper.bindResetValueOnChange = () => {};
   ConsoleOperationsClient.setAnimalVisibilitySchedule = async () => ({
      success: true,
      species: SPECIES,
      exhibit: EXHIBIT,
   });

   try {
      const { submitButtonEl } = _createController();

      await submitButtonEl.listeners.click();

      assert.ok(resets.length >= 1);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.reloadOptions = originalReload;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.bindResetValueOnChange = originalBind;
      ConsoleOperationsClient.setAnimalVisibilitySchedule = originalClient;
   }
});
