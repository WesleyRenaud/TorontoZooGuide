import { NamedItems } from './namedItems.js';

export class ConsoleOptionsLoaderHelpers {
   static cachedOptionSets = {
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

   static async loadCachedOptions({
      cacheKey,
      fetchOptions,
      resultKey,
      sortOptions = NamedItems.sortNamedOptions,
   } = {}) {
      if (ConsoleOptionsLoaderHelpers.cachedOptionSets[cacheKey]) {
         return ConsoleOptionsLoaderHelpers.cachedOptionSets[cacheKey];
      }

      const result = await fetchOptions();
      const options = result?.[resultKey] ?? [];

      ConsoleOptionsLoaderHelpers.cachedOptionSets[cacheKey] = sortOptions(options);

      return ConsoleOptionsLoaderHelpers.cachedOptionSets[cacheKey];
   }
}
