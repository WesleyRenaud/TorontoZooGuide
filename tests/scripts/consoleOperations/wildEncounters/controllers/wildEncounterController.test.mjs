import assert from 'node:assert/strict';
import test from 'node:test';

import { WildEncounterController } from '../../../../../scripts/consoleOperations/wildEncounters/controllers/wildEncounterController.js';
import { RecurringScheduleFormController } from '../../../../../scripts/consoleOperations/forms/recurringScheduleFormController.js';
import { RecurringScheduleRowsController } from '../../../../../scripts/consoleOperations/forms/recurringScheduleRowsController.js';
import { OpeningScheduleOverlapFragment } from '../../../../../scripts/consoleOperations/forms/openingScheduleOverlapFragment.js';
import { OpeningScheduleChecker } from '../../../../../scripts/consoleOperations/forms/openingScheduleChecker.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateWildEncounterScheduleController_TestWiring_ExpectFormCallbacks', async () => {
   const originalCreate = RecurringScheduleFormController.createRecurringScheduleFormController;
   const originalRows = RecurringScheduleRowsController.createRecurringScheduleRowsController;
   const originalLoad = ConsoleOptionsLoader.loadWildEncounters;
   const originalPopulate = ConsoleDropdownPopulator.populateWildEncounterDropdown;
   const originalGetField = ControllerHelper.getFieldValue;
   const originalReset = ControllerHelper.resetFormFields;
   const originalSet = ConsoleOperationsClient.setWildEncounterSchedule;
   const originalReplace = ConsoleOperationsClient.replaceWildEncounterScheduleOverlaps;
   const originalTrim = ConsoleOperationsClient.trimWildEncounterScheduleOverlaps;
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   let captured;
   const rowCalls = [];
   const scheduleRowsController = {
      getRows: () => [{ time: '11:00 AM', monday: true }],
      reset: () => {
         rowCalls.push('reset');
      },
      validate: () => null,
   };

   RecurringScheduleFormController.createRecurringScheduleFormController = (options) => {
      captured = options;
      return { controller: true };
   };
   RecurringScheduleRowsController.createRecurringScheduleRowsController = () => scheduleRowsController;
   ConsoleOptionsLoader.loadWildEncounters = async () => [{ name: 'Giraffe' }];
   ConsoleDropdownPopulator.populateWildEncounterDropdown = (...args) => {
      rowCalls.push(['populate', ...args]);
   };
   ControllerHelper.getFieldValue = () => 'Giraffe Encounter';
   ControllerHelper.resetFormFields = (...args) => {
      rowCalls.push(['resetFields', ...args]);
   };
   ConsoleOperationsClient.setWildEncounterSchedule = async (payload) => ({ success: true, ...payload });
   ConsoleOperationsClient.replaceWildEncounterScheduleOverlaps = async (payload) => ({
      replaced: true,
      ...payload,
   });
   ConsoleOperationsClient.trimWildEncounterScheduleOverlaps = async (payload) => ({
      trimmed: true,
      ...payload,
   });

   try {
      const wildEncounterEl = document.createElement('select');
      const result = WildEncounterController.createWildEncounterScheduleController({
         wildEncounterEl,
         startDateEl: {},
         endDateEl: {},
         scheduleRowsEl: {},
         addScheduleRowEl: {},
         messageEl: {},
      });

      assert.deepEqual(result, { controller: true });
      assert.equal(captured.loadErrorMessage, Strings.loadErrors.wildEncounters);
      assert.deepEqual(captured.getSelectionValues(), { wildEncounter: 'Giraffe Encounter' });
      assert.equal(
         captured.validateSelection({ wildEncounter: '' }),
         Strings.validation.entityRequired(Strings.entityLabels.wildEncounter)
      );
      assert.equal(captured.validateSelection({ wildEncounter: 'Giraffe' }), null);
      assert.equal(
         captured.successMessage({ wildEncounter: 'Giraffe' }),
         Strings.status.scheduleSaved('Giraffe')
      );
      assert.equal(captured.validateRecurringSchedule(), null);
      assert.equal(captured.shouldReportSubmitFailure({ dismissed: true }), false);

      await captured.prepareForm();
      assert.ok(rowCalls.some((call) => Array.isArray(call) && call[0] === 'populate'));

      captured.resetScheduleTimes();
      assert.ok(rowCalls.includes('reset'));

      captured.resetSelection();
      assert.ok(rowCalls.some((call) => Array.isArray(call) && call[0] === 'resetFields'));

      assert.deepEqual(
         await captured.submitSchedule({
            wildEncounter: 'Giraffe',
            startDate: '',
            endDate: '',
            message: 'hi',
         }),
         {
            success: true,
            wildEncounter: 'Giraffe',
            startDate: null,
            endDate: null,
            message: 'hi',
            scheduleRows: [{ time: '11:00 AM', monday: true }],
         }
      );

      ConsoleOperationsClient.setWildEncounterSchedule = async () => ({
         success: false,
         errorType: OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_ERROR_TYPE,
      });

      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
         OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE
      );
      assert.equal(
         (await captured.submitSchedule({
            wildEncounter: 'Giraffe',
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
            wildEncounter: 'Giraffe',
            startDate: '2026-01-01',
            endDate: '',
            message: '',
         })).trimmed,
         true
      );

      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => null;
      assert.deepEqual(
         await captured.submitSchedule({
            wildEncounter: 'Giraffe',
            startDate: '2026-01-01',
            endDate: '',
            message: '',
         }),
         { success: false, dismissed: true }
      );
   } finally {
      RecurringScheduleFormController.createRecurringScheduleFormController = originalCreate;
      RecurringScheduleRowsController.createRecurringScheduleRowsController = originalRows;
      ConsoleOptionsLoader.loadWildEncounters = originalLoad;
      ConsoleDropdownPopulator.populateWildEncounterDropdown = originalPopulate;
      ControllerHelper.getFieldValue = originalGetField;
      ControllerHelper.resetFormFields = originalReset;
      ConsoleOperationsClient.setWildEncounterSchedule = originalSet;
      ConsoleOperationsClient.replaceWildEncounterScheduleOverlaps = originalReplace;
      ConsoleOperationsClient.trimWildEncounterScheduleOverlaps = originalTrim;
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
   }
});
