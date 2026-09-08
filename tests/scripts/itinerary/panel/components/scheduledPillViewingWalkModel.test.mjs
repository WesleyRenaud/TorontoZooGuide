import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduledPillViewingWalkModel } from '../../../../../scripts/itinerary/panel/components/scheduledPillViewingWalkModel.js';

test('Test_GetAnimalViewingWalkNodeId_TestAnimal_ExpectTrimmed', () => {
   assert.equal(
      ScheduledPillViewingWalkModel.getAnimalViewingWalkNodeId({
         viewing_walk_node_id: '  node-1  ',
      }),
      'node-1'
   );
});

test('Test_GetScheduledItemViewingWalkNodeId_TestSources_ExpectResolved', () => {
   assert.equal(
      ScheduledPillViewingWalkModel.getScheduledItemViewingWalkNodeId({
         viewingWalkNodeId: '  node-2  ',
      }),
      'node-2'
   );
   assert.equal(
      ScheduledPillViewingWalkModel.getScheduledItemViewingWalkNodeId({
         item: { viewing_walk_node_id: '  node-3  ' },
      }),
      'node-3'
   );
});
