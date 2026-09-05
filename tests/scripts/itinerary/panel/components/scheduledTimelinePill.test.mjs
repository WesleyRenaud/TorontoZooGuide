import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduledTimelinePill } from '../../../../../scripts/itinerary/panel/components/scheduledTimelinePill.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_MakeScheduledPill_TestMakeScheduledPillAddsExtendedLayoutForLongerVisits_ExpectOk', () => {
   const pill = ScheduledTimelinePill.makeScheduledPill('Lunch', 40, {
      startTime: '12:00',
      endTime: '12:40',
      menuItems: [
         { label: 'Unschedule', onAction: () => {} },
         { label: 'Remove', onAction: () => {} },
      ],
      menuAriaLabel: 'Menu',
   });

   assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--extended'));
   assert.ok(pill.querySelector('.itinerary-day-scheduled-pill-header'));
   assert.equal(pill.querySelector('.itinerary-day-scheduled-pill-time-range'), null);
});

test('Test_MakeScheduledPill_TestMakeScheduledPillDoesNotShowTimeRangeForGrouped_ExpectOk', () => {
   const pill = ScheduledTimelinePill.makeScheduledPill('White-Handed Gibbon + 29', 36, {
      startTime: '10:31:30',
      endTime: '10:36:30',
      groupItems: [
         {
            label: 'White-Handed Gibbon',
            startTime: '10:31:30',
            endTime: '10:36:30',
         },
         {
            label: 'Tentacled Snake',
            startTime: '10:27:30',
            endTime: '10:31:30',
         },
      ],
   });

   assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--grouped'));
   assert.equal(pill.querySelector('.itinerary-day-scheduled-pill-time-range'), null);
});

test('Test_MakeScheduledPill_TestMakeScheduledPillKeepsCompactLayoutForShortVisits_ExpectOk', () => {
   const pill = ScheduledTimelinePill.makeScheduledPill('African Lion', 15, {
      startTime: '1:00 PM',
      endTime: '1:15 PM',
      menuItems: [{ label: 'Unschedule', onAction: () => {} }],
   });

   assert.equal(
      pill.querySelectorAll('.itinerary-day-open-pill-menu-item').length,
      1
   );

   assert.equal(pill.classList.contains('itinerary-day-scheduled-pill--extended'), false);
   assert.equal(pill.querySelector('.itinerary-day-scheduled-pill-time-range'), null);
});
