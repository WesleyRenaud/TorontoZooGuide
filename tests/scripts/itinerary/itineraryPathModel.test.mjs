import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPathModel } from '../../../scripts/itinerary/itineraryPathModel.js';
import { ScheduleItemKind } from '../../../scripts/shared/enums/scheduleItemKind.js';

test('Test_ResolveItineraryPath_TestOptionsThenItineraryThenEmpty_ExpectResolved', () => {
   const optionsPath = { stops: [{ item_key: 'a' }], legs: [], points: [] };
   const itineraryPath = { stops: [{ item_key: 'b' }], legs: [], points: [] };

   assert.equal(
      ItineraryPathModel.resolveItineraryPath({ itineraryPath: optionsPath }, { itineraryPath }),
      optionsPath
   );
   assert.equal(
      ItineraryPathModel.resolveItineraryPath({}, { itineraryPath }),
      itineraryPath
   );
   assert.equal(
      ItineraryPathModel.resolveItineraryPath({}, {}),
      ItineraryPathModel.EMPTY_ITINERARY_PATH
   );
});

test('Test_NormalizeItineraryPath_TestParts_ExpectNormalizedCollections', () => {
   const path = ItineraryPathModel.normalizeItineraryPath({
      stops: [{
         schedule_item_kind: `  ${ScheduleItemKind.ANIMAL.kind}  `,
         item_key: '  lion  ',
         walk_node_id: '  n1  ',
         start_time: '10:00',
         end_time: '10:30',
      }],
      legs: [{
         from_item_key: 'a',
         to_item_key: 'b',
         from_schedule_item_kind: ScheduleItemKind.ANIMAL.kind,
         to_schedule_item_kind: ScheduleItemKind.ATTRACTION.kind,
         node_ids: ['n1', 'n2'],
      }],
      points: [{ node_id: 'n1', x: 1, y: 2, x_px: 10, y_px: 20 }],
   });

   assert.equal(path.stops[0].itemKey, 'lion');
   assert.deepEqual(path.legs[0].nodeIds, ['n1', 'n2']);
   assert.equal(path.points[0].nodeId, 'n1');
});
