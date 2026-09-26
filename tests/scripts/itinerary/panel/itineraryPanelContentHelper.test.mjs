import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelContentHelper } from '../../../../scripts/itinerary/panel/itineraryPanelContentHelper.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

function _appendDayPlanner(deps) {
   const opens = [];
   const feedback = [];
   const refreshes = [];
   const warnings = [];
   const longWaits = [];
   let capturedOptions;
   const dayPlannerView = document.createElement('div');
   const dayPlannerClass = 'day-planner';
   const genericErrorMessage = 'generic';

   ItineraryPanelContentHelper.appendDayPlannerViewWithHours(
      dayPlannerView,
      { open: '9:00 AM', close: '6:00 PM' },
      { animals: [], itineraryConfig: {} },
      {},
      {
         onPanelRefresh: async () => {
            refreshes.push(true);
         },
         deps: {
            openModule: (options) => {
               opens.push(options);
            },
            bulkSchedule: async () => ({ itinerary: { date: '2026-06-01' } }),
            unscheduleAll: async () => ({ itinerary: { date: '2026-06-01' } }),
            hasNotEnoughTimeIssue: () => false,
            hasMultipleBuildWarnings: () => false,
            showBuildWarningsConfirmation: (payload) => {
               warnings.push(payload);
            },
            requiresLongWaitConfirmation: () => false,
            showLongWaitConfirmation: (payload) => {
               longWaits.push(payload);
            },
            setActionFeedback: (value) => {
               feedback.push(value);
            },
            buildEventTypes: () => ['animal'],
            buildScheduleHandlers: () => ({ unschedule: true }),
            makeDayPlanner: (_hours, _itin, _time, options) => {
               capturedOptions = options;
               const el = document.createElement('div');
               el.className = dayPlannerClass;
               return el;
            },
            genericErrorMessage,
            ...deps,
         },
      }
   );

   return {
      capturedOptions,
      dayPlannerClass,
      dayPlannerView,
      feedback,
      genericErrorMessage,
      longWaits,
      opens,
      refreshes,
      warnings,
   };
}

installDomTestHooks();


test('Test_AppendDayPlannerViewWithHours_TestScheduleItemClick_ExpectModuleOpened', () => {
   const { capturedOptions, dayPlannerClass, dayPlannerView, opens } = _appendDayPlanner();

   capturedOptions.onScheduleItemClick();
   const opened = opens.at(Position.FIRST);

   assert.equal(dayPlannerView.children.at(Position.FIRST).className, dayPlannerClass);
   assert.equal(opens.length, Position.SECOND);
   assert.ok(opened);
});


test('Test_AppendDayPlannerViewWithHours_TestRebuildSuccess_ExpectPanelRefreshed', async () => {
   const { capturedOptions, refreshes } = _appendDayPlanner();

   await capturedOptions.onRebuildScheduleClick();

   assert.ok(refreshes.length >= Position.SECOND);
});


test('Test_AppendDayPlannerViewWithHours_TestRebuildError_ExpectErrorFeedback', async () => {
   const errorMessage = 'nope';
   const errorType = ItineraryErrorType.SAVE_FAILED;
   const { capturedOptions, feedback } = _appendDayPlanner({
      bulkSchedule: async () => ({ errorType, message: errorMessage }),
      unscheduleAll: async () => ({}),
      buildEventTypes: () => [],
      buildScheduleHandlers: () => ({}),
   });

   await capturedOptions.onRebuildScheduleClick();
   const errorFeedback = feedback.find((entry) => entry?.variant === 'error' && entry?.message === errorMessage);

   assert.ok(errorFeedback);
});


test('Test_AppendDayPlannerViewWithHours_TestNotEnoughTime_ExpectErrorFeedback', async () => {
   const { capturedOptions, feedback } = _appendDayPlanner({
      bulkSchedule: async () => ({ issues: [ItineraryErrorType.BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME] }),
      unscheduleAll: async () => ({}),
      hasNotEnoughTimeIssue: () => true,
      buildEventTypes: () => [],
      buildScheduleHandlers: () => ({}),
   });

   await capturedOptions.onRebuildScheduleClick();
   const errorFeedback = feedback.find((entry) => entry?.variant === 'error');

   assert.ok(errorFeedback);
});


test('Test_AppendDayPlannerViewWithHours_TestMultipleBuildWarnings_ExpectConfirmationThenRebuild', async () => {
   const { capturedOptions, warnings } = _appendDayPlanner({
      bulkSchedule: async (confirmed) => {
         if (confirmed) {
            return { itinerary: {} };
         }

         return { issues: ['a', 'b'] };
      },
      unscheduleAll: async () => ({}),
      hasMultipleBuildWarnings: (issues) => issues?.length > Position.SECOND,
      buildEventTypes: () => [],
      buildScheduleHandlers: () => ({}),
   });

   await capturedOptions.onRebuildScheduleClick();
   const warning = warnings.at(Position.FIRST);

   assert.equal(warnings.length, Position.SECOND);

   await warning.onConfirm();
});


