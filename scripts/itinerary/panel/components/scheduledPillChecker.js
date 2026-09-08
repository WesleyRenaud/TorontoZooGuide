import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { ScheduledPillOverlapHelper } from './scheduledPillOverlapHelper.js';
import { TimelineLayoutConstants } from '../../../shared/timelineLayoutConstants.js';
import { Strings } from '../../../strings.js';

export class ScheduledPillChecker {
   static MAX_TIMELINE_PILL_COLUMNS = TimelineLayoutConstants.MAX_TIMELINE_PILL_COLUMNS;
   static MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS = TimelineLayoutConstants.MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS;

   static getScheduledPillMinDisplayMinutes() {
      return TimelineLayoutConstants.TIMELINE_SCHEDULED_PILL_MIN_CLUSTER_MINUTES;
   }

   static getScheduledItemTimeRange(scheduledItem = {}) {
      const startMinutes = Number(scheduledItem.startMinutes);
      const endMinutes = ScheduledPillChecker.getScheduledItemEndMinutes(scheduledItem);

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
            ScheduledPillChecker.getScheduledPillVisualBand(item)
         ));

         return {
            startMinutes: Math.min(...bands.map((band) => band.startMinutes)),
            endMinutes: Math.max(...bands.map((band) => band.endMinutes)),
         };
      }

      const { startMinutes } = ScheduledPillChecker.getScheduledItemTimeRange(scheduledItem);
      const scheduledDurationMinutes = Number(scheduledItem.maximumDuration);
      const visualStartMinutes = startMinutes - ScheduledPillOverlapHelper.minutesPerSlotFromHeightPx(
         TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX
      );
      const minimumHeightPx = scheduledItem.isPointPillBlocker
         ? TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX
         : TimelineLayoutConstants.TIMELINE_SCHEDULED_PILL_MIN_CLUSTER_HEIGHT_PX;
      const visualDurationMinutes = Math.max(
         ScheduledPillOverlapHelper.minutesPerSlotFromHeightPx(minimumHeightPx),
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
      return ScheduledPillChecker.doScheduledTimeRangesOverlap(
         ScheduledPillChecker.getScheduledPillVisualBand(leftItem),
         ScheduledPillChecker.getScheduledPillVisualBand(rightItem)
      );
   }

   static computeFirstFreeHorizontalOffsetIndex(
      placedItems = [],
      candidateItem = {},
      {
         minColumn = 0,
         maxColumn = TimelineLayoutConstants.MAX_TIMELINE_PILL_COLUMNS - 1,
      } = {}
   ) {
      const blockedColumns = new Set();

      for (const placedItem of placedItems) {
         if (!ScheduledPillChecker.scheduledPillsOverlapInDefaultPosition(placedItem, candidateItem)) {
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

      const endMinutes = ScheduledPillChecker.getScheduledItemEndMinutes(scheduledItem);
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
      const durationDelta = ScheduledPillChecker.getScheduledItemMaximumDuration(rightItem)
         - ScheduledPillChecker.getScheduledItemMaximumDuration(leftItem);

      if (durationDelta !== 0) {
         return durationDelta;
      }

      return ScheduledPillChecker.compareScheduledItemLabels(leftItem, rightItem);
   }

   static sortScheduledItemsForGroupDisplay(items = []) {
      return [...items].sort(ScheduledPillChecker.compareScheduledItemsForGroupDisplay);
   }

   static formatScheduledPillGroupLabel(items = []) {
      if (!items.length) {
         return '';
      }

      const sortedItems = ScheduledPillChecker.sortScheduledItemsForGroupDisplay(items);
      const firstLabel = ValueNormalizer.asTrimmedString(sortedItems[0]?.label);

      if (sortedItems.length === 1) {
         return firstLabel;
      }

      return Strings.itinerary.dayPlanner.scheduledPillGroupLabel(
         firstLabel,
         sortedItems.length - 1
      );
   }

}
