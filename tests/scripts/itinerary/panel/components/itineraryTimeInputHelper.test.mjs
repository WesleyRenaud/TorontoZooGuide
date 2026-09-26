import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryTimeInputHelper } from '../../../../../scripts/itinerary/panel/components/itineraryTimeInputHelper.js';
import { ItineraryItemFormatter } from '../../../../../scripts/itinerary/panel/itineraryItemFormatter.js';


test('Test_ReadPickerTimeValue_TestDateString_ExpectFormattedClock', () => {
   const dateStr = '13:05';
   const inputEl = { value: '' };

   const clockTime = ItineraryTimeInputHelper.readPickerTimeValue(null, dateStr, inputEl);

   assert.equal(clockTime, ItineraryItemFormatter.formatClockTime(dateStr));
});


test('Test_ReadPickerTimeValue_TestInstanceInput_ExpectFormattedClock', () => {
   const instanceValue = '09:00';
   const instance = { input: { value: instanceValue } };
   const inputEl = { value: '10:00' };

   const clockTime = ItineraryTimeInputHelper.readPickerTimeValue(instance, '', inputEl);

   assert.equal(clockTime, ItineraryItemFormatter.formatClockTime(instanceValue));
});


test('Test_ReadPickerTimeValue_TestInputElement_ExpectFormattedClock', () => {
   const inputValue = '16:30';
   const inputEl = { value: inputValue };

   const clockTime = ItineraryTimeInputHelper.readPickerTimeValue(null, '', inputEl);

   assert.equal(clockTime, ItineraryItemFormatter.formatClockTime(inputValue));
});
