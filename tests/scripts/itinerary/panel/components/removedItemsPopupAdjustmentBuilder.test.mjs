import assert from 'node:assert/strict';
import test from 'node:test';

import { RemovedItemsPopupAdjustmentBuilder } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupAdjustmentBuilder.js';
import { ItineraryItemFormatter } from '../../../../../scripts/itinerary/panel/itineraryItemFormatter.js';
import { ItineraryAdjustmentType } from '../../../../../scripts/shared/enums/itineraryAdjustmentType.js';
import { Strings } from '../../../../../scripts/strings.js';


test('Test_BuildAdjustmentRowSpec_TestArrivalAdjusted_ExpectItemRowContent', () => {
   const previousValue = '09:00';
   const value = '09:30';
   const adjustment = {
      type: ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED,
      previousValue,
      value,
   };

   const spec = RemovedItemsPopupAdjustmentBuilder.buildAdjustmentRowSpec(adjustment);

   assert.deepEqual(spec, {
      name: Strings.itinerary.dayPlanner.arrivalLabel,
      alertLine: Strings.itinerary.removedItems.arrivalAdjusted(
         ItineraryItemFormatter.formatClockTime(previousValue),
         ItineraryItemFormatter.formatClockTime(value)
      ),
   });
});


test('Test_BuildAdjustmentRowSpec_TestDepartureAdjusted_ExpectItemRowContent', () => {
   const previousValue = '18:30';
   const value = '18:00';
   const adjustment = {
      type: ItineraryAdjustmentType.DEPARTURE_TIME_ADJUSTED,
      previousValue,
      value,
   };

   const spec = RemovedItemsPopupAdjustmentBuilder.buildAdjustmentRowSpec(adjustment);

   assert.deepEqual(spec, {
      name: Strings.labels.departure,
      alertLine: Strings.itinerary.removedItems.departureAdjusted(
         ItineraryItemFormatter.formatClockTime(previousValue),
         ItineraryItemFormatter.formatClockTime(value)
      ),
   });
});


test('Test_BuildAdjustmentRowSpec_TestIncompleteArrival_ExpectNull', () => {
   const adjustment = {
      type: ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED,
      previousValue: '',
      value: '09:30',
   };

   const spec = RemovedItemsPopupAdjustmentBuilder.buildAdjustmentRowSpec(adjustment);

   assert.equal(spec, null);
});


test('Test_BuildAdjustmentRowSpec_TestUnknownType_ExpectNull', () => {
   const adjustment = {
      type: 'otherAdjustment',
      previousValue: '09:00',
      value: '09:30',
   };

   const spec = RemovedItemsPopupAdjustmentBuilder.buildAdjustmentRowSpec(adjustment);

   assert.equal(spec, null);
});
