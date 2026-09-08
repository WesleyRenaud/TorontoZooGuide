import assert from 'node:assert/strict';
import test from 'node:test';

import { GroupConsecutiveTransportationLegSequencesHelper } from '../../../../../scripts/itinerary/selectors/transportationSelector/groupConsecutiveTransportationLegSequencesHelper.js';

test('Test_NormalizeLegs_TestInputs_ExpectObjectLegs', () => {
   assert.deepEqual(
      GroupConsecutiveTransportationLegSequencesHelper.normalizeLegs(null),
      []
   );
   assert.deepEqual(
      GroupConsecutiveTransportationLegSequencesHelper.normalizeLegs([
         { from: 'a', to: 'b' },
         null,
      ]),
      [{ from: 'a', to: 'b' }, {}]
   );
});
