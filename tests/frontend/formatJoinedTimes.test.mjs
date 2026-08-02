import assert from 'node:assert/strict';
import test from 'node:test';

import { formatJoinedTimes } from '../../scripts/shared/formatJoinedTimes.js';

test('formatJoinedTimes joins trimmed times and ignores empties', () => {
   assert.equal(formatJoinedTimes(['11:00 AM', '2:00 PM']), '11:00 AM, 2:00 PM');
   assert.equal(formatJoinedTimes([' 11:00 AM ', '', '2:00 PM']), '11:00 AM, 2:00 PM');
   assert.equal(formatJoinedTimes(null), '');
   assert.equal(formatJoinedTimes(undefined), '');
});
