import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DayPlannerPlanController } from '../../../../scripts/itinerary/panel/dayPlannerPlanController.js';

test('Test_HasScheduledItineraryItems_TestCollections_ExpectDetected', () => {
   assert.equal(DayPlannerPlanController.hasScheduledItineraryItems({}), false);
   assert.equal(
      DayPlannerPlanController.hasScheduledItineraryItems({
         animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
      }),
      false
   );
   assert.equal(
      DayPlannerPlanController.hasScheduledItineraryItems({
         animals: [{
            species: 'Tiger',
            exhibit: 'Savanna',
            start_time: '10:00',
            end_time: '10:30',
         }],
      }),
      true
   );
   assert.equal(
      DayPlannerPlanController.hasScheduledItineraryItems({
         events: [{
            event_type: 'lunch',
            start_time: '12:00',
            end_time: '12:30',
         }],
      }),
      true
   );
   assert.equal(
      DayPlannerPlanController.hasScheduledItineraryItems({
         transportations: [{
            name: 'Zoomobile',
            start_time: '11:00',
            end_time: '11:20',
         }],
      }),
      true
   );
});
