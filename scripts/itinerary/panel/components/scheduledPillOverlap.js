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

export {
   MAX_TIMELINE_PILL_COLUMNS,
   MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS,
};

export function getScheduledPillMinDisplayMinutes() {
   return TIMELINE_SCHEDULED_PILL_MIN_CLUSTER_MINUTES;
}

function minutesPerSlotFromHeightPx(heightPx) {
   return (heightPx / TIMELINE_SLOT_HEIGHT_PX) * TIMELINE_SLOT_MINUTES;
}

export function getScheduledItemTimeRange(scheduledItem = {}) {
   const startMinutes = Number(scheduledItem.startMinutes);
   const endMinutes = getScheduledItemEndMinutes(scheduledItem);

   return {
      startMinutes,
      endMinutes,
   };
}

export function getScheduledItemEndMinutes(scheduledItem = {}) {
   const endMinutes = Number(scheduledItem.endMinutes);

   return Number.isFinite(endMinutes) ? endMinutes : Number.NaN;
}

export function getScheduledPillVisualBand(scheduledItem = {}) {
   const clusteredItems = scheduledItem.clusterItems ?? scheduledItem.summaryItems;

   if (clusteredItems?.length) {
      const bands = clusteredItems.map((item) => (
         getScheduledPillVisualBand(item)
      ));

      return {
         startMinutes: Math.min(...bands.map((band) => band.startMinutes)),
         endMinutes: Math.max(...bands.map((band) => band.endMinutes)),
      };
   }

   const { startMinutes } = getScheduledItemTimeRange(scheduledItem);
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

export function doScheduledTimeRangesOverlap(leftRange = {}, rightRange = {}) {
   return (
      leftRange.startMinutes < rightRange.endMinutes
      && rightRange.startMinutes < leftRange.endMinutes
   );
}

export function scheduledPillsOverlapInDefaultPosition(
   leftItem = {},
   rightItem = {}
) {
   return doScheduledTimeRangesOverlap(
      getScheduledPillVisualBand(leftItem),
      getScheduledPillVisualBand(rightItem)
   );
}

export function computeFirstFreeHorizontalOffsetIndex(
   placedItems = [],
   candidateItem = {},
   {
      minColumn = 0,
      maxColumn = MAX_TIMELINE_PILL_COLUMNS - 1,
   } = {}
) {
   const blockedColumns = new Set();

   for (const placedItem of placedItems) {
      if (!scheduledPillsOverlapInDefaultPosition(placedItem, candidateItem)) {
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

export function getScheduledItemMaximumDuration(scheduledItem = {}) {
   const maximumDuration = Number(scheduledItem.maximumDuration);

   if (Number.isFinite(maximumDuration) && maximumDuration > 0) {
      return maximumDuration;
   }

   const endMinutes = getScheduledItemEndMinutes(scheduledItem);
   const startMinutes = Number(scheduledItem.startMinutes);

   if (Number.isFinite(endMinutes) && Number.isFinite(startMinutes)) {
      return endMinutes - startMinutes;
   }

   return 0;
}

export function compareScheduledItemsForGroupDisplay(leftItem = {}, rightItem = {}) {
   const durationDelta = getScheduledItemMaximumDuration(rightItem)
      - getScheduledItemMaximumDuration(leftItem);

   if (durationDelta !== 0) {
      return durationDelta;
   }

   return String(leftItem.label || '').localeCompare(String(rightItem.label || ''));
}

export function sortScheduledItemsForGroupDisplay(items = []) {
   return [...items].sort(compareScheduledItemsForGroupDisplay);
}

export function formatScheduledPillGroupLabel(items = []) {
   if (!items.length) {
      return '';
   }

   const sortedItems = sortScheduledItemsForGroupDisplay(items);
   const firstLabel = String(sortedItems[0]?.label || '').trim();

   if (sortedItems.length === 1) {
      return firstLabel;
   }

   return `${firstLabel} + ${sortedItems.length - 1}`;
}
