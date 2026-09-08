import assert from 'node:assert/strict';
import test from 'node:test';

import { RowPresentationHelper } from '../../../../scripts/itinerary/panel/rowPresentationHelper.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_BuildTimeFieldLine_TestValueAndBlank_ExpectLine', () => {
   assert.equal(RowPresentationHelper.buildTimeFieldLine(''), '');
   assert.equal(
      RowPresentationHelper.buildTimeFieldLine('1:00 PM'),
      `${Strings.labels.time}: 1:00 PM`
   );
});
