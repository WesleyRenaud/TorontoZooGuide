import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkController } from '../../../../../scripts/consoleOperations/guardiansTalks/controllers/guardiansTalkController.js';
import { RecurringScheduleFormController } from '../../../../../scripts/consoleOperations/forms/recurringScheduleFormController.js';
import { WildEncounterScheduleRowsController } from '../../../../../scripts/consoleOperations/forms/wildEncounterScheduleRowsController.js';
import { OpeningScheduleOverlapFragment } from '../../../../../scripts/consoleOperations/forms/openingScheduleOverlapFragment.js';
import { OpeningScheduleChecker } from '../../../../../scripts/consoleOperations/forms/openingScheduleChecker.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateGuardiansTalkScheduleController_TestWiring_ExpectFormCallbacks', async () => {
   const originalCreate = RecurringScheduleFormController.createRecurringScheduleFormController;
   const originalRows = WildEncounterScheduleRowsController.createWildEncounterScheduleRowsController;
   const originalPopulate = ConsoleDropdownPopulator.populateGuardiansTalkDropdown;
   const originalGetField = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalSet = ConsoleOperationsClient.setGuardiansTalkSchedule;
   const originalReplace = ConsoleOperationsClient.replaceGuardiansTalkScheduleOverlaps;
   const originalTrim = ConsoleOperationsClient.trimGuardiansTalkScheduleOverlaps;
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   let captured;
   const calls = [];
   const scheduleRowsController = {
      getRows: () => [{ time: '11:00 AM', monday: true }],
      reset: () => {
         calls.push('rowsReset');
      },
      validate: () => null,
   };
   const talkLocationFilterController = {
      clear: () => {
         calls.push('talkClear');
      },
      refreshLocations: async () => {
         calls.push('refreshLocations');
      },
   };

   RecurringScheduleFormController.createRecurringScheduleFormController = (options) => {
      captured = options;
      return { controller: true };
   };
   WildEncounterScheduleRowsController.createWildEncounterScheduleRowsController = () => scheduleRowsController;
   ConsoleDropdownPopulator.populateGuardiansTalkDropdown = (...args) => {
      calls.push(['populate', ...args]);
   };
   ControllerHelper.getFieldValue = (el) => el?.value ?? '';
   ControllerHelper.resetFormFields = (...args) => {
      calls.push(['resetFields', ...args]);
   };
   ConsoleOperationsClient.setGuardiansTalkSchedule = async (payload) => ({ success: true, ...payload });
   ConsoleOperationsClient.replaceGuardiansTalkScheduleOverlaps = async (payload) => ({
      replaced: true,
      ...payload,
   });
   ConsoleOperationsClient.trimGuardiansTalkScheduleOverlaps = async (payload) => ({
      trimmed: true,
      ...payload,
   });

   try {
      const talkNameEl = document.createElement('select');
      talkNameEl.value = 'Keeper Talk';
      const locationEl = document.createElement('select');
      locationEl.value = 'Africa';

      const result = GuardiansTalkController.createGuardiansTalkScheduleController({
         talkNameEl,
         locationEl,
         startDateEl: {},
         endDateEl: {},
         scheduleRowsEl: {},
         addScheduleRowEl: {},
         messageEl: {},
         talkLocationFilterController,
      });

      assert.deepEqual(result, { controller: true });
      assert.equal(captured.loadErrorMessage, Strings.loadErrors.locations);
      assert.deepEqual(captured.getSelectionValues(), {
         talk: 'Keeper Talk',
         location: 'Africa',
      });
      assert.equal(
         captured.validateSelection({ talk: '', location: '' }),
         Strings.validation.entityRequired(Strings.labels.location)
      );
      assert.equal(
         captured.validateSelection({ talk: '', location: 'Africa' }),
         Strings.validation.entityRequired(Strings.labels.talkName)
      );
      assert.equal(captured.validateSelection({ talk: 'Talk', location: 'Africa' }), null);
      assert.equal(
         captured.successMessage({ talk: 'Talk', location: 'Africa' }),
         Strings.status.guardiansTalkScheduleSaved({ talk: 'Talk', location: 'Africa' })
      );

      await captured.prepareForm();
      assert.ok(calls.includes('refreshLocations'));

      captured.resetScheduleTimes();
      assert.ok(calls.includes('rowsReset'));

      captured.resetSelection();
      assert.ok(calls.includes('talkClear'));

      assert.deepEqual(
         await captured.submitSchedule({
            talk: 'Talk',
            location: 'Africa',
            startDate: '',
            endDate: '',
            message: 'hi',
         }),
         {
            success: true,
            talk: 'Talk',
            location: 'Africa',
            startDate: null,
            endDate: null,
            message: 'hi',
            scheduleRows: [{ time: '11:00 AM', monday: true }],
         }
      );

      ConsoleOperationsClient.setGuardiansTalkSchedule = async () => ({
         success: false,
         errorType: OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_ERROR_TYPE,
      });

      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
         OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE
      );
      assert.equal(
         (await captured.submitSchedule({
            talk: 'Talk',
            location: 'Africa',
            startDate: '2026-01-01',
            endDate: '',
            message: '',
         })).replaced,
         true
      );

      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
         OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM
      );
      assert.equal(
         (await captured.submitSchedule({
            talk: 'Talk',
            location: 'Africa',
            startDate: '2026-01-01',
            endDate: '',
            message: '',
         })).trimmed,
         true
      );

      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => null;
      assert.deepEqual(
         await captured.submitSchedule({
            talk: 'Talk',
            location: 'Africa',
            startDate: '2026-01-01',
            endDate: '',
            message: '',
         }),
         { success: false, dismissed: true }
      );
   } finally {
      RecurringScheduleFormController.createRecurringScheduleFormController = originalCreate;
      WildEncounterScheduleRowsController.createWildEncounterScheduleRowsController = originalRows;
      ConsoleDropdownPopulator.populateGuardiansTalkDropdown = originalPopulate;
      ControllerHelper.getFieldValue = originalGetField;
      ControllerHelper.resetFormFields = originalReset;
      ConsoleOperationsClient.setGuardiansTalkSchedule = originalSet;
      ConsoleOperationsClient.replaceGuardiansTalkScheduleOverlaps = originalReplace;
      ConsoleOperationsClient.trimGuardiansTalkScheduleOverlaps = originalTrim;
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
   }
});

