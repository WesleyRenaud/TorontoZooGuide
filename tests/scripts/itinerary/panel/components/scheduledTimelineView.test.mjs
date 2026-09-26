import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduledTimelineView } from '../../../../../scripts/itinerary/panel/components/scheduledTimelineView.js';
import { ScheduledPillPresenter } from '../../../../../scripts/itinerary/panel/scheduledPillPresenter.js';
import { TimelineLayoutConstants } from '../../../../../scripts/shared/timelineLayoutConstants.js';
import { ZooClockTimeHelper } from '../../../../../scripts/shared/zooClockTimeHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

function _clockAfterMinutes(clockTime, durationMinutes) {
   const startMinutes = ZooClockTimeHelper.parseMinutes(clockTime);
   const totalMinutes = startMinutes + durationMinutes;
   const hours = Math.floor(totalMinutes / 60);
   const minutes = totalMinutes % 60;

   return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
}

installDomTestHooks();


test('Test_MakeScheduledPill_TestLongerVisit_ExpectExtendedLayout', () => {
   const label = 'Tundra Grill';
   const startTime = '12:00';
   const durationMinutes = TimelineLayoutConstants.EXTENDED_SCHEDULED_PILL_MINUTES + 10;
   const endTime = _clockAfterMinutes(startTime, durationMinutes);

   const pill = ScheduledTimelineView.makeScheduledPill(label, durationMinutes, {
      startTime,
      endTime,
      menuItems: [
         { label: 'Unschedule', onAction: () => {} },
         { label: 'Remove', onAction: () => {} },
      ],
      menuAriaLabel: 'Menu',
   });

   assert.equal(
      pill.classList.contains('itinerary-day-scheduled-pill--extended'),
      ScheduledPillPresenter.isExtendedScheduledPill(durationMinutes)
   );
   assert.ok(pill.querySelector('.itinerary-day-scheduled-pill-header'));
   assert.equal(pill.querySelector('.itinerary-day-scheduled-pill-time-range'), null);
});


test('Test_MakeScheduledPill_TestGroupedItems_ExpectNoTimeRange', () => {
   const gibbon = 'White-Handed Gibbon';
   const snake = 'Tentacled Snake';
   const startTime = '10:31:30';
   const durationMinutes = TimelineLayoutConstants.EXTENDED_SCHEDULED_PILL_MINUTES + 6;
   const endTime = '10:36:30';
   const groupItems = [
      {
         label: gibbon,
         startTime,
         endTime,
      },
      {
         label: snake,
         startTime: '10:27:30',
         endTime: startTime,
      },
   ];

   const pill = ScheduledTimelineView.makeScheduledPill(
      `${gibbon} + 29`,
      durationMinutes,
      {
         startTime,
         endTime,
         groupItems,
      }
   );

   assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--grouped'));
   assert.equal(pill.querySelector('.itinerary-day-scheduled-pill-time-range'), null);
});


test('Test_MakeScheduledPill_TestShortVisit_ExpectCompactLayout', () => {
   const label = 'African Lion';
   const startTime = '13:00';
   const durationMinutes = TimelineLayoutConstants.EXTENDED_SCHEDULED_PILL_MINUTES - 15;
   const endTime = _clockAfterMinutes(startTime, durationMinutes);
   const menuItems = [{ label: 'Unschedule', onAction: () => {} }];

   const pill = ScheduledTimelineView.makeScheduledPill(label, durationMinutes, {
      startTime,
      endTime,
      menuItems,
   });

   assert.equal(
      pill.querySelectorAll('.itinerary-day-open-pill-menu-item').length,
      menuItems.length
   );
   assert.equal(
      pill.classList.contains('itinerary-day-scheduled-pill--extended'),
      ScheduledPillPresenter.isExtendedScheduledPill(durationMinutes)
   );
   assert.equal(pill.querySelector('.itinerary-day-scheduled-pill-time-range'), null);
});


test('Test_MakeScheduledPill_TestEmptyLabel_ExpectNull', () => {
   const durationMinutes = TimelineLayoutConstants.EXTENDED_SCHEDULED_PILL_MINUTES - 15;

   const pill = ScheduledTimelineView.makeScheduledPill('', durationMinutes);

   assert.equal(pill, null);
});


test('Test_MakeScheduledPill_TestZeroDuration_ExpectNull', () => {
   const label = 'Tundra Grill';
   const durationMinutes = 0;

   const pill = ScheduledTimelineView.makeScheduledPill(label, durationMinutes);

   assert.equal(pill, null);
});


test('Test_MakeScheduledPill_TestMenuless_ExpectPlainPill', () => {
   const label = 'African Lion';
   const startTime = '13:00';
   const durationMinutes = TimelineLayoutConstants.EXTENDED_SCHEDULED_PILL_MINUTES - 15;
   const endTime = _clockAfterMinutes(startTime, durationMinutes);

   const pill = ScheduledTimelineView.makeScheduledPill(label, durationMinutes, {
      startTime,
      endTime,
   });

   assert.ok(pill);
   assert.equal(pill.querySelectorAll('.itinerary-day-open-pill-menu-item').length, 0);
});
