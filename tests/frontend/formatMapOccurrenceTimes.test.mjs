import assert from 'node:assert/strict';
import test from 'node:test';

import { formatMapOccurrenceTimes } from '../../scripts/tooltips/formatMapOccurrenceTimes.js';

test('formatMapOccurrenceTimes joins times and falls back to start_time', () => {
   assert.equal(
      formatMapOccurrenceTimes({
         times: ['11:00 AM', '2:00 PM'],
         start_time: '11:00 AM',
      }),
      '11:00 AM, 2:00 PM'
   );
   assert.equal(
      formatMapOccurrenceTimes({
         start_time: '11:00 AM',
      }),
      '11:00 AM'
   );
   assert.equal(formatMapOccurrenceTimes({}), '');
});
