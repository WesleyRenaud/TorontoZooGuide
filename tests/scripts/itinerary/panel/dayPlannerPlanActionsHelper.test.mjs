import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerPlanActionsHelper } from '../../../../scripts/itinerary/panel/dayPlannerPlanActionsHelper.js';
import { Position } from '../../../../scripts/shared/enums/position.js';


test('Test_ItemHasScheduleTimes_TestStartAndEnd_ExpectTrue', () => {
   const item = {
      start_time: '10:00',
      end_time: '10:30',
   };

   const hasTimes = DayPlannerPlanActionsHelper.itemHasScheduleTimes(item);

   assert.equal(hasTimes, true);
});


test('Test_ItemHasScheduleTimes_TestBlankEnd_ExpectFalse', () => {
   const item = {
      start_time: '10:00',
      end_time: '  ',
   };

   const hasTimes = DayPlannerPlanActionsHelper.itemHasScheduleTimes(item);

   assert.equal(hasTimes, false);
});


test('Test_CollectionHasScheduledItems_TestMixedItems_ExpectTrue', () => {
   const items = [
      { start_time: '', end_time: '' },
      { start_time: '11:00', end_time: '11:30' },
   ];

   const hasScheduled = DayPlannerPlanActionsHelper.collectionHasScheduledItems(items);

   assert.equal(hasScheduled, true);
   assert.equal(
      DayPlannerPlanActionsHelper.itemHasScheduleTimes(items.at(Position.SECOND)),
      true
   );
});


test('Test_CollectionHasScheduledItems_TestEmpty_ExpectFalse', () => {
   const items = [];

   const hasScheduled = DayPlannerPlanActionsHelper.collectionHasScheduledItems(items);

   assert.equal(hasScheduled, false);
});


test('Test_CollectionHasScheduledItems_TestNull_ExpectFalse', () => {
   const items = null;

   const hasScheduled = DayPlannerPlanActionsHelper.collectionHasScheduledItems(items);

   assert.equal(hasScheduled, false);
});
