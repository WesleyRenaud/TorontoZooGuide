import assert from 'node:assert/strict';
import test from 'node:test';

import { WeatherClient } from '../../../scripts/api/weatherClient.js';
import { mockFetchJsonResponse } from '../helpers/fetchMock.mjs';
import { VisitDateValidator } from '../../../scripts/visitDates/visitDateValidator.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_FetchWeatherTempForDate_TestToday_ExpectCurrentTemp', async () => {
   const today = VisitDateValidator.toISODate(VisitDateValidator.getToday());
   const temp = 18.5;
   const urls = [];
   const originalFetch = globalThis.fetch;
   globalThis.fetch = async (url) => {
      urls.push(String(url));
      return mockFetchJsonResponse({
         main: {
            temp,
         },
      });
   };

   try {
      const weatherTemp = await WeatherClient.fetchWeatherTempForDate(today);

      assert.equal(weatherTemp, temp);
      assert.equal(urls.length, 1);
      assert.equal(urls[Position.FIRST].includes('/weather?'), true);
   } finally {
      globalThis.fetch = originalFetch;
   }
});


test('Test_FetchWeatherTempForDate_TestFutureDate_ExpectAveragedForecast', async () => {
   const tomorrow = VisitDateValidator.toISODate(VisitDateValidator.addLocalCalendarDays(VisitDateValidator.getToday(), 1));
   const morningTemp = 10;
   const afternoonTemp = 20;
   const otherDateTemp = 40;
   const urls = [];
   const originalFetch = globalThis.fetch;
   globalThis.fetch = async (url) => {
      urls.push(String(url));
      return mockFetchJsonResponse({
         list: [
            { dt_txt: `${tomorrow} 09:00:00`, main: { temp: morningTemp } },
            { dt_txt: `${tomorrow} 12:00:00`, main: { temp: afternoonTemp } },
            { dt_txt: '2099-01-01 12:00:00', main: { temp: otherDateTemp } },
         ],
      });
   };

   try {
      const weatherTemp = await WeatherClient.fetchWeatherTempForDate(tomorrow);

      assert.equal(weatherTemp, (morningTemp + afternoonTemp) / 2);
      assert.equal(urls.length, 1);
      assert.equal(urls[Position.FIRST].includes('/forecast?'), true);
   } finally {
      globalThis.fetch = originalFetch;
   }
});
