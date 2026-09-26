import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPathModel } from '../../../scripts/itinerary/itineraryPathModel.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { ScheduleItemKind } from '../../../scripts/shared/enums/scheduleItemKind.js';


test('Test_ResolveItineraryPath_TestOptionsPath_ExpectOptionsPath', () => {
   const optionsPath = { stops: [{ item_key: 'African Lion' }], legs: [], points: [] };
   const itineraryPath = { stops: [{ item_key: 'Zoomobile' }], legs: [], points: [] };

   const path = ItineraryPathModel.resolveItineraryPath({ itineraryPath: optionsPath }, { itineraryPath });

   assert.equal(path, optionsPath);
});


test('Test_ResolveItineraryPath_TestItineraryPath_ExpectItineraryPath', () => {
   const itineraryPath = { stops: [{ item_key: 'Zoomobile' }], legs: [], points: [] };

   const path = ItineraryPathModel.resolveItineraryPath({}, { itineraryPath });

   assert.equal(path, itineraryPath);
});


test('Test_ResolveItineraryPath_TestMissing_ExpectEmptyPath', () => {
   const options = {};
   const itinerary = {};

   const path = ItineraryPathModel.resolveItineraryPath(options, itinerary);

   assert.equal(path, ItineraryPathModel.EMPTY_ITINERARY_PATH);
});


test('Test_NormalizeItineraryPath_TestParts_ExpectNormalizedCollections', () => {
   const itemKey = 'lion';
   const walkNodeId = 'n1';
   const startTime = '10:00';
   const endTime = '10:30';
   const fromItemKey = 'a';
   const toItemKey = 'b';
   const fromNodeId = 'n1';
   const toNodeId = 'n2';
   const x = 1;
   const y = 2;
   const xPx = 10;
   const yPx = 20;
   const source = {
      stops: [{
         schedule_item_kind: `  ${ScheduleItemKind.ANIMAL.kind}  `,
         item_key: `  ${itemKey}  `,
         walk_node_id: `  ${walkNodeId}  `,
         start_time: startTime,
         end_time: endTime,
      }],
      legs: [{
         from_item_key: fromItemKey,
         to_item_key: toItemKey,
         from_schedule_item_kind: ScheduleItemKind.ANIMAL.kind,
         to_schedule_item_kind: ScheduleItemKind.ATTRACTION.kind,
         node_ids: [fromNodeId, toNodeId],
      }],
      points: [{ node_id: walkNodeId, x, y, x_px: xPx, y_px: yPx }],
   };

   const path = ItineraryPathModel.normalizeItineraryPath(source);

   assert.equal(path.stops[Position.FIRST].itemKey, itemKey);
   assert.deepEqual(path.legs[Position.FIRST].nodeIds, [fromNodeId, toNodeId]);
   assert.equal(path.points[Position.FIRST].nodeId, walkNodeId);
});
