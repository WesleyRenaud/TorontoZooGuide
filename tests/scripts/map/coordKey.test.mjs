import assert from 'node:assert/strict';
import test from 'node:test';

import { CoordKey } from '../../../scripts/map/coordKey.js';


test('Test_CoordKey_TestNumericCoords_ExpectFixedKey', () => {
   const x = 1.23456;
   const y = 7.8;

   const key = CoordKey.coordKey(x, y);

   assert.equal(key, `${x.toFixed(4)}|${y.toFixed(4)}`);
});


test('Test_CoordKey_TestNumericStrings_ExpectFixedKey', () => {
   const x = '2';
   const y = '3.1';

   const key = CoordKey.coordKey(x, y);

   assert.equal(key, `${Number(x).toFixed(4)}|${Number(y).toFixed(4)}`);
});
