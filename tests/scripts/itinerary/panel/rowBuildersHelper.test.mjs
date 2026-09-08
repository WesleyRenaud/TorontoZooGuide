import assert from 'node:assert/strict';
import test from 'node:test';

import { RowBuildersHelper } from '../../../../scripts/itinerary/panel/rowBuildersHelper.js';

test('Test_NormalizeItems_TestMapper_ExpectMapped', () => {
   assert.deepEqual(
      RowBuildersHelper.normalizeItems(['a', 'b'], (item) => item.toUpperCase()),
      ['A', 'B']
   );
});

test('Test_MaxStoredLikelihood_TestValues_ExpectMaxOrNull', () => {
   assert.equal(RowBuildersHelper.maxStoredLikelihood(1, '', 4, null), 4);
   assert.equal(RowBuildersHelper.maxStoredLikelihood(null, ''), null);
});
