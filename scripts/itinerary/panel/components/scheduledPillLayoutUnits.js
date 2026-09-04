import { DayPlannerTimelineMarkers } from '../dayPlannerTimelineMarkers.js';
import { ScheduledPillOverlap } from './scheduledPillOverlap.js';
import { ScheduledPillViewingWalkNode } from './scheduledPillViewingWalkNode.js';
import { TIMELINE_SLOT_MINUTES } from '../../../shared/constants.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';

function getScheduledItemDurationMinutes(scheduledItem = {}) {
   const endMinutes = ScheduledPillOverlap.getScheduledItemEndMinutes(scheduledItem);
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
   const endMinutes = Math.max(...items.map(ScheduledPillOverlap.getScheduledItemEndMinutes));

   return endMinutes - startMinutes;
}

function isCarouselMergeableItem(scheduledItem = {}) {
   return ScheduleItemKind.isScheduleItemModuleItemType(scheduledItem.scheduleItemKind);
}

function canMergeCarouselLayoutUnits(leftUnit = {}, rightUnit = {}) {
   return [...ScheduledPillLayoutUnits.getLayoutUnitItems(leftUnit), ...ScheduledPillLayoutUnits.getLayoutUnitItems(rightUnit)]
      .every(isCarouselMergeableItem);
}

function mergeLayoutUnits(leftUnit = {}, rightUnit = {}) {
   const items = ScheduledPillOverlap.sortScheduledItemsForGroupDisplay([
      ...ScheduledPillLayoutUnits.getLayoutUnitItems(leftUnit),
      ...ScheduledPillLayoutUnits.getLayoutUnitItems(rightUnit),
   ]);

   if (items.length === 1) {
      return items[0];
   }

   return buildClusterLayoutItem(items);
}

function getLayoutUnitStartMinutes(layoutUnit = {}) {
   return Math.min(
      ...ScheduledPillLayoutUnits.getLayoutUnitItems(layoutUnit).map((item) => item.startMinutes)
   );
}

function getLayoutUnitEndMinutes(layoutUnit = {}) {
   return Math.max(
      ...ScheduledPillLayoutUnits.getLayoutUnitItems(layoutUnit).map(ScheduledPillOverlap.getScheduledItemEndMinutes)
   );
}

function getLayoutUnitWallSpanMinutes(layoutUnit = {}) {
   return getClusterWallSpanMinutes(ScheduledPillLayoutUnits.getLayoutUnitItems(layoutUnit));
}

function areConsecutiveLayoutUnits(leftUnit = {}, rightUnit = {}) {
   return getLayoutUnitEndMinutes(leftUnit) === getLayoutUnitStartMinutes(rightUnit);
}

function isUnderMinDisplayLayoutUnit(
   layoutUnit = {},
   minDisplayMinutes = ScheduledPillOverlap.getScheduledPillMinDisplayMinutes()
) {
   return getLayoutUnitWallSpanMinutes(layoutUnit) < minDisplayMinutes;
}

