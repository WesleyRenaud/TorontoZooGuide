import { ScheduledPillChecker } from './scheduledPillChecker.js';
import { ScheduledPillLayoutHelper } from './scheduledPillLayoutHelper.js';

export class ScheduledPillRenderPlanBuilder {
   static appendRenderGroup(groupsByAnchor, anchorSlotMinutes, renderGroup) {
      const groups = groupsByAnchor.get(anchorSlotMinutes) ?? [];

      groups.push(renderGroup);
      groupsByAnchor.set(anchorSlotMinutes, groups);
   }

   static buildRenderGroup(layoutUnit, horizontalOffsetIndex) {
      const items = ScheduledPillLayoutHelper.getLayoutUnitItems(layoutUnit);
      const { slotSpanMinutes } = ScheduledPillLayoutHelper.getLayoutUnitSlotContext(layoutUnit);
      const startMinutes = Math.min(...items.map((item) => item.startMinutes));
      const endMinutes = Math.max(...items.map(ScheduledPillChecker.getScheduledItemEndMinutes));
      const wallDurationMinutes = endMinutes - startMinutes;
      const minDisplayMinutes = ScheduledPillChecker.getScheduledPillMinDisplayMinutes();
      const grouped = items.length > 1;
      const visualBand = ScheduledPillChecker.getScheduledPillVisualBand({
         summaryItems: items,
      });

      return {
         items,
         offsetFraction: ScheduledPillLayoutHelper.getLayoutUnitScheduleOffsetFraction(layoutUnit),
         slotSpanMinutes,
         horizontalOffsetIndex,
         durationMinutes: wallDurationMinutes,
         displayDurationMinutes: Math.max(wallDurationMinutes, minDisplayMinutes),
         visualStartMinutes: visualBand.startMinutes,
         visualEndMinutes: visualBand.endMinutes,
         label: grouped
            ? ScheduledPillChecker.formatScheduledPillGroupLabel(items)
            : undefined,
      };
   }

   static compareRenderGroupsForDisplay(leftGroup = {}, rightGroup = {}) {
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

   static assignLayoutUnitsByRenderAnchor(layoutUnits = []) {
      return layoutUnits.reduce((unitsByAnchor, layoutUnit) => {
         const { anchorSlotMinutes } = ScheduledPillLayoutHelper.getLayoutUnitSlotContext(layoutUnit);

         if (!Number.isFinite(anchorSlotMinutes)) {
            return unitsByAnchor;
         }

         const units = unitsByAnchor.get(anchorSlotMinutes) ?? [];

         units.push(layoutUnit);
         unitsByAnchor.set(anchorSlotMinutes, units);

         return unitsByAnchor;
      }, new Map());
   }
}
