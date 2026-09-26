import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduledPillViewingWalkModel } from '../../../../../scripts/itinerary/panel/components/scheduledPillViewingWalkModel.js';


test('Test_GetAnimalViewingWalkNodeId_TestAnimal_ExpectTrimmed', () => {
   const nodeId = 'node-lion';
   const animal = { viewing_walk_node_id: `  ${nodeId}  ` };

   const viewingWalkNodeId = ScheduledPillViewingWalkModel.getAnimalViewingWalkNodeId(animal);

   assert.equal(viewingWalkNodeId, nodeId);
});


test('Test_GetScheduledItemViewingWalkNodeId_TestItemField_ExpectTrimmed', () => {
   const nodeId = 'node-tiger';
   const scheduledItem = { viewingWalkNodeId: `  ${nodeId}  ` };

   const viewingWalkNodeId = ScheduledPillViewingWalkModel.getScheduledItemViewingWalkNodeId(
      scheduledItem
   );

   assert.equal(viewingWalkNodeId, nodeId);
});


test('Test_GetScheduledItemViewingWalkNodeId_TestNestedAnimal_ExpectTrimmed', () => {
   const nodeId = 'node-gorilla';
   const scheduledItem = { item: { viewing_walk_node_id: `  ${nodeId}  ` } };

   const viewingWalkNodeId = ScheduledPillViewingWalkModel.getScheduledItemViewingWalkNodeId(
      scheduledItem
   );

   assert.equal(viewingWalkNodeId, nodeId);
});
