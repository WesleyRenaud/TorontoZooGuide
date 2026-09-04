import assert from 'node:assert/strict';
import test from 'node:test';

import { DateContext } from '../../../scripts/map/dateContext.js';

test('Test_BuildMapDateContext_TestSummerAnchor_ExpectPresetYear', async () => {
   assert.deepEqual(
      await DateContext.buildMapDateContext('summer', '2028-07-04'),
      {
         preset: 'summer',
         date: '',
         month: 'JUL',
         day: 20,
         dayOfWeek: null,
         temp: null,
         year: 2028,
      }
   );
});

test('Test_BuildMapDateContext_TestSummerAnchorAlt_ExpectYearFromIso', async () => {
   const ctx = await DateContext.buildMapDateContext('summer', '2031-12-15');

   assert.equal(ctx.preset, 'summer');
   assert.equal(ctx.month, 'JUL');
   assert.equal(ctx.day, 20);
   assert.equal(ctx.year, 2031);
});
