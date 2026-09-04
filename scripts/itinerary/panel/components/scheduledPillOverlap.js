import {
   MAX_TIMELINE_PILL_COLUMNS,
   MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS,
   TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
   TIMELINE_POINT_PILL_HEIGHT_PX,
   TIMELINE_SCHEDULED_PILL_MIN_CLUSTER_HEIGHT_PX,
   TIMELINE_SCHEDULED_PILL_MIN_CLUSTER_MINUTES,
   TIMELINE_SLOT_HEIGHT_PX,
   TIMELINE_SLOT_MINUTES,
} from '../../../shared/constants.js';
import { APP_STRINGS } from '../../../strings.js';

const { dayPlanner } = APP_STRINGS.itinerary;

export {
   MAX_TIMELINE_PILL_COLUMNS,
   MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS,
};

function minutesPerSlotFromHeightPx(heightPx) {
   return (heightPx / TIMELINE_SLOT_HEIGHT_PX) * TIMELINE_SLOT_MINUTES;
}

export class ScheduledPillOverlap {
   static getScheduledPillMinDisplayMinutes() {
      return TIMELINE_SCHEDULED_PILL_MIN_CLUSTER_MINUTES;
   }


   static getScheduledItemTimeRange(scheduledItem = {}) {
      const startMinutes = Number(scheduledItem.startMinutes);
      const endMinutes = ScheduledPillOverlap.getScheduledItemEndMinutes(scheduledItem);

      return {
         startMinutes,
         endMinutes,
      };
   }


   static getScheduledItemEndMinutes(scheduledItem = {}) {
      const endMinutes = Number(scheduledItem.endMinutes);

      return Number.isFinite(endMinutes) ? endMinutes : Number.NaN;
   }


   static getScheduledPillVisualBand(scheduledItem = {}) {
      const clusteredItems = scheduledItem.clusterItems ?? scheduledItem.summaryItems;

      if (clusteredItems?.length) {
         const bands = clusteredItems.map((item) => (
            ScheduledPillOverlap.getScheduledPillVisualBand(item)
         ));

         return {
            startMinutes: Math.min(...bands.map((band) => band.startMinutes)),
            endMinutes: Math.max(...bands.map((band) => band.endMinutes)),
         };
      }

      const { startMinutes } = ScheduledPillOverlap.getScheduledItemTimeRange(scheduledItem);
      const scheduledDurationMinutes = Number(scheduledItem.maximumDuration);
      const visualStartMinutes = startMinutes - minutesPerSlotFromHeightPx(
         TIMELINE_PILL_STRIP_TOP_OFFSET_PX
      );
      const minimumHeightPx = scheduledItem.isPointPillBlocker
         ? TIMELINE_POINT_PILL_HEIGHT_PX
         : TIMELINE_SCHEDULED_PILL_MIN_CLUSTER_HEIGHT_PX;
      const visualDurationMinutes = Math.max(
         minutesPerSlotFromHeightPx(minimumHeightPx),
         scheduledDurationMinutes
      );

      return {
         startMinutes: visualStartMinutes,
         endMinutes: visualStartMinutes + visualDurationMinutes,
      };
   }


   static doScheduledTimeRangesOverlap(leftRange = {}, rightRange = {}) {
      return (
         leftRange.startMinutes < rightRange.endMinutes
         && rightRange.startMinutes < leftRange.endMinutes
      );
   }


   static scheduledPillsOverlapInDefaultPosition(
      leftItem = {},
      rightItem = {}
   ) {
      return ScheduledPillOverlap.doScheduledTimeRangesOverlap(
         ScheduledPillOverlap.getScheduledPillVisualBand(leftItem),
         ScheduledPillOverlap.getScheduledPillVisualBand(rightItem)
      );
   }


   static computeFirstFreeHorizontalOffsetIndex(
      placedItems = [],
      candidateItem = {},
      {
         minColumn = 0,
         maxColumn = MAX_TIMELINE_PILL_COLUMNS - 1,
      } = {}
   ) {
      const blockedColumns = new Set();

      for (const placedItem of placedItems) {
         if (!ScheduledPillOverlap.scheduledPillsOverlapInDefaultPosition(placedItem, candidateItem)) {
            continue;
         }

         blockedColumns.add(placedItem.horizontalOffsetIndex ?? 0);
      }

      for (let column = minColumn; column <= maxColumn; column += 1) {
         if (!blockedColumns.has(column)) {
            return column;
         }
      }

      return maxColumn + 1;
   }


   static getScheduledItemMaximumDuration(scheduledItem = {}) {
      const maximumDuration = Number(scheduledItem.maximumDuration);

      if (Number.isFinite(maximumDuration) && maximumDuration > 0) {
         return maximumDuration;
      }

      const endMinutes = ScheduledPillOverlap.getScheduledItemEndMinutes(scheduledItem);
      const startMinutes = Number(scheduledItem.startMinutes);

      if (Number.isFinite(endMinutes) && Number.isFinite(startMinutes)) {
         return endMinutes - startMinutes;
      }

      return 0;
   }


   static compareScheduledItemLabels(leftItem = {}, rightItem = {}) {
      return (leftItem.label ?? '').localeCompare(rightItem.label ?? '');
   }


   static compareScheduledItemsForGroupDisplay(leftItem = {}, rightItem = {}) {
      const durationDelta = ScheduledPillOverlap.getScheduledItemMaximumDuration(rightItem)
         - ScheduledPillOverlap.getScheduledItemMaximumDuration(leftItem);

      if (durationDelta !== 0) {
         return durationDelta;
      }

      return ScheduledPillOverlap.compareScheduledItemLabels(leftItem, rightItem);
   }


   static sortScheduledItemsForGroupDisplay(items = []) {
      return [...items].sort(ScheduledPillOverlap.compareScheduledItemsForGroupDisplay);
   }


   static formatScheduledPillGroupLabel(items = []) {
      if (!items.length) {
         return '';
      }

      const sortedItems = ScheduledPillOverlap.sortScheduledItemsForGroupDisplay(items);
      const firstLabel = (sortedItems[0]?.label ?? '').trim();

      if (sortedItems.length === 1) {
         return firstLabel;
      }

      return dayPlanner.scheduledPillGroupLabel(
         firstLabel,
         sortedItems.length - 1
      );
   }

}
