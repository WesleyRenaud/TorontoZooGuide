import assert from 'node:assert/strict';
import test from 'node:test';

import { RowBuildersHelper } from '../../../../scripts/itinerary/panel/rowBuildersHelper.js';


test('Test_NormalizeItems_TestNames_ExpectMapped', () => {
   const africanLion = 'African Lion';
   const snowLeopard = 'Snow Leopard';
   const items = [africanLion, snowLeopard];

   const normalized = RowBuildersHelper.normalizeItems(items, (item) => item.toUpperCase());

   assert.deepEqual(normalized, [africanLion.toUpperCase(), snowLeopard.toUpperCase()]);
});


test('Test_MaxStoredLikelihood_TestMixedValues_ExpectMax', () => {
   const first = 1;
   const second = 4;

   const max = RowBuildersHelper.maxStoredLikelihood(first, '', second, null);

   assert.equal(max, Math.max(first, second));
});


test('Test_MaxStoredLikelihood_TestEmptyValues_ExpectNull', () => {
   const first = null;
   const second = '';

   const max = RowBuildersHelper.maxStoredLikelihood(first, second);

   assert.equal(max, null);
});
