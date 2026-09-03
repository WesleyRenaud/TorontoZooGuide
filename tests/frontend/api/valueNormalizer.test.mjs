import assert from 'node:assert/strict';
import test from 'node:test';

import { ValueNormalizer } from '../../../scripts/api/valueNormalizer.js';

test('keeps valid API collection and object values intact', () => {
   const animals = [{ species: 'African Lion' }];
   const giftShop = { name: 'Zootique' };

   assert.equal(ValueNormalizer.asArray(animals), animals);
   assert.equal(ValueNormalizer.asObject(giftShop), giftShop);
});

test('falls back when API collection and object values are missing', () => {
   assert.deepEqual(ValueNormalizer.asArray(null), []);
   assert.deepEqual(ValueNormalizer.asArray({ name: 'Conservation Carousel' }), []);
   assert.deepEqual(ValueNormalizer.asObject(null), {});
   assert.deepEqual(ValueNormalizer.asObject('African Rainforest'), {});
});

test('normalizes scalar API values without inventing truthy values', () => {
   assert.equal(ValueNormalizer.asTrimmedString('  Amur Tiger  '), 'Amur Tiger');
   assert.equal(ValueNormalizer.asTrimmedString(42), '');
   assert.equal(ValueNormalizer.asNullableString('  Snow Leopard  '), 'Snow Leopard');
   assert.equal(ValueNormalizer.asNullableString('  '), null);
   assert.equal(ValueNormalizer.asBoolean(true), true);
   assert.equal(ValueNormalizer.asBoolean(1), false);
   assert.equal(ValueNormalizer.asBoolean('true'), false);
   assert.equal(ValueNormalizer.normalizeNumber(75), 75);
   assert.equal(ValueNormalizer.normalizeNumber('75'), 75);
   assert.equal(ValueNormalizer.normalizeNumber('abc'), null);
   assert.equal(ValueNormalizer.normalizeNumber(undefined), null);
});

test('ValueNormalizer.asTrimmedStringList trims values and drops blanks', () => {
   assert.deepEqual(
      ValueNormalizer.asTrimmedStringList([ ' 2:00 PM ', '', null, '3:30 PM' ]),
      [ '2:00 PM', '3:30 PM' ]
   );
   assert.deepEqual(ValueNormalizer.asTrimmedStringList(null), []);
});
