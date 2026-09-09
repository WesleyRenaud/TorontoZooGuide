import assert from 'node:assert/strict';
import test from 'node:test';

import { ZooClockTimeHelper } from '../../../scripts/shared/zooClockTimeHelper.js';

test('Test_ParseMinutes_TestFormats_ExpectMinutes', () => {
   assert.equal(ZooClockTimeHelper.parseMinutes('09:30'), 9 * 60 + 30);
   assert.equal(ZooClockTimeHelper.parseMinutes('09:30:30'), 9 * 60 + 30.5);
   assert.equal(ZooClockTimeHelper.parseMinutes('1:00 PM'), 13 * 60);
   assert.equal(ZooClockTimeHelper.parseMinutes('10:00:30 AM'), 10 * 60 + 0.5);
   assert.equal(ZooClockTimeHelper.parseMinutes('12:15 AM'), 15);
   assert.equal(ZooClockTimeHelper.parseMinutes('12:00 PM'), 12 * 60);
   assert.equal(ZooClockTimeHelper.parseMinutes(''), null);
   assert.equal(ZooClockTimeHelper.parseMinutes('25:00'), null);
   assert.equal(ZooClockTimeHelper.parseMinutes('0:00 AM'), null);
   assert.equal(ZooClockTimeHelper.parseMinutes('13:00 PM'), null);
   assert.equal(ZooClockTimeHelper.parseMinutes('bad'), null);
});

test('Test_FormatDisplay_TestValues_ExpectTwelveHourDisplay', () => {
   assert.equal(ZooClockTimeHelper.formatDisplay('1:00 PM'), '1:00 PM');
   assert.equal(ZooClockTimeHelper.formatDisplay('15:30'), '3:30 PM');
   assert.equal(ZooClockTimeHelper.formatDisplay('10:00'), '10:00 AM');
   assert.equal(ZooClockTimeHelper.formatDisplay('09:30:45'), '9:30 AM');
   assert.equal(ZooClockTimeHelper.formatDisplay(''), null);
   assert.equal(ZooClockTimeHelper.formatDisplay('not-a-time'), null);
});

test('Test_NormalizeScheduleTime_TestValues_ExpectFormatDisplayAlias', () => {
   assert.equal(ZooClockTimeHelper.normalizeScheduleTime('19:00'), '7:00 PM');
   assert.equal(ZooClockTimeHelper.normalizeScheduleTime('7:00 PM'), '7:00 PM');
});

test('Test_FormatClockTime_TestValues_ExpectTwelveHourOrPassthrough', () => {
   assert.equal(ZooClockTimeHelper.formatClockTime('09:30'), '9:30 AM');
   assert.equal(ZooClockTimeHelper.formatClockTime('09:30:30'), '9:30:30 AM');
   assert.equal(ZooClockTimeHelper.formatClockTime('19:00'), '7:00 PM');
   assert.equal(ZooClockTimeHelper.formatClockTime('', 'Fallback Time'), 'Fallback Time');
   assert.equal(ZooClockTimeHelper.formatClockTime('not-a-clock'), 'not-a-clock');
});
