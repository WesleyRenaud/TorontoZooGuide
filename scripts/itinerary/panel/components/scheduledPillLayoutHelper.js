import { DayPlannerTimelineRenderer } from '../dayPlannerTimelineRenderer.js';
import { ScheduledPillChecker } from './scheduledPillChecker.js';
import { ScheduledPillViewingWalkModel } from './scheduledPillViewingWalkModel.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';
import { TimelineLayoutConstants } from '../../../shared/timelineLayoutConstants.js';

export class ScheduledPillLayoutHelper {
   static getScheduledItemDurationMinutes(scheduledItem = {}) {
      const endMinutes = ScheduledPillChecker.getScheduledItemEndMinutes(scheduledItem);
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
      const endMinutes = Math.max(...items.map(ScheduledPillChecker.getScheduledItemEndMinutes));

      return endMinutes - startMinutes;
   }

   static isCarouselMergeableItem(scheduledItem = {}) {
      return ScheduleItemKind.isScheduleItemModuleItemType(scheduledItem.scheduleItemKind);
   }

   static canMergeCarouselLayoutUnits(leftUnit = {}, rightUnit = {}) {
      return [...ScheduledPillLayoutHelper.getLayoutUnitItems(leftUnit), ...ScheduledPillLayoutHelper.getLayoutUnitItems(rightUnit)]
         .every(ScheduledPillLayoutHelper.isCarouselMergeableItem);
   }

   static mergeLayoutUnits(leftUnit = {}, rightUnit = {}) {
      const items = ScheduledPillChecker.sortScheduledItemsForGroupDisplay([
         ...ScheduledPillLayoutHelper.getLayoutUnitItems(leftUnit),
         ...ScheduledPillLayoutHelper.getLayoutUnitItems(rightUnit),
      ]);

      if (items.length === 1) {
         return items[0];
      }

      return ScheduledPillLayoutHelper.buildClusterLayoutItem(items);
   }

   static getLayoutUnitStartMinutes(layoutUnit = {}) {
      return Math.min(
         ...ScheduledPillLayoutHelper.getLayoutUnitItems(layoutUnit).map((item) => item.startMinutes)
      );
   }

   static getLayoutUnitEndMinutes(layoutUnit = {}) {
      return Math.max(
         ...ScheduledPillLayoutHelper.getLayoutUnitItems(layoutUnit).map(ScheduledPillChecker.getScheduledItemEndMinutes)
      );
   }

   static getLayoutUnitWallSpanMinutes(layoutUnit = {}) {
      return ScheduledPillLayoutHelper.getClusterWallSpanMinutes(ScheduledPillLayoutHelper.getLayoutUnitItems(layoutUnit));
   }

   static areConsecutiveLayoutUnits(leftUnit = {}, rightUnit = {}) {
      return ScheduledPillLayoutHelper.getLayoutUnitEndMinutes(leftUnit) === ScheduledPillLayoutHelper.getLayoutUnitStartMinutes(rightUnit);
   }

   static isUnderMinDisplayLayoutUnit(
      layoutUnit = {},
      minDisplayMinutes = ScheduledPillChecker.getScheduledPillMinDisplayMinutes()
   ) {
      return ScheduledPillLayoutHelper.getLayoutUnitWallSpanMinutes(layoutUnit) < minDisplayMinutes;
   }

   static underMinLayoutUnitsNeedMerge(
      leftUnit = {},
      rightUnit = {},
      minDisplayMinutes = ScheduledPillChecker.getScheduledPillMinDisplayMinutes()
   ) {
      const leftStartMinutes = ScheduledPillLayoutHelper.getLayoutUnitStartMinutes(leftUnit);
      const leftEndMinutes = ScheduledPillLayoutHelper.getLayoutUnitEndMinutes(leftUnit);
      const rightStartMinutes = ScheduledPillLayoutHelper.getLayoutUnitStartMinutes(rightUnit);
      const rightEndMinutes = ScheduledPillLayoutHelper.getLayoutUnitEndMinutes(rightUnit);

      if (
         !Number.isFinite(leftStartMinutes)
         || !Number.isFinite(leftEndMinutes)
         || !Number.isFinite(rightStartMinutes)
         || !Number.isFinite(rightEndMinutes)
      ) {
         return false;
      }

      return (
         ScheduledPillLayoutHelper.isUnderMinDisplayLayoutUnit(leftUnit, minDisplayMinutes)
         && leftStartMinutes + minDisplayMinutes >= rightStartMinutes
      ) || (
         ScheduledPillLayoutHelper.isUnderMinDisplayLayoutUnit(rightUnit, minDisplayMinutes)
         && rightEndMinutes - minDisplayMinutes <= leftEndMinutes
      );
   }

