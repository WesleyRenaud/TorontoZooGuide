export class ItineraryDraftModel {
   static asItineraryDraftSource(value) {
      return value && typeof value === 'object'
         ? value
         : {};
   }

   static normalizeItineraryDate(value) {
      return typeof value === 'string'
         ? value
         : '';
   }

   static normalizeItineraryTime(value) {
      return typeof value === 'string'
         ? value
         : '';
   }

   static cloneItineraryItems(items) {
      return items.slice();
   }
}
