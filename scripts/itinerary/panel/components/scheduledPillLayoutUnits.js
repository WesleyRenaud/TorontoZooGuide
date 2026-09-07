import { DayPlannerTimelineMarkers } from '../dayPlannerTimelineMarkers.js';
import { ScheduledPillOverlap } from './scheduledPillOverlap.js';
import { ScheduledPillViewingWalkNode } from './scheduledPillViewingWalkNode.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';
import { TimelineLayoutConstants } from '../../../shared/timelineLayoutConstants.js';

export class ScheduledPillLayoutUnits {
   static getScheduledItemDurationMinutes(scheduledItem = {}) {
      const endMinutes = ScheduledPillOverlap.getScheduledItemEndMinutes(scheduledItem);
      const startMinutes = Number(scheduledItem.startMinutes);

      if (Number.isFinite(endMinutes) && Number.isFinite(startMinutes)) {
         return endMinutes - startMinutes;
      }

      return Number(scheduledItem.maximumDuration) || 0;
   }

   static getClusterWallSpanMinutes(items = []) {
      if (!items.length) {
         return 0;
      }

      const startMinutes = Math.min(...items.map((item) => item.startMinutes));
      const endMinutes = Math.max(...items.map(ScheduledPillOverlap.getScheduledItemEndMinutes));

      return endMinutes - startMinutes;
   }

   static isCarouselMergeableItem(scheduledItem = {}) {
      return ScheduleItemKind.isScheduleItemModuleItemType(scheduledItem.scheduleItemKind);
   }

   static canMergeCarouselLayoutUnits(leftUnit = {}, rightUnit = {}) {
      return [...ScheduledPillLayoutUnits.getLayoutUnitItems(leftUnit), ...ScheduledPillLayoutUnits.getLayoutUnitItems(rightUnit)]
         .every(ScheduledPillLayoutUnits.isCarouselMergeableItem);
   }

   static mergeLayoutUnits(leftUnit = {}, rightUnit = {}) {
      const items = ScheduledPillOverlap.sortScheduledItemsForGroupDisplay([
         ...ScheduledPillLayoutUnits.getLayoutUnitItems(leftUnit),
         ...ScheduledPillLayoutUnits.getLayoutUnitItems(rightUnit),
      ]);

      if (items.length === 1) {
         return items[0];
      }

      return ScheduledPillLayoutUnits.buildClusterLayoutItem(items);
   }

   static getLayoutUnitStartMinutes(layoutUnit = {}) {
      return Math.min(
         ...ScheduledPillLayoutUnits.getLayoutUnitItems(layoutUnit).map((item) => item.startMinutes)
      );
   }

   static getLayoutUnitEndMinutes(layoutUnit = {}) {
      return Math.max(
         ...ScheduledPillLayoutUnits.getLayoutUnitItems(layoutUnit).map(ScheduledPillOverlap.getScheduledItemEndMinutes)
      );
   }

   static getLayoutUnitWallSpanMinutes(layoutUnit = {}) {
      return ScheduledPillLayoutUnits.getClusterWallSpanMinutes(ScheduledPillLayoutUnits.getLayoutUnitItems(layoutUnit));
   }

   static areConsecutiveLayoutUnits(leftUnit = {}, rightUnit = {}) {
      return ScheduledPillLayoutUnits.getLayoutUnitEndMinutes(leftUnit) === ScheduledPillLayoutUnits.getLayoutUnitStartMinutes(rightUnit);
   }

   static isUnderMinDisplayLayoutUnit(
      layoutUnit = {},
      minDisplayMinutes = ScheduledPillOverlap.getScheduledPillMinDisplayMinutes()
   ) {
      return ScheduledPillLayoutUnits.getLayoutUnitWallSpanMinutes(layoutUnit) < minDisplayMinutes;
   }

   static underMinLayoutUnitsNeedMerge(
      leftUnit = {},
      rightUnit = {},
      minDisplayMinutes = ScheduledPillOverlap.getScheduledPillMinDisplayMinutes()
   ) {
      const leftStartMinutes = ScheduledPillLayoutUnits.getLayoutUnitStartMinutes(leftUnit);
      const leftEndMinutes = ScheduledPillLayoutUnits.getLayoutUnitEndMinutes(leftUnit);
      const rightStartMinutes = ScheduledPillLayoutUnits.getLayoutUnitStartMinutes(rightUnit);
      const rightEndMinutes = ScheduledPillLayoutUnits.getLayoutUnitEndMinutes(rightUnit);

      if (
         !Number.isFinite(leftStartMinutes)
         || !Number.isFinite(leftEndMinutes)
         || !Number.isFinite(rightStartMinutes)
         || !Number.isFinite(rightEndMinutes)
      ) {
         return false;
      }

      return (
         ScheduledPillLayoutUnits.isUnderMinDisplayLayoutUnit(leftUnit, minDisplayMinutes)
         && leftStartMinutes + minDisplayMinutes >= rightStartMinutes
      ) || (
         ScheduledPillLayoutUnits.isUnderMinDisplayLayoutUnit(rightUnit, minDisplayMinutes)
         && rightEndMinutes - minDisplayMinutes <= leftEndMinutes
      );
   }

