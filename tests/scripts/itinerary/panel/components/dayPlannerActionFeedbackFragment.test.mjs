import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerActionFeedbackFragment } from '../../../../../scripts/itinerary/panel/components/dayPlannerActionFeedbackFragment.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_AppendDayPlannerActionFeedbackSlot_TestContainer_ExpectSlot', () => {
   assert.equal(DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackSlot(null), null);

   const container = document.createElement('div');
   const slot = DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackSlot(container);
   assert.equal(slot.className, 'itinerary-day-action-feedback-slot');
   assert.equal(slot.getAttribute('aria-live'), 'polite');
   assert.equal(container.children.length, 1);
});

test('Test_AppendDayPlannerActionFeedbackBanner_TestMessage_ExpectBannerAndCleanup', async () => {
   const slot = document.createElement('div');
   assert.equal(DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackBanner(slot, {}), null);

   const banner = DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackBanner(
      slot,
      { variant: 'success', message: 'Saved' },
      { dismissMs: 10_000, fadeMs: 10_000 }
   );

   assert.equal(banner.getAttribute('role'), 'status');
   assert.match(banner.className, /itinerary-day-action-feedback--success/);
   assert.equal(banner.classList.contains('is-visible'), true);
   banner.__tzgCleanup();
   assert.equal(slot.children.length, 0);

   const autoBanner = DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackBanner(
      slot,
      { variant: 'success', message: 'Auto dismiss' },
      { dismissMs: 5, fadeMs: 5 }
   );

   await new Promise((resolve) => {
      setTimeout(resolve, 20);
   });

   assert.equal(slot.contains(autoBanner), false);

   const midFadeBanner = DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackBanner(
      slot,
      { variant: 'success', message: 'Mid fade' },
      { dismissMs: 5, fadeMs: 10_000 }
   );

   await new Promise((resolve) => {
      setTimeout(resolve, 15);
   });

   assert.equal(midFadeBanner.classList.contains('is-dismissing'), true);
   midFadeBanner.__tzgCleanup();
   assert.equal(slot.children.length, 0);
});
