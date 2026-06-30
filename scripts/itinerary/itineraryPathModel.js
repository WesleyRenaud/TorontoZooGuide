import {
   asArray,
   asObject,
   asTrimmedString,
} from '../api/normalizeValues.js';

export const EMPTY_ITINERARY_PATH = Object.freeze({
   stops: [],
   legs: [],
   points: [],
});

function normalizeItineraryPathStop(stop) {
   const source = asObject(stop);
   const walkNodeId = asTrimmedString(source.walk_node_id);

   return {
      scheduleItemKind: asTrimmedString(source.schedule_item_kind),
      itemKey: asTrimmedString(source.item_key),
      walkNodeId: walkNodeId || null,
      startTime: asTrimmedString(source.start_time) || null,
      endTime: asTrimmedString(source.end_time) || null,
   };
}

function normalizeItineraryPathLeg(leg) {
   const source = asObject(leg);

   return {
      fromItemKey: asTrimmedString(source.from_item_key),
      toItemKey: asTrimmedString(source.to_item_key),
      fromScheduleItemKind: asTrimmedString(source.from_schedule_item_kind),
      toScheduleItemKind: asTrimmedString(source.to_schedule_item_kind),
      nodeIds: asArray(source.node_ids)
         .map(asTrimmedString)
         .filter(Boolean),
   };
}

function normalizeItineraryPathPoint(point) {
   const source = asObject(point);

   return {
      nodeId: asTrimmedString(source.node_id),
      x: Number(source.x),
      y: Number(source.y),
      xPx: Number(source.x_px),
      yPx: Number(source.y_px),
   };
}

export function normalizeItineraryPath(itineraryPath) {
   const source = asObject(itineraryPath);

   return {
      stops: asArray(source.stops).map(normalizeItineraryPathStop),
      legs: asArray(source.legs).map(normalizeItineraryPathLeg),
      points: asArray(source.points).map(normalizeItineraryPathPoint),
   };
}
