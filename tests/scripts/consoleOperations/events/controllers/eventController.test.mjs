import assert from 'node:assert/strict';
import test from 'node:test';

import { EventController } from '../../../../../scripts/consoleOperations/events/controllers/eventController.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { VisitDateValidator } from '../../../../../scripts/visitDates/visitDateValidator.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateCreateEventController_TestShowHideAndSubmit_ExpectFlows', async () => {
   const statuses = [];
   const activations = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalReset = ControllerHelper.resetFormFields;
   const originalGet = ControllerHelper.getFieldValue;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalResolveStart = VisitDateValidator.resolveOptionalStartDate;
   const originalCreate = ConsoleOperationsClient.createEvent;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;
   let hideCalls = 0;

   ConsoleStatusPresenter.setStatus = (...args) => { statuses.push(args); };
   ControllerHelper.hideConsolePanel = () => { hideCalls += 1; };
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.validateOptionalDateRange = () => null;
   VisitDateValidator.resolveOptionalStartDate = (value) => value || null;
   ConsoleOperationsClient.createEvent = async () => ({ success: true, name: 'Festival' });
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'mutation failed';

   try {
      const showButtonEl = document.createElement('button');
      const cancelButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const nameEl = document.createElement('input');
      const descriptionEl = document.createElement('input');
      const linkEl = document.createElement('input');
      nameEl.value = 'Festival';
      descriptionEl.value = 'Details';
      linkEl.value = 'https://example.com';

      const controller = EventController.createCreateEventController({
         showButtonEl,
         cancelButtonEl,
         submitButtonEl,
         panelEl: { id: 'create-event' },
         statusEl: {},
         nameEl,
         locationEl: document.createElement('input'),
         descriptionEl,
         linkEl,
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         activatePanel: (panel) => { activations.push(panel); },
      });

      controller.show();
      assert.deepEqual(activations, [{ id: 'create-event' }]);

      controller.hide();
      assert.equal(hideCalls, 1);

      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.status.eventCreated({ name: 'Festival' })));

      statuses.length = 0;
      nameEl.value = '';
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[2] === 'is-error'));

      statuses.length = 0;
      nameEl.value = 'Festival';
      ConsoleOperationsClient.createEvent = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      ConsoleOperationsClient.createEvent = async () => { throw new Error('network'); };
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.common.requestFailed));
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.hideConsolePanel = originalHide;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.validateOptionalDateRange = originalValidate;
      VisitDateValidator.resolveOptionalStartDate = originalResolveStart;
      ConsoleOperationsClient.createEvent = originalCreate;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
