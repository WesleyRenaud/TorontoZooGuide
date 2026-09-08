import assert from 'node:assert/strict';
import test from 'node:test';

import { RecurringScheduleFormController } from '../../../../scripts/consoleOperations/forms/recurringScheduleFormController.js';
import { ConsoleStatusPresenter } from '../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { ControllerHelper } from '../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ApiErrorMessageResolver } from '../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateRecurringScheduleFormController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const resets = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalHasChecked = ControllerHelper.hasCheckedField;
   const originalValidate = ControllerHelper.validateOptionalDateRange;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {
      resets.push(true);
   };
   ControllerHelper.hasCheckedField = () => true;
   ControllerHelper.validateOptionalDateRange = () => null;

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const timeEl = document.createElement('input');
      timeEl.value = '11:00 AM';

      const controller = RecurringScheduleFormController.createRecurringScheduleFormController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: { id: 'recurring' },
         statusEl: {},
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         timeEl,
         dayFieldEls: [document.createElement('input')],
         activatePanel: (panel) => {
            activations.push(panel);
         },
         getSelectionValues: () => ({ entity: 'Giraffe' }),
         validateSelection: () => null,
         prepareForm: async () => {},
         submitSchedule: async (values) => ({ success: true, ...values }),
         successMessage: (result) => Strings.status.scheduleWasSaved,
      });

      await showButtonEl.listeners.click();
      assert.deepEqual(activations, [{ id: 'recurring' }]);
      assert.ok(resets.length >= 1);

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.status.scheduleWasSaved && entry[2] === 'is-success'
         ))
      );

      controller.show();
      assert.equal(activations.length, 2);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.hasCheckedField = originalHasChecked;
      ControllerHelper.validateOptionalDateRange = originalValidate;
   }
});

test('Test_CreateRecurringScheduleFormController_TestScheduleTimesAndCustomValidation_ExpectPaths', async () => {
   const statuses = [];
   const scheduleResets = [];
   const selectionResets = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalHasChecked = ControllerHelper.hasCheckedField;
   const originalValidate = ControllerHelper.validateOptionalDateRange;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = () => '';
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.hasCheckedField = () => false;
   ControllerHelper.validateOptionalDateRange = () => null;

   try {
      const submitButtonEl = document.createElement('button');
      let times = [];

      RecurringScheduleFormController.createRecurringScheduleFormController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         panelEl: {},
         statusEl: {},
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         getScheduleTimes: () => times,
         resetScheduleTimes: () => {
            scheduleResets.push(true);
         },
         resetSelection: () => {
            selectionResets.push(true);
         },
         getSelectionValues: () => ({ entity: 'Ok' }),
         validateSelection: () => null,
         submitSchedule: async () => ({ success: true }),
         successMessage: () => 'saved',
      });

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.time)
         ))
      );

      statuses.length = 0;
      times = ['11:00 AM'];
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.validation.oneDay));

      statuses.length = 0;
      const customSubmitEl = document.createElement('button');
      RecurringScheduleFormController.createRecurringScheduleFormController({
         showButtonEl: document.createElement('button'),
         submitButtonEl: customSubmitEl,
         panelEl: {},
         statusEl: {},
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         timeEl: document.createElement('input'),
         getSelectionValues: () => ({}),
         validateSelection: () => 'selection required',
         submitSchedule: async () => ({ success: true }),
      });
      await customSubmitEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'selection required'));

      statuses.length = 0;
      const recurringSubmitEl = document.createElement('button');
      RecurringScheduleFormController.createRecurringScheduleFormController({
         showButtonEl: document.createElement('button'),
         submitButtonEl: recurringSubmitEl,
         panelEl: {},
         statusEl: {},
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         timeEl: document.createElement('input'),
         getSelectionValues: () => ({}),
         validateSelection: () => null,
         validateRecurringSchedule: () => 'bad recurring',
         submitSchedule: async () => ({ success: true }),
      });
      await recurringSubmitEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'bad recurring'));

      statuses.length = 0;
      ControllerHelper.hasCheckedField = () => true;
      ControllerHelper.validateOptionalDateRange = () => 'bad range';
      const rangeSubmitEl = document.createElement('button');
      const timeEl = document.createElement('input');
      timeEl.value = '11:00 AM';
      ControllerHelper.getFieldValue = (el) => el?.value ?? '';
      RecurringScheduleFormController.createRecurringScheduleFormController({
         showButtonEl: document.createElement('button'),
         submitButtonEl: rangeSubmitEl,
         panelEl: {},
         statusEl: {},
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         timeEl,
         dayFieldEls: [document.createElement('input')],
         getSelectionValues: () => ({}),
         validateSelection: () => null,
         resetScheduleTimes: () => {
            scheduleResets.push(true);
         },
         resetSelection: () => {
            selectionResets.push(true);
         },
         submitSchedule: async () => ({ success: true }),
         successMessage: () => 'saved',
      });
      await rangeSubmitEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'bad range'));

      ControllerHelper.validateOptionalDateRange = () => null;
      statuses.length = 0;
      await rangeSubmitEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'saved' && entry[2] === 'is-success'));
      assert.ok(scheduleResets.length >= 1);
      assert.ok(selectionResets.length >= 1);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.hasCheckedField = originalHasChecked;
      ControllerHelper.validateOptionalDateRange = originalValidate;
   }
});

