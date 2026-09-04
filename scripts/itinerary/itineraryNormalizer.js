import { ItineraryPathModel } from './itineraryPathModel.js';
import { ItineraryShape } from './itineraryShape.js';
import { ItineraryValidation } from './itineraryValidation.js';

export class ItineraryNormalizer {
   static createEmptyItinerary() {
      return {
         ...ItineraryShape.createEmptyItineraryDraft(),
         isActive: false,
      };
   }

   static isItineraryEmpty(itinerary) {
      return ItineraryShape.isItineraryEmptyDraft(
         normalizeItinerarySource(itinerary)
      );
   }

   static normalizeItineraryFromApiResult(result) {
      return ItineraryNormalizer.normalizeItinerary({
         ...result?.itinerary,
         itineraryConfig: result?.itineraryConfig,
         itineraryPath: result?.itineraryPath,
      });
   }

   static normalizeItinerary(itinerary) {
      const normalizedDraft = ItineraryShape.normalizeItineraryDraft(
         normalizeItinerarySource(itinerary)
      );

      return {
         ...normalizedDraft,
         itineraryConfig: itinerary?.itineraryConfig ?? null,
         itineraryPath: itinerary?.itineraryPath ?? ItineraryPathModel.EMPTY_ITINERARY_PATH,
         validation: ItineraryValidation.buildItineraryValidationState(
            normalizedDraft,
            itinerary?.itineraryConfig ?? {}
         ),
         isActive: ItineraryShape.hasSavedItineraryContent(normalizedDraft),
      };
   }
}

function normalizeItinerarySource(itinerary) {
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
