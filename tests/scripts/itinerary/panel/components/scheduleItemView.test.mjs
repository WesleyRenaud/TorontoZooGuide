import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { ScheduleItemView } from '../../../../../scripts/itinerary/panel/components/scheduleItemView.js';
import { DayPlannerBuilder } from '../../../../../scripts/itinerary/panel/components/dayPlannerBuilder.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../../scripts/strings.js';
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
   const label = Strings.itinerary.dayPlanner.scheduleItemButton;
   let clicked = false;

   const button = ScheduleItemView.makeScheduleItemButton({
      label,
      onClick: () => {
         clicked = true;
      },
   });
   button.listeners.click();

   assert.equal(button.textContent, label);
   assert.equal(button.type, 'button');
   assert.equal(clicked, true);
});


test('Test_MakeDayPlannerPreview_TestRebuildButton_ExpectBelowScheduleItem', () => {
   installTestWindow();
   installDocument();
   let rebuildScheduleClicked = false;

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
         onRebuildScheduleClick: () => {
            rebuildScheduleClicked = true;
         },
      }
   );
   const buttons = planner.querySelectorAll('.itinerary-day-schedule-item-btn');
   const scheduleLabel = buttons[Position.FIRST].textContent;
   const rebuildLabel = buttons[Position.SECOND].textContent;
   buttons[Position.SECOND].listeners.click();

   assert.equal(buttons.length, 2);
   assert.equal(scheduleLabel, Strings.itinerary.dayPlanner.scheduleItemButton);
   assert.equal(rebuildLabel, Strings.itinerary.dayPlanner.rebuildScheduleButton);
   assert.equal(rebuildScheduleClicked, true);
   assert.ok(planner.querySelector('.itinerary-day-schedule-actions'));
   assert.ok(planner.querySelector('.itinerary-day-module-schedule-actions'));
   assert.ok(buttons[Position.SECOND].classList.contains('itinerary-day-schedule-item-btn--secondary'));
});


test('Test_MakeDayPlannerPreview_TestScheduledItems_ExpectUnscheduleButton', () => {
   installTestWindow();
   installDocument();
   let unscheduleAllClicked = false;
   let rebuildScheduleClicked = false;

   const planner = DayPlannerBuilder.makeDayPlannerPreview(
      {
         date: '2026-06-20',
         openTime: '09:30',
         closeTime: '19:00',
      },
      {
         animals: [{
            species: 'Amur Tiger',
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
   const rebuildLabel = buttons[Position.SECOND].textContent;
   const unscheduleLabel = buttons[Position.THIRD].textContent;
   buttons[Position.SECOND].listeners.click();
   buttons[Position.THIRD].listeners.click();

   assert.equal(buttons.length, 3);
   assert.equal(actionRows.length, 1);
   assert.equal(rebuildLabel, Strings.itinerary.dayPlanner.rebuildScheduleButton);
   assert.equal(unscheduleLabel, Strings.itinerary.dayPlanner.unscheduleAllButton);
   assert.ok(buttons[Position.THIRD].classList.contains('itinerary-day-schedule-item-btn--destructive'));
   assert.equal(rebuildScheduleClicked, true);
   assert.equal(unscheduleAllClicked, true);
});


test('Test_MakeDayPlannerPreview_TestEmptyItinerary_ExpectUnscheduleButton', () => {
   installTestWindow();
   installDocument();
   let unscheduleAllClicked = false;

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
         onUnscheduleAllItemsClick: () => {
            unscheduleAllClicked = true;
         },
      }
   );
   const buttons = planner.querySelectorAll('.itinerary-day-schedule-item-btn');
   const unscheduleLabel = buttons[Position.THIRD].textContent;
   buttons[Position.THIRD].listeners.click();

   assert.equal(buttons.length, 3);
   assert.equal(unscheduleLabel, Strings.itinerary.dayPlanner.unscheduleAllButton);
   assert.equal(unscheduleAllClicked, true);
});


test('Test_SetScheduleItemButtonBusy_TestBusy_ExpectLabelAndState', () => {
   installTestWindow();
   installDocument();
   const label = Strings.itinerary.dayPlanner.rebuildScheduleButton;
   const busyLabel = Strings.itinerary.dayPlanner.rebuildScheduleButtonBusy;

   const button = ScheduleItemView.makeScheduleItemButton({
      label,
      variant: 'secondary',
   });
   ScheduleItemView.setScheduleItemButtonBusy(button, true, busyLabel);

   assert.equal(button.textContent, busyLabel);
   assert.equal(button.disabled, true);
   assert.equal(button.getAttribute('aria-busy'), 'true');
   assert.equal(button.classList.contains('is-busy'), true);
});


test('Test_SetScheduleItemButtonBusy_TestClear_ExpectRestored', () => {
   installTestWindow();
   installDocument();
   const label = Strings.itinerary.dayPlanner.rebuildScheduleButton;
   const busyLabel = Strings.itinerary.dayPlanner.rebuildScheduleButtonBusy;

   const button = ScheduleItemView.makeScheduleItemButton({
      label,
      variant: 'secondary',
   });
   ScheduleItemView.setScheduleItemButtonBusy(button, true, busyLabel);
   ScheduleItemView.setScheduleItemButtonBusy(button, false);

   assert.equal(button.textContent, label);
   assert.equal(button.disabled, false);
   assert.equal(button.getAttribute('aria-busy'), 'false');
   assert.equal(button.classList.contains('is-busy'), false);
});


test('Test_RunScheduleItemButtonAction_TestAwait_ExpectBusyUntilDone', async () => {
   installTestWindow();
   installDocument();
   const label = Strings.itinerary.dayPlanner.rebuildScheduleButton;
   const busyLabel = Strings.itinerary.dayPlanner.rebuildScheduleButtonBusy;
   const button = ScheduleItemView.makeScheduleItemButton({
      label,
      variant: 'secondary',
   });
   const states = [];

   await ScheduleItemView.runScheduleItemButtonAction(button, async () => {
      states.push({
         textContent: button.textContent,
         disabled: button.disabled,
         isBusy: button.classList.contains('is-busy'),
      });
   }, busyLabel);

   assert.deepEqual(states, [{
      textContent: busyLabel,
      disabled: true,
      isBusy: true,
   }]);
   assert.equal(button.textContent, label);
   assert.equal(button.disabled, false);
   assert.equal(button.classList.contains('is-busy'), false);
});


test('Test_RunScheduleItemButtonAction_TestAlreadyDisabled_ExpectNoOp', async () => {
   installTestWindow();
   installDocument();
   const button = ScheduleItemView.makeScheduleItemButton({
      label: Strings.itinerary.dayPlanner.rebuildScheduleButton,
   });
   button.disabled = true;
   let ran = false;

   await ScheduleItemView.runScheduleItemButtonAction(button, async () => {
      ran = true;
   });

   assert.equal(ran, false);
});


test('Test_SetScheduleItemButtonBusy_TestExistingDefaultLabel_ExpectPreserved', () => {
   installTestWindow();
   installDocument();
   const defaultLabel = 'Fresh';
   const busyLabel = 'Busy…';
   const button = document.createElement('button');
   button.textContent = defaultLabel;

   ScheduleItemView.setScheduleItemButtonBusy(button, true, busyLabel);
   const storedDefault = button.dataset.defaultLabel;
   ScheduleItemView.setScheduleItemButtonBusy(button, false);

   assert.equal(storedDefault, defaultLabel);
   assert.equal(button.textContent, defaultLabel);
});
