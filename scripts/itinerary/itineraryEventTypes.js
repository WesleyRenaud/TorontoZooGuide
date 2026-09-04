export class ItineraryEventTypes {
   static isScheduleItemEventType(selection, eventTypes = []) {
      return eventTypes.includes(selection);
   }

   static requiresRemoveItineraryItemConfirmation(itemType, itineraryConfig) {
      if (!itineraryConfig) {
         return true;
      }

      return !ItineraryEventTypes.isScheduleItemEventType(itemType, itineraryConfig.eventTypes);
   }

   static normalizeVisitBoundaryEventTypes(source = {}) {
      const visitBoundary = source && typeof source === 'object'
         ? source
         : {};

      return {
         arrival: typeof visitBoundary.arrival === 'string'
            ? visitBoundary.arrival
            : '',
         departure: typeof visitBoundary.departure === 'string'
            ? visitBoundary.departure
            : '',
      };
   }

   static isItineraryVisitBoundaryEventType(
      value,
      visitBoundaryEventTypes = {}
   ) {
      const boundaries = ItineraryEventTypes.normalizeVisitBoundaryEventTypes(
         visitBoundaryEventTypes
      );
      const normalizedValue = String(value ?? '').trim();

      return normalizedValue === boundaries.arrival
         || normalizedValue === boundaries.departure;
   }

   static buildSchedulableEventTypes(itineraryConfig) {
      if (!itineraryConfig) {
         return [];
      }

      const boundaries = ItineraryEventTypes.normalizeVisitBoundaryEventTypes(
         itineraryConfig.visitBoundaryEventTypes
      );
      const excluded = new Set(
         [boundaries.arrival, boundaries.departure].filter(Boolean)
      );

      return itineraryConfig.eventTypes.filter((eventType) => !excluded.has(eventType));
   }
}
