import assert from 'node:assert/strict';
import test from 'node:test';

import { SearchContext } from '../../../scripts/search/searchContext.js';
import { WeatherClient } from '../../../scripts/api/weatherClient.js';
import { VisitDateValidator } from '../../../scripts/visitDates/visitDateValidator.js';

test('Test_BuildDateSearchContext_TestWithoutTemp_ExpectDateFields', async () => {
   const context = await SearchContext.buildDateSearchContext('2026-06-15', { includeTemp: false });
   assert.equal(context.date, '2026-06-15');
   assert.equal(context.month, VisitDateValidator.getMonth('2026-06-15'));
   assert.equal(context.day, 15);
   assert.equal(context.temp, null);
});

test('Test_BuildDateSearchContext_TestEmptyDate_ExpectNullFields', async () => {
   const context = await SearchContext.buildDateSearchContext('');
   assert.deepEqual(context, {
      date: '',
      month: null,
      day: null,
      year: null,
      dayOfWeek: null,
      temp: null,
   });
});

test('Test_BuildDateSearchContext_TestWithinWeek_ExpectTemp', async () => {
   const originalWithin = VisitDateValidator.isWithinNextNDays;
   const originalWeather = WeatherClient.fetchWeatherTempForDate;
   VisitDateValidator.isWithinNextNDays = () => true;
   WeatherClient.fetchWeatherTempForDate = async () => 22;

   try {
      const context = await SearchContext.buildDateSearchContext('2026-06-15');
      assert.equal(context.temp, 22);
   } finally {
      VisitDateValidator.isWithinNextNDays = originalWithin;
      WeatherClient.fetchWeatherTempForDate = originalWeather;
   }
});

test('Test_BuildDateSearchContext_TestWeatherError_ExpectNullTemp', async () => {
   const originalWithin = VisitDateValidator.isWithinNextNDays;
   const originalWeather = WeatherClient.fetchWeatherTempForDate;
   VisitDateValidator.isWithinNextNDays = () => true;
   WeatherClient.fetchWeatherTempForDate = async () => { throw new Error('fail'); };

   try {
      const context = await SearchContext.buildDateSearchContext('2026-06-15');
      assert.equal(context.temp, null);
   } finally {
      VisitDateValidator.isWithinNextNDays = originalWithin;
      WeatherClient.fetchWeatherTempForDate = originalWeather;
   }
});
