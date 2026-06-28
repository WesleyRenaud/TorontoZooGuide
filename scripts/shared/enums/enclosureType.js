import { asTrimmedString } from '../../api/normalizeValues.js';

export const EnclosureType = Object.freeze({
   INDOOR: 'Indoor',
   OUTDOOR: 'Outdoor',
});

const ENCLOSURE_TYPES = new Set(Object.values(EnclosureType));

export function normalizeEnclosureType(value) {
   const normalized = asTrimmedString(value);

   return ENCLOSURE_TYPES.has(normalized)
      ? normalized
      : null;
}

export function isEnclosureType(value) {
   return normalizeEnclosureType(value) !== null;
}
