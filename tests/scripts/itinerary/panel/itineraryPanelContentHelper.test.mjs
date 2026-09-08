import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelContentHelper } from '../../../../scripts/itinerary/panel/itineraryPanelContentHelper.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_AppendDayPlannerViewWithHours_TestScheduleAndRebuild_ExpectCallbacks', async () => {
   const opens = [];
   const feedback = [];
   const refreshes = [];
   let capturedOptions;

   const dayPlannerView = document.createElement('div');
   ItineraryPanelContentHelper.appendDayPlannerViewWithHours(
      dayPlannerView,
      { open: '9:00 AM', close: '6:00 PM' },
      { animals: [], itineraryConfig: {} },
      {},
      {
         onPanelRefresh: async () => { refreshes.push(true); },
         deps: {
            openModule: (options) => { opens.push(options); },
            bulkSchedule: async () => ({ itinerary: { date: '2026-06-01' } }),
            unscheduleAll: async () => ({ itinerary: { date: '2026-06-01' } }),
            hasNotEnoughTimeIssue: () => false,
            hasMultipleBuildWarnings: () => false,
            showBuildWarningsConfirmation: async () => {},
            requiresLongWaitConfirmation: () => false,
            showLongWaitConfirmation: async () => {},
            setActionFeedback: (value) => { feedback.push(value); },
            buildEventTypes: () => ['animal'],
            buildScheduleHandlers: () => ({ unschedule: true }),
            makeDayPlanner: (_hours, _itin, _time, options) => {
               capturedOptions = options;
               const el = document.createElement('div');
               el.className = 'day-planner';
               return el;
            },
            genericErrorMessage: 'generic',
         },
      }
   );

   assert.equal(dayPlannerView.children[0].className, 'day-planner');
   capturedOptions.onScheduleItemClick();
   assert.equal(opens.length, 1);

   await capturedOptions.onRebuildScheduleClick();
   assert.ok(refreshes.length >= 1);

   let errorOptions;
   ItineraryPanelContentHelper.appendDayPlannerViewWithHours(
      document.createElement('div'),
      {},
      {},
      {},
      {
         onPanelRefresh: async () => {},
         deps: {
            openModule: () => {},
            bulkSchedule: async () => ({ errorType: 'bad', message: 'nope' }),
            unscheduleAll: async () => ({}),
            hasNotEnoughTimeIssue: () => false,
            hasMultipleBuildWarnings: () => false,
            showBuildWarningsConfirmation: async () => {},
            requiresLongWaitConfirmation: () => false,
            showLongWaitConfirmation: async () => {},
            setActionFeedback: (value) => { feedback.push(value); },
            buildEventTypes: () => [],
            buildScheduleHandlers: () => ({}),
            makeDayPlanner: (_h, _i, _t, options) => {
               errorOptions = options;
               return document.createElement('div');
            },
            genericErrorMessage: 'generic',
         },
      }
   );

   await errorOptions.onRebuildScheduleClick();
   assert.ok(feedback.some((entry) => entry?.variant === 'error' && entry?.message === 'nope'));
});

test('Test_AppendDayPlannerViewWithHours_TestWarningsLongWaitNotEnoughAndErrors_ExpectBranches', async () => {
   const feedback = [];
   const warnings = [];
   const longWaits = [];
   const originalError = console.error;
   console.error = () => {};

   function _makeController(deps) {
      let options;
      ItineraryPanelContentHelper.appendDayPlannerViewWithHours(
         document.createElement('div'),
         {},
         {},
         {},
         {
            onPanelRefresh: async () => {},
            deps: {
               openModule: () => {},
               hasNotEnoughTimeIssue: () => false,
               hasMultipleBuildWarnings: () => false,
               showBuildWarningsConfirmation: (payload) => { warnings.push(payload); },
               requiresLongWaitConfirmation: () => false,
               showLongWaitConfirmation: (payload) => { longWaits.push(payload); },
               setActionFeedback: (value) => { feedback.push(value); },
               buildEventTypes: () => [],
               buildScheduleHandlers: () => ({}),
               makeDayPlanner: (_h, _i, _t, captured) => {
                  options = captured;
                  return document.createElement('div');
               },
               genericErrorMessage: 'generic',
               ...deps,
            },
         }
      );
      return options;
   }

   try {
      const notEnough = _makeController({
         bulkSchedule: async () => ({ issues: ['not-enough'] }),
         unscheduleAll: async () => ({}),
         hasNotEnoughTimeIssue: () => true,
      });
      await notEnough.onRebuildScheduleClick();
      assert.ok(feedback.some((entry) => entry?.variant === 'error'));

      const warningOptions = _makeController({
         bulkSchedule: async (confirmed) => {
            if (confirmed) {
               return { itinerary: {} };
            }
            return { issues: ['a', 'b'] };
         },
         unscheduleAll: async () => ({}),
         hasMultipleBuildWarnings: (issues) => issues?.length > 1,
      });
      await warningOptions.onRebuildScheduleClick();
      assert.equal(warnings.length, 1);
      await warnings[0].onConfirm();

      const longWaitOptions = _makeController({
         bulkSchedule: async (confirmed) => {
            if (confirmed?.confirmingFixedTimeItemLongWait) {
               return { itinerary: {} };
            }
            return { errorType: 'longWait', issues: [] };
         },
         unscheduleAll: async () => ({}),
         requiresLongWaitConfirmation: (errorType) => errorType === 'longWait',
      });
      await longWaitOptions.onRebuildScheduleClick();
      assert.equal(longWaits.length, 1);
      await longWaits[0].onConfirm();

      const rebuildThrow = _makeController({
         bulkSchedule: async () => {
            throw new Error('rebuild boom');
         },
         unscheduleAll: async () => ({}),
      });
      await rebuildThrow.onRebuildScheduleClick();
      assert.ok(feedback.some((entry) => entry?.message === 'rebuild boom'));

      const confirmThrow = _makeController({
         bulkSchedule: async (confirmed) => {
            if (confirmed) {
               throw new Error('confirm boom');
            }
            return { issues: ['a', 'b'] };
         },
         unscheduleAll: async () => ({}),
         hasMultipleBuildWarnings: () => true,
      });
      await confirmThrow.onRebuildScheduleClick();
      await warnings.at(-1).onConfirm();
      assert.ok(feedback.some((entry) => entry?.message === 'confirm boom'));

      const unscheduleError = _makeController({
         bulkSchedule: async () => ({}),
         unscheduleAll: async () => ({ errorType: 'bad', message: 'unschedule failed' }),
      });
      await unscheduleError.onUnscheduleAllItemsClick();
      assert.ok(feedback.some((entry) => entry?.message === 'unschedule failed'));

      const unscheduleOk = _makeController({
         bulkSchedule: async () => ({}),
         unscheduleAll: async () => ({}),
      });
      await unscheduleOk.onUnscheduleAllItemsClick();
      assert.ok(feedback.some((entry) => entry?.variant === 'success'));

      const unscheduleThrow = _makeController({
         bulkSchedule: async () => ({}),
         unscheduleAll: async () => {
            throw new Error('unschedule boom');
         },
      });
      await unscheduleThrow.onUnscheduleAllItemsClick();
      assert.ok(feedback.some((entry) => entry?.message === 'unschedule boom'));
   } finally {
      console.error = originalError;
   }
});
