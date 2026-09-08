import { NamedItems } from './namedItems.js';

const cachedOptionSets = {
   species: null,
   exhibits: null,
   restaurants: null,
   restrooms: null,
   giftShops: null,
   attractions: null,
   transportationStations: null,
   guardiansTalks: null,
   wildEncounters: null,
};

export class ConsoleOptionsLoaderHelpers {
   static async loadCachedOptions({
      cacheKey,
      fetchOptions,
      resultKey,
      sortOptions = NamedItems.sortNamedOptions,
   } = {}) {
      if (cachedOptionSets[cacheKey]) {
         return cachedOptionSets[cacheKey];
      }

      const result = await fetchOptions();
      const options = result?.[resultKey] ?? [];

      cachedOptionSets[cacheKey] = sortOptions(options);

      return cachedOptionSets[cacheKey];
   }
}
