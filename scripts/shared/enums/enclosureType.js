import { ValueNormalizer } from '../../api/valueNormalizer.js';

export class EnclosureType {
   static INDOOR = 'Indoor';
   static OUTDOOR = 'Outdoor';

   static normalizeEnclosureType(value) {
      const normalized = ValueNormalizer.asTrimmedString(value);

      return ENCLOSURE_TYPES.has(normalized)
         ? normalized
         : null;
   }

   static isEnclosureType(value) {
      return EnclosureType.normalizeEnclosureType(value) !== null;
   }
}

const ENCLOSURE_TYPES = new Set([
   EnclosureType.INDOOR,
   EnclosureType.OUTDOOR,
]);
