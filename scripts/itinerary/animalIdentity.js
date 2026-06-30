import {
   asNullableString,
   asTrimmedString,
} from '../api/normalizeValues.js';

export function normalizeAnimalIdentityFields(source = {}) {
   return {
      species: asTrimmedString(source?.species),
      exhibit: asTrimmedString(source?.exhibit),
      enclosure_name: asNullableString(source?.enclosure_name),
   };
}

export function normalizeAnimalIdentitySearchFields(source = {}) {
   const { species, exhibit, enclosure_name } = normalizeAnimalIdentityFields(source);

   return {
      species: species.toLowerCase(),
      exhibit: exhibit.toLowerCase(),
      enclosure_name: enclosure_name ? enclosure_name.toLowerCase() : '',
   };
}

export function buildAnimalIdentityComparisonKey(source = {}) {
   const { species, exhibit, enclosure_name } = normalizeAnimalIdentitySearchFields(source);

   return [species, exhibit, enclosure_name].join('||');
}

export function buildAnimalIdentityStorageKey(source = {}) {
   const { species, exhibit, enclosure_name } = normalizeAnimalIdentitySearchFields(source);

   if (!species) {
      return '';
   }

   const base = `${species}||${exhibit}`;

   return enclosure_name ? `${base}||${enclosure_name}` : base;
}

export function normalizeAnimalForSave(source) {
   if (!source || typeof source !== 'object') {
      return null;
   }

   const { species, exhibit, enclosure_name } = normalizeAnimalIdentityFields(source);

   if (!species || !exhibit) {
      return null;
   }

   return {
      species,
      exhibit,
      ...(enclosure_name ? { enclosure_name } : {}),
   };
}
