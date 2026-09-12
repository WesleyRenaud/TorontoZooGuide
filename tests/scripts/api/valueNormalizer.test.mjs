import assert from 'node:assert/strict';
import test from 'node:test';

import { ValueNormalizer } from '../../../scripts/api/valueNormalizer.js';

test('Test_AsArray_TestValidCollection_ExpectSameReference', () => {
   const animals = [{ species: 'African Lion' }];

   assert.equal(ValueNormalizer.asArray(animals), animals);
});

test('Test_AsObject_TestValidObject_ExpectSameReference', () => {
   const giftShop = { name: 'Zootique' };

   assert.equal(ValueNormalizer.asObject(giftShop), giftShop);
});

test('Test_AsArray_TestMissingValues_ExpectEmptyArray', () => {
   assert.deepEqual(ValueNormalizer.asArray(null), []);
   assert.deepEqual(ValueNormalizer.asArray({ name: 'Conservation Carousel' }), []);
});

test('Test_AsObject_TestMissingValues_ExpectEmptyObject', () => {
   assert.deepEqual(ValueNormalizer.asObject(null), {});
   assert.deepEqual(ValueNormalizer.asObject('African Rainforest'), {});
});

test('Test_AsTrimmedString_TestWhitespace_ExpectTrimmed', () => {
   assert.equal(ValueNormalizer.asTrimmedString('  Amur Tiger  '), 'Amur Tiger');
});

test('Test_AsTrimmedString_TestNullish_ExpectEmpty', () => {
   assert.equal(ValueNormalizer.asTrimmedString(null), '');
   assert.equal(ValueNormalizer.asTrimmedString(undefined), '');
});

test('Test_AsTrimmedString_TestNonStrings_ExpectCoerced', () => {
   assert.equal(ValueNormalizer.asTrimmedString(42), '42');
   assert.equal(ValueNormalizer.asTrimmedString(false), 'false');
   assert.equal(ValueNormalizer.asTrimmedString(true), 'true');
});

test('Test_AsNullableString_TestBlank_ExpectNull', () => {
   assert.equal(ValueNormalizer.asNullableString('  Snow Leopard  '), 'Snow Leopard');
   assert.equal(ValueNormalizer.asNullableString('  '), null);
   assert.equal(ValueNormalizer.asNullableString(null), null);
});

test('Test_AsBoolean_TestTruthyInputs_ExpectStrictTrueOnly', () => {
   assert.equal(ValueNormalizer.asBoolean(true), true);
   assert.equal(ValueNormalizer.asBoolean(1), false);
   assert.equal(ValueNormalizer.asBoolean('true'), false);
});

test('Test_NormalizeNumber_TestValidAndInvalid_ExpectNumberOrNull', () => {
   assert.equal(ValueNormalizer.normalizeNumber(75), 75);
   assert.equal(ValueNormalizer.normalizeNumber('75'), 75);
   assert.equal(ValueNormalizer.normalizeNumber('abc'), null);
   assert.equal(ValueNormalizer.normalizeNumber(undefined), null);
});

test('Test_AsPositiveFiniteNumber_TestValidAndInvalid_ExpectPositiveOrNull', () => {
   assert.equal(ValueNormalizer.asPositiveFiniteNumber(30), 30);
   assert.equal(ValueNormalizer.asPositiveFiniteNumber('15'), 15);
   assert.equal(ValueNormalizer.asPositiveFiniteNumber(0), null);
   assert.equal(ValueNormalizer.asPositiveFiniteNumber(-5), null);
   assert.equal(ValueNormalizer.asPositiveFiniteNumber('abc'), null);
   assert.equal(ValueNormalizer.asPositiveFiniteNumber(null), null);
});

test('Test_AsTrimmedStringList_TestMixedValues_ExpectTrimmedNonEmpty', () => {
   assert.deepEqual(
      ValueNormalizer.asTrimmedStringList([ ' 2:00 PM ', '', null, '3:30 PM', 42 ]),
      [ '2:00 PM', '3:30 PM', '42' ]
   );
   assert.deepEqual(ValueNormalizer.asTrimmedStringList(null), []);
});
