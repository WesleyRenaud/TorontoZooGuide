import assert from 'node:assert/strict';
import test from 'node:test';

import { NamedItems } from '../../../../scripts/consoleOperations/options/namedItems.js';


test('Test_GetOptionItemName_TestString_ExpectName', () => {
   const name = 'Carousel';

   const optionName = NamedItems.getOptionItemName(name);

   assert.equal(optionName, name);
});


test('Test_GetOptionItemName_TestObject_ExpectName', () => {
   const name = 'Zoomobile';
   const item = { name };

   const optionName = NamedItems.getOptionItemName(item);

   assert.equal(optionName, name);
});


test('Test_SortNamedOptions_TestUnsorted_ExpectSorted', () => {
   const lion = { name: 'Lion' };
   const tiger = { name: 'Tiger' };
   const items = [tiger, lion];

   const sorted = NamedItems.sortNamedOptions(items);

   assert.deepEqual(sorted, [lion, tiger]);
});
