import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { makeScheduleItemButton } from '../../scripts/itinerary/panel/components/scheduleItemButton.js';
import { makeDayPlannerPreview } from '../../scripts/itinerary/panel/components/dayPlanner.js';
import {
   installDocument,
   teardownDocument,
} from './helpers/domMock.mjs';

afterEach(() => {
   teardownDocument();
});

test('makeScheduleItemButton wires an optional click handler', () => {
   installDocument();

   let clicked = false;
   const button = makeScheduleItemButton({
      label: 'Schedule an item',
      onClick: () => {
         clicked = true;
      },
   });

   assert.equal(button.textContent, 'Schedule an item');
   assert.equal(button.type, 'button');

   button.listeners.click();
   assert.equal(clicked, true);
});

test('makeDayPlannerPreview renders bulk schedule button below schedule item button', () => {
   installDocument();

   let bulkScheduleClicked = false;
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
         onBulkScheduleAnimalsClick: () => {
            bulkScheduleClicked = true;
         },
      }
   );

   const buttons = planner.querySelectorAll('.itinerary-day-schedule-item-btn');

   assert.equal(buttons.length, 2);
   assert.equal(buttons[0].textContent, 'Schedule an item');
   assert.equal(buttons[1].textContent, 'Schedule all animals');

   buttons[1].listeners.click();
   assert.equal(bulkScheduleClicked, true);

   const actionsBar = planner.querySelector('.itinerary-day-schedule-actions');
   assert.ok(actionsBar);
   assert.ok(buttons[1].classList.contains('itinerary-day-schedule-item-btn--secondary'));
});
