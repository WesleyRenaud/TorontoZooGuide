import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPathNormalizer } from '../../../scripts/itinerary/itineraryPathNormalizer.js';
import { ScheduleItemKind } from '../../../scripts/shared/enums/scheduleItemKind.js';


test('Test_NormalizeItineraryPathStop_TestFields_ExpectNormalized', () => {
   const itemKey = 'African Lion|African Savanna';
   const walkNodeId = 'node-1';
   const startTime = '10:00';
   const endTime = '10:30';
   const stop = {
      schedule_item_kind: `  ${ScheduleItemKind.ANIMAL.kind}  `,
      item_key: `  ${itemKey}  `,
      walk_node_id: `  ${walkNodeId}  `,
      start_time: `  ${startTime}  `,
      end_time: `  ${endTime}  `,
   };

   const normalized = ItineraryPathNormalizer.normalizeItineraryPathStop(stop);

   assert.deepEqual(normalized, {
      scheduleItemKind: ScheduleItemKind.ANIMAL.kind,
      itemKey,
      walkNodeId,
      startTime,
      endTime,
   });
});


test('Test_NormalizeItineraryPathStop_TestBlankWalkNode_ExpectNull', () => {
   const itemKey = 'Conservation Carousel';
   const stop = {
      schedule_item_kind: ScheduleItemKind.ATTRACTION.kind,
      item_key: itemKey,
      walk_node_id: '  ',
      start_time: '',
      end_time: '',
   };

   const normalized = ItineraryPathNormalizer.normalizeItineraryPathStop(stop);

   assert.deepEqual(normalized, {
      scheduleItemKind: ScheduleItemKind.ATTRACTION.kind,
      itemKey,
      walkNodeId: null,
      startTime: null,
      endTime: null,
   });
});


test('Test_NormalizeItineraryPathLeg_TestNodeIds_ExpectTrimmed', () => {
   const fromItemKey = 'a';
   const toItemKey = 'b';
   const fromNodeId = 'n1';
   const toNodeId = 'n2';
   const leg = {
      from_item_key: `  ${fromItemKey}  `,
      to_item_key: `  ${toItemKey}  `,
      from_schedule_item_kind: `  ${ScheduleItemKind.ANIMAL.kind}  `,
      to_schedule_item_kind: `  ${ScheduleItemKind.ATTRACTION.kind}  `,
      node_ids: [`  ${fromNodeId}  `, '', toNodeId],
   };

   const normalized = ItineraryPathNormalizer.normalizeItineraryPathLeg(leg);

   assert.deepEqual(normalized, {
      fromItemKey,
      toItemKey,
      fromScheduleItemKind: ScheduleItemKind.ANIMAL.kind,
      toScheduleItemKind: ScheduleItemKind.ATTRACTION.kind,
      nodeIds: [fromNodeId, toNodeId],
   });
});


test('Test_NormalizeItineraryPathPoint_TestCoordinates_ExpectNumbers', () => {
   const nodeId = 'n1';
   const x = '1.5';
   const y = '2.5';
   const xPx = '10';
   const yPx = '20';
   const point = {
      node_id: `  ${nodeId}  `,
      x,
      y,
      x_px: xPx,
      y_px: yPx,
   };

   const normalized = ItineraryPathNormalizer.normalizeItineraryPathPoint(point);

   assert.deepEqual(normalized, {
      nodeId,
      x: Number(x),
      y: Number(y),
      xPx: Number(xPx),
      yPx: Number(yPx),
   });
});
