import assert from 'node:assert/strict';
import test from 'node:test';

import { AddGuardiansTalkController } from '../../../../../scripts/consoleOperations/guardiansTalks/controllers/addGuardiansTalkController.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateAddGuardiansTalkOccurrenceController_TestShowAndSubmitSuccess_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];
   const filterCalls = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalAdd = ConsoleOperationsClient.addGuardiansTalkOccurrence;

   ConsoleStatusPresenter.setStatus = (...args) => {
      statuses.push(args);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = () => {};
   ConsoleOperationsClient.addGuardiansTalkOccurrence = async (payload) => {
      assert.deepEqual(payload, {
         talk: 'Keeper Talk',
         location: 'Africa',
         date: '2026-07-01',
         times: ['11:00 AM'],
      });
      return {
         success: true,
         talk: 'Keeper Talk',
         location: 'Africa',
         date: '2026-07-01',
         times: ['11:00 AM'],
      };
   };

   try {
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const talkNameEl = document.createElement('select');
      const locationEl = document.createElement('select');
      const dateEl = document.createElement('input');
      const timeEl = document.createElement('input');
      talkNameEl.value = 'Keeper Talk';
      locationEl.value = 'Africa';
      dateEl.value = '2026-07-01';
      timeEl.value = '11:00 AM';

      const talkLocationFilterController = {
         clear: () => {
            filterCalls.push('clear');
         },
         refreshLocations: async () => {
            filterCalls.push('refresh');
         },
      };

      const controller = AddGuardiansTalkController.createAddGuardiansTalkOccurrenceController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl: document.createElement('button'),
         panelEl: { id: 'add-talk' },
         statusEl: {},
         talkNameEl,
         locationEl,
         dateEl,
         timeEl,
         activatePanel: (panel) => {
            activations.push(panel);
         },
         talkLocationFilterController,
      });

      await showButtonEl.listeners.click();
      assert.deepEqual(activations, [{ id: 'add-talk' }]);
      assert.ok(filterCalls.includes('refresh'));
      assert.ok(filterCalls.includes('clear'));

      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === 'Keeper Talk in Africa on 2026-07-01 at 11:00 AM was added.'
            && entry[2] === 'is-success'
         ))
      );

      controller.show();
   } finally {
      ConsoleStatusPresenter.setStatus = originalStatus;
      ControllerHelper.getFieldValue = originalGet;
      ControllerHelper.resetFormFields = originalReset;
      ConsoleOperationsClient.addGuardiansTalkOccurrence = originalAdd;
   }
});

test('Test_CreateAddGuardiansTalkOccurrenceController_TestValidationAndFailures_ExpectErrorStatus', async () => {
   const statuses = [];
   const hides = [];
   const originalStatus = ConsoleStatusPresenter.setStatus;
   const originalGet = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalHide = ControllerHelper.hideConsolePanel;
   const originalAdd = ConsoleOperationsClient.addGuardiansTalkOccurrence;
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
      const showButtonEl = document.createElement('button');
      const submitButtonEl = document.createElement('button');
      const cancelButtonEl = document.createElement('button');
      const talkNameEl = document.createElement('select');
      const locationEl = document.createElement('select');
      const dateEl = document.createElement('input');
      const timeEl = document.createElement('input');

      const controller = AddGuardiansTalkController.createAddGuardiansTalkOccurrenceController({
         showButtonEl,
         submitButtonEl,
         cancelButtonEl,
         panelEl: {},
         statusEl: {},
         talkNameEl,
         locationEl,
         dateEl,
         timeEl,
         activatePanel: () => {},
         talkLocationFilterController: {
            refreshLocations: async () => {
               throw new Error('load failed');
            },
            clear: () => {},
         },
      });

      await showButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.loadErrors.locations && entry[2] === 'is-error'
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = () => '';
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.location)
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = (el) => {
         if (el === locationEl) return 'Africa';
         return '';
      };
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.talkName)
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = (el) => {
         if (el === locationEl) return 'Africa';
         if (el === talkNameEl) return 'Talk';
         return '';
      };
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.date)
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = (el) => {
         if (el === locationEl) return 'Africa';
         if (el === talkNameEl) return 'Talk';
         if (el === dateEl) return '2026-07-01';
         return '';
      };
      await submitButtonEl.listeners.click();
      assert.ok(
         statuses.some((entry) => (
            entry[1] === Strings.validation.entityRequired(Strings.labels.talkTime)
         ))
      );

      statuses.length = 0;
      ControllerHelper.getFieldValue = (el) => {
         if (el === locationEl) return 'Africa';
         if (el === talkNameEl) return 'Talk';
         if (el === dateEl) return '2026-07-01';
         if (el === timeEl) return '11:00 AM';
         return '';
      };
      ConsoleOperationsClient.addGuardiansTalkOccurrence = async () => ({ success: false });
      await submitButtonEl.listeners.click();
      assert.ok(statuses.some((entry) => entry[1] === 'mutation failed'));

      statuses.length = 0;
      ConsoleOperationsClient.addGuardiansTalkOccurrence = async () => {
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
      ControllerHelper.hideConsolePanel = originalHide;
      ConsoleOperationsClient.addGuardiansTalkOccurrence = originalAdd;
      ApiErrorMessageResolver.resolveConsoleMutationError = originalResolve;
   }
});
