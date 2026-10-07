import assert from 'node:assert/strict';
import test from 'node:test';

import { WeatherApiFetcher } from '../../../scripts/api/weatherApiFetcher.js';
import { AppConfig } from '../../../scripts/config/appConfig.js';
import { mockFetchJsonResponse } from '../helpers/fetchMock.mjs';


test('Test_WeatherApiUrl_TestPath_ExpectQuery', () => {
   const path = 'weather';

   const url = WeatherApiFetcher.weatherApiUrl(path);

   assert.match(url, new RegExp(`api\\.openweathermap\\.org/data/2\\.5/${path}`));
   assert.match(url, new RegExp(`lat=${AppConfig.TORONTO_ZOO_COORDINATES.lat}`));
   assert.match(url, new RegExp(`appid=${AppConfig.OPEN_WEATHER_API_KEY}`));
});


test('Test_FetchJson_TestPath_ExpectJsonFromPathUrl', async (t) => {
   const path = 'forecast';
   const body = { list: [] };
   const urls = [];
   const originalFetch = globalThis.fetch;
   globalThis.fetch = async (url) => {
      urls.push(String(url));
      return mockFetchJsonResponse(body);
   };
   t.after(() => {
      globalThis.fetch = originalFetch;
   });

   const data = await WeatherApiFetcher.fetchJson(path);

   assert.equal(data, body);
   assert.deepEqual(urls, [WeatherApiFetcher.weatherApiUrl(path)]);
});
