import { EMPTY_ITINERARY_PATH } from './itineraryPathModel.js';
import {
   createEmptyItineraryDraft,
   hasSavedItineraryContent,
   isItineraryEmptyDraft,
   normalizeItineraryDraft,
   normalizeItineraryItems,
} from './itineraryShape.js';
import { buildItineraryValidationState } from './itineraryValidation.js';

export class ItineraryNormalizer {
   static createEmptyItinerary() {
      return {
         ...createEmptyItineraryDraft(),
         isActive: false,
      };
   }

   static isItineraryEmpty(itinerary) {
      return isItineraryEmptyDraft(
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
      const normalizedDraft = normalizeItineraryDraft(
         normalizeItinerarySource(itinerary)
      );

      return {
         ...normalizedDraft,
         itineraryConfig: itinerary?.itineraryConfig ?? null,
         itineraryPath: itinerary?.itineraryPath ?? EMPTY_ITINERARY_PATH,
         validation: buildItineraryValidationState(
            normalizedDraft,
            itinerary?.itineraryConfig ?? {}
         ),
         isActive: hasSavedItineraryContent(normalizedDraft),
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
      animals: normalizeItineraryItems(source.animals),
      attractions: normalizeItineraryItems(source.attractions),
      guardiansTalks: normalizeItineraryItems(source.guardiansTalks),
      wildEncounters: normalizeItineraryItems(source.wildEncounters),
      transportations: normalizeItineraryItems(source.transportations),
      transportationStations: normalizeItineraryItems(source.transportationStations),
      events: normalizeItineraryItems(source.events),
   };
}
