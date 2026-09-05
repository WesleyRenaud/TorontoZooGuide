import { ConsoleOperationsApi } from '../../api/consoleOperationsApi.js';
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

async function loadCachedOptions({
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

export async function loadSpecies() {
   return loadCachedOptions({
      cacheKey: 'species',
      fetchOptions: ConsoleOperationsApi.getSpeciesOptions,
      resultKey: 'species',
   });
}

export async function loadExhibits() {
   return loadCachedOptions({
      cacheKey: 'exhibits',
      fetchOptions: ConsoleOperationsApi.getExhibitOptions,
      resultKey: 'exhibits',
   });
}

export async function loadRestaurants() {
   return loadCachedOptions({
      cacheKey: 'restaurants',
      fetchOptions: ConsoleOperationsApi.getRestaurantNameOptions,
      resultKey: 'restaurants',
   });
}

export async function loadRestrooms() {
   return loadCachedOptions({
      cacheKey: 'restrooms',
      fetchOptions: ConsoleOperationsApi.getRestroomNameOptions,
      resultKey: 'restrooms',
   });
}

export async function loadGiftShops() {
   return loadCachedOptions({
      cacheKey: 'giftShops',
      fetchOptions: ConsoleOperationsApi.getGiftShopNameOptions,
      resultKey: 'gift_shops',
   });
}

export async function loadAttractions() {
   return loadCachedOptions({
      cacheKey: 'attractions',
      fetchOptions: ConsoleOperationsApi.getAttractionNameOptions,
      resultKey: 'attractions',
   });
}

export async function loadTransportationStations() {
   return loadCachedOptions({
      cacheKey: 'transportationStations',
      fetchOptions: ConsoleOperationsApi.getTransportationStationNameOptions,
      resultKey: 'transportation_stations',
   });
}

export async function loadGuardiansTalks() {
   return loadCachedOptions({
      cacheKey: 'guardiansTalks',
      fetchOptions: ConsoleOperationsApi.getGuardiansTalkNameOptions,
      resultKey: 'guardians_talks',
   });
}

export async function loadWildEncounters() {
   return loadCachedOptions({
      cacheKey: 'wildEncounters',
      fetchOptions: ConsoleOperationsApi.getWildEncounterNameOptions,
      resultKey: 'wild_encounters',
   });
}
