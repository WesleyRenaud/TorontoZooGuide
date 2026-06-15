import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySaveIssueItemType } from '../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { resolveScheduleTimeConflictSelection } from '../../scripts/itinerary/panel/scheduleTimeConflictResolution.js';
import { createConflictSelection } from '../../scripts/itinerary/wizard/scheduleConflictCompatibility.js';

const firstEncounter = {
   name: 'From Howls to Honks',
   start_time: '13:00',
   end_time: '13:45',
   item_type: ItinerarySaveIssueItemType.wildEncounter,
   meeting_spot: 'Wild Encounter - Mayan Temple Meeting Spot',
};

const secondEncounter = {
   name: 'Great Barrier Reef',
   start_time: '13:00',
   end_time: '13:45',
   item_type: ItinerarySaveIssueItemType.wildEncounter,
   meeting_spot: 'Wild Encounter - Eurasia Meeting Spot',
};

const thirdEncounter = {
   name: 'Savanna Safari',
   start_time: '14:00',
   end_time: '14:30',
   item_type: ItinerarySaveIssueItemType.wildEncounter,
   meeting_spot: 'Wild Encounter - Penguin Meeting Spot',
};

function createConfirmationRecorder() {
   const calls = [];

   return {
      calls,
      confirmations: {
         showProceedWithoutSelection() {
            calls.push('without-selection');
         },
         showProceedWithUnresolved({ onConfirm } = {}) {
            calls.push('unresolved');
            return onConfirm?.();
         },
         showProceedWithAdditional({ onConfirm } = {}) {
            calls.push('additional');
            return onConfirm?.();
         },
      },
   };
}

test('resolveScheduleTimeConflictSelection prompts when nothing is selected', async () => {
   const { calls, confirmations } = createConfirmationRecorder();
   const resolvedCalls = [];

   const resolved = await resolveScheduleTimeConflictSelection(
      [{
         selection: createConflictSelection(),
         items: [firstEncounter, secondEncounter],
      }],
      async (selectedItems) => {
         resolvedCalls.push(selectedItems);
      },
      confirmations
   );

   assert.equal(resolved, false);
   assert.deepEqual(calls, ['without-selection']);
   assert.deepEqual(resolvedCalls, []);
});

test('resolveScheduleTimeConflictSelection prompts when conflict groups stay unresolved', async () => {
   const { calls, confirmations } = createConfirmationRecorder();
   const resolvedCalls = [];
   const firstSelection = createConflictSelection();
   const secondSelection = createConflictSelection();

   firstSelection.items.push(firstEncounter);

   const resolved = await resolveScheduleTimeConflictSelection(
      [
         {
            selection: firstSelection,
            items: [firstEncounter, secondEncounter],
         },
         {
            selection: secondSelection,
            items: [thirdEncounter],
         },
      ],
      async (selectedItems) => {
         resolvedCalls.push(selectedItems.map(item => item.name));
      },
      confirmations
   );

   assert.equal(resolved, false);
   assert.deepEqual(calls, ['unresolved']);
   assert.deepEqual(resolvedCalls, [['From Howls to Honks']]);
});

test('resolveScheduleTimeConflictSelection prompts when more compatible activities remain', async () => {
   const { calls, confirmations } = createConfirmationRecorder();
   const resolvedCalls = [];
   const selection = createConflictSelection();

   selection.items.push(firstEncounter);

   const resolved = await resolveScheduleTimeConflictSelection(
      [{
         selection,
         items: [firstEncounter, thirdEncounter],
      }],
      async (selectedItems) => {
         resolvedCalls.push(selectedItems.map(item => item.name));
      },
      confirmations
   );

   assert.equal(resolved, false);
   assert.deepEqual(calls, ['additional']);
   assert.deepEqual(resolvedCalls, [['From Howls to Honks']]);
});

test('resolveScheduleTimeConflictSelection resolves immediately when every group is settled', async () => {
   const { calls, confirmations } = createConfirmationRecorder();
   const resolvedCalls = [];
   const selection = createConflictSelection();

   selection.items.push(firstEncounter, secondEncounter);

   const resolved = await resolveScheduleTimeConflictSelection(
      [{
         selection,
         items: [firstEncounter, secondEncounter],
      }],
      async (selectedItems) => {
         resolvedCalls.push(selectedItems.map(item => item.name));
      },
      confirmations
   );

   assert.equal(resolved, true);
   assert.deepEqual(calls, []);
   assert.deepEqual(
      resolvedCalls,
      [['From Howls to Honks', 'Great Barrier Reef']]
   );
});
