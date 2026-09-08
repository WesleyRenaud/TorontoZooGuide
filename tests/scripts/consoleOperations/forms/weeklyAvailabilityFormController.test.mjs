import assert from 'node:assert/strict';
import test from 'node:test';

import { WeeklyAvailabilityFormController } from '../../../../scripts/consoleOperations/forms/weeklyAvailabilityFormController.js';
import { OpeningScheduleChecker } from '../../../../scripts/consoleOperations/forms/openingScheduleChecker.js';
import { ConsoleStatusPresenter } from '../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { ControllerHelper } from '../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ApiErrorMessageResolver } from '../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _createDayEls() {
   return {
      mondayEl: document.createElement('input'),
      tuesdayEl: document.createElement('input'),
      wednesdayEl: document.createElement('input'),
      thursdayEl: document.createElement('input'),
      fridayEl: document.createElement('input'),
      saturdayEl: document.createElement('input'),
      sundayEl: document.createElement('input'),
      holidaysOnlyEl: document.createElement('input'),
   };
}

test('Test_CreateWeeklyAvailabilityFormController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const originalLoad = ControllerHelper.loadOptionsAndShowPanel;
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalHasChecked = ControllerHelper.hasCheckedField;
   const originalValidate = ControllerHelper.validateOptionalDateRange;

   ControllerHelper.loadOptionsAndShowPanel = async (options) => {
      activations.push(options.panelEl);
      assert.equal(options.errorMessage, Strings.loadErrors.entityOptions('restaurants'));
      options.resetForm?.();
   };
   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.hasCheckedField = () => true;
   ControllerHelper.validateOptionalDateRange = () => null;

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const entityEl = document.createElement('select');
      const presetEl = document.createElement('select');
      const dayEls = _createDayEls();
      entityEl.value = 'Peaks Cafe';
      presetEl.value = 'everyDay';

      const controller = WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: { id: 'weekly' },
         statusEl: {},
         entityEl,
         presetEl,
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         messageEl: document.createElement('input'),
         ...dayEls,
         activatePanel: () => {},
         loadOptions: async () => [],
         populateOptions: () => {},
         submitSchedule: async (payload) => {
            assert.equal(payload.restaurant, 'Peaks Cafe');
            assert.equal(payload.monday, true);
            assert.equal(payload.holidaysOnly, true);
            return { success: true, restaurant: 'Peaks Cafe' };
         },
         entityLabel: Strings.entityLabels.restaurant,
         optionsLabel: 'restaurants',
         payloadKey: 'restaurant',
      });

      await showButtonEl.listeners.click();
      assert.deepEqual(activations, [{ id: 'weekly' }]);
      assert.equal(dayEls.mondayEl.checked, true);
      assert.equal(dayEls.mondayEl.disabled, true);
      assert.equal(dayEls.holidaysOnlyEl.checked, true);

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.status.openingScheduleSaved('Peaks Cafe')
            && entry[2] === 'is-success'
         ))
      );

      controller.show();
   } finally {
      ControllerHelper.loadOptionsAndShowPanel = originalLoad;
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.hasCheckedField = originalHasChecked;
      ControllerHelper.validateOptionalDateRange = originalValidate;
   }
});

