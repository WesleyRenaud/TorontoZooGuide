import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { DayPlannerActionPresenter } from '../../../../scripts/itinerary/panel/dayPlannerActionPresenter.js';
import { DayPlannerActionFeedbackFragment } from '../../../../scripts/itinerary/panel/components/dayPlannerActionFeedbackFragment.js';
import { DayPlannerBuilder } from '../../../../scripts/itinerary/panel/components/dayPlannerBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

afterEach(() => {
   DayPlannerActionPresenter.resetPendingDayPlannerActionFeedback();
});

installDomTestHooks();

test('Test_SetPendingDayPlannerActionFeedback_TestConsume_ExpectOnce', () => {
   DayPlannerActionPresenter.setPendingDayPlannerActionFeedback({
      variant: 'success',
      message: 'All items unscheduled',
   });

   assert.deepEqual(DayPlannerActionPresenter.consumePendingDayPlannerActionFeedback(), {
      variant: 'success',
      message: 'All items unscheduled',
   });
   assert.equal(DayPlannerActionPresenter.consumePendingDayPlannerActionFeedback(), null);
});

test('Test_AppendDayPlannerActionFeedbackBanner_TestSuccess_ExpectStatusBanner', () => {
   const slot = document.createElement('div');
   slot.className = 'itinerary-day-action-feedback-slot';

   DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackBanner(slot, {
      variant: 'success',
      message: 'All items unscheduled',
   }, {
      dismissMs: 10_000,
      fadeMs: 300,
   });

   const banner = slot.querySelector('.itinerary-day-action-feedback--success');

   assert.ok(banner);
   assert.equal(banner.textContent, 'All items unscheduled');
   assert.equal(banner.getAttribute('role'), 'status');
});

test('Test_AppendDayPlannerActionFeedbackBanner_TestError_ExpectStatusBanner', () => {
   const slot = document.createElement('div');
   slot.className = 'itinerary-day-action-feedback-slot';

   DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackBanner(slot, {
      variant: 'error',
      message: 'There were no items to unschedule.',
   }, {
      dismissMs: 10_000,
      fadeMs: 300,
   });

   const banner = slot.querySelector('.itinerary-day-action-feedback--error');

   assert.ok(banner);
   assert.equal(banner.textContent, 'There were no items to unschedule.');
   assert.equal(banner.getAttribute('role'), 'status');
});

test('Test_MakeDayPlannerPreview_TestPendingFeedback_ExpectBelowButtons', () => {
   DayPlannerActionPresenter.setPendingDayPlannerActionFeedback({
      variant: 'success',
      message: 'All items unscheduled',
   });

   const planner = DayPlannerBuilder.makeDayPlannerPreview(
      {
         date: '2026-06-20',
         openTime: '09:30',
         closeTime: '19:00',
      },
      {
         animals: [{
            species: 'Tiger',
            exhibit: 'Savanna',
            start_time: '10:00',
            end_time: '10:30',
         }],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
      },
      {},
      {
         onScheduleItemClick: () => {},
         onRebuildScheduleClick: () => {},
         onUnscheduleAllItemsClick: () => {},
      }
   );

   const banner = planner.querySelector('.itinerary-day-action-feedback--success');
   const buttonBar = planner.querySelector('.itinerary-day-schedule-actions');
   const feedbackSlot = planner.querySelector('.itinerary-day-action-feedback-slot');
   const scheduleActions = planner.querySelector('.itinerary-day-module-schedule-actions');

   assert.ok(banner);
   assert.equal(banner.textContent, 'All items unscheduled');
   assert.ok(feedbackSlot);
   assert.ok(feedbackSlot.contains(banner));
   assert.equal(scheduleActions?.querySelector('.itinerary-day-schedule-actions'), buttonBar);
   assert.equal(scheduleActions?.querySelector('.itinerary-day-action-feedback-slot'), feedbackSlot);
   assert.equal(DayPlannerActionPresenter.consumePendingDayPlannerActionFeedback(), null);
});

test('Test_MakeDayPlannerPreview_TestNoFeedback_ExpectReservedSlot', () => {
   const planner = DayPlannerBuilder.makeDayPlannerPreview(
      { date: '2026-06-20' },
      {
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
      },
      {},
      {
         onScheduleItemClick: () => {},
         onRebuildScheduleClick: () => {},
      }
   );

   const scheduleActions = planner.querySelector('.itinerary-day-module-schedule-actions');
   const buttonBar = planner.querySelector('.itinerary-day-schedule-actions');
   const feedbackSlot = planner.querySelector('.itinerary-day-action-feedback-slot');

   assert.ok(scheduleActions);
   assert.ok(buttonBar);
   assert.ok(feedbackSlot);
   assert.equal(scheduleActions.querySelector('.itinerary-day-action-feedback--success'), null);
});
