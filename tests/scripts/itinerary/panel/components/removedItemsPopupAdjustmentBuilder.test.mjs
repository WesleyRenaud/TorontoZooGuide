import assert from 'node:assert/strict';
import test from 'node:test';

import { RemovedItemsPopupAdjustmentBuilder } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupAdjustmentBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_BuildAdjustmentRowSpec_TestMapsArrivalAdjustmentsToItemRowContent_ExpectOk', () => {
   assert.deepEqual(
      RemovedItemsPopupAdjustmentBuilder.buildAdjustmentRowSpec({
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
   assert.deepEqual(
      RemovedItemsPopupAdjustmentBuilder.buildAdjustmentRowSpec({
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
   assert.equal(
      RemovedItemsPopupAdjustmentBuilder.buildAdjustmentRowSpec({
         type: 'arrivalTimeAdjusted',
         previousValue: '',
         value: '09:30',
      }),
      null
   );
   assert.equal(
      RemovedItemsPopupAdjustmentBuilder.buildAdjustmentRowSpec({
         type: 'otherAdjustment',
         previousValue: '09:00',
         value: '09:30',
      }),
      null
   );
});
