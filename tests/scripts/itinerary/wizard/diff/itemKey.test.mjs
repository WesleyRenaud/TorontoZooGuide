import assert from 'node:assert/strict';
import test from 'node:test';

import { ItemKey } from '../../../../../scripts/itinerary/wizard/diff/itemKey.js';


test('Test_BuildItemKey_TestName_ExpectLowerTrimmed', () => {
   const name = 'Conservation Carousel';
   const field = 'name';
   const item = { [field]: `  ${name}  ` };

   const key = ItemKey.buildItemKey(item, field);

   assert.equal(key, name.toLowerCase());
});


test('Test_BuildItemKey_TestMissingField_ExpectEmpty', () => {
   const item = {};
   const field = 'name';

   const key = ItemKey.buildItemKey(item, field);

   assert.equal(key, '');
});
