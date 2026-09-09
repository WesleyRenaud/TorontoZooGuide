import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleItemKeySeparator } from '../../../scripts/itinerary/scheduleItemKeySeparator.js';

test('Test_Value_TestSeparator_ExpectDoublePipe', () => {
   assert.equal(ScheduleItemKeySeparator.VALUE, '||');
});
