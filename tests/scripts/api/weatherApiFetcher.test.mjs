import assert from 'node:assert/strict';
import test from 'node:test';

import { WeatherApiFetcher } from '../../../scripts/api/weatherApiFetcher.js';
import { AppConfig } from '../../../scripts/config/appConfig.js';
import { VisitDateValidator } from '../../../scripts/visitDates/visitDateValidator.js';

test('Test_WeatherApiUrl_TestPath_ExpectQuery', () => {
   const url = WeatherApiFetcher.weatherApiUrl('weather');
   assert.match(url, /api\.openweathermap\.org\/data\/2\.5\/weather/);
   assert.match(url, new RegExp(`lat=${AppConfig.TORONTO_ZOO_COORDINATES.lat}`));
   assert.match(url, new RegExp(`appid=${AppConfig.OPEN_WEATHER_API_KEY}`));
});

test('Test_IsTodayDate_TestIso_ExpectBoolean', () => {
   const today = VisitDateValidator.toISODate(VisitDateValidator.getToday());
   assert.equal(WeatherApiFetcher.isTodayDate(today), true);
   assert.equal(WeatherApiFetcher.isTodayDate('2099-01-01'), false);
});

test('Test_FetchCurrentTemp_TestResponse_ExpectNumberOrNull', async () => {
   const originalFetch = globalThis.fetch;
   globalThis.fetch = async () => ({
      json: async () => ({ main: { temp: 18.5 } }),
   });

   try {
      assert.equal(await WeatherApiFetcher.fetchCurrentTemp(), 18.5);
   } finally {
      globalThis.fetch = originalFetch;
   }
});

test('Test_FetchForecastDateTemp_TestDailyAverage_ExpectAverage', async () => {
   const originalFetch = globalThis.fetch;
   globalThis.fetch = async () => ({
      json: async () => ({
         list: [
            { dt_txt: '2026-06-15 09:00:00', main: { temp: 10 } },
            { dt_txt: '2026-06-15 12:00:00', main: { temp: 20 } },
            { dt_txt: '2026-06-16 09:00:00', main: { temp: 99 } },
         ],
      }),
   });

   try {
      assert.equal(await WeatherApiFetcher.fetchForecastDateTemp('2026-06-15'), 15);
      assert.equal(await WeatherApiFetcher.fetchForecastDateTemp('2026-06-20'), null);
   } finally {
      globalThis.fetch = originalFetch;
   }
});
