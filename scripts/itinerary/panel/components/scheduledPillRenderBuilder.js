import { ScheduledPillChecker } from './scheduledPillChecker.js';
import { ScheduledPillLayoutHelper } from './scheduledPillLayoutHelper.js';
import { ScheduledPillRenderPlanBuilder } from './scheduledPillRenderPlanBuilder.js';

export class ScheduledPillRenderBuilder {
   static planScheduledPillRenderGroupsByAnchor(
      scheduledItems = [],
      _pointPillMarkers = []
   ) {
      const groupsByAnchor = new Map();
      const minDisplayMinutes = ScheduledPillChecker.getScheduledPillMinDisplayMinutes();
      const viewingNodeLayoutUnits = ScheduledPillLayoutHelper.clusterScheduledAnimalItemsByViewingWalkNode(
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
         const layoutUnits = ScheduledPillLayoutHelper.normalizeLayoutUnitsForDisplay(
            ScheduledPillLayoutHelper.clusterShortScheduledItemsForDisplay(
               layoutUnitsByRenderAnchor.get(anchorSlotMinutes) ?? []
            ),
            minDisplayMinutes
         ).sort(ScheduledPillLayoutHelper.compareScheduledItemsForLayout);

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
