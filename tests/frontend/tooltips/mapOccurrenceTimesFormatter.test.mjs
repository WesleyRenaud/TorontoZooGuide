import assert from 'node:assert/strict';
import test from 'node:test';

import { MapOccurrenceTimesFormatter } from '../../../scripts/tooltips/mapOccurrenceTimesFormatter.js';

test('MapOccurrenceTimesFormatter.format joins times and falls back to start_time', () => {
   assert.equal(
      MapOccurrenceTimesFormatter.format({
         times: ['11:00 AM', '2:00 PM'],
         start_time: '11:00 AM',
      }),
      '11:00 AM, 2:00 PM'
   );
   assert.equal(
      MapOccurrenceTimesFormatter.format({
         start_time: '11:00 AM',
      }),
      '11:00 AM'
   );
   assert.equal(MapOccurrenceTimesFormatter.format({}), '');
});
