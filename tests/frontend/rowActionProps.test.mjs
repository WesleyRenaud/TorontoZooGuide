import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   buildUnscheduleRowProps,
   canShowItineraryItemScheduleControls,
} from '../../scripts/itinerary/panel/rowActionProps.js';
import { ScheduleItemKind } from '../../scripts/shared/enums/scheduleItemKind.js';

test('canShowItineraryItemScheduleControls hides schedule for pure transportations', () => {
   assert.equal(
      canShowItineraryItemScheduleControls(
         ScheduleItemKind.TRANSPORTATION.itemType,
         { name: 'Zoomobile', added_as_attraction: false }
      ),
      false
   );
});

test('canShowItineraryItemScheduleControls allows schedule for added-as-attraction transportations', () => {
   assert.equal(
      canShowItineraryItemScheduleControls(
         ScheduleItemKind.TRANSPORTATION.itemType,
         { name: 'Zoomobile', added_as_attraction: true }
      ),
      true
   );
});

test('canShowItineraryItemScheduleControls allows schedule for non-transportation items', () => {
   assert.equal(
      canShowItineraryItemScheduleControls(
         ScheduleItemKind.ANIMAL.itemType,
         { species: 'Giant Panda' }
      ),
      true
   );
   assert.equal(
      canShowItineraryItemScheduleControls(
         ScheduleItemKind.ATTRACTION.itemType,
         { name: 'Conservation Carousel' }
      ),
      true
   );
});

test('buildUnscheduleRowProps hides unschedule for pure transportations', () => {
   assert.deepEqual(
      buildUnscheduleRowProps(
         ScheduleItemKind.TRANSPORTATION.itemType,
         {
            name: 'Zoomobile',
            added_as_attraction: false,
            start_time: '2:30 PM',
            end_time: '3:00 PM',
         },
         () => {}
      ),
      {}
   );
});

test('buildUnscheduleRowProps allows unschedule for added-as-attraction transportations', () => {
   const props = buildUnscheduleRowProps(
      ScheduleItemKind.TRANSPORTATION.itemType,
      {
         name: 'Zoomobile',
         added_as_attraction: true,
         start_time: '2:30 PM',
         end_time: '3:00 PM',
      },
      () => {}
   );

   assert.equal(props.actionLabel, 'Unschedule');
   assert.equal(typeof props.onAction, 'function');
});
