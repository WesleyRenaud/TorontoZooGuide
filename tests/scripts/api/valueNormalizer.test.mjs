import assert from 'node:assert/strict';
import test from 'node:test';

import { ValueNormalizer } from '../../../scripts/api/valueNormalizer.js';


test('Test_AsArray_TestValidCollection_ExpectSameReference', () => {
   const animals = [{ species: 'African Lion' }];

   const values = ValueNormalizer.asArray(animals);

   assert.equal(values, animals);
});


test('Test_AsArray_TestNull_ExpectEmptyArray', () => {
   const value = null;

   const values = ValueNormalizer.asArray(value);

   assert.deepEqual(values, []);
});


test('Test_AsArray_TestObject_ExpectEmptyArray', () => {
   const value = { name: 'Conservation Carousel' };

   const values = ValueNormalizer.asArray(value);

   assert.deepEqual(values, []);
});


test('Test_AsObject_TestValidObject_ExpectSameReference', () => {
   const giftShop = { name: 'Zootique' };

   const object = ValueNormalizer.asObject(giftShop);

   assert.equal(object, giftShop);
});


test('Test_AsObject_TestNull_ExpectEmptyObject', () => {
   const value = null;

   const object = ValueNormalizer.asObject(value);

   assert.deepEqual(object, {});
});


test('Test_AsObject_TestString_ExpectEmptyObject', () => {
   const value = 'African Rainforest';

   const object = ValueNormalizer.asObject(value);

   assert.deepEqual(object, {});
});


test('Test_AsTrimmedString_TestWhitespace_ExpectTrimmed', () => {
   const name = 'Amur Tiger';
   const value = `  ${name}  `;

   const trimmed = ValueNormalizer.asTrimmedString(value);

   assert.equal(trimmed, name);
});


test('Test_AsTrimmedString_TestNull_ExpectEmpty', () => {
   const value = null;

   const trimmed = ValueNormalizer.asTrimmedString(value);

   assert.equal(trimmed, '');
});


test('Test_AsTrimmedString_TestUndefined_ExpectEmpty', () => {
   const value = undefined;

   const trimmed = ValueNormalizer.asTrimmedString(value);

   assert.equal(trimmed, '');
});


test('Test_AsTrimmedString_TestNumber_ExpectCoerced', () => {
   const value = 42;

   const trimmed = ValueNormalizer.asTrimmedString(value);

   assert.equal(trimmed, String(value));
});


test('Test_AsTrimmedString_TestFalse_ExpectCoerced', () => {
   const value = false;

   const trimmed = ValueNormalizer.asTrimmedString(value);

   assert.equal(trimmed, String(value));
});


test('Test_AsTrimmedString_TestTrue_ExpectCoerced', () => {
   const value = true;

   const trimmed = ValueNormalizer.asTrimmedString(value);

   assert.equal(trimmed, String(value));
});


test('Test_AsNullableString_TestWhitespace_ExpectTrimmed', () => {
   const name = 'Snow Leopard';
   const value = `  ${name}  `;

   const trimmed = ValueNormalizer.asNullableString(value);

   assert.equal(trimmed, name);
});


test('Test_AsNullableString_TestBlank_ExpectNull', () => {
   const value = '  ';

   const trimmed = ValueNormalizer.asNullableString(value);

   assert.equal(trimmed, null);
});


test('Test_AsNullableString_TestNull_ExpectNull', () => {
   const value = null;

   const trimmed = ValueNormalizer.asNullableString(value);

   assert.equal(trimmed, null);
});


test('Test_AsBoolean_TestTrue_ExpectTrue', () => {
   const value = true;

   const flag = ValueNormalizer.asBoolean(value);

   assert.equal(flag, value);
});


test('Test_AsBoolean_TestOne_ExpectFalse', () => {
   const value = 1;

   const flag = ValueNormalizer.asBoolean(value);

   assert.equal(flag, false);
});


test('Test_AsBoolean_TestTrueString_ExpectFalse', () => {
   const value = 'true';

   const flag = ValueNormalizer.asBoolean(value);

   assert.equal(flag, false);
});


test('Test_NormalizeNumber_TestNumber_ExpectNumber', () => {
   const value = 75;

   const number = ValueNormalizer.normalizeNumber(value);

   assert.equal(number, value);
});


test('Test_NormalizeNumber_TestNumericString_ExpectNumber', () => {
   const value = '75';

   const number = ValueNormalizer.normalizeNumber(value);

   assert.equal(number, Number(value));
});


test('Test_NormalizeNumber_TestNonNumeric_ExpectNull', () => {
   const value = 'abc';

   const number = ValueNormalizer.normalizeNumber(value);

   assert.equal(number, null);
});


test('Test_NormalizeNumber_TestUndefined_ExpectNull', () => {
   const value = undefined;

   const number = ValueNormalizer.normalizeNumber(value);

   assert.equal(number, null);
});


test('Test_AsPositiveFiniteNumber_TestNumber_ExpectNumber', () => {
   const value = 30;

   const number = ValueNormalizer.asPositiveFiniteNumber(value);

   assert.equal(number, value);
});


test('Test_AsPositiveFiniteNumber_TestNumericString_ExpectNumber', () => {
   const value = '15';

   const number = ValueNormalizer.asPositiveFiniteNumber(value);

   assert.equal(number, Number(value));
});


test('Test_AsPositiveFiniteNumber_TestZero_ExpectNull', () => {
   const value = 0;

   const number = ValueNormalizer.asPositiveFiniteNumber(value);

   assert.equal(number, null);
});


test('Test_AsPositiveFiniteNumber_TestNegative_ExpectNull', () => {
   const value = -5;

   const number = ValueNormalizer.asPositiveFiniteNumber(value);

   assert.equal(number, null);
});


test('Test_AsPositiveFiniteNumber_TestNonNumeric_ExpectNull', () => {
   const value = 'abc';

   const number = ValueNormalizer.asPositiveFiniteNumber(value);

   assert.equal(number, null);
});


test('Test_AsPositiveFiniteNumber_TestNull_ExpectNull', () => {
   const value = null;

   const number = ValueNormalizer.asPositiveFiniteNumber(value);

   assert.equal(number, null);
});


test('Test_AsTrimmedStringList_TestMixedValues_ExpectTrimmedNonEmpty', () => {
   const afternoon = '2:00 PM';
   const later = '3:30 PM';
   const count = 42;
   const values = [` ${afternoon} `, '', null, later, count];

   const list = ValueNormalizer.asTrimmedStringList(values);

   assert.deepEqual(list, [afternoon, later, String(count)]);
});


test('Test_AsTrimmedStringList_TestNull_ExpectEmpty', () => {
   const value = null;

   const list = ValueNormalizer.asTrimmedStringList(value);

   assert.deepEqual(list, []);
});
