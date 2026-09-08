import { ItineraryNormalizerHelper } from './itineraryNormalizerHelper.js';
import { ItineraryPathModel } from './itineraryPathModel.js';
import { ItineraryShape } from './itineraryShape.js';
import { ItineraryValidator } from './itineraryValidator.js';

export class ItineraryNormalizer {
   static createEmptyItinerary() {
      return {
         ...ItineraryShape.createEmptyItineraryDraft(),
         isActive: false,
      };
   }

   static isItineraryEmpty(itinerary) {
      return ItineraryShape.isItineraryEmptyDraft(
         ItineraryNormalizerHelper.normalizeItinerarySource(itinerary)
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
         ItineraryNormalizerHelper.normalizeItinerarySource(itinerary)
      );

      return {
         ...normalizedDraft,
         itineraryConfig: itinerary?.itineraryConfig ?? null,
         itineraryPath: itinerary?.itineraryPath ?? ItineraryPathModel.EMPTY_ITINERARY_PATH,
         validation: ItineraryValidator.buildItineraryValidationState(
            normalizedDraft,
            itinerary?.itineraryConfig ?? {}
         ),
         isActive: ItineraryShape.hasSavedItineraryContent(normalizedDraft),
      };
   }
}

