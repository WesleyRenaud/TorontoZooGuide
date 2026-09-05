import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { ScheduleItemButton } from '../../../../../scripts/itinerary/panel/components/scheduleItemButton.js';
import { DayPlanner } from '../../../../../scripts/itinerary/panel/components/dayPlanner.js';
import {
   installDocument,
   installTestWindow,
   teardownDocument,
} from '../../../helpers/domMock.mjs';

afterEach(() => {
   teardownDocument();
   delete globalThis.window;
});

test('Test_MakeScheduleItemButton_TestOptionalClick_ExpectWired', () => {
   installTestWindow();
   installDocument();

   let clicked = false;
   const button = ScheduleItemButton.makeScheduleItemButton({
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

test('Test_MakeDayPlannerPreview_TestRebuildButton_ExpectBelowScheduleItem', () => {
   installTestWindow();
   installDocument();

   let rebuildScheduleClicked = false;
   const planner = DayPlanner.makeDayPlannerPreview(
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
         onRebuildScheduleClick: () => {
            rebuildScheduleClicked = true;
         },
      }
   );

   const buttons = planner.querySelectorAll('.itinerary-day-schedule-item-btn');

   assert.equal(buttons.length, 2);
   assert.equal(buttons[0].textContent, 'Schedule an item');
   assert.equal(buttons[1].textContent, 'Rebuild schedule');

   buttons[1].listeners.click();
   assert.equal(rebuildScheduleClicked, true);

   const actionsBar = planner.querySelector('.itinerary-day-schedule-actions');
   const scheduleActions = planner.querySelector('.itinerary-day-module-schedule-actions');

   assert.ok(actionsBar);
   assert.ok(scheduleActions);
   assert.ok(buttons[1].classList.contains('itinerary-day-schedule-item-btn--secondary'));
});

test('Test_MakeDayPlannerPreview_TestScheduledItems_ExpectUnscheduleButton', () => {
   installTestWindow();
   installDocument();

   let unscheduleAllClicked = false;
   let rebuildScheduleClicked = false;
   const planner = DayPlanner.makeDayPlannerPreview(
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
         onRebuildScheduleClick: () => {
            rebuildScheduleClicked = true;
         },
         onUnscheduleAllItemsClick: () => {
            unscheduleAllClicked = true;
         },
      }
   );

   const buttons = planner.querySelectorAll('.itinerary-day-schedule-item-btn');
   const actionRows = planner.querySelectorAll('.itinerary-day-schedule-actions');

   assert.equal(buttons.length, 3);
   assert.equal(actionRows.length, 1);
   assert.equal(buttons[1].textContent, 'Rebuild schedule');
   assert.equal(buttons[2].textContent, 'Unschedule all items');
   assert.ok(buttons[2].classList.contains('itinerary-day-schedule-item-btn--destructive'));

   buttons[1].listeners.click();
   buttons[2].listeners.click();

   assert.equal(rebuildScheduleClicked, true);
   assert.equal(unscheduleAllClicked, true);
});

test('Test_MakeDayPlannerPreview_TestEmptyItinerary_ExpectUnscheduleButton', () => {
   installTestWindow();
   installDocument();

   let unscheduleAllClicked = false;
   const planner = DayPlanner.makeDayPlannerPreview(
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
         onUnscheduleAllItemsClick: () => {
            unscheduleAllClicked = true;
         },
      }
   );

   const buttons = planner.querySelectorAll('.itinerary-day-schedule-item-btn');

   assert.equal(buttons.length, 3);
   assert.equal(buttons[2].textContent, 'Unschedule all items');

   buttons[2].listeners.click();
   assert.equal(unscheduleAllClicked, true);
});

test('Test_SetScheduleItemButtonBusy_TestToggle_ExpectLabelAndState', () => {
   installTestWindow();
   installDocument();

   const button = ScheduleItemButton.makeScheduleItemButton({
      label: 'Rebuild schedule',
      variant: 'secondary',
   });

   ScheduleItemButton.setScheduleItemButtonBusy(button, true, 'Rebuilding…');

   assert.equal(button.textContent, 'Rebuilding…');
   assert.equal(button.disabled, true);
   assert.equal(button.getAttribute('aria-busy'), 'true');
   assert.equal(button.classList.contains('is-busy'), true);

   ScheduleItemButton.setScheduleItemButtonBusy(button, false);

   assert.equal(button.textContent, 'Rebuild schedule');
   assert.equal(button.disabled, false);
   assert.equal(button.getAttribute('aria-busy'), 'false');
   assert.equal(button.classList.contains('is-busy'), false);
});

test('Test_RunScheduleItemButtonAction_TestAwait_ExpectBusyUntilDone', async () => {
   installTestWindow();
   installDocument();

   const button = ScheduleItemButton.makeScheduleItemButton({
      label: 'Rebuild schedule',
      variant: 'secondary',
   });
   const states = [];

   await ScheduleItemButton.runScheduleItemButtonAction(button, async () => {
      states.push({
         textContent: button.textContent,
         disabled: button.disabled,
         isBusy: button.classList.contains('is-busy'),
      });
   }, 'Rebuilding…');

   assert.deepEqual(states, [{
      textContent: 'Rebuilding…',
      disabled: true,
      isBusy: true,
   }]);
   assert.equal(button.textContent, 'Rebuild schedule');
   assert.equal(button.disabled, false);
   assert.equal(button.classList.contains('is-busy'), false);
});
