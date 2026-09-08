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