function underMinLayoutUnitsNeedMerge(
   leftUnit = {},
   rightUnit = {},
   minDisplayMinutes = ScheduledPillOverlap.getScheduledPillMinDisplayMinutes()
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
   minDisplayMinutes = ScheduledPillOverlap.getScheduledPillMinDisplayMinutes()
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
   minDisplayMinutes = ScheduledPillOverlap.getScheduledPillMinDisplayMinutes()
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
   minDisplayMinutes = ScheduledPillOverlap.getScheduledPillMinDisplayMinutes()
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
   minDisplayMinutes = ScheduledPillOverlap.getScheduledPillMinDisplayMinutes()
) {
   const items = ScheduledPillLayoutUnits.getLayoutUnitItems(layoutUnit);
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
   minDisplayMinutes = ScheduledPillOverlap.getScheduledPillMinDisplayMinutes()
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

function getEarliestScheduledItemByStartTime(items = []) {
   if (!items.length) {
      return null;
   }

   let earliestItem = items[0];

   for (const item of items) {
      if (item.startMinutes < earliestItem.startMinutes) {
         earliestItem = item;
      }
   }

   return earliestItem;
}

function getLayoutUnitAnchorItem(layoutUnit = {}) {
   return getEarliestScheduledItemByStartTime(ScheduledPillLayoutUnits.getLayoutUnitItems(layoutUnit));
}

function buildClusterLayoutItem(items = []) {
   const displayItems = ScheduledPillOverlap.sortScheduledItemsForGroupDisplay(items);
   const startMinutes = Math.min(...items.map((item) => item.startMinutes));
   const endMinutes = Math.max(...items.map(ScheduledPillOverlap.getScheduledItemEndMinutes));
   const anchorItem = getEarliestScheduledItemByStartTime(items);
   const layoutUnit = {
      clusterItems: displayItems,
      startMinutes,
      endMinutes,
      maximumDuration: endMinutes - startMinutes,
      anchorSlotMinutes: anchorItem?.anchorSlotMinutes,
      slotEndMinutes: anchorItem?.slotEndMinutes,
      label: ScheduledPillOverlap.formatScheduledPillGroupLabel(displayItems),
   };

   return {
      ...layoutUnit,
      offsetFraction: ScheduledPillLayoutUnits.getLayoutUnitScheduleOffsetFraction(layoutUnit),
   };
}

function areConsecutiveScheduledItems(previousItem = {}, nextItem = {}) {
   return ScheduledPillOverlap.getScheduledItemEndMinutes(previousItem) === nextItem.startMinutes;
}

function isAnimalScheduledItem(scheduledItem = {}) {
   return scheduledItem.scheduleItemKind === ScheduleItemKind.ANIMAL.itemType;
}

function areAdjacentOrOverlappingScheduledItems(previousItem = {}, nextItem = {}) {
   const previousEndMinutes = getLayoutUnitEndMinutes(previousItem);
   const nextStartMinutes = Number(nextItem.startMinutes);

   if (!Number.isFinite(previousEndMinutes) || !Number.isFinite(nextStartMinutes)) {
      return false;
   }

   return nextStartMinutes <= previousEndMinutes;
}

function canGroupScheduledItemsByViewingWalkNode(previousItem = {}, nextItem = {}) {
   if (!isAnimalScheduledItem(nextItem)) {
      return false;
   }

   const previousItems = ScheduledPillLayoutUnits.getLayoutUnitItems(previousItem);

   if (!previousItems.every(isAnimalScheduledItem)) {
      return false;
   }

   const nextNodeId = ScheduledPillViewingWalkNode.getScheduledItemViewingWalkNodeId(nextItem);

   if (!nextNodeId) {
      return false;
   }

   if (!previousItems.every((item) => (
      ScheduledPillViewingWalkNode.getScheduledItemViewingWalkNodeId(item) === nextNodeId
   ))) {
      return false;
   }

   return areAdjacentOrOverlappingScheduledItems(previousItem, nextItem);
}

function flushViewingWalkNodeClusterItems(clusterItems = [], clusters = []) {
   if (clusterItems.length === 1) {
      clusters.push(clusterItems[0]);
   }
   else if (clusterItems.length > 1) {
      clusters.push(buildClusterLayoutItem(clusterItems));
   }
}

export class ScheduledPillLayoutUnits {
   static compareScheduledItemsForLayout(leftItem = {}, rightItem = {}) {
      const startDelta = leftItem.startMinutes - rightItem.startMinutes;

      if (startDelta !== 0) {
         return startDelta;
      }

      return ScheduledPillOverlap.compareScheduledItemLabels(leftItem, rightItem);
   }


   static getLayoutUnitItems(scheduledItem = {}) {
      return scheduledItem.clusterItems
         ?? scheduledItem.summaryItems
         ?? [scheduledItem];
   }


   static normalizeLayoutUnitsForDisplay(
      layoutUnits = [],
      minDisplayMinutes = ScheduledPillOverlap.getScheduledPillMinDisplayMinutes()
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


   static getLayoutUnitSlotContext(layoutUnit = {}) {
      const anchorItem = getLayoutUnitAnchorItem(layoutUnit);
      const anchorSlotMinutes = layoutUnit.anchorSlotMinutes
         ?? anchorItem?.anchorSlotMinutes;
      const slotEndMinutes = layoutUnit.slotEndMinutes
         ?? anchorItem?.slotEndMinutes
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


   static getLayoutUnitScheduleOffsetFraction(layoutUnit = {}) {
      const items = ScheduledPillLayoutUnits.getLayoutUnitItems(layoutUnit);
      const { anchorSlotMinutes, slotEndMinutes } = ScheduledPillLayoutUnits.getLayoutUnitSlotContext(layoutUnit);
      const startMinutes = Math.min(...items.map((item) => item.startMinutes));

      return DayPlannerTimelineMarkers.computeMarkerOffsetFraction(
         startMinutes,
         anchorSlotMinutes,
         slotEndMinutes
      );
   }


   static clusterScheduledAnimalItemsByViewingWalkNode(scheduledItems = []) {
      const sortedItems = [...scheduledItems].sort(ScheduledPillLayoutUnits.compareScheduledItemsForLayout);
      const clusters = [];
      let clusterItems = [];

      sortedItems.forEach((scheduledItem) => {
         const previousItem = clusterItems[clusterItems.length - 1];

         if (
            previousItem
            && canGroupScheduledItemsByViewingWalkNode(previousItem, scheduledItem)
         ) {
            clusterItems.push(scheduledItem);
            return;
         }

         flushViewingWalkNodeClusterItems(clusterItems, clusters);

         const lastCluster = clusters[clusters.length - 1];

         if (
            lastCluster
            && canGroupScheduledItemsByViewingWalkNode(lastCluster, scheduledItem)
         ) {
            clusters.pop();
            clusterItems = [
               ...ScheduledPillLayoutUnits.getLayoutUnitItems(lastCluster),
               scheduledItem,
            ];
            return;
         }

         clusterItems = [scheduledItem];
      });

      flushViewingWalkNodeClusterItems(clusterItems, clusters);

      return clusters;
   }


   static clusterShortScheduledItemsForDisplay(
      scheduledItems = [],
      minDisplayMinutes = ScheduledPillOverlap.getScheduledPillMinDisplayMinutes()
   ) {
      const sortedItems = [...scheduledItems].sort(ScheduledPillLayoutUnits.compareScheduledItemsForLayout);
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


   static clusterScheduledItemsByDuration(
      scheduledItems = [],
      minDisplayMinutes = ScheduledPillOverlap.getScheduledPillMinDisplayMinutes(),
      _windowStartMinutes = 0
   ) {
      return ScheduledPillLayoutUnits.clusterShortScheduledItemsForDisplay(
         scheduledItems,
         minDisplayMinutes
      );
   }


   /** @deprecated */
   static clusterScheduledItemsByStartTimeProximity(...args) {
      return ScheduledPillLayoutUnits.clusterScheduledItemsByDuration(...args);
   }
}
