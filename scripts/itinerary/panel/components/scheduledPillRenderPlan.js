import {
   clusterShortScheduledItemsForDisplay,
   getLayoutUnitItems,
   getLayoutUnitScheduleOffsetFraction,
   getLayoutUnitSlotContext,
   normalizeLayoutUnitsForDisplay,
} from './scheduledPillLayoutUnits.js';
import {
   formatScheduledPillGroupLabel,
   getScheduledItemEndMinutes,
   getScheduledPillMinDisplayMinutes,
   getScheduledPillVisualBand,
} from './scheduledPillOverlap.js';

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
