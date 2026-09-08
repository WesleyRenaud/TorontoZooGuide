import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { AnimalVisibilityController } from '../../../../../scripts/consoleOperations/animals/controllers/animalVisibilityController.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { Strings } from '../../../../../scripts/strings.js';

function _createField(value = '') {
   return { value };
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
   const speciesEl = _createField(overrides.species ?? 'Lion');
   const exhibitEl = _createField(overrides.exhibit ?? 'Savanna');
   const startDateEl = _createField(overrides.startDate ?? '2026-01-01');
   const endDateEl = _createField(overrides.endDate ?? '2026-01-02');
   const dailyStartTimeEl = _createField(overrides.dailyStartTime ?? '10:00 AM');
   const dailyEndTimeEl = _createField(overrides.dailyEndTime ?? '4:00 PM');
   const messageEl = _createField(overrides.message ?? 'note');
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

test('Test_CreateAnimalVisibilityScheduleController_TestValidationAndSubmit_ExpectStatusFlows', async () => {
   const statusCalls = [];
   const resets = [];
   const hides = [];
   const payloads = [];
   const originalGet = ControllerHelper.getFieldValue;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalReset = ControllerHelper.resetFormFields;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalLoad = ControllerHelper.loadOptionsAndShowPanel;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   const originalSetStatus = ConsoleStatusPresenter.setStatus;
   const originalClient = ConsoleOperationsClient.setAnimalVisibilitySchedule;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;

   ControllerHelper.getFieldValue = (el) => el.value;
   ControllerHelper.validateOptionalDateRange = () => '';
   ControllerHelper.resetFormFields = () => { resets.push(true); };
   ControllerHelper.hideConsolePanel = () => { hides.push(true); };
   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      options.resetForm();
      options.activatePanel?.(options.panelEl);
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

   try {
      const missingSpecies = _createController({ species: '' });
      await missingSpecies.submitButtonEl.listeners.click();
      assert.equal(statusCalls.at(-1).tone, 'is-error');
      assert.equal(
         statusCalls.at(-1).message,
         Strings.validation.entityRequired(Strings.labels.species)
      );

      const missingExhibit = _createController({ exhibit: '' });
      await missingExhibit.submitButtonEl.listeners.click();
      assert.equal(
         statusCalls.at(-1).message,
         Strings.validation.entityRequired(Strings.entityLabels.exhibit)
      );

      const missingTimes = _createController({ dailyStartTime: '', dailyEndTime: '' });
      await missingTimes.submitButtonEl.listeners.click();
      assert.equal(statusCalls.at(-1).message, Strings.validation.dailyViewingTimes);

      const ok = _createController();
      await ok.showButtonEl.listeners.click();
      assert.equal(ok.activateCalls[0].id, 'panel');
      assert.ok(resets.length >= 1);

      await ok.submitButtonEl.listeners.click();
      assert.deepEqual(payloads.at(-1), {
         species: 'Lion',
         exhibit: 'Savanna',
         startDate: '2026-01-01',
         endDate: '2026-01-02',
         dailyStartTime: '10:00 AM',
         dailyEndTime: '4:00 PM',
         message: 'note',
      });
      assert.equal(statusCalls.at(-1).tone, 'is-success');
      assert.match(statusCalls.at(-1).message, /Lion in Savanna/);

      ConsoleOperationsClient.setAnimalVisibilitySchedule = async () => ({ success: false });
      await ok.submitButtonEl.listeners.click();
      assert.equal(statusCalls.at(-1).message, 'resolved-error');

      ConsoleOperationsClient.setAnimalVisibilitySchedule = async () => {
         throw new Error('network');
      };
      await ok.submitButtonEl.listeners.click();
      assert.equal(statusCalls.at(-1).message, Strings.common.requestFailed);

      ok.cancelButtonEl.listeners.click();
      assert.ok(hides.length >= 1);
      ok.controller.hide();
   } finally {
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.validateOptionalDateRange = originalValidate;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.hideConsolePanel = originalHide;
      ControllerHelper.loadOptionsAndShowPanel = originalLoad;
      ControllerHelper.bindResetValueOnChange = originalBind;
      ConsoleStatusPresenter.setStatus = originalSetStatus;
      ConsoleOperationsClient.setAnimalVisibilitySchedule = originalClient;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});

test('Test_CreateAnimalVisibilityScheduleController_TestShow_ExpectExhibitLoaders', async () => {
   const originalLoad = ControllerHelper.loadOptionsAndShowPanel;
   const originalBind = ControllerHelper.bindResetValueOnChange;
   let captured;

   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      captured = options;
   };
   ControllerHelper.bindResetValueOnChange = () => {};

   try {
      const { showButtonEl } = _createController();
      await showButtonEl.listeners.click();
      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadExhibits);
      assert.equal(captured.populateOptions, ConsoleDropdownPopulator.populateExhibitDropdown);
      assert.equal(captured.setStatus, ConsoleStatusPresenter.setStatus);
      assert.equal(captured.errorMessage, Strings.loadErrors.exhibits);
   } finally {
      ControllerHelper.loadOptionsAndShowPanel = originalLoad;
      ControllerHelper.bindResetValueOnChange = originalBind;
   }
});
