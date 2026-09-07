import { ValueNormalizer } from '../api/valueNormalizer.js';
import { ItineraryPathNormalizer } from './itineraryPathNormalizer.js';

export class ItineraryPathModel {
   static EMPTY_ITINERARY_PATH = Object.freeze({
      stops: [],
      legs: [],
      points: [],
   });

   static resolveItineraryPath(options, itinerary) {
      return options?.itineraryPath
         ?? itinerary?.itineraryPath
         ?? ItineraryPathModel.EMPTY_ITINERARY_PATH;
   }

   static normalizeItineraryPath(itineraryPath) {
      const source = ValueNormalizer.asObject(itineraryPath);

      return {
         stops: ValueNormalizer.asArray(source.stops).map(ItineraryPathNormalizer.normalizeItineraryPathStop),
         legs: ValueNormalizer.asArray(source.legs).map(ItineraryPathNormalizer.normalizeItineraryPathLeg),
         points: ValueNormalizer.asArray(source.points).map(ItineraryPathNormalizer.normalizeItineraryPathPoint),
      };
   }
}
