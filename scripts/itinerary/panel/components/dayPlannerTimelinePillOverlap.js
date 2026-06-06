import {
   MAX_TIMELINE_PILL_COLUMNS,
   MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS,
   TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
   TIMELINE_POINT_PILL_HEIGHT_PX,
   TIMELINE_SCHEDULED_PILL_MIN_HEIGHT_PX,
   TIMELINE_SLOT_HEIGHT_PX,
   TIMELINE_SLOT_MINUTES,
} from '../../../shared/constants.js';

export {
   MAX_TIMELINE_PILL_COLUMNS,
   MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS,
};

export function getScheduledPillMinDisplayMinutes() {
   return minutesPerSlotFromHeightPx(TIMELINE_SCHEDULED_PILL_MIN_HEIGHT_PX);
}

function getScheduledPillMinDisplayDurationFraction() {
   return TIMELINE_SCHEDULED_PILL_MIN_HEIGHT_PX / TIMELINE_SLOT_HEIGHT_PX;
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
      : TIMELINE_SCHEDULED_PILL_MIN_HEIGHT_PX;
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

export function formatScheduledPillGroupLabel(items = []) {
   if (!items.length) {
      return '';
   }

   const firstLabel = String(items[0]?.label || '').trim();

   if (items.length === 1) {
      return firstLabel;
   }

   return `${firstLabel} + ${items.length - 1}`;
}

function compareScheduledItemsForLayout(leftItem = {}, rightItem = {}) {
   const startDelta = leftItem.startMinutes - rightItem.startMinutes;

   if (startDelta !== 0) {
      return startDelta;
   }

   return String(leftItem.label || '').localeCompare(String(rightItem.label || ''));
}

function appendRenderGroup(groupsByAnchor, anchorSlotMinutes, renderGroup) {
   const groups = groupsByAnchor.get(anchorSlotMinutes) ?? [];

   groups.push(renderGroup);
   groupsByAnchor.set(anchorSlotMinutes, groups);
}

function getLayoutUnitItems(scheduledItem = {}) {
   return scheduledItem.clusterItems
      ?? scheduledItem.summaryItems
      ?? [scheduledItem];
}

function getScheduledItemDurationMinutes(scheduledItem = {}) {
   const endMinutes = getScheduledItemEndMinutes(scheduledItem);
   const startMinutes = Number(scheduledItem.startMinutes);

   if (Number.isFinite(endMinutes) && Number.isFinite(startMinutes)) {
      return endMinutes - startMinutes;
   }

   return Number(scheduledItem.maximumDuration) || 0;
}

function isShortScheduledItem(
   scheduledItem = {},
   minDisplayMinutes = getScheduledPillMinDisplayMinutes()
) {
   return getScheduledItemDurationMinutes(scheduledItem) < minDisplayMinutes;
}

function getClusterWallSpanMinutes(items = []) {
   if (!items.length) {
      return 0;
   }

   const startMinutes = Math.min(...items.map((item) => item.startMinutes));
   const endMinutes = Math.max(...items.map(getScheduledItemEndMinutes));

   return endMinutes - startMinutes;
}

function buildClusterLayoutItem(items = []) {
   const startMinutes = Math.min(...items.map((item) => item.startMinutes));
   const endMinutes = Math.max(...items.map(getScheduledItemEndMinutes));

   return {
      clusterItems: items,
      startMinutes,
      endMinutes,
      maximumDuration: endMinutes - startMinutes,
      offsetFraction: Math.min(...items.map((item) => item.offsetFraction ?? 0)),
      anchorSlotMinutes: items[0].anchorSlotMinutes,
      label: formatScheduledPillGroupLabel(items),
   };
}

export function clusterShortScheduledItemsForDisplay(
   scheduledItems = [],
   minDisplayMinutes = getScheduledPillMinDisplayMinutes()
) {
   const sortedItems = [...scheduledItems].sort(compareScheduledItemsForLayout);
   const clusters = [];
   let index = 0;

   while (index < sortedItems.length) {
      const item = sortedItems[index];

      if (!isShortScheduledItem(item, minDisplayMinutes)) {
         clusters.push(item);
         index += 1;
         continue;
      }

      const clusterItems = [item];
      index += 1;

      while (index < sortedItems.length) {
         const nextItem = sortedItems[index];

         if (!isShortScheduledItem(nextItem, minDisplayMinutes)) {
            break;
         }

         const candidateSpan = getClusterWallSpanMinutes([
            ...clusterItems,
            nextItem,
         ]);

         if (candidateSpan > minDisplayMinutes && clusterItems.length >= 1) {
            break;
         }

         clusterItems.push(nextItem);
         index += 1;

         if (getClusterWallSpanMinutes(clusterItems) >= minDisplayMinutes) {
            break;
         }
      }

      clusters.push(
         clusterItems.length === 1
            ? clusterItems[0]
            : buildClusterLayoutItem(clusterItems)
      );
   }

   return clusters;
}

/** @deprecated Use clusterShortScheduledItemsForDisplay */
export function clusterScheduledItemsByDuration(
   scheduledItems = [],
   minDisplayMinutes = getScheduledPillMinDisplayMinutes(),
   _windowStartMinutes = 0
) {
   return clusterShortScheduledItemsForDisplay(
      scheduledItems,
      minDisplayMinutes
   );
}

/** @deprecated Use clusterShortScheduledItemsForDisplay */
export const clusterScheduledItemsByStartTimeProximity = clusterScheduledItemsByDuration;

function buildRenderGroup(items, horizontalOffsetIndex) {
   const startMinutes = Math.min(...items.map((item) => item.startMinutes));
   const endMinutes = Math.max(...items.map(getScheduledItemEndMinutes));
   const visualBand = getScheduledPillVisualBand({
      summaryItems: items,
   });

   return {
      items,
      offsetFraction: Math.min(...items.map((item) => item.offsetFraction ?? 0)),
      horizontalOffsetIndex,
      durationMinutes: endMinutes - startMinutes,
      visualStartMinutes: visualBand.startMinutes,
      visualEndMinutes: visualBand.endMinutes,
      label: items.length > 1
         ? formatScheduledPillGroupLabel(items)
         : undefined,
   };
}

function getLayoutUnitDurationFraction(layoutUnit = {}) {
   const items = getLayoutUnitItems(layoutUnit);
   const startMinutes = Math.min(...items.map((item) => item.startMinutes));
   const endMinutes = Math.max(...items.map(getScheduledItemEndMinutes));
   const durationMinutes = endMinutes - startMinutes;

   return Math.max(
      durationMinutes / TIMELINE_SLOT_MINUTES,
      getScheduledPillMinDisplayDurationFraction()
   );
}

function getLayoutUnitNaturalOffsetFraction(layoutUnit = {}) {
   return Math.min(
      ...getLayoutUnitItems(layoutUnit).map((item) => item.offsetFraction ?? 0)
   );
}

function compareRenderGroupsForDisplay(leftGroup = {}, rightGroup = {}) {
   const offsetDelta = (leftGroup.offsetFraction ?? 0) - (
      rightGroup.offsetFraction ?? 0
   );

   if (offsetDelta !== 0) {
      return offsetDelta;
   }

   return (leftGroup.horizontalOffsetIndex ?? 0) - (
      rightGroup.horizontalOffsetIndex ?? 0
   );
}

export function planScheduledPillRenderGroupsByAnchor(
   scheduledItems = [],
   _pointPillMarkers = []
) {
   const itemsByAnchor = new Map();

   scheduledItems.forEach((scheduledItem) => {
      const anchorItems = itemsByAnchor.get(scheduledItem.anchorSlotMinutes) ?? [];

      anchorItems.push(scheduledItem);
      itemsByAnchor.set(scheduledItem.anchorSlotMinutes, anchorItems);
   });

   const groupsByAnchor = new Map();
   const sortedAnchorSlots = [...itemsByAnchor.keys()].sort((left, right) => (
      left - right
   ));
   let carryOverFraction = 0;

   sortedAnchorSlots.forEach((anchorSlotMinutes) => {
      const anchorItems = itemsByAnchor.get(anchorSlotMinutes) ?? [];
      const layoutUnits = clusterShortScheduledItemsForDisplay(anchorItems)
         .sort(compareScheduledItemsForLayout);
      let nextStackedOffsetFraction = null;

      layoutUnits.forEach((layoutUnit) => {
         const naturalOffsetFraction = getLayoutUnitNaturalOffsetFraction(
            layoutUnit
         );
         const offsetFraction = nextStackedOffsetFraction === null
            ? Math.max(naturalOffsetFraction, carryOverFraction)
            : Math.max(naturalOffsetFraction, nextStackedOffsetFraction);
         const renderGroup = buildRenderGroup(getLayoutUnitItems(layoutUnit), 0);

         renderGroup.offsetFraction = offsetFraction;
         nextStackedOffsetFraction = (
            offsetFraction + getLayoutUnitDurationFraction(layoutUnit)
         );

         appendRenderGroup(groupsByAnchor, anchorSlotMinutes, renderGroup);
      });

      if (layoutUnits.length > 0 && nextStackedOffsetFraction !== null) {
         carryOverFraction = Math.max(0, nextStackedOffsetFraction - 1);
      }
   });

   groupsByAnchor.forEach((groups) => {
      groups.sort(compareRenderGroupsForDisplay);
   });

   return groupsByAnchor;
}
