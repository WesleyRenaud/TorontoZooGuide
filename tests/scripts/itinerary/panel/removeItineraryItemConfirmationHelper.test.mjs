import assert from 'node:assert/strict';
import test from 'node:test';

import { RemoveItineraryItemConfirmationHelper } from '../../../../scripts/itinerary/panel/removeItineraryItemConfirmationHelper.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_IsTransitModeTransportationRemove_TestKeys_ExpectBoolean', () => {
   assert.equal(
      RemoveItineraryItemConfirmationHelper.isTransitModeTransportationRemove(
         ScheduleItemKind.TRANSPORTATION.itemType,
         'Zoomobile||0'
      ),
      true
   );
   assert.equal(
      RemoveItineraryItemConfirmationHelper.isTransitModeTransportationRemove(
         ScheduleItemKind.TRANSPORTATION.itemType,
         'Zoomobile||1'
      ),
      false
   );
   assert.equal(
      RemoveItineraryItemConfirmationHelper.isTransitModeTransportationRemove(
         ScheduleItemKind.ATTRACTION.itemType,
         'Zoomobile||0'
      ),
      false
   );
});

test('Test_RemoveConfirmationMessage_TestTransitAndDefault_ExpectStrings', () => {
   assert.equal(
      RemoveItineraryItemConfirmationHelper.removeConfirmationMessage(
         ScheduleItemKind.TRANSPORTATION.itemType,
         'Zoomobile||0'
      ),
      Strings.itinerary.confirmation.removeTransitTransportationMessage
   );
   assert.equal(
      RemoveItineraryItemConfirmationHelper.removeConfirmationMessage(
         ScheduleItemKind.ATTRACTION.itemType,
         'Carousel'
      ),
      Strings.itinerary.confirmation.removeItemMessage
   );
});
