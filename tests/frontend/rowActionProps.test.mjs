import assert from 'node:assert/strict';
import { test } from 'node:test';

import { canShowItineraryItemScheduleAction } from '../../scripts/itinerary/panel/rowActionProps.js';
import { ScheduleItemKind } from '../../scripts/shared/enums/scheduleItemKind.js';

test('canShowItineraryItemScheduleAction hides schedule for pure transportations', () => {
   assert.equal(
      canShowItineraryItemScheduleAction(
         ScheduleItemKind.TRANSPORTATION.itemType,
         { name: 'Zoomobile', added_as_attraction: false }
      ),
      false
   );
});

test('canShowItineraryItemScheduleAction allows schedule for added-as-attraction transportations', () => {
   assert.equal(
      canShowItineraryItemScheduleAction(
         ScheduleItemKind.TRANSPORTATION.itemType,
         { name: 'Zoomobile', added_as_attraction: true }
      ),
      true
   );
});

test('canShowItineraryItemScheduleAction allows schedule for non-transportation items', () => {
   assert.equal(
      canShowItineraryItemScheduleAction(
         ScheduleItemKind.ANIMAL.itemType,
         { species: 'Giant Panda' }
      ),
      true
   );
   assert.equal(
      canShowItineraryItemScheduleAction(
         ScheduleItemKind.ATTRACTION.itemType,
         { name: 'Conservation Carousel' }
      ),
      true
   );
});
