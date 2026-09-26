import assert from 'node:assert/strict';
import test from 'node:test';

import { JoinedTimesFormatter } from '../../../scripts/shared/joinedTimesFormatter.js';
import { Strings } from '../../../scripts/strings.js';


test('Test_Format_TestTrimmedTimes_ExpectJoined', () => {
   const morning = '11:00 AM';
   const afternoon = '2:00 PM';
   const times = [morning, afternoon];

   const formatted = JoinedTimesFormatter.format(times);

   assert.equal(formatted, `${morning}${Strings.format.listJoin}${afternoon}`);
});


test('Test_Format_TestWhitespaceAndBlank_ExpectTrimmedJoined', () => {
   const morning = '11:00 AM';
   const afternoon = '2:00 PM';
   const times = [` ${morning} `, '', afternoon];

   const formatted = JoinedTimesFormatter.format(times);

   assert.equal(formatted, `${morning}${Strings.format.listJoin}${afternoon}`);
});


test('Test_Format_TestNull_ExpectEmptyString', () => {
   const times = null;

   const formatted = JoinedTimesFormatter.format(times);

   assert.equal(formatted, '');
});


test('Test_Format_TestUndefined_ExpectEmptyString', () => {
   const times = undefined;

   const formatted = JoinedTimesFormatter.format(times);

   assert.equal(formatted, '');
});
