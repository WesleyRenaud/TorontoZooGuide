import { ValueNormalizer } from '../api/valueNormalizer.js';

export class AnimalIdentity {
   static normalizeAnimalIdentityFields(source = {}) {
      return {
         species: ValueNormalizer.asTrimmedString(source?.species),
         exhibit: ValueNormalizer.asTrimmedString(source?.exhibit),
         enclosure_name: ValueNormalizer.asNullableString(source?.enclosure_name),
      };
   }

   static normalizeAnimalIdentitySearchFields(source = {}) {
      const { species, exhibit, enclosure_name } = AnimalIdentity.normalizeAnimalIdentityFields(source);

      return {
         species: species.toLowerCase(),
         exhibit: exhibit.toLowerCase(),
         enclosure_name: enclosure_name ? enclosure_name.toLowerCase() : '',
      };
   }

   static buildAnimalIdentityComparisonKey(source = {}) {
      const { species, exhibit, enclosure_name } = AnimalIdentity.normalizeAnimalIdentitySearchFields(source);

      return [species, exhibit, enclosure_name].join('||');
   }

   static buildAnimalIdentityStorageKey(source = {}) {
      const { species, exhibit, enclosure_name } = AnimalIdentity.normalizeAnimalIdentitySearchFields(source);

      if (!species) {
         return '';
      }

      const base = `${species}||${exhibit}`;

      return enclosure_name ? `${base}||${enclosure_name}` : base;
   }

   static normalizeAnimalForSave(source) {
      if (!source || typeof source !== 'object') {
         return null;
      }

      const { species, exhibit, enclosure_name } = AnimalIdentity.normalizeAnimalIdentityFields(source);

      if (!species || !exhibit) {
         return null;
      }

      return {
         species,
         exhibit,
         ...(enclosure_name ? { enclosure_name } : {}),
      };
   }
}
