import assert from 'node:assert/strict';
import test from 'node:test';

import { WarningFixedTimeDraftFilter } from '../../../../scripts/itinerary/wizard/warningFixedTimeDraftFilter.js';
import { ItineraryItemFormatter } from '../../../../scripts/itinerary/panel/itineraryItemFormatter.js';


test('Test_FixedTimeOccurrenceKey_TestNameAndTime_ExpectKey', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   const name = 'Amur Tiger';
   const startTime = '11:00 AM';
   ItineraryItemFormatter.formatClockTime = () => startTime;

   try {
      const key = WarningFixedTimeDraftFilter.fixedTimeOccurrenceKey({
         name,
         start_time: startTime,
      });

      assert.equal(key, `${name.toLowerCase()}${String.fromCharCode(0)}${startTime}`);
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});


test('Test_FixedTimeOccurrenceKey_TestEmptyName_ExpectEmpty', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   const startTime = '11:00 AM';
   ItineraryItemFormatter.formatClockTime = () => startTime;

   try {
      const key = WarningFixedTimeDraftFilter.fixedTimeOccurrenceKey({ name: '' });

      assert.equal(key, '');
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});


test('Test_FixedTimeOccurrenceKey_TestMissingTime_ExpectNameKey', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   ItineraryItemFormatter.formatClockTime = () => '';
   const name = 'Lion Talk';

   try {
      const key = WarningFixedTimeDraftFilter.fixedTimeOccurrenceKey({ name });

      assert.equal(key, `name:${name.toLowerCase()}`);
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});


test('Test_RejectedOccurrenceKeys_TestFilter_ExpectRejected', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   const startTime = '1:00 PM';
   const name = 'Masai Giraffe';
   ItineraryItemFormatter.formatClockTime = () => startTime;
   const items = [
      { name, start_time: startTime, item_type: 'wild' },
      { name: 'Skip', item_type: 'other' },
   ];

   try {
      const rejected = WarningFixedTimeDraftFilter.rejectedOccurrenceKeys(
         items,
         (item) => item.item_type === 'wild'
      );

      assert.equal(rejected.has(`${name.toLowerCase()}${String.fromCharCode(0)}${startTime}`), true);
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});


test('Test_KeepDraftItem_TestRejected_ExpectFalse', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   const startTime = '1:00 PM';
   const name = 'Masai Giraffe';
   ItineraryItemFormatter.formatClockTime = () => startTime;
   const items = [
      { name, start_time: startTime, item_type: 'wild' },
      { name: 'Skip', item_type: 'other' },
   ];

   try {
      const rejected = WarningFixedTimeDraftFilter.rejectedOccurrenceKeys(
         items,
         (item) => item.item_type === 'wild'
      );
      const keep = WarningFixedTimeDraftFilter.keepDraftItem(
         { name, start_time: startTime },
         rejected
      );

      assert.equal(keep, false);
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});


test('Test_KeepDraftItem_TestOtherTalk_ExpectTrue', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   const startTime = '1:00 PM';
   const name = 'Masai Giraffe';
   ItineraryItemFormatter.formatClockTime = () => startTime;
   const items = [
      { name, start_time: startTime, item_type: 'wild' },
      { name: 'Skip', item_type: 'other' },
   ];

   try {
      const rejected = WarningFixedTimeDraftFilter.rejectedOccurrenceKeys(
         items,
         (item) => item.item_type === 'wild'
      );
      const keep = WarningFixedTimeDraftFilter.keepDraftItem(
         { name: 'Other Talk' },
         rejected
      );

      assert.equal(keep, true);
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});
