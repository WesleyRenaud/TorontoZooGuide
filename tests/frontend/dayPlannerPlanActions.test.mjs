import assert from 'node:assert/strict';
import { test } from 'node:test';

import { hasScheduledItineraryItems } from '../../scripts/itinerary/panel/dayPlannerPlanActions.js';

test('hasScheduledItineraryItems detects scheduled rows across collections', () => {
   assert.equal(hasScheduledItineraryItems({}), false);
   assert.equal(
      hasScheduledItineraryItems({
         animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
      }),
      false
   );
   assert.equal(
      hasScheduledItineraryItems({
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
      hasScheduledItineraryItems({
         events: [{
            event_type: 'lunch',
            start_time: '12:00',
            end_time: '12:30',
         }],
      }),
      true
   );
   assert.equal(
      hasScheduledItineraryItems({
         transportations: [{
            name: 'Zoomobile',
            start_time: '11:00',
            end_time: '11:20',
         }],
      }),
      true
   );
});
