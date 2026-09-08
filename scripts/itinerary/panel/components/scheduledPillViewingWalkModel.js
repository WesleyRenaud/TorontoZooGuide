export class ScheduledPillViewingWalkModel {
   static normalizeViewingWalkNodeId(value) {
      return String(value ?? '').trim();
   }

   static getAnimalViewingWalkNodeId(animal = {}) {
      return ScheduledPillViewingWalkModel.normalizeViewingWalkNodeId(animal.viewing_walk_node_id);
   }

   static getScheduledItemViewingWalkNodeId(scheduledItem = {}) {
      return ScheduledPillViewingWalkModel.normalizeViewingWalkNodeId(
         scheduledItem.viewingWalkNodeId
         ?? scheduledItem.item?.viewing_walk_node_id
      );
   }

}
