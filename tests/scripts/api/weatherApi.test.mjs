import assert from 'node:assert/strict';
import test from 'node:test';

import { WeatherApi } from '../../../scripts/api/weatherApi.js';
import { mockFetchJsonResponse } from '../helpers/fetchMock.mjs';
import {
   addLocalCalendarDays,
   getToday,
   toISODate,
} from '../../../scripts/visitDates/visitDateRules.js';

test('Test_FetchWeatherTempForDate_TestToday_ExpectCurrentTemp', async () => {
   const today = toISODate(getToday());
   const urls = [];
   const originalFetch = globalThis.fetch;

   globalThis.fetch = async (url) => {
      urls.push(String(url));
      return mockFetchJsonResponse({
         main: {
            temp: 18.5,
         },
      });
   };

   try {
      assert.equal(await WeatherApi.fetchWeatherTempForDate(today), 18.5);
      assert.equal(urls.length, 1);
      assert.equal(urls[0].includes('/weather?'), true);
   } finally {
      globalThis.fetch = originalFetch;
   }
});

test('Test_FetchWeatherTempForDate_TestFutureDate_ExpectAveragedForecast', async () => {
   const tomorrow = toISODate(addLocalCalendarDays(getToday(), 1));
   const urls = [];
   const originalFetch = globalThis.fetch;

   globalThis.fetch = async (url) => {
      urls.push(String(url));
      return mockFetchJsonResponse({
         list: [
            { dt_txt: `${tomorrow} 09:00:00`, main: { temp: 10 } },
            { dt_txt: `${tomorrow} 12:00:00`, main: { temp: 20 } },
            { dt_txt: '2099-01-01 12:00:00', main: { temp: 40 } },
         ],
      });
   };

   try {
      assert.equal(await WeatherApi.fetchWeatherTempForDate(tomorrow), 15);
      assert.equal(urls.length, 1);
      assert.equal(urls[0].includes('/forecast?'), true);
   } finally {
      globalThis.fetch = originalFetch;
   }
});
