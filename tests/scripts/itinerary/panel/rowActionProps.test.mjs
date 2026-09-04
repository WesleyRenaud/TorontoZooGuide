import assert from 'node:assert/strict';
import { test } from 'node:test';

import { RowActionProps } from '../../../../scripts/itinerary/panel/rowActionProps.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';

test('Test_CanShowItineraryItemScheduleControls_TestHidesScheduleForPureTransportations_ExpectOk', () => {
   assert.equal(
      RowActionProps.canShowItineraryItemScheduleControls(
         ScheduleItemKind.TRANSPORTATION.itemType,
         { name: 'Zoomobile', added_as_attraction: false }
      ),
      false
   );
});

test('Test_CanShowItineraryItemScheduleControls_TestAllowsScheduleForAddedAsAttractionTransportations_ExpectOk', () => {
   assert.equal(
      RowActionProps.canShowItineraryItemScheduleControls(
         ScheduleItemKind.TRANSPORTATION.itemType,
         { name: 'Zoomobile', added_as_attraction: true }
      ),
      true
   );
});

test('Test_CanShowItineraryItemScheduleControls_TestAllowsScheduleForNonTransportationItems_ExpectOk', () => {
   assert.equal(
      RowActionProps.canShowItineraryItemScheduleControls(
         ScheduleItemKind.ANIMAL.itemType,
         { species: 'Giant Panda' }
      ),
      true
   );
   assert.equal(
      RowActionProps.canShowItineraryItemScheduleControls(
         ScheduleItemKind.ATTRACTION.itemType,
         { name: 'Conservation Carousel' }
      ),
      true
   );
});

test('Test_BuildUnscheduleRowProps_TestHidesUnscheduleForPureTransportations_ExpectOk', () => {
   assert.deepEqual(
      RowActionProps.buildUnscheduleRowProps(
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

test('Test_BuildUnscheduleRowProps_TestAllowsUnscheduleForAddedAsAttractionTransportations_ExpectOk', () => {
   const props = RowActionProps.buildUnscheduleRowProps(
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
