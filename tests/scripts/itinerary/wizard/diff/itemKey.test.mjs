import assert from 'node:assert/strict';
import test from 'node:test';

import { ItemKey } from '../../../../../scripts/itinerary/wizard/diff/itemKey.js';

test('Test_BuildItemKey_TestField_ExpectLowerTrimmed', () => {
   assert.equal(
      ItemKey.buildItemKey({ name: '  Conservation Carousel  ' }, 'name'),
      'conservation carousel'
   );
   assert.equal(ItemKey.buildItemKey({}, 'name'), '');
});
