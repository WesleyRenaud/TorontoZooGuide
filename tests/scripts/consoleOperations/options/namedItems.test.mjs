import assert from 'node:assert/strict';
import test from 'node:test';

import { NamedItems } from '../../../../scripts/consoleOperations/options/namedItems.js';

test('Test_GetOptionItemName_TestStringAndObject_ExpectName', () => {
   assert.equal(NamedItems.getOptionItemName('Carousel'), 'Carousel');
   assert.equal(NamedItems.getOptionItemName({ name: 'Zoomobile' }), 'Zoomobile');
});

test('Test_SortNamedOptions_TestUnsorted_ExpectSorted', () => {
   assert.deepEqual(
      NamedItems.sortNamedOptions([{ name: 'Tiger' }, { name: 'Lion' }]),
      [{ name: 'Lion' }, { name: 'Tiger' }]
   );
});
