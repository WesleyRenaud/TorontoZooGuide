import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationRouteController } from '../../../../../scripts/consoleOperations/transportation/controllers/transportationRouteController.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateTransportationRouteController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalSet = ConsoleOperationsClient.setCurrentTransportationRoute;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.validateOptionalDateRange = () => null;
   ConsoleOperationsClient.setCurrentTransportationRoute = async (payload) => {
      assert.deepEqual(payload, {
         route: 'summer',
         startDate: '2026-06-01',
         endDate: null,
      });
      return { success: true, route: 'summer' };
   };

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const startDateEl = document.createElement('input');
      const summerRouteEl = document.createElement('input');
      const winterRouteEl = document.createElement('input');
      startDateEl.value = '2026-06-01';
      summerRouteEl.checked = true;
      winterRouteEl.checked = false;

      const controller = TransportationRouteController.createTransportationRouteController({
         showButtonEl,
         submitButtonEl,
         panelEl: { id: 'route-panel' },
         statusEl: {},
         startDateEl,
         endDateEl: document.createElement('input'),
         summerRouteEl,
         winterRouteEl,
         activatePanel: (panel) => {
            activations.push(panel);
         },
      });

      controller.show();
      assert.deepEqual(activations, [{ id: 'route-panel' }]);
      assert.equal(summerRouteEl.checked, true);

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.status.transportationRouteSet({ route: 'summer' })
            && entry[2] === 'is-success'
         ))
      );
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.validateOptionalDateRange = originalValidate;
      ConsoleOperationsClient.setCurrentTransportationRoute = originalSet;
   }
});

test('Test_CreateTransportationRouteController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalValidate = ControllerHelper.validateOptionalDateRange;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalSet = ConsoleOperationsClient.setCurrentTransportationRoute;
   const originalResolve = ApiErrorMessageResolver.resolveConsoleMutationError;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = () => '';
   ControllerHelper.resetFormFields = () => {};
   ControllerHelper.hideConsolePanel = (args) => {
      hides.push(args);
   };
   ApiErrorMessageResolver.resolveConsoleMutationError = () => 'mutation failed';

   try {
      const submitButtonEl = document.createElement('button');
      const summerRouteEl = document.createElement('input');
      const winterRouteEl = document.createElement('input');
      summerRouteEl.checked = false;
      winterRouteEl.checked = false;

      const controller = TransportationRouteController.createTransportationRouteController({
         showButtonEl: document.createElement('button'),
         submitButtonEl,
         panelEl: {},
         statusEl: {},
         startDateEl: document.createElement('input'),
         endDateEl: document.createElement('input'),
         summerRouteEl,
         winterRouteEl,
         activatePanel: () => {},
      });

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.route)
            && entry[2] === 'is-error'
         ))
      );

      statuses.length = 0;
      winterRouteEl.checked = true;
      ControllerHelper.validateOptionalDateRange = () => 'bad range';
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'bad range'));

      statuses.length = 0;
      ControllerHelper.validateOptionalDateRange = () => null;
      ConsoleOperationsClient.setCurrentTransportationRoute = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      ConsoleOperationsClient.setCurrentTransportationRoute = async () => {
         throw new Error('network');
      };
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === Strings.common.requestFailed));

      controller.hide();
      assert.equal(hides.length, 1);
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ControllerHelper.validateOptionalDateRange = originalValidate;
      ControllerHelper.hideConsolePanel = originalHide;
      ConsoleOperationsClient.setCurrentTransportationRoute = originalSet;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
