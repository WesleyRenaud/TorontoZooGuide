import { ItineraryNormalizerHelpers } from './itineraryNormalizerHelpers.js';
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
         ItineraryNormalizerHelpers.normalizeItinerarySource(itinerary)
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
         ItineraryNormalizerHelpers.normalizeItinerarySource(itinerary)
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

