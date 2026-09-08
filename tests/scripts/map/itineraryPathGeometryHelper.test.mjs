import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPathGeometryHelper } from '../../../scripts/map/itineraryPathGeometryHelper.js';

test('Test_LegsShareJoinNode_TestSharedAndSeparate_ExpectBoolean', () => {
   assert.equal(
      ItineraryPathGeometryHelper.legsShareJoinNode(
         { nodeIds: ['a', 'b'] },
         { nodeIds: ['b', 'c'] }
      ),
      true
   );
   assert.equal(
      ItineraryPathGeometryHelper.legsShareJoinNode(
         { nodeIds: ['a', 'b'] },
         { nodeIds: ['c', 'd'] }
      ),
      false
   );
});
