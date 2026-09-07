import { ScheduledPillLayoutUnits } from './scheduledPillLayoutUnits.js';
import { ScheduledPillOverlap } from './scheduledPillOverlap.js';
import { ScheduledPillRenderPlanBuilder } from './scheduledPillRenderPlanBuilder.js';

export class ScheduledPillRenderPlan {
   static planScheduledPillRenderGroupsByAnchor(
      scheduledItems = [],
      _pointPillMarkers = []
   ) {
      const groupsByAnchor = new Map();
      const minDisplayMinutes = ScheduledPillOverlap.getScheduledPillMinDisplayMinutes();
      const viewingNodeLayoutUnits = ScheduledPillLayoutUnits.clusterScheduledAnimalItemsByViewingWalkNode(
         scheduledItems
      );
      const layoutUnitsByRenderAnchor = ScheduledPillRenderPlanBuilder.assignLayoutUnitsByRenderAnchor(
         viewingNodeLayoutUnits
      );
      const sortedAnchorSlots = [...layoutUnitsByRenderAnchor.keys()].sort((
         left,
         right
      ) => left - right);

      sortedAnchorSlots.forEach((anchorSlotMinutes) => {
         const layoutUnits = ScheduledPillLayoutUnits.normalizeLayoutUnitsForDisplay(
            ScheduledPillLayoutUnits.clusterShortScheduledItemsForDisplay(
               layoutUnitsByRenderAnchor.get(anchorSlotMinutes) ?? []
            ),
            minDisplayMinutes
         ).sort(ScheduledPillLayoutUnits.compareScheduledItemsForLayout);

         layoutUnits.forEach((layoutUnit) => {
            ScheduledPillRenderPlanBuilder.appendRenderGroup(
               groupsByAnchor,
               anchorSlotMinutes,
               ScheduledPillRenderPlanBuilder.buildRenderGroup(layoutUnit, 0)
            );
         });
      });

      groupsByAnchor.forEach((groups) => {
         groups.sort(ScheduledPillRenderPlanBuilder.compareRenderGroupsForDisplay);
      });

      return groupsByAnchor;
   }

}
