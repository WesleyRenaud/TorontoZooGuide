import assert from 'node:assert/strict';
import test from 'node:test';

import { APP_STRINGS } from '../../scripts/strings.js';

function collectStringValues(value, path = 'APP_STRINGS', values = new Map()) {
   if (typeof value === 'string') {
      const paths = values.get(value) ?? [];
      paths.push(path);
      values.set(value, paths);
      return values;
   }

   if (Array.isArray(value)) {
      value.forEach((item, index) => {
         collectStringValues(item, `${path}[${index}]`, values);
      });
      return values;
   }

   if (value && typeof value === 'object') {
      Object.entries(value).forEach(([key, item]) => {
         collectStringValues(item, `${path}.${key}`, values);
      });
   }

   return values;
}

test('APP_STRINGS does not contain duplicate string values', () => {
   const duplicates = [...collectStringValues(APP_STRINGS).entries()]
      .filter(([, paths]) => paths.length > 1)
      .map(([value, paths]) => `${JSON.stringify(value)}:\n${paths.join('\n')}`);

   assert.deepEqual(duplicates, []);
});
