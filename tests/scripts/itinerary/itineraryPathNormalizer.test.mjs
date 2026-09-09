import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPathNormalizer } from '../../../scripts/itinerary/itineraryPathNormalizer.js';
import { ScheduleItemKind } from '../../../scripts/shared/enums/scheduleItemKind.js';

test('Test_NormalizeItineraryPathStop_TestFields_ExpectNormalized', () => {
   assert.deepEqual(
      ItineraryPathNormalizer.normalizeItineraryPathStop({
         schedule_item_kind: `  ${ScheduleItemKind.ANIMAL.kind}  `,
         item_key: '  African Lion|African Savanna  ',
         walk_node_id: '  node-1  ',
         start_time: '  10:00  ',
         end_time: '  10:30  ',
      }),
      {
         scheduleItemKind: ScheduleItemKind.ANIMAL.kind,
         itemKey: 'African Lion|African Savanna',
         walkNodeId: 'node-1',
         startTime: '10:00',
         endTime: '10:30',
      }
   );
});

test('Test_NormalizeItineraryPathStop_TestBlankWalkNode_ExpectNull', () => {
   assert.deepEqual(
      ItineraryPathNormalizer.normalizeItineraryPathStop({
         schedule_item_kind: ScheduleItemKind.ATTRACTION.kind,
         item_key: 'Carousel',
         walk_node_id: '  ',
         start_time: '',
         end_time: '',
      }),
      {
         scheduleItemKind: ScheduleItemKind.ATTRACTION.kind,
         itemKey: 'Carousel',
         walkNodeId: null,
         startTime: null,
         endTime: null,
      }
   );
});

test('Test_NormalizeItineraryPathLeg_TestNodeIds_ExpectTrimmed', () => {
   assert.deepEqual(
      ItineraryPathNormalizer.normalizeItineraryPathLeg({
         from_item_key: '  a  ',
         to_item_key: '  b  ',
         from_schedule_item_kind: `  ${ScheduleItemKind.ANIMAL.kind}  `,
         to_schedule_item_kind: `  ${ScheduleItemKind.ATTRACTION.kind}  `,
         node_ids: ['  n1  ', '', 'n2'],
      }),
      {
         fromItemKey: 'a',
         toItemKey: 'b',
         fromScheduleItemKind: ScheduleItemKind.ANIMAL.kind,
         toScheduleItemKind: ScheduleItemKind.ATTRACTION.kind,
         nodeIds: ['n1', 'n2'],
      }
   );
});

test('Test_NormalizeItineraryPathPoint_TestCoordinates_ExpectNumbers', () => {
   assert.deepEqual(
      ItineraryPathNormalizer.normalizeItineraryPathPoint({
         node_id: '  n1  ',
         x: '1.5',
         y: '2.5',
         x_px: '10',
         y_px: '20',
      }),
      {
         nodeId: 'n1',
         x: 1.5,
         y: 2.5,
         xPx: 10,
         yPx: 20,
      }
   );
});
