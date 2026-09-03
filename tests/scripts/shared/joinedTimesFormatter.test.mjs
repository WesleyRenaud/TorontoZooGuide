import assert from 'node:assert/strict';
import test from 'node:test';

import { JoinedTimesFormatter } from '../../../scripts/shared/joinedTimesFormatter.js';

test('Test_Format_TestTrimmedTimes_ExpectJoined', () => {
   assert.equal(
      JoinedTimesFormatter.format(['11:00 AM', '2:00 PM']),
      '11:00 AM, 2:00 PM'
   );
   assert.equal(
      JoinedTimesFormatter.format([' 11:00 AM ', '', '2:00 PM']),
      '11:00 AM, 2:00 PM'
   );
});

test('Test_Format_TestMissingTimes_ExpectEmptyString', () => {
   assert.equal(JoinedTimesFormatter.format(null), '');
   assert.equal(JoinedTimesFormatter.format(undefined), '');
});