test('Test_CreateRecurringScheduleFormController_TestLoadAndSubmitFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalHasChecked = ControllerHelper.hasCheckedField;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.hasCheckedField = () => true;
   ControllerHelper.validateOptionalDateRange = () => null;
   ControllerHelper.hideConsolePanel = (args) => {
      hides.push(args);
   };
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'mutation failed';

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const cancelButtonEl = document.createElement('button');
      const timeEl = document.createElement('input');
      timeEl.value = '11:00 AM';

      const controller = RecurringScheduleFormController.createRecurringScheduleFormController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl,
         panelEl: {},
         statusEl: {},
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         timeEl,
         dayFieldEls: [document.createElement('input')],
         activatePanel: () => {},
         getSelectionValues: () => ({ entity: 'Ok' }),
         validateSelection: () => null,
         prepareForm: async () => {
            throw new Error('load failed');
         },
         loadErrorMessage: 'could not load',
         submitSchedule: async () => ({ success: false }),
      });

      await showButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'could not load' && entry[2] === 'is-error'));

      statuses.length = 0;
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      const suppressSubmitEl = document.createElement('button');
      const suppressTimeEl = document.createElement('input');
      suppressTimeEl.value = '11:00 AM';
      RecurringScheduleFormController.createRecurringScheduleFormController({
         showButtonEl: document.createElement('button'),
         submitButtonEl: suppressSubmitEl,
         panelEl: {},
         statusEl: {},
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         timeEl: suppressTimeEl,
         dayFieldEls: [document.createElement('input')],
         getSelectionValues: () => ({}),
         validateSelection: () => null,
         submitSchedule: async () => ({ success: false }),
         shouldReportSubmitFailure: () => false,
      });
      await suppressSubmitEl.listeners.click();
      assert.equal(statuses.length, 1);
      assert.equal(statuses[0][1], '');

      statuses.length = 0;
      const networkSubmitEl = document.createElement('button');
      const networkTimeEl = document.createElement('input');
      networkTimeEl.value = '11:00 AM';
      RecurringScheduleFormController.createRecurringScheduleFormController({
         showButtonEl: document.createElement('button'),
         submitButtonEl: networkSubmitEl,
         panelEl: {},
         statusEl: {},
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         timeEl: networkTimeEl,
         dayFieldEls: [document.createElement('input')],
         getSelectionValues: () => ({}),
         validateSelection: () => null,
         submitSchedule: async () => {
            throw new Error('network');
         },
      });
      await networkSubmitEl.listeners.click();
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
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
