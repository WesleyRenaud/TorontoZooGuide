import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   formatScheduledPillTimeRange,
   isExtendedScheduledPill,
} from '../../scripts/itinerary/panel/scheduledPillPresentation.js';
import { EXTENDED_SCHEDULED_PILL_MINUTES } from '../../scripts/shared/constants.js';
import { makeScheduledPill } from '../../scripts/itinerary/panel/components/dayPlannerTimePill.js';

test('isExtendedScheduledPill uses the half-hour slot as the threshold', () => {
   assert.equal(EXTENDED_SCHEDULED_PILL_MINUTES, 30);
   assert.equal(isExtendedScheduledPill(30), false);
   assert.equal(isExtendedScheduledPill(31), true);
});

test('formatScheduledPillTimeRange formats start and end labels', () => {
   assert.equal(
      formatScheduledPillTimeRange('12:00', '12:40'),
      '12:00 PM – 12:40 PM'
   );
   assert.equal(formatScheduledPillTimeRange('12:00', ''), '');
});

test('makeScheduledPill adds extended layout for longer visits', () => {
   const pill = makeScheduledPill('Lunch', 40, {
      startTime: '12:00',
      endTime: '12:40',
      onUnschedule: () => {},
      menuAriaLabel: 'Menu',
      unscheduleLabel: 'Unschedule',
   });

   assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--extended'));
   assert.ok(pill.querySelector('.itinerary-day-scheduled-pill-header'));
   assert.equal(
      pill.querySelector('.itinerary-day-scheduled-pill-time-range')?.textContent,
      '12:00 PM – 12:40 PM'
   );
});

test('makeScheduledPill keeps compact layout for short visits', () => {
   const pill = makeScheduledPill('African Lion', 15, {
      startTime: '1:00 PM',
      endTime: '1:15 PM',
      onUnschedule: () => {},
   });

   assert.equal(pill.classList.contains('itinerary-day-scheduled-pill--extended'), false);
   assert.equal(pill.querySelector('.itinerary-day-scheduled-pill-time-range'), null);
});
