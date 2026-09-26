import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPathGeometryHelper } from '../../../scripts/map/itineraryPathGeometryHelper.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_LegsShareJoinNode_TestShared_ExpectTrue', () => {
   const joinNode = 'b';
   const first = { nodeIds: ['a', joinNode] };
   const second = { nodeIds: [joinNode, 'c'] };

   const shared = ItineraryPathGeometryHelper.legsShareJoinNode(first, second);

   assert.equal(shared, true);
});


test('Test_LegsShareJoinNode_TestSeparate_ExpectFalse', () => {
   const first = { nodeIds: ['a', 'b'] };
   const second = { nodeIds: ['c', 'd'] };

   const shared = ItineraryPathGeometryHelper.legsShareJoinNode(first, second);

   assert.equal(shared, false);
   assert.notEqual(first.nodeIds.at(Position.LAST), second.nodeIds.at(Position.FIRST));
});
