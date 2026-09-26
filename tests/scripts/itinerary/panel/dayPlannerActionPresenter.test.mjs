import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { DayPlannerActionFeedbackFragment } from '../../../../scripts/itinerary/panel/components/dayPlannerActionFeedbackFragment.js';
import { DayPlannerBuilder } from '../../../../scripts/itinerary/panel/components/dayPlannerBuilder.js';
import { DayPlannerActionPresenter } from '../../../../scripts/itinerary/panel/dayPlannerActionPresenter.js';
import { TimelineLayoutConstants } from '../../../../scripts/shared/timelineLayoutConstants.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

afterEach(() => {
   DayPlannerActionPresenter.resetPendingDayPlannerActionFeedback();
});


test('Test_SetPendingDayPlannerActionFeedback_TestConsume_ExpectOnce', () => {
   const feedback = {
      variant: 'success',
      message: 'All items unscheduled',
   };

   DayPlannerActionPresenter.setPendingDayPlannerActionFeedback(feedback);

   const first = DayPlannerActionPresenter.consumePendingDayPlannerActionFeedback();
   const second = DayPlannerActionPresenter.consumePendingDayPlannerActionFeedback();

   assert.deepEqual(first, feedback);
   assert.equal(second, null);
});


test('Test_AppendDayPlannerActionFeedbackBanner_TestSuccess_ExpectStatusBanner', () => {
   const slot = document.createElement('div');
   slot.className = 'itinerary-day-action-feedback-slot';
   const message = 'All items unscheduled';
   const variant = 'success';

   DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackBanner(slot, {
      variant,
      message,
   }, {
      dismissMs: 10_000,
      fadeMs: TimelineLayoutConstants.DAY_PLANNER_ACTION_FEEDBACK_FADE_MS,
   });

   const banner = slot.querySelector(`.itinerary-day-action-feedback--${variant}`);

   assert.ok(banner);
   assert.equal(banner.textContent, message);
   assert.equal(banner.getAttribute('role'), 'status');
});


test('Test_AppendDayPlannerActionFeedbackBanner_TestError_ExpectStatusBanner', () => {
   const slot = document.createElement('div');
   slot.className = 'itinerary-day-action-feedback-slot';
   const message = 'There were no items to unschedule.';
   const variant = 'error';

   DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackBanner(slot, {
      variant,
      message,
   }, {
      dismissMs: 10_000,
      fadeMs: TimelineLayoutConstants.DAY_PLANNER_ACTION_FEEDBACK_FADE_MS,
   });

   const banner = slot.querySelector(`.itinerary-day-action-feedback--${variant}`);

   assert.ok(banner);
   assert.equal(banner.textContent, message);
   assert.equal(banner.getAttribute('role'), 'status');
});


test('Test_MakeDayPlannerPreview_TestPendingFeedback_ExpectBelowButtons', () => {
   const message = 'All items unscheduled';
   const variant = 'success';
   DayPlannerActionPresenter.setPendingDayPlannerActionFeedback({
      variant,
      message,
   });

   const planner = DayPlannerBuilder.makeDayPlannerPreview(
      {
         date: '2026-06-20',
         openTime: '09:30',
         closeTime: '19:00',
      },
      {
         animals: [{
            species: 'Amur Tiger',
            exhibit: 'Eurasia Wilds',
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

   const banner = planner.querySelector(`.itinerary-day-action-feedback--${variant}`);
   const buttonBar = planner.querySelector('.itinerary-day-schedule-actions');
   const feedbackSlot = planner.querySelector('.itinerary-day-action-feedback-slot');
   const scheduleActions = planner.querySelector('.itinerary-day-module-schedule-actions');

   assert.ok(banner);
   assert.equal(banner.textContent, message);
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
