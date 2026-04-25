import assert from 'node:assert/strict';
import test from 'node:test';

import {
   asArray,
   asBoolean,
   asNullableString,
   asObject,
   asTrimmedString,
} from '../../scripts/api/normalizeValues.js';

test('keeps valid API collection and object values intact', () => {
   const animals = [{ species: 'African Lion' }];
   const giftShop = { name: 'Zootique' };

   assert.equal(asArray(animals), animals);
   assert.equal(asObject(giftShop), giftShop);
});

test('falls back when API collection and object values are missing', () => {
   assert.deepEqual(asArray(null), []);
   assert.deepEqual(asArray({ name: 'Conservation Carousel' }), []);
   assert.deepEqual(asObject(null), {});
   assert.deepEqual(asObject('African Rainforest'), {});
});

test('normalizes scalar API values without inventing truthy values', () => {
   assert.equal(asTrimmedString('  Amur Tiger  '), 'Amur Tiger');
   assert.equal(asTrimmedString(42), '');
   assert.equal(asNullableString('  Snow Leopard  '), 'Snow Leopard');
   assert.equal(asNullableString('  '), null);
   assert.equal(asBoolean(true), true);
   assert.equal(asBoolean(1), false);
   assert.equal(asBoolean('true'), false);
});
