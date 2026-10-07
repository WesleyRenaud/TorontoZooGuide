import assert from 'node:assert/strict';
import test from 'node:test';

import { SearchContext } from '../../../scripts/search/searchContext.js';
import { VisitDateValidator } from '../../../scripts/visitDates/visitDateValidator.js';
import { DailyHighTemperatureResolver } from '../../../scripts/weather/dailyHighTemperatureResolver.js';


test('Test_BuildDateSearchContext_TestWithoutTemp_ExpectDateFields', async () => {
   const date = '2026-06-15';

   const context = await SearchContext.buildDateSearchContext(date, { includeTemp: false });

   assert.equal(context.date, date);
   assert.equal(context.month, VisitDateValidator.getMonth(date));
   assert.equal(context.day, VisitDateValidator.getDay(date));
   assert.equal(context.temp, null);
});


test('Test_BuildDateSearchContext_TestEmptyDate_ExpectNullFields', async () => {
   const date = '';

   const context = await SearchContext.buildDateSearchContext(date);

   assert.deepEqual(context, {
      date,
      month: null,
      day: null,
      year: null,
      dayOfWeek: null,
      temp: null,
   });
});


test('Test_BuildDateSearchContext_TestWithinWeek_ExpectTemp', async () => {
   const date = '2026-06-15';
   const temp = 22;
   const originalWithin = VisitDateValidator.isWithinNextNDays;
   const originalWeather = DailyHighTemperatureResolver.resolve;
   VisitDateValidator.isWithinNextNDays = () => true;
   DailyHighTemperatureResolver.resolve = async () => temp;

   try {
      const context = await SearchContext.buildDateSearchContext(date);

      assert.equal(context.temp, temp);
   } finally {
      VisitDateValidator.isWithinNextNDays = originalWithin;
      DailyHighTemperatureResolver.resolve = originalWeather;
   }
});


test('Test_BuildDateSearchContext_TestWeatherError_ExpectNullTemp', async () => {
   const date = '2026-06-15';
   const originalWithin = VisitDateValidator.isWithinNextNDays;
   const originalWeather = DailyHighTemperatureResolver.resolve;
   VisitDateValidator.isWithinNextNDays = () => true;
   DailyHighTemperatureResolver.resolve = async () => { throw new Error('fail'); };

   try {
      const context = await SearchContext.buildDateSearchContext(date);

      assert.equal(context.temp, null);
   } finally {
      VisitDateValidator.isWithinNextNDays = originalWithin;
      DailyHighTemperatureResolver.resolve = originalWeather;
   }
});
