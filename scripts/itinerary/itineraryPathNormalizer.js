import { ValueNormalizer } from '../api/valueNormalizer.js';

export class ItineraryPathNormalizer {
   static normalizeItineraryPathStop(stop) {
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

   static normalizeItineraryPathLeg(leg) {
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

   static normalizeItineraryPathPoint(point) {
      const source = ValueNormalizer.asObject(point);

      return {
         nodeId: ValueNormalizer.asTrimmedString(source.node_id),
         x: Number(source.x),
         y: Number(source.y),
         xPx: Number(source.x_px),
         yPx: Number(source.y_px),
      };
   }
}
