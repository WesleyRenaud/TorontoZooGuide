import assert from 'node:assert/strict';
import test from 'node:test';

import { buildMapDateContext } from '../../scripts/map/dateContext.js';

test('preset map context takes year from anchor ISO (same extraction as visit date)', async () => {
   assert.deepEqual(
      await buildMapDateContext('summer', '2028-07-04'),
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
