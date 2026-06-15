import assert from 'node:assert/strict';
import { test } from 'node:test';

import { makeScheduledPill } from '../../scripts/itinerary/panel/components/scheduledTimelinePill.js';

test('makeScheduledPill adds extended layout for longer visits', () => {
   const pill = makeScheduledPill('Lunch', 40, {
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
   assert.equal(
      pill.querySelector('.itinerary-day-scheduled-pill-time-range')?.textContent,
      '12:00 PM – 12:40 PM'
   );
});

test('makeScheduledPill keeps compact layout for short visits', () => {
   const pill = makeScheduledPill('African Lion', 15, {
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
