import assert from 'node:assert/strict';
import test from 'node:test';

import { WeatherApiFetcher } from '../../../scripts/api/weatherApiFetcher.js';
import { AppConfig } from '../../../scripts/config/appConfig.js';
import { VisitDateValidator } from '../../../scripts/visitDates/visitDateValidator.js';


test('Test_WeatherApiUrl_TestPath_ExpectQuery', () => {
   const path = 'weather';

   const url = WeatherApiFetcher.weatherApiUrl(path);

   assert.match(url, new RegExp(`api\\.openweathermap\\.org/data/2\\.5/${path}`));
   assert.match(url, new RegExp(`lat=${AppConfig.TORONTO_ZOO_COORDINATES.lat}`));
   assert.match(url, new RegExp(`appid=${AppConfig.OPEN_WEATHER_API_KEY}`));
});


test('Test_IsTodayDate_TestToday_ExpectTrue', () => {
   const today = VisitDateValidator.toISODate(VisitDateValidator.getToday());

   const isToday = WeatherApiFetcher.isTodayDate(today);

   assert.equal(isToday, true);
});


test('Test_IsTodayDate_TestFutureDate_ExpectFalse', () => {
   const date = '2099-01-01';

   const isToday = WeatherApiFetcher.isTodayDate(date);

   assert.equal(isToday, false);
});


test('Test_FetchCurrentTemp_TestResponse_ExpectNumber', async () => {
   const temp = 18.5;
   const originalFetch = globalThis.fetch;
   globalThis.fetch = async () => ({
      json: async () => ({ main: { temp } }),
   });

   try {
      const currentTemp = await WeatherApiFetcher.fetchCurrentTemp();

      assert.equal(currentTemp, temp);
   } finally {
      globalThis.fetch = originalFetch;
   }
});


test('Test_FetchForecastDateTemp_TestDailyAverage_ExpectAverage', async () => {
   const date = '2026-06-15';
   const morningTemp = 10;
   const afternoonTemp = 20;
   const otherDateTemp = 99;
   const originalFetch = globalThis.fetch;
   globalThis.fetch = async () => ({
      json: async () => ({
         list: [
            { dt_txt: `${date} 09:00:00`, main: { temp: morningTemp } },
            { dt_txt: `${date} 12:00:00`, main: { temp: afternoonTemp } },
            { dt_txt: '2026-06-16 09:00:00', main: { temp: otherDateTemp } },
         ],
      }),
   });

   try {
      const average = await WeatherApiFetcher.fetchForecastDateTemp(date);

      assert.equal(average, (morningTemp + afternoonTemp) / 2);
   } finally {
      globalThis.fetch = originalFetch;
   }
});


test('Test_FetchForecastDateTemp_TestMissingDate_ExpectNull', async () => {
   const date = '2026-06-20';
   const otherDate = '2026-06-15';
   const morningTemp = 10;
   const originalFetch = globalThis.fetch;
   globalThis.fetch = async () => ({
      json: async () => ({
         list: [
            { dt_txt: `${otherDate} 09:00:00`, main: { temp: morningTemp } },
         ],
      }),
   });

   try {
      const average = await WeatherApiFetcher.fetchForecastDateTemp(date);

      assert.equal(average, null);
   } finally {
      globalThis.fetch = originalFetch;
   }
});
