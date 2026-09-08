import assert from 'node:assert/strict';
import test from 'node:test';

import { CoordKey } from '../../../scripts/map/coordKey.js';

test('Test_CoordKey_TestNumericCoords_ExpectFixedKey', () => {
   assert.equal(CoordKey.coordKey(1.23456, 7.8), '1.2346|7.8000');
   assert.equal(CoordKey.coordKey('2', '3.1'), '2.0000|3.1000');
});