   static mergeConsecutiveUnderMinDisplayLayoutUnits(
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
               && ScheduledPillLayoutUnits.areConsecutiveLayoutUnits(previousUnit, layoutUnit)
               && ScheduledPillLayoutUnits.isUnderMinDisplayLayoutUnit(previousUnit, minDisplayMinutes)
               && ScheduledPillLayoutUnits.canMergeCarouselLayoutUnits(previousUnit, layoutUnit)
            ) {
               nextUnits[nextUnits.length - 1] = ScheduledPillLayoutUnits.mergeLayoutUnits(
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

   static mergeUnderMinDisplayLayoutUnits(
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
            ScheduledPillLayoutUnits.isUnderMinDisplayLayoutUnit(layoutUnit, minDisplayMinutes)
            && nextUnit
            && ScheduledPillLayoutUnits.underMinLayoutUnitsNeedMerge(layoutUnit, nextUnit, minDisplayMinutes)
            && ScheduledPillLayoutUnits.canMergeCarouselLayoutUnits(layoutUnit, nextUnit)
         ) {
            nextUnits.push(ScheduledPillLayoutUnits.mergeLayoutUnits(layoutUnit, nextUnit));
            index += 2;
            changed = true;
            continue;
         }

         if (
            ScheduledPillLayoutUnits.isUnderMinDisplayLayoutUnit(layoutUnit, minDisplayMinutes)
            && nextUnits.length > 0
            && ScheduledPillLayoutUnits.underMinLayoutUnitsNeedMerge(
               nextUnits[nextUnits.length - 1],
               layoutUnit,
               minDisplayMinutes
            )
            && ScheduledPillLayoutUnits.canMergeCarouselLayoutUnits(nextUnits[nextUnits.length - 1], layoutUnit)
         ) {
            nextUnits[nextUnits.length - 1] = ScheduledPillLayoutUnits.mergeLayoutUnits(
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

   static absorbHeadOrphanLayoutUnits(
      layoutUnits = [],
      minDisplayMinutes = ScheduledPillOverlap.getScheduledPillMinDisplayMinutes()
   ) {
      if (layoutUnits.length < 2) {
         return layoutUnits;
      }

      const firstUnit = layoutUnits[0];
      const secondUnit = layoutUnits[1];

      if (
         !ScheduledPillLayoutUnits.isUnderMinDisplayLayoutUnit(firstUnit, minDisplayMinutes)
         || !ScheduledPillLayoutUnits.areConsecutiveLayoutUnits(firstUnit, secondUnit)
         || !ScheduledPillLayoutUnits.canMergeCarouselLayoutUnits(firstUnit, secondUnit)
      ) {
         return layoutUnits;
      }

      return [
         ScheduledPillLayoutUnits.mergeLayoutUnits(firstUnit, secondUnit),
         ...layoutUnits.slice(2),
      ];
   }

   static isTailOrphanLayoutUnit(
      layoutUnit = {},
      minDisplayMinutes = ScheduledPillOverlap.getScheduledPillMinDisplayMinutes()
   ) {
      const items = ScheduledPillLayoutUnits.getLayoutUnitItems(layoutUnit);
      const wallSpanMinutes = ScheduledPillLayoutUnits.getClusterWallSpanMinutes(items);

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

   static absorbTailOrphanLayoutUnits(
      layoutUnits = [],
      minDisplayMinutes = ScheduledPillOverlap.getScheduledPillMinDisplayMinutes()
   ) {
      if (layoutUnits.length < 2) {
         return layoutUnits;
      }

      const lastUnit = layoutUnits[layoutUnits.length - 1];

      if (!ScheduledPillLayoutUnits.isTailOrphanLayoutUnit(lastUnit, minDisplayMinutes)) {
         return layoutUnits;
      }

      const previousUnit = layoutUnits[layoutUnits.length - 2];

      if (!ScheduledPillLayoutUnits.canMergeCarouselLayoutUnits(previousUnit, lastUnit)) {
         return layoutUnits;
      }

      return [
         ...layoutUnits.slice(0, -2),
         ScheduledPillLayoutUnits.mergeLayoutUnits(previousUnit, lastUnit),
      ];
   }

   static getEarliestScheduledItemByStartTime(items = []) {
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

   static getLayoutUnitAnchorItem(layoutUnit = {}) {
      return ScheduledPillLayoutUnits.getEarliestScheduledItemByStartTime(ScheduledPillLayoutUnits.getLayoutUnitItems(layoutUnit));
   }

   static buildClusterLayoutItem(items = []) {
      const displayItems = ScheduledPillOverlap.sortScheduledItemsForGroupDisplay(items);
      const startMinutes = Math.min(...items.map((item) => item.startMinutes));
      const endMinutes = Math.max(...items.map(ScheduledPillOverlap.getScheduledItemEndMinutes));
      const anchorItem = ScheduledPillLayoutUnits.getEarliestScheduledItemByStartTime(items);
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

   static areConsecutiveScheduledItems(previousItem = {}, nextItem = {}) {
      return ScheduledPillOverlap.getScheduledItemEndMinutes(previousItem) === nextItem.startMinutes;
   }

   static isAnimalScheduledItem(scheduledItem = {}) {
      return scheduledItem.scheduleItemKind === ScheduleItemKind.ANIMAL.itemType;
   }

   static areAdjacentOrOverlappingScheduledItems(previousItem = {}, nextItem = {}) {
      const previousEndMinutes = ScheduledPillLayoutUnits.getLayoutUnitEndMinutes(previousItem);
      const nextStartMinutes = Number(nextItem.startMinutes);

      if (!Number.isFinite(previousEndMinutes) || !Number.isFinite(nextStartMinutes)) {
         return false;
      }

      return nextStartMinutes <= previousEndMinutes;
   }

   static canGroupScheduledItemsByViewingWalkNode(previousItem = {}, nextItem = {}) {
      if (!ScheduledPillLayoutUnits.isAnimalScheduledItem(nextItem)) {
         return false;
      }

      const previousItems = ScheduledPillLayoutUnits.getLayoutUnitItems(previousItem);

      if (!previousItems.every(ScheduledPillLayoutUnits.isAnimalScheduledItem)) {
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

      return ScheduledPillLayoutUnits.areAdjacentOrOverlappingScheduledItems(previousItem, nextItem);
   }

   static flushViewingWalkNodeClusterItems(clusterItems = [], clusters = []) {
      if (clusterItems.length === 1) {
         clusters.push(clusterItems[0]);
      }
      else if (clusterItems.length > 1) {
         clusters.push(ScheduledPillLayoutUnits.buildClusterLayoutItem(clusterItems));
      }
   }

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

         normalizedUnits = ScheduledPillLayoutUnits.mergeConsecutiveUnderMinDisplayLayoutUnits(
            ScheduledPillLayoutUnits.absorbTailOrphanLayoutUnits(
               ScheduledPillLayoutUnits.absorbHeadOrphanLayoutUnits(normalizedUnits, minDisplayMinutes),
               minDisplayMinutes
            ),
            minDisplayMinutes
         );
         const underMinMergeResult = ScheduledPillLayoutUnits.mergeUnderMinDisplayLayoutUnits(
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
      const anchorItem = ScheduledPillLayoutUnits.getLayoutUnitAnchorItem(layoutUnit);
      const anchorSlotMinutes = layoutUnit.anchorSlotMinutes
         ?? anchorItem?.anchorSlotMinutes;
      const slotEndMinutes = layoutUnit.slotEndMinutes
         ?? anchorItem?.slotEndMinutes
         ?? (
            Number.isFinite(anchorSlotMinutes)
               ? anchorSlotMinutes + TimelineLayoutConstants.TIMELINE_SLOT_MINUTES
               : TimelineLayoutConstants.TIMELINE_SLOT_MINUTES
         );
      const slotSpanMinutes = slotEndMinutes - anchorSlotMinutes;

      return {
         anchorSlotMinutes,
         slotEndMinutes,
         slotSpanMinutes: Number.isFinite(slotSpanMinutes) && slotSpanMinutes > 0
            ? slotSpanMinutes
            : TimelineLayoutConstants.TIMELINE_SLOT_MINUTES,
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
            && ScheduledPillLayoutUnits.canGroupScheduledItemsByViewingWalkNode(previousItem, scheduledItem)
         ) {
            clusterItems.push(scheduledItem);
            return;
         }

         ScheduledPillLayoutUnits.flushViewingWalkNodeClusterItems(clusterItems, clusters);

         const lastCluster = clusters[clusters.length - 1];

         if (
            lastCluster
            && ScheduledPillLayoutUnits.canGroupScheduledItemsByViewingWalkNode(lastCluster, scheduledItem)
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

      ScheduledPillLayoutUnits.flushViewingWalkNodeClusterItems(clusterItems, clusters);

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
         const itemDurationMinutes = ScheduledPillLayoutUnits.getScheduledItemDurationMinutes(item);

         if (itemDurationMinutes >= minDisplayMinutes) {
            clusters.push(item);
            index += 1;
            continue;
         }

         const clusterItems = [item];
         index += 1;

         while (
            index < sortedItems.length
            && ScheduledPillLayoutUnits.getClusterWallSpanMinutes(clusterItems) < minDisplayMinutes
         ) {
            const nextItem = sortedItems[index];

            if (!ScheduledPillLayoutUnits.areConsecutiveScheduledItems(
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
               : ScheduledPillLayoutUnits.buildClusterLayoutItem(clusterItems)
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
