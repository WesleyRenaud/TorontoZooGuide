import { ValueNormalizer } from '../../../api/valueNormalizer.js';

export class GroupConsecutiveTransportationLegSequencesHelper {
   static normalizeLegs(legs) {
      if (!Array.isArray(legs)) {
         return [];
      }

      return legs.map((leg) => ValueNormalizer.asObject(leg));
   }
}
