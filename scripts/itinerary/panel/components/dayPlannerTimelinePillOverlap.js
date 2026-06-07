import { computeMarkerOffsetFraction } from '../dayPlannerTimelineMarkers.js';
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
import { isScheduleItemModuleItemType } from '../../../shared/enums/scheduleItemKind.js';

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

function getClusterWallSpanMinutes(items = []) {
   if (!items.length) {
      return 0;
   }

   const startMinutes = Math.min(...items.map((item) => item.startMinutes));
   const endMinutes = Math.max(...items.map(getScheduledItemEndMinutes));

   return endMinutes - startMinutes;
}

function isCarouselMergeableItem(scheduledItem = {}) {
   return isScheduleItemModuleItemType(scheduledItem.scheduleItemKind);
}

function canMergeCarouselLayoutUnits(leftUnit = {}, rightUnit = {}) {
   return [...getLayoutUnitItems(leftUnit), ...getLayoutUnitItems(rightUnit)]
      .every(isCarouselMergeableItem);
}

function mergeLayoutUnits(leftUnit = {}, rightUnit = {}) {
   const items = [...getLayoutUnitItems(leftUnit), ...getLayoutUnitItems(rightUnit)]
      .sort(compareScheduledItemsForLayout);

   if (items.length === 1) {
      return items[0];
   }

   return buildClusterLayoutItem(items);
}

function getLayoutUnitStartMinutes(layoutUnit = {}) {
   return Math.min(
      ...getLayoutUnitItems(layoutUnit).map((item) => item.startMinutes)
   );
}

function getLayoutUnitEndMinutes(layoutUnit = {}) {
   return Math.max(
      ...getLayoutUnitItems(layoutUnit).map(getScheduledItemEndMinutes)
   );
}

function getLayoutUnitWallSpanMinutes(layoutUnit = {}) {
   return getClusterWallSpanMinutes(getLayoutUnitItems(layoutUnit));
}

function areConsecutiveLayoutUnits(leftUnit = {}, rightUnit = {}) {
   return getLayoutUnitEndMinutes(leftUnit) === getLayoutUnitStartMinutes(rightUnit);
}

function isUnderMinDisplayLayoutUnit(
   layoutUnit = {},
   minDisplayMinutes = getScheduledPillMinDisplayMinutes()
) {
   return getLayoutUnitWallSpanMinutes(layoutUnit) < minDisplayMinutes;
}

function mergeConsecutiveUnderMinDisplayLayoutUnits(
   layoutUnits = [],
   minDisplayMinutes = getScheduledPillMinDisplayMinutes()
) {
   let mergedUnits = [...layoutUnits];
   let changed = true;

   while (changed) {
      changed = false;
      const nextUnits = [];

      mergedUnits.forEach((layoutUnit) => {
         const previousUnit = nextUnits[nextUnits.length - 1];

         if (
            previousUnit
            && areConsecutiveLayoutUnits(previousUnit, layoutUnit)
            && isUnderMinDisplayLayoutUnit(previousUnit, minDisplayMinutes)
            && canMergeCarouselLayoutUnits(previousUnit, layoutUnit)
         ) {
            nextUnits[nextUnits.length - 1] = mergeLayoutUnits(
               previousUnit,
               layoutUnit
            );
            changed = true;
            return;
         }

         nextUnits.push(layoutUnit);
      });

      mergedUnits = nextUnits;
   }

   return mergedUnits;
}

function absorbHeadOrphanLayoutUnits(
   layoutUnits = [],
   minDisplayMinutes = getScheduledPillMinDisplayMinutes()
) {
   if (layoutUnits.length < 2) {
      return layoutUnits;
   }

   const firstUnit = layoutUnits[0];
   const secondUnit = layoutUnits[1];

   if (
      !isUnderMinDisplayLayoutUnit(firstUnit, minDisplayMinutes)
      || !areConsecutiveLayoutUnits(firstUnit, secondUnit)
      || !canMergeCarouselLayoutUnits(firstUnit, secondUnit)
   ) {
      return layoutUnits;
   }

   return [
      mergeLayoutUnits(firstUnit, secondUnit),
      ...layoutUnits.slice(2),
   ];
}

