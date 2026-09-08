import assert from 'node:assert/strict';
import test from 'node:test';

import { AppConfig } from '../../../scripts/config/appConfig.js';

test('Test_AppConfig_TestCoordinatesAndDefaults_ExpectValues', () => {
   assert.equal(typeof AppConfig.OPEN_WEATHER_API_KEY, 'string');
   assert.ok(AppConfig.OPEN_WEATHER_API_KEY.length > 0);
   assert.deepEqual(AppConfig.TORONTO_ZOO_COORDINATES, {
      lat: 43.8177,
      lon: -79.1859,
   });
   assert.equal(AppConfig.DEFAULT_MAP_CONTAIN, 'outside');
});
