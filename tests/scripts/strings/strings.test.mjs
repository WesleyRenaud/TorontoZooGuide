import assert from 'node:assert/strict';
import test from 'node:test';

import { Strings } from '../../../scripts/strings.js';

function collectStringValues(value, path = 'Strings', values = new Map()) {
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

test('Test_Strings_TestStringsDoesNotContainDuplicateStringValues_ExpectOk', () => {
   const stringBags = Object.fromEntries(
      Object.getOwnPropertyNames(Strings)
         .filter((key) => {
            const value = Strings[key];
            return value && typeof value === 'object';
         })
         .map((key) => [key, Strings[key]])
   );
   const duplicates = [...collectStringValues(stringBags).entries()]
      .filter(([, paths]) => paths.length > 1)
      .map(([value, paths]) => `${JSON.stringify(value)}:\n${paths.join('\n')}`);

   assert.deepEqual(duplicates, []);
});