function normalizeLayoutUnitsForDisplay(
   layoutUnits = [],
   minDisplayMinutes = getScheduledPillMinDisplayMinutes()
) {
   let normalizedUnits = [...layoutUnits];
   let changed = true;

   while (changed) {
      const previousUnits = normalizedUnits;

      normalizedUnits = mergeConsecutiveUnderMinDisplayLayoutUnits(
         absorbTailOrphanLayoutUnits(
            absorbHeadOrphanLayoutUnits(normalizedUnits, minDisplayMinutes),
            minDisplayMinutes
         ),
         minDisplayMinutes
      );
      changed = normalizedUnits.length !== previousUnits.length
         || normalizedUnits.some((layoutUnit, index) => (
            layoutUnit !== previousUnits[index]
         ));
   }

   return normalizedUnits;
}

function isTailOrphanLayoutUnit(
   layoutUnit = {},
   minDisplayMinutes = getScheduledPillMinDisplayMinutes()
) {
   const items = getLayoutUnitItems(layoutUnit);
   const wallSpanMinutes = getClusterWallSpanMinutes(items);

   if (wallSpanMinutes >= minDisplayMinutes) {
      return false;
   }

   const startMinutes = Math.min(...items.map((item) => item.startMinutes));
   const slotEndMinutes = items.find((item) => (
      Number.isFinite(item.slotEndMinutes)
   ))?.slotEndMinutes;

   if (!Number.isFinite(slotEndMinutes)) {
      return false;
   }

   return slotEndMinutes - startMinutes < minDisplayMinutes;
}

function absorbTailOrphanLayoutUnits(
   layoutUnits = [],
   minDisplayMinutes = getScheduledPillMinDisplayMinutes()
) {
   if (layoutUnits.length < 2) {
      return layoutUnits;
   }

   const lastUnit = layoutUnits[layoutUnits.length - 1];

   if (!isTailOrphanLayoutUnit(lastUnit, minDisplayMinutes)) {
      return layoutUnits;
   }

   const previousUnit = layoutUnits[layoutUnits.length - 2];

   if (!canMergeCarouselLayoutUnits(previousUnit, lastUnit)) {
      return layoutUnits;
   }

   return [
      ...layoutUnits.slice(0, -2),
      mergeLayoutUnits(previousUnit, lastUnit),
   ];
}

function getLayoutUnitSlotContext(layoutUnit = {}) {
   const items = getLayoutUnitItems(layoutUnit);
   const anchorSlotMinutes = layoutUnit.anchorSlotMinutes
      ?? items[0]?.anchorSlotMinutes;
   const slotEndMinutes = layoutUnit.slotEndMinutes
      ?? items.find((item) => Number.isFinite(item.slotEndMinutes))?.slotEndMinutes
      ?? (
         Number.isFinite(anchorSlotMinutes)
            ? anchorSlotMinutes + TIMELINE_SLOT_MINUTES
            : TIMELINE_SLOT_MINUTES
      );
   const slotSpanMinutes = slotEndMinutes - anchorSlotMinutes;

   return {
      anchorSlotMinutes,
      slotEndMinutes,
      slotSpanMinutes: Number.isFinite(slotSpanMinutes) && slotSpanMinutes > 0
         ? slotSpanMinutes
         : TIMELINE_SLOT_MINUTES,
   };
}

function getLayoutUnitScheduleOffsetFraction(layoutUnit = {}) {
   const items = getLayoutUnitItems(layoutUnit);
   const { anchorSlotMinutes, slotEndMinutes } = getLayoutUnitSlotContext(layoutUnit);
   const startMinutes = Math.min(...items.map((item) => item.startMinutes));

   return computeMarkerOffsetFraction(
      startMinutes,
      anchorSlotMinutes,
      slotEndMinutes
   );
}

