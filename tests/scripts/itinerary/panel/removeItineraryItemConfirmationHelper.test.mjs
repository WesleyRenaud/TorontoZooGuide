import assert from 'node:assert/strict';
import test from 'node:test';

import { RemoveItineraryItemConfirmationHelper } from '../../../../scripts/itinerary/panel/removeItineraryItemConfirmationHelper.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import { Strings } from '../../../../scripts/strings.js';
import { TransportationScheduleItemKey } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationScheduleItemKey.js';

test('Test_IsTransitModeTransportationRemove_TestKeys_ExpectBoolean', () => {
   assert.equal(
      RemoveItineraryItemConfirmationHelper.isTransitModeTransportationRemove(
         ScheduleItemKind.TRANSPORTATION.itemType,
         new TransportationScheduleItemKey('Zoomobile', false).toWire()
      ),
      true
   );
   assert.equal(
      RemoveItineraryItemConfirmationHelper.isTransitModeTransportationRemove(
         ScheduleItemKind.TRANSPORTATION.itemType,
         new TransportationScheduleItemKey('Zoomobile', true).toWire()
      ),
      false
   );
   assert.equal(
      RemoveItineraryItemConfirmationHelper.isTransitModeTransportationRemove(
         ScheduleItemKind.ATTRACTION.itemType,
         new TransportationScheduleItemKey('Zoomobile', false).toWire()
      ),
      false
   );
});

test('Test_RemoveConfirmationMessage_TestTransitAndDefault_ExpectStrings', () => {
   assert.equal(
      RemoveItineraryItemConfirmationHelper.removeConfirmationMessage(
         ScheduleItemKind.TRANSPORTATION.itemType,
         new TransportationScheduleItemKey('Zoomobile', false).toWire()
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
