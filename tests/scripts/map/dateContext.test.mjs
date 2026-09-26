import assert from 'node:assert/strict';
import test from 'node:test';

import { DateContext } from '../../../scripts/map/dateContext.js';
import { SearchContext } from '../../../scripts/search/searchContext.js';


test('Test_BuildMapDateContext_TestSummerAnchor_ExpectPresetYear', async () => {
   const preset = 'summer';
   const year = 2028;
   const dateStr = `${year}-07-04`;

   const context = await DateContext.buildMapDateContext(preset, dateStr);

   assert.deepEqual(context, {
      preset,
      ...DateContext.PRESET_DATE_CONTEXTS[preset],
      year,
   });
});


test('Test_BuildMapDateContext_TestSummerAnchorAlt_ExpectYearFromIso', async () => {
   const preset = 'summer';
   const year = 2031;
   const dateStr = `${year}-12-15`;

   const context = await DateContext.buildMapDateContext(preset, dateStr);

   assert.equal(context.preset, preset);
   assert.equal(context.month, DateContext.PRESET_DATE_CONTEXTS[preset].month);
   assert.equal(context.day, DateContext.PRESET_DATE_CONTEXTS[preset].day);
   assert.equal(context.year, year);
});


test('Test_BuildMapDateContext_TestCustomDate_ExpectSearchContext', async () => {
   const preset = 'custom';
   const dateStr = '2027-03-15';
   const month = 'MAR';
   const day = 15;
   const year = 2027;
   const originalBuild = SearchContext.buildDateSearchContext;
   SearchContext.buildDateSearchContext = async (nextDate) => ({
      date: nextDate,
      month,
      day,
      year,
   });

   try {
      const context = await DateContext.buildMapDateContext(preset, dateStr);

      assert.deepEqual(context, {
         preset,
         date: dateStr,
         month,
         day,
         year,
      });
   } finally {
      SearchContext.buildDateSearchContext = originalBuild;
   }
});