test('Test_CreateWeeklyAvailabilityFormController_TestPresets_ExpectDayState', () => {
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalReset = ControllerHelper.resetFormFields;
   ConsoleStatusPresenter.setStatus = () => {};
   ControllerHelper.resetFormFields = () => {};

   try {
      const presetEl = document.createElement('select');
      const dayEls = _createDayEls();

      WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController({
         showButtonEl: document.createElement('button'),
         submitButtonEl: document.createElement('button'),
         panelEl: {},
         statusEl: {},
         entityEl: document.createElement('select'),
         presetEl,
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         messageEl: document.createElement('input'),
         ...dayEls,
         loadOptions: async () => [],
         populateOptions: () => {},
         submitSchedule: async () => ({ success: true }),
      });

      presetEl.value = 'weekendsOnly';
      presetEl.listeners.change();
      assert.equal(dayEls.saturdayEl.checked, true);
      assert.equal(dayEls.sundayEl.checked, true);
      assert.equal(dayEls.mondayEl.disabled, true);
      assert.equal(dayEls.holidaysOnlyEl.checked, false);
      assert.equal(dayEls.holidaysOnlyEl.disabled, true);

      presetEl.value = 'weekendsAndHolidays';
      presetEl.listeners.change();
      assert.equal(dayEls.saturdayEl.checked, true);
      assert.equal(dayEls.sundayEl.checked, true);
      assert.equal(dayEls.holidaysOnlyEl.checked, true);
      assert.equal(dayEls.holidaysOnlyEl.disabled, true);

      presetEl.value = 'custom';
      presetEl.listeners.change();
      assert.equal(dayEls.mondayEl.disabled, false);
      assert.equal(dayEls.holidaysOnlyEl.disabled, false);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.resetFormFields = originalReset;
   }
});

test('Test_CreateWeeklyAvailabilityFormController_TestValidationOverlapAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalHasChecked = ControllerHelper.hasCheckedField;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalOverlap = OpeningScheduleChecker.resultHasOpeningScheduleOverlap;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.hideConsolePanel = (args) => {
      hides.push(args);
   };
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'mutation failed';

   try {
      const submitButtonEl = document.createElement('button');
      const cancelButtonEl = document.createElement('button');
      const entityEl = document.createElement('select');
      const dayEls = _createDayEls();
      let submitImpl = async () => ({ success: false });
      let resolveOverlapConflict = null;

      const controller = WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         cancelButtonEl,
         panelEl: {},
         statusEl: {},
         entityEl,
         presetEl: document.createElement('select'),
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         messageEl: document.createElement('input'),
         ...dayEls,
         activatePanel: () => {},
         loadOptions: async () => [],
         populateOptions: () => {},
         submitSchedule: async (payload) => submitImpl(payload),
         resolveOverlapConflict: async (payload) => resolveOverlapConflict?.(payload),
         entityLabel: 'Restaurant',
         payloadKey: 'restaurant',
      });

      ControllerHelper.getFieldValue = () => '';
      ControllerHelper.hasCheckedField = () => true;
      ControllerHelper.validateOptionalDateRange = () => null;
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired('Restaurant')
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = () => 'Peaks';
      ControllerHelper.hasCheckedField = () => false;
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => entry[1] === Strings.validation.weeklyAvailability)
      );

      statuses.length = 0;
      ControllerHelper.hasCheckedField = () => true;
      ControllerHelper.validateOptionalDateRange = () => 'bad range';
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'bad range'));

      statuses.length = 0;
      ControllerHelper.validateOptionalDateRange = () => null;
      OpeningScheduleChecker.resultHasOpeningScheduleOverlap = () => false;
      submitImpl = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      OpeningScheduleChecker.resultHasOpeningScheduleOverlap = () => true;
      resolveOverlapConflict = async () => null;
      await submitButtonEl.listeners.click();
      assert.equal(statuses.filter((entry) => entry[1] !== '').length, 0);

      statuses.length = 0;
      resolveOverlapConflict = async () => ({ success: true, restaurant: 'Peaks' });
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.status.openingScheduleSaved('Peaks')
            && entry[2] === 'is-success'
         ))
      );

      statuses.length = 0;
      resolveOverlapConflict = async () => ({ success: false, error: 'overlap unresolved' });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'overlap unresolved'));

      statuses.length = 0;
      OpeningScheduleChecker.resultHasOpeningScheduleOverlap = () => false;
      submitImpl = async () => {
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
      ControllerHelper.hasCheckedField = originalHasChecked;
      ControllerHelper.validateOptionalDateRange = originalValidate;
      ControllerHelper.hideConsolePanel = originalHide;
      OpeningScheduleChecker.resultHasOpeningScheduleOverlap = originalOverlap;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
