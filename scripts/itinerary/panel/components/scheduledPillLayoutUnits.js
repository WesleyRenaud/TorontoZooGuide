import { computeMarkerOffsetFraction } from '../dayPlannerTimelineMarkers.js';
import {
   formatScheduledPillGroupLabel,
   getScheduledItemEndMinutes,
   getScheduledPillMinDisplayMinutes,
   sortScheduledItemsForGroupDisplay,
} from './scheduledPillOverlap.js';
import { TIMELINE_SLOT_MINUTES } from '../../../shared/constants.js';
import { isScheduleItemModuleItemType } from '../../../shared/enums/scheduleItemKind.js';

function compareScheduledItemsForLayout(leftItem = {}, rightItem = {}) {
   const startDelta = leftItem.startMinutes - rightItem.startMinutes;

   if (startDelta !== 0) {
      return startDelta;
   }

   return String(leftItem.label || '').localeCompare(String(rightItem.label || ''));
}

export function getLayoutUnitItems(scheduledItem = {}) {
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
   const items = sortScheduledItemsForGroupDisplay([
      ...getLayoutUnitItems(leftUnit),
      ...getLayoutUnitItems(rightUnit),
   ]);

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

function underMinLayoutUnitsNeedMerge(
   leftUnit = {},
   rightUnit = {},
   minDisplayMinutes = getScheduledPillMinDisplayMinutes()
) {
   const leftStartMinutes = getLayoutUnitStartMinutes(leftUnit);
   const leftEndMinutes = getLayoutUnitEndMinutes(leftUnit);
   const rightStartMinutes = getLayoutUnitStartMinutes(rightUnit);
   const rightEndMinutes = getLayoutUnitEndMinutes(rightUnit);

   if (
      !Number.isFinite(leftStartMinutes)
      || !Number.isFinite(leftEndMinutes)
      || !Number.isFinite(rightStartMinutes)
      || !Number.isFinite(rightEndMinutes)
   ) {
      return false;
   }

   return (
      isUnderMinDisplayLayoutUnit(leftUnit, minDisplayMinutes)
      && leftStartMinutes + minDisplayMinutes >= rightStartMinutes
   ) || (
      isUnderMinDisplayLayoutUnit(rightUnit, minDisplayMinutes)
      && rightEndMinutes - minDisplayMinutes <= leftEndMinutes
   );
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

function mergeUnderMinDisplayLayoutUnits(
   layoutUnits = [],
   minDisplayMinutes = getScheduledPillMinDisplayMinutes()
) {
   const nextUnits = [];
   let index = 0;
   let changed = false;

   while (index < layoutUnits.length) {
      const layoutUnit = layoutUnits[index];
      const nextUnit = layoutUnits[index + 1];

      if (
         isUnderMinDisplayLayoutUnit(layoutUnit, minDisplayMinutes)
         && nextUnit
         && underMinLayoutUnitsNeedMerge(layoutUnit, nextUnit, minDisplayMinutes)
         && canMergeCarouselLayoutUnits(layoutUnit, nextUnit)
      ) {
         nextUnits.push(mergeLayoutUnits(layoutUnit, nextUnit));
         index += 2;
         changed = true;
         continue;
      }

      if (
         isUnderMinDisplayLayoutUnit(layoutUnit, minDisplayMinutes)
         && nextUnits.length > 0
         && underMinLayoutUnitsNeedMerge(
            nextUnits[nextUnits.length - 1],
            layoutUnit,
            minDisplayMinutes
         )
         && canMergeCarouselLayoutUnits(nextUnits[nextUnits.length - 1], layoutUnit)
      ) {
         nextUnits[nextUnits.length - 1] = mergeLayoutUnits(
            nextUnits[nextUnits.length - 1],
            layoutUnit
         );
         index += 1;
         changed = true;
         continue;
      }

      nextUnits.push(layoutUnit);
      index += 1;
   }

   return { layoutUnits: nextUnits, changed };
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

export function normalizeLayoutUnitsForDisplay(
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
      const underMinMergeResult = mergeUnderMinDisplayLayoutUnits(
         normalizedUnits,
         minDisplayMinutes
      );

      normalizedUnits = underMinMergeResult.layoutUnits;
      changed = normalizedUnits.length !== previousUnits.length
         || normalizedUnits.some((layoutUnit, index) => (
            layoutUnit !== previousUnits[index]
         ))
         || underMinMergeResult.changed;
   }

   return normalizedUnits;
}

export function getLayoutUnitSlotContext(layoutUnit = {}) {
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

export function getLayoutUnitScheduleOffsetFraction(layoutUnit = {}) {
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
   const displayItems = sortScheduledItemsForGroupDisplay(items);
   const startMinutes = Math.min(...items.map((item) => item.startMinutes));
   const endMinutes = Math.max(...items.map(getScheduledItemEndMinutes));
   const layoutUnit = {
      clusterItems: displayItems,
      startMinutes,
      endMinutes,
      maximumDuration: endMinutes - startMinutes,
      anchorSlotMinutes: items[0].anchorSlotMinutes,
      slotEndMinutes: items.find((item) => (
         Number.isFinite(item.slotEndMinutes)
      ))?.slotEndMinutes,
      label: formatScheduledPillGroupLabel(displayItems),
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
