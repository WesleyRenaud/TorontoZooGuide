import assert from 'node:assert/strict';
import test from 'node:test';

import { WeatherClient } from '../../../scripts/api/weatherClient.js';
import { VisitDateValidator } from '../../../scripts/visitDates/visitDateValidator.js';
import { DailyHighTemperatureResolver } from '../../../scripts/weather/dailyHighTemperatureResolver.js';

const TORONTO_OFFSET_SECONDS = -14400;

const DATE = '2026-06-15';


function _slot(localDate, localHour, tempMax) {
   const [year, month, day] = localDate.split('-').map(Number);
   const localSeconds = Date.UTC(year, month - 1, day, localHour) / 1000;

   return { unixSeconds: localSeconds - TORONTO_OFFSET_SECONDS, tempMax };
}


function _forecast(slots) {
   return { timezoneOffsetSeconds: TORONTO_OFFSET_SECONDS, slots };
}


function _mockWeatherClient(t, { currentTemp, forecastSlots }) {
   const calls = [];
   const originalGetCurrentTemp = WeatherClient.getCurrentTemp;
   const originalGetForecast = WeatherClient.getForecast;
   WeatherClient.getCurrentTemp = async () => {
      calls.push('current');
      return currentTemp;
   };
   WeatherClient.getForecast = async () => {
      calls.push('forecast');
      return _forecast(forecastSlots);
   };
   t.after(() => {
      WeatherClient.getCurrentTemp = originalGetCurrentTemp;
      WeatherClient.getForecast = originalGetForecast;
   });

   return calls;
}


test('Test_IsTodayDate_TestToday_ExpectTrue', () => {
   const today = VisitDateValidator.toISODate(VisitDateValidator.getToday());

   const isToday = DailyHighTemperatureResolver.isTodayDate(today);

   assert.equal(isToday, true);
});


test('Test_IsTodayDate_TestFutureDate_ExpectFalse', () => {
   const date = '2099-01-01';

   const isToday = DailyHighTemperatureResolver.isTodayDate(date);

   assert.equal(isToday, false);
});


test('Test_ToLocalISODate_TestUtcMidnight_ExpectPreviousLocalDate', () => {
   const utcMidnightSeconds = Date.UTC(2026, 5, 16, 0) / 1000;

   const localDate = DailyHighTemperatureResolver.toLocalISODate(utcMidnightSeconds, TORONTO_OFFSET_SECONDS);

   assert.equal(localDate, DATE);
});


test('Test_GetForecastHigh_TestLocalDateSlots_ExpectHighestForLocalDate', () => {
   const afternoonTemp = 20;
   const forecast = _forecast([
      _slot('2026-06-14', 20, 25),
      _slot(DATE, 8, 10),
      _slot(DATE, 14, afternoonTemp),
      _slot('2026-06-16', 14, 30),
   ]);

   const high = DailyHighTemperatureResolver.getForecastHigh(forecast, DATE);

   assert.equal(high, afternoonTemp);
});


test('Test_GetForecastHigh_TestMissingDate_ExpectNull', () => {
   const forecast = _forecast([_slot('2026-06-16', 14, 20)]);

   const high = DailyHighTemperatureResolver.getForecastHigh(forecast, DATE);

   assert.equal(high, null);
});


test('Test_GetTodayHigh_TestForecastHigher_ExpectForecastHigh', () => {
   const forecastHigh = 20;

   const high = DailyHighTemperatureResolver.getTodayHigh(8, forecastHigh);

   assert.equal(high, forecastHigh);
});


test('Test_GetTodayHigh_TestCurrentHigher_ExpectCurrentTemp', () => {
   const currentTemp = 22;

   const high = DailyHighTemperatureResolver.getTodayHigh(currentTemp, 19);

   assert.equal(high, currentTemp);
});


test('Test_GetTodayHigh_TestNoForecastHigh_ExpectCurrentTemp', () => {
   const currentTemp = -4;

   const high = DailyHighTemperatureResolver.getTodayHigh(currentTemp, null);

   assert.equal(high, currentTemp);
});


test('Test_Resolve_TestToday_ExpectHigherOfCurrentAndForecast', async (t) => {
   const today = VisitDateValidator.toISODate(VisitDateValidator.getToday());
   const afternoonTemp = 20;
   const calls = _mockWeatherClient(t, {
      currentTemp: 8,
      forecastSlots: [_slot(today, 14, afternoonTemp)],
   });

   const high = await DailyHighTemperatureResolver.resolve(today);

   assert.equal(high, afternoonTemp);
   assert.deepEqual(calls.sort(), ['current', 'forecast']);
});


test('Test_Resolve_TestFutureDate_ExpectForecastHighOnly', async (t) => {
   const tomorrow = VisitDateValidator.toISODate(VisitDateValidator.addLocalCalendarDays(VisitDateValidator.getToday(), 1));
   const afternoonTemp = 20;
   const calls = _mockWeatherClient(t, {
      currentTemp: 40,
      forecastSlots: [_slot(tomorrow, 8, 10), _slot(tomorrow, 14, afternoonTemp)],
   });

   const high = await DailyHighTemperatureResolver.resolve(tomorrow);

   assert.equal(high, afternoonTemp);
   assert.deepEqual(calls, ['forecast']);
});