   static mergeConsecutiveUnderMinDisplayLayoutUnits(
      layoutUnits = [],
      minDisplayMinutes = ScheduledPillChecker.getScheduledPillMinDisplayMinutes()
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
               && ScheduledPillLayoutHelper.areConsecutiveLayoutUnits(previousUnit, layoutUnit)
               && ScheduledPillLayoutHelper.isUnderMinDisplayLayoutUnit(previousUnit, minDisplayMinutes)
               && ScheduledPillLayoutHelper.canMergeCarouselLayoutUnits(previousUnit, layoutUnit)
            ) {
               nextUnits[nextUnits.length - 1] = ScheduledPillLayoutHelper.mergeLayoutUnits(
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
      minDisplayMinutes = ScheduledPillChecker.getScheduledPillMinDisplayMinutes()
   ) {
      const nextUnits = [];
      let index = 0;
      let changed = false;

      while (index < layoutUnits.length) {
         const layoutUnit = layoutUnits[index];
         const nextUnit = layoutUnits[index + 1];

         if (
            ScheduledPillLayoutHelper.isUnderMinDisplayLayoutUnit(layoutUnit, minDisplayMinutes)
            && nextUnit
            && ScheduledPillLayoutHelper.underMinLayoutUnitsNeedMerge(layoutUnit, nextUnit, minDisplayMinutes)
            && ScheduledPillLayoutHelper.canMergeCarouselLayoutUnits(layoutUnit, nextUnit)
         ) {
            nextUnits.push(ScheduledPillLayoutHelper.mergeLayoutUnits(layoutUnit, nextUnit));
            index += 2;
            changed = true;
            continue;
         }

         if (
            ScheduledPillLayoutHelper.isUnderMinDisplayLayoutUnit(layoutUnit, minDisplayMinutes)
            && nextUnits.length > 0
            && ScheduledPillLayoutHelper.underMinLayoutUnitsNeedMerge(
               nextUnits[nextUnits.length - 1],
               layoutUnit,
               minDisplayMinutes
            )
            && ScheduledPillLayoutHelper.canMergeCarouselLayoutUnits(nextUnits[nextUnits.length - 1], layoutUnit)
         ) {
            nextUnits[nextUnits.length - 1] = ScheduledPillLayoutHelper.mergeLayoutUnits(
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
      minDisplayMinutes = ScheduledPillChecker.getScheduledPillMinDisplayMinutes()
   ) {
      if (layoutUnits.length < 2) {
         return layoutUnits;
      }

      const firstUnit = layoutUnits[0];
      const secondUnit = layoutUnits[1];

      if (
         !ScheduledPillLayoutHelper.isUnderMinDisplayLayoutUnit(firstUnit, minDisplayMinutes)
         || !ScheduledPillLayoutHelper.areConsecutiveLayoutUnits(firstUnit, secondUnit)
         || !ScheduledPillLayoutHelper.canMergeCarouselLayoutUnits(firstUnit, secondUnit)
      ) {
         return layoutUnits;
      }

      return [
         ScheduledPillLayoutHelper.mergeLayoutUnits(firstUnit, secondUnit),
         ...layoutUnits.slice(2),
      ];
   }

   static isTailOrphanLayoutUnit(
      layoutUnit = {},
      minDisplayMinutes = ScheduledPillChecker.getScheduledPillMinDisplayMinutes()
   ) {
      const items = ScheduledPillLayoutHelper.getLayoutUnitItems(layoutUnit);
      const wallSpanMinutes = ScheduledPillLayoutHelper.getClusterWallSpanMinutes(items);

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
      minDisplayMinutes = ScheduledPillChecker.getScheduledPillMinDisplayMinutes()
   ) {
      if (layoutUnits.length < 2) {
         return layoutUnits;
      }

      const lastUnit = layoutUnits[layoutUnits.length - 1];

      if (!ScheduledPillLayoutHelper.isTailOrphanLayoutUnit(lastUnit, minDisplayMinutes)) {
         return layoutUnits;
      }

      const previousUnit = layoutUnits[layoutUnits.length - 2];

      if (!ScheduledPillLayoutHelper.canMergeCarouselLayoutUnits(previousUnit, lastUnit)) {
         return layoutUnits;
      }

      return [
         ...layoutUnits.slice(0, -2),
         ScheduledPillLayoutHelper.mergeLayoutUnits(previousUnit, lastUnit),
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
      return ScheduledPillLayoutHelper.getEarliestScheduledItemByStartTime(ScheduledPillLayoutHelper.getLayoutUnitItems(layoutUnit));
   }

   static buildClusterLayoutItem(items = []) {
      const displayItems = ScheduledPillChecker.sortScheduledItemsForGroupDisplay(items);
      const startMinutes = Math.min(...items.map((item) => item.startMinutes));
      const endMinutes = Math.max(...items.map(ScheduledPillChecker.getScheduledItemEndMinutes));
      const anchorItem = ScheduledPillLayoutHelper.getEarliestScheduledItemByStartTime(items);
      const layoutUnit = {
         clusterItems: displayItems,
         startMinutes,
         endMinutes,
         maximumDuration: endMinutes - startMinutes,
         anchorSlotMinutes: anchorItem?.anchorSlotMinutes,
         slotEndMinutes: anchorItem?.slotEndMinutes,
         label: ScheduledPillChecker.formatScheduledPillGroupLabel(displayItems),
      };

      return {
         ...layoutUnit,
         offsetFraction: ScheduledPillLayoutHelper.getLayoutUnitScheduleOffsetFraction(layoutUnit),
      };
   }

   static areConsecutiveScheduledItems(previousItem = {}, nextItem = {}) {
      return ScheduledPillChecker.getScheduledItemEndMinutes(previousItem) === nextItem.startMinutes;
   }

   static isAnimalScheduledItem(scheduledItem = {}) {
      return scheduledItem.scheduleItemKind === ScheduleItemKind.ANIMAL.itemType;
   }

   static areAdjacentOrOverlappingScheduledItems(previousItem = {}, nextItem = {}) {
      const previousEndMinutes = ScheduledPillLayoutHelper.getLayoutUnitEndMinutes(previousItem);
      const nextStartMinutes = Number(nextItem.startMinutes);

      if (!Number.isFinite(previousEndMinutes) || !Number.isFinite(nextStartMinutes)) {
         return false;
      }

      return nextStartMinutes <= previousEndMinutes;
   }

   static canGroupScheduledItemsByViewingWalkNode(previousItem = {}, nextItem = {}) {
      if (!ScheduledPillLayoutHelper.isAnimalScheduledItem(nextItem)) {
         return false;
      }

      const previousItems = ScheduledPillLayoutHelper.getLayoutUnitItems(previousItem);

      if (!previousItems.every(ScheduledPillLayoutHelper.isAnimalScheduledItem)) {
         return false;
      }

      const nextNodeId = ScheduledPillViewingWalkModel.getScheduledItemViewingWalkNodeId(nextItem);

      if (!nextNodeId) {
         return false;
      }

      if (!previousItems.every((item) => (
         ScheduledPillViewingWalkModel.getScheduledItemViewingWalkNodeId(item) === nextNodeId
      ))) {
         return false;
      }

      return ScheduledPillLayoutHelper.areAdjacentOrOverlappingScheduledItems(previousItem, nextItem);
   }

   static flushViewingWalkNodeClusterItems(clusterItems = [], clusters = []) {
      if (clusterItems.length === 1) {
         clusters.push(clusterItems[0]);
      }
      else if (clusterItems.length > 1) {
         clusters.push(ScheduledPillLayoutHelper.buildClusterLayoutItem(clusterItems));
      }
   }

   static compareScheduledItemsForLayout(leftItem = {}, rightItem = {}) {
      const startDelta = leftItem.startMinutes - rightItem.startMinutes;

      if (startDelta !== 0) {
         return startDelta;
      }

      return ScheduledPillChecker.compareScheduledItemLabels(leftItem, rightItem);
   }


   static getLayoutUnitItems(scheduledItem = {}) {
      return scheduledItem.clusterItems
         ?? scheduledItem.summaryItems
         ?? [scheduledItem];
   }


   static normalizeLayoutUnitsForDisplay(
      layoutUnits = [],
      minDisplayMinutes = ScheduledPillChecker.getScheduledPillMinDisplayMinutes()
   ) {
      let normalizedUnits = [...layoutUnits];
      let changed = true;

      while (changed) {
         const previousUnits = normalizedUnits;

         normalizedUnits = ScheduledPillLayoutHelper.mergeConsecutiveUnderMinDisplayLayoutUnits(
            ScheduledPillLayoutHelper.absorbTailOrphanLayoutUnits(
               ScheduledPillLayoutHelper.absorbHeadOrphanLayoutUnits(normalizedUnits, minDisplayMinutes),
               minDisplayMinutes
            ),
            minDisplayMinutes
         );
         const underMinMergeResult = ScheduledPillLayoutHelper.mergeUnderMinDisplayLayoutUnits(
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
      const anchorItem = ScheduledPillLayoutHelper.getLayoutUnitAnchorItem(layoutUnit);
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
      const items = ScheduledPillLayoutHelper.getLayoutUnitItems(layoutUnit);
      const { anchorSlotMinutes, slotEndMinutes } = ScheduledPillLayoutHelper.getLayoutUnitSlotContext(layoutUnit);
      const startMinutes = Math.min(...items.map((item) => item.startMinutes));

      return DayPlannerTimelineRenderer.computeMarkerOffsetFraction(
         startMinutes,
         anchorSlotMinutes,
         slotEndMinutes
      );
   }


   static clusterScheduledAnimalItemsByViewingWalkNode(scheduledItems = []) {
      const sortedItems = [...scheduledItems].sort(ScheduledPillLayoutHelper.compareScheduledItemsForLayout);
      const clusters = [];
      let clusterItems = [];

      sortedItems.forEach((scheduledItem) => {
         const previousItem = clusterItems[clusterItems.length - 1];

         if (
            previousItem
            && ScheduledPillLayoutHelper.canGroupScheduledItemsByViewingWalkNode(previousItem, scheduledItem)
         ) {
            clusterItems.push(scheduledItem);
            return;
         }

         ScheduledPillLayoutHelper.flushViewingWalkNodeClusterItems(clusterItems, clusters);

         const lastCluster = clusters[clusters.length - 1];

         if (
            lastCluster
            && ScheduledPillLayoutHelper.canGroupScheduledItemsByViewingWalkNode(lastCluster, scheduledItem)
         ) {
            clusters.pop();
            clusterItems = [
               ...ScheduledPillLayoutHelper.getLayoutUnitItems(lastCluster),
               scheduledItem,
            ];
            return;
         }

         clusterItems = [scheduledItem];
      });

      ScheduledPillLayoutHelper.flushViewingWalkNodeClusterItems(clusterItems, clusters);

      return clusters;
   }


   static clusterShortScheduledItemsForDisplay(
      scheduledItems = [],
      minDisplayMinutes = ScheduledPillChecker.getScheduledPillMinDisplayMinutes()
   ) {
      const sortedItems = [...scheduledItems].sort(ScheduledPillLayoutHelper.compareScheduledItemsForLayout);
      const clusters = [];
      let index = 0;

      while (index < sortedItems.length) {
         const item = sortedItems[index];
         const itemDurationMinutes = ScheduledPillLayoutHelper.getScheduledItemDurationMinutes(item);

         if (itemDurationMinutes >= minDisplayMinutes) {
            clusters.push(item);
            index += 1;
            continue;
         }

         const clusterItems = [item];
         index += 1;

         while (
            index < sortedItems.length
            && ScheduledPillLayoutHelper.getClusterWallSpanMinutes(clusterItems) < minDisplayMinutes
         ) {
            const nextItem = sortedItems[index];

            if (!ScheduledPillLayoutHelper.areConsecutiveScheduledItems(
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
               : ScheduledPillLayoutHelper.buildClusterLayoutItem(clusterItems)
         );
      }

      return clusters;
   }


   static clusterScheduledItemsByDuration(
      scheduledItems = [],
      minDisplayMinutes = ScheduledPillChecker.getScheduledPillMinDisplayMinutes(),
      _windowStartMinutes = 0
   ) {
      return ScheduledPillLayoutHelper.clusterShortScheduledItemsForDisplay(
         scheduledItems,
         minDisplayMinutes
      );
   }


   /** @deprecated */
   static clusterScheduledItemsByStartTimeProximity(...args) {
      return ScheduledPillLayoutHelper.clusterScheduledItemsByDuration(...args);
   }
}
