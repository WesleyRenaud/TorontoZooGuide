import assert from 'node:assert/strict';
import test from 'node:test';

import { RecurringScheduleSetControllerFactory } from '../../../../scripts/consoleOperations/forms/recurringScheduleSetControllerFactory.js';
import { RecurringScheduleFormController } from '../../../../scripts/consoleOperations/forms/recurringScheduleFormController.js';
import { RecurringScheduleRowsController } from '../../../../scripts/consoleOperations/forms/recurringScheduleRowsController.js';
import { OpeningScheduleOverlapFragment } from '../../../../scripts/consoleOperations/forms/openingScheduleOverlapFragment.js';
import { OpeningScheduleChecker } from '../../../../scripts/consoleOperations/forms/openingScheduleChecker.js';

test('Test_CreateRecurringScheduleSetController_TestWiring_ExpectRowsFormAndOverlap', async () => {
   const originalForm = RecurringScheduleFormController.createRecurringScheduleFormController;
   const originalRows = RecurringScheduleRowsController.createRecurringScheduleRowsController;
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   let captured;
   const rowCalls = [];
   const scheduleRowsController = {
      getRows: () => [{ time: '11:00 AM', monday: true }],
      reset: () => {
         rowCalls.push('reset');
      },
      validate: () => 'row-error',
   };
   let setScheduleImpl = async (payload) => ({ success: true, ...payload });

   RecurringScheduleFormController.createRecurringScheduleFormController = (options) => {
      captured = options;
      return { created: true };
   };
   RecurringScheduleRowsController.createRecurringScheduleRowsController = (options) => {
      rowCalls.push(['createRows', options]);
      return scheduleRowsController;
   };

   try {
      const controller = RecurringScheduleSetControllerFactory.createRecurringScheduleSetController({
         scheduleRowsEl: { rows: true },
         addScheduleRowEl: { add: true },
         startDateEl: {},
         endDateEl: {},
         messageEl: {},
         getSelectionValues: () => ({ entity: 'A' }),
         validateSelection: () => null,
         resetSelection: () => {},
         prepareForm: async () => {},
         loadErrorMessage: 'load failed',
         successMessage: () => 'saved',
         setSchedule: async (payload) => setScheduleImpl(payload),
         replaceOverlaps: async (payload) => ({ replaced: true, ...payload }),
         trimOverlaps: async (payload) => ({ trimmed: true, ...payload }),
      });

      assert.deepEqual(controller, { created: true });
      assert.deepEqual(rowCalls[0], [
         'createRows',
         {
            rowsEl: { rows: true },
            addRowButtonEl: { add: true },
         },
      ]);
      assert.equal(captured.loadErrorMessage, 'load failed');
      assert.equal(captured.validateRecurringSchedule(), 'row-error');
      assert.equal(captured.shouldReportSubmitFailure({ dismissed: true }), false);

      captured.resetScheduleTimes();
      assert.ok(rowCalls.includes('reset'));

      const successPayload = await captured.submitSchedule({
         entity: 'A',
         startDate: '',
         endDate: '',
         message: 'hi',
         time: 'ignored',
      });
      assert.deepEqual(successPayload, {
         success: true,
         entity: 'A',
         startDate: null,
         endDate: null,
         message: 'hi',
         scheduleRows: [{ time: '11:00 AM', monday: true }],
      });
      assert.equal('time' in successPayload, false);

      setScheduleImpl = async () => ({
         success: false,
         errorType: OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_ERROR_TYPE,
      });

      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
         OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE
      );
      assert.equal(
         (await captured.submitSchedule({
            entity: 'B',
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
            entity: 'B',
            startDate: '2026-01-01',
            endDate: '',
            message: '',
         })).trimmed,
         true
      );

      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => null;
      assert.deepEqual(
         await captured.submitSchedule({
            entity: 'B',
            startDate: '2026-01-01',
            endDate: '',
            message: '',
         }),
         { success: false, dismissed: true }
      );
   } finally {
      RecurringScheduleFormController.createRecurringScheduleFormController = originalForm;
      RecurringScheduleRowsController.createRecurringScheduleRowsController = originalRows;
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
   }
});
