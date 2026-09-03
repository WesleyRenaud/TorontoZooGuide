import assert from 'node:assert/strict';
import test from 'node:test';

import { MapOccurrenceTimesFormatter } from '../../../scripts/tooltips/mapOccurrenceTimesFormatter.js';

test('Test_Format_TestJoinedTimes_ExpectCommaSeparated', () => {
   assert.equal(
      MapOccurrenceTimesFormatter.format({
         times: ['11:00 AM', '2:00 PM'],
         start_time: '11:00 AM',
      }),
      '11:00 AM, 2:00 PM'
   );
});

test('Test_Format_TestMissingTimes_ExpectStartTimeFallback', () => {
   assert.equal(
      MapOccurrenceTimesFormatter.format({
         start_time: '11:00 AM',
      }),
      '11:00 AM'
   );
});

test('Test_Format_TestEmptyItem_ExpectEmptyString', () => {
   assert.equal(MapOccurrenceTimesFormatter.format({}), '');
});
