import assert from 'node:assert/strict';
import test from 'node:test';

import { AppConfig } from '../../../scripts/config/appConfig.js';


test('Test_AppConfig_TestOpenWeatherApiKey_ExpectNonEmptyString', () => {
   const apiKey = AppConfig.OPEN_WEATHER_API_KEY;

   assert.equal(typeof apiKey, 'string');
   assert.ok(apiKey.length > 0);
});


test('Test_AppConfig_TestCoordinates_ExpectTorontoZoo', () => {
   const latitude = 43.8177;
   const longitude = -79.1859;

   const coordinates = AppConfig.TORONTO_ZOO_COORDINATES;

   assert.deepEqual(coordinates, {
      lat: latitude,
      lon: longitude,
   });
});


test('Test_AppConfig_TestDefaultMapContain_ExpectOutside', () => {
   const contain = AppConfig.DEFAULT_MAP_CONTAIN;

   assert.equal(contain, 'outside');
});