test('Test_AppendDayPlannerViewWithHours_TestLongWait_ExpectConfirmationThenRebuild', async () => {
   const errorType = ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT;
   const { capturedOptions, longWaits } = _appendDayPlanner({
      bulkSchedule: async (confirmed) => {
         if (confirmed?.confirmingFixedTimeItemLongWait) {
            return { itinerary: {} };
         }

         return { errorType, issues: [] };
      },
      unscheduleAll: async () => ({}),
      requiresLongWaitConfirmation: (resultErrorType) => resultErrorType === errorType,
      buildEventTypes: () => [],
      buildScheduleHandlers: () => ({}),
   });

   await capturedOptions.onRebuildScheduleClick();
   const longWait = longWaits.at(Position.FIRST);

   assert.equal(longWaits.length, Position.SECOND);

   await longWait.onConfirm();
});


test('Test_AppendDayPlannerViewWithHours_TestRebuildThrows_ExpectErrorFeedback', async () => {
   const originalError = console.error;
   const failure = new Error('rebuild boom');
   console.error = () => {};
   const { capturedOptions, feedback } = _appendDayPlanner({
      bulkSchedule: async () => {
         throw failure;
      },
      unscheduleAll: async () => ({}),
      buildEventTypes: () => [],
      buildScheduleHandlers: () => ({}),
   });

   try {
      await capturedOptions.onRebuildScheduleClick();
      const errorFeedback = feedback.find((entry) => entry?.message === failure.message);

      assert.ok(errorFeedback);
   } finally {
      console.error = originalError;
   }
});


test('Test_AppendDayPlannerViewWithHours_TestConfirmThrows_ExpectErrorFeedback', async () => {
   const originalError = console.error;
   const failure = new Error('confirm boom');
   console.error = () => {};
   const { capturedOptions, feedback, warnings } = _appendDayPlanner({
      bulkSchedule: async (confirmed) => {
         if (confirmed) {
            throw failure;
         }

         return { issues: ['a', 'b'] };
      },
      unscheduleAll: async () => ({}),
      hasMultipleBuildWarnings: () => true,
      buildEventTypes: () => [],
      buildScheduleHandlers: () => ({}),
   });

   try {
      await capturedOptions.onRebuildScheduleClick();
      await warnings.at(Position.LAST).onConfirm();
      const errorFeedback = feedback.find((entry) => entry?.message === failure.message);

      assert.ok(errorFeedback);
   } finally {
      console.error = originalError;
   }
});


test('Test_AppendDayPlannerViewWithHours_TestUnscheduleError_ExpectErrorFeedback', async () => {
   const errorMessage = 'unschedule failed';
   const { capturedOptions, feedback } = _appendDayPlanner({
      bulkSchedule: async () => ({}),
      unscheduleAll: async () => ({ errorType: ItineraryErrorType.SAVE_FAILED, message: errorMessage }),
      buildEventTypes: () => [],
      buildScheduleHandlers: () => ({}),
   });

   await capturedOptions.onUnscheduleAllItemsClick();
   const errorFeedback = feedback.find((entry) => entry?.message === errorMessage);

   assert.ok(errorFeedback);
});


test('Test_AppendDayPlannerViewWithHours_TestUnscheduleSuccess_ExpectSuccessFeedback', async () => {
   const { capturedOptions, feedback } = _appendDayPlanner({
      bulkSchedule: async () => ({}),
      unscheduleAll: async () => ({}),
      buildEventTypes: () => [],
      buildScheduleHandlers: () => ({}),
   });

   await capturedOptions.onUnscheduleAllItemsClick();
   const successFeedback = feedback.find((entry) => entry?.variant === 'success');

   assert.ok(successFeedback);
});


test('Test_AppendDayPlannerViewWithHours_TestUnscheduleThrows_ExpectErrorFeedback', async () => {
   const originalError = console.error;
   const failure = new Error('unschedule boom');
   console.error = () => {};
   const { capturedOptions, feedback } = _appendDayPlanner({
      bulkSchedule: async () => ({}),
      unscheduleAll: async () => {
         throw failure;
      },
      buildEventTypes: () => [],
      buildScheduleHandlers: () => ({}),
   });

   try {
      await capturedOptions.onUnscheduleAllItemsClick();
      const errorFeedback = feedback.find((entry) => entry?.message === failure.message);

      assert.ok(errorFeedback);
   } finally {
      console.error = originalError;
   }
});
