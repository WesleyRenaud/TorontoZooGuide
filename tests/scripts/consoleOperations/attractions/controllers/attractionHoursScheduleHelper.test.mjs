import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionHoursScheduleHelper } from '../../../../../scripts/consoleOperations/attractions/controllers/attractionHoursScheduleHelper.js';

test('Test_TimePairIsOrdered_TestPairs_ExpectBoolean', () => {
   assert.equal(AttractionHoursScheduleHelper.timePairIsOrdered('09:00', '17:00'), true);
   assert.equal(AttractionHoursScheduleHelper.timePairIsOrdered('17:00', '09:00'), false);
   assert.equal(AttractionHoursScheduleHelper.timePairIsOrdered('bad', '17:00'), false);
});
