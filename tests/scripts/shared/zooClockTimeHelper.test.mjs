import assert from 'node:assert/strict';
import test from 'node:test';

import { ZooClockTimeHelper } from '../../../scripts/shared/zooClockTimeHelper.js';


test('Test_ParseMinutes_TestTwentyFourHour_ExpectMinutes', () => {
   const hours = 9;
   const minutes = 30;
   const time = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;

   const parsed = ZooClockTimeHelper.parseMinutes(time);

   assert.equal(parsed, (hours * 60) + minutes);
});


test('Test_ParseMinutes_TestTwentyFourHourWithSeconds_ExpectFractionalMinutes', () => {
   const hours = 9;
   const minutes = 30;
   const seconds = 30;
   const time = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

   const parsed = ZooClockTimeHelper.parseMinutes(time);

   assert.equal(parsed, (hours * 60) + minutes + (seconds / 60));
});


test('Test_ParseMinutes_TestAfternoonDisplay_ExpectMinutes', () => {
   const hours = 1;
   const minutes = 0;
   const time = `${hours}:${String(minutes).padStart(2, '0')} PM`;

   const parsed = ZooClockTimeHelper.parseMinutes(time);

   assert.equal(parsed, ((hours % 12) + 12) * 60 + minutes);
});


test('Test_ParseMinutes_TestMorningDisplayWithSeconds_ExpectFractionalMinutes', () => {
   const hours = 10;
   const minutes = 0;
   const seconds = 30;
   const time = `${hours}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')} AM`;

   const parsed = ZooClockTimeHelper.parseMinutes(time);

   assert.equal(parsed, (hours * 60) + minutes + (seconds / 60));
});


test('Test_ParseMinutes_TestMidnightDisplay_ExpectMinutes', () => {
   const hours = 12;
   const minutes = 15;
   const time = `${hours}:${String(minutes).padStart(2, '0')} AM`;

   const parsed = ZooClockTimeHelper.parseMinutes(time);

   assert.equal(parsed, ((hours % 12) * 60) + minutes);
});


test('Test_ParseMinutes_TestNoonDisplay_ExpectMinutes', () => {
   const hours = 12;
   const minutes = 0;
   const time = `${hours}:${String(minutes).padStart(2, '0')} PM`;

   const parsed = ZooClockTimeHelper.parseMinutes(time);

   assert.equal(parsed, ((hours % 12) + 12) * 60 + minutes);
});


test('Test_ParseMinutes_TestEmpty_ExpectNull', () => {
   const time = '';

   const parsed = ZooClockTimeHelper.parseMinutes(time);

   assert.equal(parsed, null);
});


test('Test_ParseMinutes_TestInvalidHour_ExpectNull', () => {
   const time = '25:00';

   const parsed = ZooClockTimeHelper.parseMinutes(time);

   assert.equal(parsed, null);
});


test('Test_ParseMinutes_TestZeroHourDisplay_ExpectNull', () => {
   const time = '0:00 AM';

   const parsed = ZooClockTimeHelper.parseMinutes(time);

   assert.equal(parsed, null);
});


test('Test_ParseMinutes_TestThirteenHourDisplay_ExpectNull', () => {
   const time = '13:00 PM';

   const parsed = ZooClockTimeHelper.parseMinutes(time);

   assert.equal(parsed, null);
});


test('Test_ParseMinutes_TestNonTime_ExpectNull', () => {
   const time = 'bad';

   const parsed = ZooClockTimeHelper.parseMinutes(time);

   assert.equal(parsed, null);
});


test('Test_FormatDisplay_TestAfternoonDisplay_ExpectSame', () => {
   const time = '1:00 PM';

   const display = ZooClockTimeHelper.formatDisplay(time);

   assert.equal(display, time);
});


test('Test_FormatDisplay_TestAfternoonTwentyFourHour_ExpectTwelveHour', () => {
   const hours = 15;
   const minutes = 30;
   const time = `${hours}:${String(minutes).padStart(2, '0')}`;

   const display = ZooClockTimeHelper.formatDisplay(time);

   assert.equal(display, `${hours % 12}:${String(minutes).padStart(2, '0')} PM`);
});


test('Test_FormatDisplay_TestMorningTwentyFourHour_ExpectTwelveHour', () => {
   const hours = 10;
   const minutes = 0;
   const time = `${hours}:${String(minutes).padStart(2, '0')}`;

   const display = ZooClockTimeHelper.formatDisplay(time);

   assert.equal(display, `${hours}:${String(minutes).padStart(2, '0')} AM`);
});


test('Test_FormatDisplay_TestMorningWithSeconds_ExpectMinutesOnly', () => {
   const hours = 9;
   const minutes = 30;
   const seconds = 45;
   const time = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

   const display = ZooClockTimeHelper.formatDisplay(time);

   assert.equal(display, `${hours}:${String(minutes).padStart(2, '0')} AM`);
});


test('Test_FormatDisplay_TestEmpty_ExpectNull', () => {
   const time = '';

   const display = ZooClockTimeHelper.formatDisplay(time);

   assert.equal(display, null);
});


test('Test_FormatDisplay_TestNonTime_ExpectNull', () => {
   const time = 'not-a-time';

   const display = ZooClockTimeHelper.formatDisplay(time);

   assert.equal(display, null);
});


test('Test_NormalizeScheduleTime_TestEveningTwentyFourHour_ExpectTwelveHour', () => {
   const hours = 19;
   const minutes = 0;
   const time = `${hours}:${String(minutes).padStart(2, '0')}`;

   const display = ZooClockTimeHelper.normalizeScheduleTime(time);

   assert.equal(display, ZooClockTimeHelper.formatDisplay(time));
});


test('Test_NormalizeScheduleTime_TestEveningDisplay_ExpectSame', () => {
   const time = '7:00 PM';

   const display = ZooClockTimeHelper.normalizeScheduleTime(time);

   assert.equal(display, time);
});


test('Test_FormatClockTime_TestMorningTwentyFourHour_ExpectTwelveHour', () => {
   const hours = 9;
   const minutes = 30;
   const time = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;

   const display = ZooClockTimeHelper.formatClockTime(time);

   assert.equal(display, `${hours}:${String(minutes).padStart(2, '0')} AM`);
});


test('Test_FormatClockTime_TestMorningWithSeconds_ExpectSecondsKept', () => {
   const hours = 9;
   const minutes = 30;
   const seconds = 30;
   const time = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

   const display = ZooClockTimeHelper.formatClockTime(time);

   assert.equal(
      display,
      `${hours}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')} AM`
   );
});


test('Test_FormatClockTime_TestEveningTwentyFourHour_ExpectTwelveHour', () => {
   const hours = 19;
   const minutes = 0;
   const time = `${hours}:${String(minutes).padStart(2, '0')}`;

   const display = ZooClockTimeHelper.formatClockTime(time);

   assert.equal(display, `${hours % 12}:${String(minutes).padStart(2, '0')} PM`);
});


test('Test_FormatClockTime_TestEmpty_ExpectFallback', () => {
   const time = '';
   const fallback = 'Fallback Time';

   const display = ZooClockTimeHelper.formatClockTime(time, fallback);

   assert.equal(display, fallback);
});


test('Test_FormatClockTime_TestNonClock_ExpectPassthrough', () => {
   const time = 'not-a-clock';

   const display = ZooClockTimeHelper.formatClockTime(time);

   assert.equal(display, time);
});
