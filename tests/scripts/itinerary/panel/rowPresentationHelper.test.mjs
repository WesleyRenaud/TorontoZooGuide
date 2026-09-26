import assert from 'node:assert/strict';
import test from 'node:test';

import { RowPresentationHelper } from '../../../../scripts/itinerary/panel/rowPresentationHelper.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_BuildTimeFieldLine_TestBlank_ExpectEmpty', () => {
   const value = '';

   const line = RowPresentationHelper.buildTimeFieldLine(value);

   assert.equal(line, value);
});


test('Test_BuildTimeFieldLine_TestClockTime_ExpectLabeled', () => {
   const clockTime = '1:00 PM';

   const line = RowPresentationHelper.buildTimeFieldLine(clockTime);

   assert.equal(line, Strings.format.labeledValue(Strings.labels.time, clockTime));
});
