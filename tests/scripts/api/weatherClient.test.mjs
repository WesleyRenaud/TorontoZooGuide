import assert from 'node:assert/strict';
import test from 'node:test';

import { WeatherApiFetcher } from '../../../scripts/api/weatherApiFetcher.js';
import { WeatherClient } from '../../../scripts/api/weatherClient.js';


function _mockFetchJson(t, body) {
   const paths = [];
   const originalFetchJson = WeatherApiFetcher.fetchJson;
   WeatherApiFetcher.fetchJson = async (path) => {
      paths.push(path);
      return body;
   };
   t.after(() => {
      WeatherApiFetcher.fetchJson = originalFetchJson;
   });

   return paths;
}


test('Test_GetCurrentTemp_TestWeatherResponse_ExpectMainTemp', async (t) => {
   const temp = 18.5;
   const paths = _mockFetchJson(t, { main: { temp } });

   const currentTemp = await WeatherClient.getCurrentTemp();

   assert.equal(currentTemp, temp);
   assert.deepEqual(paths, ['weather']);
});


test('Test_GetForecast_TestForecastResponse_ExpectTimezoneAndSlots', async (t) => {
   const timezone = -14400;
   const dt = 1791471600;
   const tempMax = 17.23;
   const paths = _mockFetchJson(t, {
      city: { timezone },
      list: [{ dt, dt_txt: '2026-10-08 15:00:00', main: { temp: 17, temp_max: tempMax } }],
   });

   const forecast = await WeatherClient.getForecast();

   assert.deepEqual(forecast, {
      timezoneOffsetSeconds: timezone,
      slots: [{ unixSeconds: dt, tempMax }],
   });
   assert.deepEqual(paths, ['forecast']);
});
