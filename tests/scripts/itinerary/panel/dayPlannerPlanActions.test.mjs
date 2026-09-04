import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DayPlannerPlanActions } from '../../../../scripts/itinerary/panel/dayPlannerPlanActions.js';

test('Test_HasScheduledItineraryItems_TestCollections_ExpectDetected', () => {
   assert.equal(DayPlannerPlanActions.hasScheduledItineraryItems({}), false);
   assert.equal(
      DayPlannerPlanActions.hasScheduledItineraryItems({
         animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
      }),
      false
   );
   assert.equal(
      DayPlannerPlanActions.hasScheduledItineraryItems({
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
      DayPlannerPlanActions.hasScheduledItineraryItems({
         events: [{
            event_type: 'lunch',
            start_time: '12:00',
            end_time: '12:30',
         }],
      }),
      true
   );
   assert.equal(
      DayPlannerPlanActions.hasScheduledItineraryItems({
         transportations: [{
            name: 'Zoomobile',
            start_time: '11:00',
            end_time: '11:20',
         }],
      }),
      true
   );
});
