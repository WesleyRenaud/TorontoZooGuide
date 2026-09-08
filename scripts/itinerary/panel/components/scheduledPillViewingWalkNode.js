import { ValueNormalizer } from '../../../api/valueNormalizer.js';

export class ScheduledPillViewingWalkNode {
   static getAnimalViewingWalkNodeId(animal = {}) {
      return ValueNormalizer.asTrimmedString(animal.viewing_walk_node_id);
   }

   static getScheduledItemViewingWalkNodeId(scheduledItem = {}) {
      return ValueNormalizer.asTrimmedString(
         scheduledItem.viewingWalkNodeId
         ?? scheduledItem.item?.viewing_walk_node_id
      );
   }

}
