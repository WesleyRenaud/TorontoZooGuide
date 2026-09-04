import { ValueNormalizer } from '../api/valueNormalizer.js';

function normalizeItineraryPathStop(stop) {
   const source = ValueNormalizer.asObject(stop);
   const walkNodeId = ValueNormalizer.asTrimmedString(source.walk_node_id);

   return {
      scheduleItemKind: ValueNormalizer.asTrimmedString(source.schedule_item_kind),
      itemKey: ValueNormalizer.asTrimmedString(source.item_key),
      walkNodeId: walkNodeId || null,
      startTime: ValueNormalizer.asTrimmedString(source.start_time) || null,
      endTime: ValueNormalizer.asTrimmedString(source.end_time) || null,
   };
}

function normalizeItineraryPathLeg(leg) {
   const source = ValueNormalizer.asObject(leg);

   return {
      fromItemKey: ValueNormalizer.asTrimmedString(source.from_item_key),
      toItemKey: ValueNormalizer.asTrimmedString(source.to_item_key),
      fromScheduleItemKind: ValueNormalizer.asTrimmedString(source.from_schedule_item_kind),
      toScheduleItemKind: ValueNormalizer.asTrimmedString(source.to_schedule_item_kind),
      nodeIds: ValueNormalizer.asArray(source.node_ids)
         .map(ValueNormalizer.asTrimmedString)
         .filter(Boolean),
   };
}

function normalizeItineraryPathPoint(point) {
   const source = ValueNormalizer.asObject(point);

   return {
      nodeId: ValueNormalizer.asTrimmedString(source.node_id),
      x: Number(source.x),
      y: Number(source.y),
      xPx: Number(source.x_px),
      yPx: Number(source.y_px),
   };
}

export class ItineraryPathModel {
   static EMPTY_ITINERARY_PATH = Object.freeze({
      stops: [],
      legs: [],
      points: [],
   });

   static resolveItineraryPath(options, itinerary) {
      return options?.itineraryPath
         ?? itinerary?.itineraryPath
         ?? ItineraryPathModel.EMPTY_ITINERARY_PATH;
   }

   static normalizeItineraryPath(itineraryPath) {
      const source = ValueNormalizer.asObject(itineraryPath);

      return {
         stops: ValueNormalizer.asArray(source.stops).map(normalizeItineraryPathStop),
         legs: ValueNormalizer.asArray(source.legs).map(normalizeItineraryPathLeg),
         points: ValueNormalizer.asArray(source.points).map(normalizeItineraryPathPoint),
      };
   }
}