function buildClusterLayoutItem(items = []) {
   const startMinutes = Math.min(...items.map((item) => item.startMinutes));
   const endMinutes = Math.max(...items.map(getScheduledItemEndMinutes));
   const layoutUnit = {
      clusterItems: items,
      startMinutes,
      endMinutes,
      maximumDuration: endMinutes - startMinutes,
      anchorSlotMinutes: items[0].anchorSlotMinutes,
      slotEndMinutes: items.find((item) => (
         Number.isFinite(item.slotEndMinutes)
      ))?.slotEndMinutes,
      label: formatScheduledPillGroupLabel(items),
   };

   return {
      ...layoutUnit,
      offsetFraction: getLayoutUnitScheduleOffsetFraction(layoutUnit),
   };
}

function areConsecutiveScheduledItems(previousItem = {}, nextItem = {}) {
   return getScheduledItemEndMinutes(previousItem) === nextItem.startMinutes;
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
      const itemDurationMinutes = getScheduledItemDurationMinutes(item);

      if (itemDurationMinutes >= minDisplayMinutes) {
         clusters.push(item);
         index += 1;
         continue;
      }

      const clusterItems = [item];
      index += 1;

      while (
         index < sortedItems.length
         && getClusterWallSpanMinutes(clusterItems) < minDisplayMinutes
      ) {
         const nextItem = sortedItems[index];

         if (!areConsecutiveScheduledItems(
            clusterItems[clusterItems.length - 1],
            nextItem
         )) {
            break;
         }

         clusterItems.push(nextItem);
         index += 1;
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

function buildRenderGroup(layoutUnit, horizontalOffsetIndex) {
   const items = getLayoutUnitItems(layoutUnit);
   const { slotSpanMinutes } = getLayoutUnitSlotContext(layoutUnit);
   const startMinutes = Math.min(...items.map((item) => item.startMinutes));
   const endMinutes = Math.max(...items.map(getScheduledItemEndMinutes));
   const wallDurationMinutes = endMinutes - startMinutes;
   const minDisplayMinutes = getScheduledPillMinDisplayMinutes();
   const grouped = items.length > 1;
   const visualBand = getScheduledPillVisualBand({
      summaryItems: items,
   });

   return {
      items,
      offsetFraction: getLayoutUnitScheduleOffsetFraction(layoutUnit),
      slotSpanMinutes,
      horizontalOffsetIndex,
      durationMinutes: wallDurationMinutes,
      displayDurationMinutes: Math.max(wallDurationMinutes, minDisplayMinutes),
      visualStartMinutes: visualBand.startMinutes,
      visualEndMinutes: visualBand.endMinutes,
      label: grouped
         ? formatScheduledPillGroupLabel(items)
         : undefined,
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
   _pointPillMarkers = []
) {
   const itemsByAnchor = new Map();

   scheduledItems.forEach((scheduledItem) => {
      const anchorItems = itemsByAnchor.get(scheduledItem.anchorSlotMinutes) ?? [];

      anchorItems.push(scheduledItem);
      itemsByAnchor.set(scheduledItem.anchorSlotMinutes, anchorItems);
   });

   const groupsByAnchor = new Map();
   const minDisplayMinutes = getScheduledPillMinDisplayMinutes();
   const sortedAnchorSlots = [...itemsByAnchor.keys()].sort((left, right) => (
      left - right
   ));

   sortedAnchorSlots.forEach((anchorSlotMinutes) => {
      const anchorItems = itemsByAnchor.get(anchorSlotMinutes) ?? [];
      const layoutUnits = normalizeLayoutUnitsForDisplay(
         clusterShortScheduledItemsForDisplay(anchorItems),
         minDisplayMinutes
      ).sort(compareScheduledItemsForLayout);

      layoutUnits.forEach((layoutUnit) => {
         appendRenderGroup(
            groupsByAnchor,
            anchorSlotMinutes,
            buildRenderGroup(layoutUnit, 0)
         );
      });
   });

   groupsByAnchor.forEach((groups) => {
      groups.sort(compareRenderGroupsForDisplay);
   });

   return groupsByAnchor;
}
