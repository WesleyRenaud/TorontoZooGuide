export class ScheduledPillViewingWalkNode {
   static normalizeViewingWalkNodeId(value) {
      return String(value ?? '').trim();
   }

   static getAnimalViewingWalkNodeId(animal = {}) {
      return ScheduledPillViewingWalkNode.normalizeViewingWalkNodeId(animal.viewing_walk_node_id);
   }

   static getScheduledItemViewingWalkNodeId(scheduledItem = {}) {
      return ScheduledPillViewingWalkNode.normalizeViewingWalkNodeId(
         scheduledItem.viewingWalkNodeId
         ?? scheduledItem.item?.viewing_walk_node_id
      );
   }

}
