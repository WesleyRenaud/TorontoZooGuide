import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerPlanActionsHelper } from '../../../../scripts/itinerary/panel/dayPlannerPlanActionsHelper.js';

test('Test_ItemHasScheduleTimes_TestTimes_ExpectBoolean', () => {
   assert.equal(
      DayPlannerPlanActionsHelper.itemHasScheduleTimes({
         start_time: '10:00',
         end_time: '10:30',
      }),
      true
   );
   assert.equal(
      DayPlannerPlanActionsHelper.itemHasScheduleTimes({
         start_time: '10:00',
         end_time: '  ',
      }),
      false
   );
});

test('Test_CollectionHasScheduledItems_TestItems_ExpectBoolean', () => {
   assert.equal(
      DayPlannerPlanActionsHelper.collectionHasScheduledItems([
         { start_time: '', end_time: '' },
         { start_time: '11:00', end_time: '11:30' },
      ]),
      true
   );
   assert.equal(DayPlannerPlanActionsHelper.collectionHasScheduledItems([]), false);
   assert.equal(DayPlannerPlanActionsHelper.collectionHasScheduledItems(null), false);
});
