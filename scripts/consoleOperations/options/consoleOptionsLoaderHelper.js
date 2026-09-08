import { NamedItems } from './namedItems.js';

export class ConsoleOptionsLoaderHelper {
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
      if (ConsoleOptionsLoaderHelper.cachedOptionSets[cacheKey]) {
         return ConsoleOptionsLoaderHelper.cachedOptionSets[cacheKey];
      }

      const result = await fetchOptions();
      const options = result?.[resultKey] ?? [];

      ConsoleOptionsLoaderHelper.cachedOptionSets[cacheKey] = sortOptions(options);

      return ConsoleOptionsLoaderHelper.cachedOptionSets[cacheKey];
   }
}
