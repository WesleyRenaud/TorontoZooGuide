import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryTimeInputHelper } from '../../../../../scripts/itinerary/panel/components/itineraryTimeInputHelper.js';

test('Test_ReadPickerTimeValue_TestSources_ExpectFormattedClock', () => {
   assert.equal(
      ItineraryTimeInputHelper.readPickerTimeValue(null, '13:05', { value: '' }),
      '1:05 PM'
   );
   assert.equal(
      ItineraryTimeInputHelper.readPickerTimeValue(
         { input: { value: '09:00' } },
         '',
         { value: '10:00' }
      ),
      '9:00 AM'
   );
   assert.equal(
      ItineraryTimeInputHelper.readPickerTimeValue(null, '', { value: '16:30' }),
      '4:30 PM'
   );
});
