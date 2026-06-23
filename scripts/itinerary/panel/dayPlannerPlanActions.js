function itemHasScheduleTimes(item) {
   return Boolean(String(item?.start_time ?? '').trim())
      && Boolean(String(item?.end_time ?? '').trim());
}

function collectionHasScheduledItems(items) {
   return Array.isArray(items)
      && items.some(itemHasScheduleTimes);
}

export function hasScheduledItineraryItems(itinerary = {}) {
   return collectionHasScheduledItems(itinerary.animals)
      || collectionHasScheduledItems(itinerary.attractions)
      || collectionHasScheduledItems(itinerary.guardiansTalks)
      || collectionHasScheduledItems(itinerary.wildEncounters)
      || collectionHasScheduledItems(itinerary.events);
}
