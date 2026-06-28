export function normalizeViewingWalkNodeId(value) {
   return String(value ?? '').trim();
}

export function getAnimalViewingWalkNodeId(animal = {}) {
   return normalizeViewingWalkNodeId(animal.viewing_walk_node_id);
}

export function getScheduledItemViewingWalkNodeId(scheduledItem = {}) {
   return normalizeViewingWalkNodeId(
      scheduledItem.viewingWalkNodeId
      ?? scheduledItem.item?.viewing_walk_node_id
   );
}
