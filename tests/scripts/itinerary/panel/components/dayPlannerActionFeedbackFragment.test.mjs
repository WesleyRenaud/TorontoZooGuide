import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerActionFeedbackFragment } from '../../../../../scripts/itinerary/panel/components/dayPlannerActionFeedbackFragment.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_AppendDayPlannerActionFeedbackSlot_TestNullContainer_ExpectNull', () => {
   const slot = DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackSlot(null);

   assert.equal(slot, null);
});


test('Test_AppendDayPlannerActionFeedbackSlot_TestContainer_ExpectSlot', () => {
   const container = document.createElement('div');

   const slot = DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackSlot(container);

   assert.equal(slot.className, 'itinerary-day-action-feedback-slot');
   assert.equal(slot.getAttribute('aria-live'), 'polite');
   assert.equal(container.children.length, 1);
});


test('Test_AppendDayPlannerActionFeedbackBanner_TestEmptyMessage_ExpectNull', () => {
   const slot = document.createElement('div');

   const banner = DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackBanner(slot, {});

   assert.equal(banner, null);
});


test('Test_AppendDayPlannerActionFeedbackBanner_TestMessage_ExpectBannerAndCleanup', () => {
   const slot = document.createElement('div');
   const message = 'Saved itinerary';
   const variant = 'success';

   const banner = DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackBanner(
      slot,
      { variant, message },
      { dismissMs: 10_000, fadeMs: 10_000 }
   );
   banner.__tzgCleanup();

   assert.equal(banner.getAttribute('role'), 'status');
   assert.match(banner.className, new RegExp(`itinerary-day-action-feedback--${variant}`));
   assert.equal(banner.classList.contains('is-visible'), true);
   assert.equal(slot.children.length, 0);
});


test('Test_AppendDayPlannerActionFeedbackBanner_TestAutoDismiss_ExpectRemoved', async () => {
   const slot = document.createElement('div');
   const dismissMs = 5;
   const fadeMs = 5;

   const autoBanner = DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackBanner(
      slot,
      { variant: 'success', message: 'Auto dismiss' },
      { dismissMs, fadeMs }
   );
   const removed = await new Promise((resolve) => {
      const deadline = Date.now() + dismissMs + fadeMs + 200;
      const poll = () => {
         if (!slot.contains(autoBanner)) {
            resolve(true);
            return;
         }

         if (Date.now() >= deadline) {
            resolve(false);
            return;
         }

         setTimeout(poll, dismissMs);
      };

      setTimeout(poll, dismissMs + fadeMs);
   });

   assert.equal(removed, true);
   assert.equal(slot.contains(autoBanner), false);
});


test('Test_AppendDayPlannerActionFeedbackBanner_TestMidFade_ExpectDismissing', async () => {
   const slot = document.createElement('div');
   const dismissMs = 5;
   const fadeMs = 10_000;

   const midFadeBanner = DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackBanner(
      slot,
      { variant: 'success', message: 'Mid fade' },
      { dismissMs, fadeMs }
   );
   await new Promise((resolve) => {
      setTimeout(resolve, dismissMs + 10);
   });

   assert.equal(midFadeBanner.classList.contains('is-dismissing'), true);
   midFadeBanner.__tzgCleanup();
   assert.equal(slot.children.length, 0);
});
