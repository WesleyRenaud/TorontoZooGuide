import { ValueNormalizer } from '../../api/valueNormalizer.js';
import enclosureTypeValues from '../../../shared/enums/enclosureType.json' with { type: 'json' };

export class EnclosureType {
   static {
      Object.assign(EnclosureType, enclosureTypeValues);
      EnclosureType.ENCLOSURE_TYPES = new Set(Object.values(enclosureTypeValues));
   }

   static normalizeEnclosureType(value) {
      const normalized = ValueNormalizer.asTrimmedString(value);

      return EnclosureType.ENCLOSURE_TYPES.has(normalized)
         ? normalized
         : null;
   }

   static isEnclosureType(value) {
      return EnclosureType.normalizeEnclosureType(value) !== null;
   }
}
