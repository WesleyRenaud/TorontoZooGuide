import assert from 'node:assert/strict';
import test from 'node:test';

import { WarningFixedTimeDraftFilter } from '../../../../scripts/itinerary/wizard/warningFixedTimeDraftFilter.js';
import { ItineraryItemFormatter } from '../../../../scripts/itinerary/panel/itineraryItemFormatter.js';

test('Test_FixedTimeOccurrenceKey_TestNameAndTime_ExpectKey', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   ItineraryItemFormatter.formatClockTime = () => '11:00 AM';

   try {
      assert.equal(
         WarningFixedTimeDraftFilter.fixedTimeOccurrenceKey({
            name: 'Amur Tiger',
            start_time: '11:00 AM',
         }),
         `amur tiger${String.fromCharCode(0)}11:00 AM`
      );
      assert.equal(WarningFixedTimeDraftFilter.fixedTimeOccurrenceKey({ name: '' }), '');
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});

test('Test_FixedTimeOccurrenceKey_TestMissingTime_ExpectNameKey', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   ItineraryItemFormatter.formatClockTime = () => '';

   try {
      assert.equal(
         WarningFixedTimeDraftFilter.fixedTimeOccurrenceKey({ name: 'Talk' }),
         'name:talk'
      );
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});

test('Test_RejectedOccurrenceKeysAndKeepDraftItem_TestFilter_ExpectBoolean', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   ItineraryItemFormatter.formatClockTime = () => '1:00 PM';

   try {
      const rejected = WarningFixedTimeDraftFilter.rejectedOccurrenceKeys(
         [
            { name: 'Giraffe', start_time: '1:00 PM', item_type: 'wild' },
            { name: 'Skip', item_type: 'other' },
         ],
         (item) => item.item_type === 'wild'
      );

      assert.equal(rejected.has(`giraffe${String.fromCharCode(0)}1:00 PM`), true);
      assert.equal(
         WarningFixedTimeDraftFilter.keepDraftItem({ name: 'Giraffe', start_time: '1:00 PM' }, rejected),
         false
      );
      assert.equal(
         WarningFixedTimeDraftFilter.keepDraftItem({ name: 'Other Talk' }, rejected),
         true
      );
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});
