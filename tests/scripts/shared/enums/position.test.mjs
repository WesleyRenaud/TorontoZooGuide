import assert from 'node:assert/strict';
import test from 'node:test';

import { Position } from '../../../../scripts/shared/enums/position.js';

test('Test_Position_TestStaticFields_ExpectIndexValues', () => {
   assert.equal(Position.FIRST, 0);
   assert.equal(Position.SECOND, 1);
   assert.equal(Position.THIRD, 2);
   assert.equal(Position.LAST, -1);
});
