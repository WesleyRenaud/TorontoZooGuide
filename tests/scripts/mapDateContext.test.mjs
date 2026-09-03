import assert from 'node:assert/strict';
import test from 'node:test';

import { buildMapDateContext } from '../../scripts/map/dateContext.js';

test('preset map context takes year from anchor ISO (same extraction as visit date)', async () => {
   const ctx = await buildMapDateContext('summer', '2031-12-15');

   assert.equal(ctx.preset, 'summer');
   assert.equal(ctx.month, 'JUL');
   assert.equal(ctx.day, 20);
   assert.equal(ctx.year, 2031);
});
