import assert from 'node:assert/strict';
import test from 'node:test';

import { JoinedTimesFormatter } from '../../../scripts/shared/joinedTimesFormatter.js';
import { MapOccurrenceTimesFormatter } from '../../../scripts/tooltips/mapOccurrenceTimesFormatter.js';


test('Test_Format_TestJoinedTimes_ExpectCommaSeparated', () => {
   const morning = '11:00 AM';
   const afternoon = '2:00 PM';
   const item = {
      times: [morning, afternoon],
      start_time: morning,
   };

   const formatted = MapOccurrenceTimesFormatter.format(item);

   assert.equal(formatted, JoinedTimesFormatter.format(item.times));
});


test('Test_Format_TestMissingTimes_ExpectStartTimeFallback', () => {
   const startTime = '11:00 AM';
   const item = { start_time: startTime };

   const formatted = MapOccurrenceTimesFormatter.format(item);

   assert.equal(formatted, startTime);
});


test('Test_Format_TestEmptyItem_ExpectEmptyString', () => {
   const item = {};

   const formatted = MapOccurrenceTimesFormatter.format(item);

   assert.equal(formatted, '');
});
