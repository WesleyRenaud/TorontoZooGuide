import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryAdjustmentTypes } from '../../../../../scripts/itinerary/itineraryAdjustmentTypes.js';
import { RemovedItemsPopupAdjustmentSpecs } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupAdjustmentSpecs.js';
import { Strings } from '../../../../../scripts/strings.js';

const ADJUSTMENT_TYPES = {
   ARRIVAL_TIME_ADJUSTED: 'arrivalTimeAdjusted',
   DEPARTURE_TIME_ADJUSTED: 'departureTimeAdjusted',
};

test('Test_BuildAdjustmentRowSpec_TestMapsArrivalAdjustmentsToItemRowContent_ExpectOk', () => {
   ItineraryAdjustmentTypes.updateItineraryAdjustmentTypesFromConfig({
      adjustmentTypes: ADJUSTMENT_TYPES,
   });

   assert.deepEqual(
      RemovedItemsPopupAdjustmentSpecs.buildAdjustmentRowSpec({
         type: 'arrivalTimeAdjusted',
         previousValue: '09:00',
         value: '09:30',
      }),
      {
         name: Strings.itinerary.dayPlanner.arrivalLabel,
         alertLine: Strings.itinerary.removedItems.arrivalAdjusted(
            '9:00 AM',
            '9:30 AM'
         ),
      }
   );
});

test('Test_BuildAdjustmentRowSpec_TestMapsDepartureAdjustmentsToItemRowContent_ExpectOk', () => {
   ItineraryAdjustmentTypes.updateItineraryAdjustmentTypesFromConfig({
      adjustmentTypes: ADJUSTMENT_TYPES,
   });

   assert.deepEqual(
      RemovedItemsPopupAdjustmentSpecs.buildAdjustmentRowSpec({
         type: 'departureTimeAdjusted',
         previousValue: '18:30',
         value: '18:00',
      }),
      {
         name: Strings.labels.departure,
         alertLine: Strings.itinerary.removedItems.departureAdjusted(
            '6:30 PM',
            '6:00 PM'
         ),
      }
   );
});

test('Test_BuildAdjustmentRowSpec_TestIgnoresUnknownOrIncompleteAdjustments_ExpectOk', () => {
   ItineraryAdjustmentTypes.updateItineraryAdjustmentTypesFromConfig({
      adjustmentTypes: ADJUSTMENT_TYPES,
   });

   assert.equal(
      RemovedItemsPopupAdjustmentSpecs.buildAdjustmentRowSpec({
         type: 'arrivalTimeAdjusted',
         previousValue: '',
         value: '09:30',
      }),
      null
   );
   assert.equal(
      RemovedItemsPopupAdjustmentSpecs.buildAdjustmentRowSpec({
         type: 'otherAdjustment',
         previousValue: '09:00',
         value: '09:30',
      }),
      null
   );
});