test('Test_CreateGuardiansTalkScheduleController_TestResetWithoutFilter_ExpectPopulate', () => {
   const originalCreate = RecurringScheduleFormController.createRecurringScheduleFormController;
   const originalRows = WildEncounterScheduleRowsController.createWildEncounterScheduleRowsController;
   const originalPopulate = ConsoleDropdownPopulator.populateGuardiansTalkDropdown;
   const originalGetField = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   let captured;
   const populateCalls = [];

   RecurringScheduleFormController.createRecurringScheduleFormController = (options) => {
      captured = options;
      return {};
   };
   WildEncounterScheduleRowsController.createWildEncounterScheduleRowsController = () => ({
      getRows: () => [],
      reset: () => {},
      validate: () => null,
   });
   ConsoleDropdownPopulator.populateGuardiansTalkDropdown = (...args) => {
      populateCalls.push(args);
   };
   ControllerHelper.getFieldValue = () => '';
   ControllerHelper.resetFormFields = () => {};

   try {
      GuardiansTalkController.createGuardiansTalkScheduleController({
         talkNameEl: document.createElement('select'),
         locationEl: document.createElement('select'),
         scheduleRowsEl: {},
         addScheduleRowEl: {},
      });

      captured.resetSelection();
      assert.equal(populateCalls.length, 1);
      assert.deepEqual(populateCalls[0][1], []);

      const talkNameEl = document.createElement('input');
      talkNameEl.value = 'Old Talk';
      GuardiansTalkController.createGuardiansTalkScheduleController({
         talkNameEl,
         locationEl: document.createElement('select'),
         scheduleRowsEl: {},
         addScheduleRowEl: {},
      });
      captured.resetSelection();
      assert.equal(talkNameEl.value, '');
   } finally {
      RecurringScheduleFormController.createRecurringScheduleFormController = originalCreate;
      WildEncounterScheduleRowsController.createWildEncounterScheduleRowsController = originalRows;
      ConsoleDropdownPopulator.populateGuardiansTalkDropdown = originalPopulate;
      ControllerHelper.getFieldValue = originalGetField;
      ControllerHelper.resetFormFields = originalReset;
   }
});
