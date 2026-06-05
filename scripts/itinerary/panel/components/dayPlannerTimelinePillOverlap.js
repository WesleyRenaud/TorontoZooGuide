import {
   MAX_TIMELINE_PILL_COLUMNS,
   MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS,
   SCHEDULED_PILL_TIME_CLUSTER_MINUTES,
   TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
   TIMELINE_POINT_PILL_HEIGHT_PX,
   TIMELINE_SCHEDULED_PILL_MIN_HEIGHT_PX,
   TIMELINE_SLOT_HEIGHT_PX,
   TIMELINE_SLOT_MINUTES,
} from '../../../shared/constants.js';

export {
   MAX_TIMELINE_PILL_COLUMNS,
   MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS,
   SCHEDULED_PILL_TIME_CLUSTER_MINUTES,
};

function minutesPerSlotFromHeightPx(heightPx) {
   return (heightPx / TIMELINE_SLOT_HEIGHT_PX) * TIMELINE_SLOT_MINUTES;
}

export function getScheduledItemTimeRange(scheduledItem = {}) {
   const startMinutes = Number(scheduledItem.startMinutes);
   const durationMinutes = Number(scheduledItem.maximumDuration);

   return {
      startMinutes,
      endMinutes: startMinutes + durationMinutes,
   };
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

function buildPointPillPlacementBlockers(pointPillMarkers = []) {
   return pointPillMarkers
      .filter((marker) => Number.isFinite(marker?.startMinutes))
      .map((marker) => ({
         isPointPillBlocker: true,
         startMinutes: marker.startMinutes,
         maximumDuration: 0,
         horizontalOffsetIndex: 0,
      }));
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

function buildClusterLayoutItem(items = []) {
   const startMinutes = Math.min(...items.map((item) => item.startMinutes));
   const endMinutes = Math.max(
      ...items.map((item) => item.startMinutes + item.maximumDuration)
   );

   return {
      clusterItems: items,
      startMinutes,
      maximumDuration: endMinutes - startMinutes,
      offsetFraction: Math.min(...items.map((item) => item.offsetFraction ?? 0)),
      anchorSlotMinutes: items[0].anchorSlotMinutes,
      label: formatScheduledPillGroupLabel(items),
   };
}

export function clusterScheduledItemsByStartTimeProximity(
   scheduledItems = [],
   clusterWindowMinutes = SCHEDULED_PILL_TIME_CLUSTER_MINUTES,
   windowStartMinutes = 0
) {
   const sortedItems = [...scheduledItems].sort(compareScheduledItemsForLayout);
   const clustersByBucket = new Map();

   sortedItems.forEach((scheduledItem) => {
      const bucketIndex = Math.floor(
         (scheduledItem.startMinutes - windowStartMinutes) / clusterWindowMinutes
      );
      const bucketStartMinutes = windowStartMinutes + (
         bucketIndex * clusterWindowMinutes
      );
      const currentCluster = clustersByBucket.get(bucketStartMinutes) ?? {
         startMinutes: bucketStartMinutes,
         items: [],
      };

      currentCluster.items.push(scheduledItem);
      clustersByBucket.set(bucketStartMinutes, currentCluster);
   });

   return [...clustersByBucket.values()].map((cluster) => (
      cluster.items.length === 1
         ? cluster.items[0]
         : buildClusterLayoutItem(cluster.items)
   ));
}

function clusterScheduledItemsByAnchorSlot(scheduledItems = []) {
   const itemsByAnchor = new Map();

   scheduledItems.forEach((scheduledItem) => {
      const anchorItems = itemsByAnchor.get(scheduledItem.anchorSlotMinutes) ?? [];

      anchorItems.push(scheduledItem);
      itemsByAnchor.set(scheduledItem.anchorSlotMinutes, anchorItems);
   });

   return [...itemsByAnchor.values()].flatMap((anchorItems) => (
      clusterScheduledItemsByStartTimeProximity(
         anchorItems,
         SCHEDULED_PILL_TIME_CLUSTER_MINUTES,
         anchorItems[0]?.anchorSlotMinutes ?? 0
      )
   ));
}

function buildRenderGroup(items, horizontalOffsetIndex) {
   const startMinutes = Math.min(...items.map((item) => item.startMinutes));
   const endMinutes = Math.max(
      ...items.map((item) => item.startMinutes + item.maximumDuration)
   );
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

function buildRenderGroupPlacementProxy(renderGroup = {}) {
   return buildPlacementProxy(
      {
         startMinutes: Math.min(
            ...(renderGroup.items ?? []).map((item) => item.startMinutes)
         ),
         maximumDuration: renderGroup.durationMinutes,
         label: renderGroup.label,
      },
      renderGroup.horizontalOffsetIndex
   );
}

function findOverlappingRenderGroupForOverflow(
   groupsByAnchor,
   anchorSlotMinutes,
   layoutUnit
) {
   const groups = groupsByAnchor.get(anchorSlotMinutes) ?? [];

   return [...groups].reverse().find((group) => (
      scheduledPillsOverlapInDefaultPosition(
         buildRenderGroupPlacementProxy(group),
         layoutUnit
      )
   )) ?? null;
}

function mergeLayoutUnitIntoRenderGroup(renderGroup, layoutUnit) {
   const layoutUnitItems = getLayoutUnitItems(layoutUnit);

   renderGroup.items.push(...layoutUnitItems);
   renderGroup.items.sort(compareScheduledItemsForLayout);
   renderGroup.offsetFraction = Math.min(
      ...renderGroup.items.map((item) => item.offsetFraction ?? 0)
   );
   renderGroup.durationMinutes = Math.max(
      ...renderGroup.items.map((item) => item.startMinutes + item.maximumDuration)
   ) - Math.min(...renderGroup.items.map((item) => item.startMinutes));
   const visualBand = getScheduledPillVisualBand({
      summaryItems: renderGroup.items,
   });

   renderGroup.visualStartMinutes = visualBand.startMinutes;
   renderGroup.visualEndMinutes = visualBand.endMinutes;
   renderGroup.label = formatScheduledPillGroupLabel(renderGroup.items);

   layoutUnitItems.forEach((scheduledItem) => {
      scheduledItem.horizontalOffsetIndex = renderGroup.horizontalOffsetIndex;
   });
}

function buildPlacementProxy(layoutUnit, horizontalOffsetIndex) {
   const items = getLayoutUnitItems(layoutUnit);

   if (items.length === 1) {
      return items[0];
   }

   return {
      horizontalOffsetIndex,
      startMinutes: layoutUnit.startMinutes,
      maximumDuration: layoutUnit.maximumDuration,
      label: layoutUnit.label,
   };
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
   pointPillMarkers = []
) {
   const layoutUnits = clusterScheduledItemsByAnchorSlot(scheduledItems)
      .sort(compareScheduledItemsForLayout);
   const placedItems = buildPointPillPlacementBlockers(pointPillMarkers);
   const groupsByAnchor = new Map();

   layoutUnits.forEach((layoutUnit) => {
      const anchorSlotMinutes = layoutUnit.anchorSlotMinutes;
      const layoutUnitItems = getLayoutUnitItems(layoutUnit);
      const layoutUnitPlacementProxy = buildPlacementProxy(layoutUnit, 0);
      const horizontalOffsetIndex = computeFirstFreeHorizontalOffsetIndex(
         placedItems,
         layoutUnitPlacementProxy,
         {
            minColumn: 0,
            maxColumn: MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS - 1,
         }
      );
      const resolvedHorizontalOffsetIndex = horizontalOffsetIndex
         >= MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS
         ? MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS - 1
         : horizontalOffsetIndex;

      if (horizontalOffsetIndex >= MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS) {
         const overlappingRenderGroup = findOverlappingRenderGroupForOverflow(
            groupsByAnchor,
            anchorSlotMinutes,
            layoutUnitPlacementProxy
         );

         if (overlappingRenderGroup) {
            mergeLayoutUnitIntoRenderGroup(overlappingRenderGroup, layoutUnit);
            placedItems.push(
               buildPlacementProxy(layoutUnit, overlappingRenderGroup.horizontalOffsetIndex)
            );
            return;
         }
      }

      layoutUnit.horizontalOffsetIndex = resolvedHorizontalOffsetIndex;
      layoutUnitItems.forEach((scheduledItem) => {
         scheduledItem.horizontalOffsetIndex = resolvedHorizontalOffsetIndex;
      });
      placedItems.push(
         buildPlacementProxy(layoutUnit, resolvedHorizontalOffsetIndex)
      );
      appendRenderGroup(
         groupsByAnchor,
         anchorSlotMinutes,
         buildRenderGroup(layoutUnitItems, resolvedHorizontalOffsetIndex)
      );
   });

   groupsByAnchor.forEach((groups) => {
      groups.sort(compareRenderGroupsForDisplay);
   });

   return groupsByAnchor;
}
