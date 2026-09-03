import assert from 'node:assert/strict';
import test from 'node:test';

import { updateItineraryAdjustmentTypesFromConfig } from '../../scripts/itinerary/itineraryAdjustmentTypes.js';
import { buildAdjustmentRowSpec } from '../../scripts/itinerary/panel/components/removedItemsPopupAdjustmentSpecs.js';
import { APP_STRINGS } from '../../scripts/strings.js';

const ADJUSTMENT_TYPES = {
   ARRIVAL_TIME_ADJUSTED: 'arrivalTimeAdjusted',
   DEPARTURE_TIME_ADJUSTED: 'departureTimeAdjusted',
};

test('buildAdjustmentRowSpec maps arrival adjustments to item row content', () => {
   updateItineraryAdjustmentTypesFromConfig({
      adjustmentTypes: ADJUSTMENT_TYPES,
   });

   assert.deepEqual(
      buildAdjustmentRowSpec({
         type: 'arrivalTimeAdjusted',
         previousValue: '09:00',
         value: '09:30',
      }),
      {
         name: APP_STRINGS.itinerary.dayPlanner.arrivalLabel,
         alertLine: APP_STRINGS.itinerary.removedItems.arrivalAdjusted(
            '9:00 AM',
            '9:30 AM'
         ),
      }
   );
});

test('buildAdjustmentRowSpec maps departure adjustments to item row content', () => {
   updateItineraryAdjustmentTypesFromConfig({
      adjustmentTypes: ADJUSTMENT_TYPES,
   });

   assert.deepEqual(
      buildAdjustmentRowSpec({
         type: 'departureTimeAdjusted',
         previousValue: '18:30',
         value: '18:00',
      }),
      {
         name: APP_STRINGS.labels.departure,
         alertLine: APP_STRINGS.itinerary.removedItems.departureAdjusted(
            '6:30 PM',
            '6:00 PM'
         ),
      }
   );
});

test('buildAdjustmentRowSpec ignores unknown or incomplete adjustments', () => {
   updateItineraryAdjustmentTypesFromConfig({
      adjustmentTypes: ADJUSTMENT_TYPES,
   });

   assert.equal(
      buildAdjustmentRowSpec({
         type: 'arrivalTimeAdjusted',
         previousValue: '',
         value: '09:30',
      }),
      null
   );
   assert.equal(
      buildAdjustmentRowSpec({
         type: 'otherAdjustment',
         previousValue: '09:00',
         value: '09:30',
      }),
      null
   );
});
