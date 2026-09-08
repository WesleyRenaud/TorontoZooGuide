import { ItineraryShape } from './itineraryShape.js';

export class ItineraryNormalizerHelpers {
   static normalizeItinerarySource(itinerary) {
      const source = itinerary && typeof itinerary === 'object'
         ? itinerary
         : {};

      return {
         date: source.date,
         arrivalTime: source.arrivalTime,
         departureTime: source.departureTime,
         selectedExhibits: source.selectedExhibits,
         animals: ItineraryShape.normalizeItineraryItems(source.animals),
         attractions: ItineraryShape.normalizeItineraryItems(source.attractions),
         guardiansTalks: ItineraryShape.normalizeItineraryItems(source.guardiansTalks),
         wildEncounters: ItineraryShape.normalizeItineraryItems(source.wildEncounters),
         transportations: ItineraryShape.normalizeItineraryItems(source.transportations),
         transportationStations: ItineraryShape.normalizeItineraryItems(source.transportationStations),
         events: ItineraryShape.normalizeItineraryItems(source.events),
      };
   }
}
