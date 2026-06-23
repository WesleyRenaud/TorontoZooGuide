import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import {
   consumePendingDayPlannerActionFeedback,
   resetPendingDayPlannerActionFeedback,
   setPendingDayPlannerActionFeedback,
} from '../../scripts/itinerary/panel/dayPlannerActionFeedback.js';
import { appendDayPlannerActionFeedbackBanner } from '../../scripts/itinerary/panel/components/dayPlannerActionFeedbackBanner.js';
import { makeDayPlannerPreview } from '../../scripts/itinerary/panel/components/dayPlanner.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

test.describe('dayPlannerActionFeedback', () => {
   afterEach(() => {
      resetPendingDayPlannerActionFeedback();
   });

   test('setPendingDayPlannerActionFeedback is consumed once', () => {
      setPendingDayPlannerActionFeedback({
         variant: 'success',
         message: 'All items unscheduled',
      });

      assert.deepEqual(consumePendingDayPlannerActionFeedback(), {
         variant: 'success',
         message: 'All items unscheduled',
      });
      assert.equal(consumePendingDayPlannerActionFeedback(), null);
   });
});

test.describe('dayPlannerActionFeedbackBanner', () => {
   installDomTestHooks();

   test('appendDayPlannerActionFeedbackBanner renders a success status banner', () => {
      const slot = document.createElement('div');
      slot.className = 'itinerary-day-action-feedback-slot';

      appendDayPlannerActionFeedbackBanner(slot, {
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

   test('makeDayPlannerPreview renders pending action feedback below schedule buttons', () => {
      setPendingDayPlannerActionFeedback({
         variant: 'success',
         message: 'All items unscheduled',
      });

      const planner = makeDayPlannerPreview(
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
      assert.equal(consumePendingDayPlannerActionFeedback(), null);
   });

   test('makeDayPlannerPreview reserves feedback slot below schedule buttons', () => {
      const planner = makeDayPlannerPreview(
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
});
