export function normalizeVisitBoundaryEventTypes(source = {}) {
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

export function isItineraryVisitBoundaryEventType(
   value,
   visitBoundaryEventTypes = {}
) {
   const boundaries = normalizeVisitBoundaryEventTypes(visitBoundaryEventTypes);
   const normalizedValue = String(value ?? '').trim();

   return normalizedValue === boundaries.arrival
      || normalizedValue === boundaries.departure;
}

export function buildSchedulableEventTypes(itineraryConfig = {}) {
   const eventTypes = Array.isArray(itineraryConfig?.eventTypes)
      ? itineraryConfig.eventTypes
      : [];
   const boundaries = normalizeVisitBoundaryEventTypes(
      itineraryConfig?.visitBoundaryEventTypes
   );
   const excluded = new Set(
      [boundaries.arrival, boundaries.departure].filter(Boolean)
   );

   return eventTypes.filter((eventType) => !excluded.has(eventType));
}
