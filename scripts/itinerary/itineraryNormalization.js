import { EMPTY_ITINERARY_PATH } from './itineraryPathModel.js';
import {
   createEmptyItineraryDraft,
   hasSavedItineraryContent,
   isItineraryEmptyDraft,
   normalizeItineraryDraft,
   normalizeItineraryItems,
} from './itineraryShape.js';
import { buildItineraryValidationState } from './itineraryValidation.js';

export function createEmptyItinerary() {
   return {
      ...createEmptyItineraryDraft(),
      isActive: false,
   };
}

function normalizeItinerarySource(itinerary) {
   const source = itinerary && typeof itinerary === 'object'
      ? itinerary
      : {};

   return {
      date: source.date,
      arrivalTime: source.arrivalTime,
      departureTime: source.departureTime,
      animals: normalizeItineraryItems(source.animals),
      attractions: normalizeItineraryItems(source.attractions),
      guardiansTalks: normalizeItineraryItems(source.guardiansTalks),
      wildEncounters: normalizeItineraryItems(source.wildEncounters),
      events: normalizeItineraryItems(source.events),
   };
}

export function isItineraryEmpty(itinerary) {
   return isItineraryEmptyDraft(
      normalizeItinerarySource(itinerary)
   );
}

export function normalizeItineraryFromApiResult(result) {
   return normalizeItinerary({
      ...result?.itinerary,
      itineraryConfig: result?.itineraryConfig,
      itineraryPath: result?.itineraryPath,
   });
}

export function normalizeItinerary(itinerary) {
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
