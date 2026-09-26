import assert from 'node:assert/strict';
import test from 'node:test';

import { RemoveItineraryItemConfirmationHelper } from '../../../../scripts/itinerary/panel/removeItineraryItemConfirmationHelper.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import { Strings } from '../../../../scripts/strings.js';
import { TransportationScheduleItemKey } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationScheduleItemKey.js';


test('Test_IsTransitModeTransportationRemove_TestTransitKey_ExpectTrue', () => {
   const itemType = ScheduleItemKind.TRANSPORTATION.itemType;
   const key = new TransportationScheduleItemKey('Zoomobile', false).toWire();

   const isTransit = RemoveItineraryItemConfirmationHelper.isTransitModeTransportationRemove(
      itemType,
      key
   );

   assert.equal(isTransit, true);
});


test('Test_IsTransitModeTransportationRemove_TestAttractionKey_ExpectFalse', () => {
   const itemType = ScheduleItemKind.TRANSPORTATION.itemType;
   const key = new TransportationScheduleItemKey('Zoomobile', true).toWire();

   const isTransit = RemoveItineraryItemConfirmationHelper.isTransitModeTransportationRemove(
      itemType,
      key
   );

   assert.equal(isTransit, false);
});


test('Test_IsTransitModeTransportationRemove_TestAttractionType_ExpectFalse', () => {
   const itemType = ScheduleItemKind.ATTRACTION.itemType;
   const key = new TransportationScheduleItemKey('Zoomobile', false).toWire();

   const isTransit = RemoveItineraryItemConfirmationHelper.isTransitModeTransportationRemove(
      itemType,
      key
   );

   assert.equal(isTransit, false);
});


test('Test_RemoveConfirmationMessage_TestTransit_ExpectTransitMessage', () => {
   const itemType = ScheduleItemKind.TRANSPORTATION.itemType;
   const key = new TransportationScheduleItemKey('Zoomobile', false).toWire();

   const message = RemoveItineraryItemConfirmationHelper.removeConfirmationMessage(itemType, key);

   assert.equal(message, Strings.itinerary.confirmation.removeTransitTransportationMessage);
});


test('Test_RemoveConfirmationMessage_TestAttraction_ExpectDefaultMessage', () => {
   const itemType = ScheduleItemKind.ATTRACTION.itemType;
   const key = 'Conservation Carousel';

   const message = RemoveItineraryItemConfirmationHelper.removeConfirmationMessage(itemType, key);

   assert.equal(message, Strings.itinerary.confirmation.removeItemMessage);
});
