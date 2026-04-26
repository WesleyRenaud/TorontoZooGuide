import {
   getAttractionNameOptions,
   getExhibitOptions,
   getGiftShopNameOptions,
   getGuardiansTalkNameOptions,
   getRestaurantNameOptions,
   getRestroomNameOptions,
   getSpeciesOptions,
   getWildEncounterNameOptions,
   getZoomobileStationNameOptions,
} from '../../api/consoleOperationsApi.js';
import { sortNamedOptions } from './namedItems.js';

const cachedOptionSets = {
   species: null,
   exhibits: null,
   restaurants: null,
   restrooms: null,
   giftShops: null,
   attractions: null,
   zoomobileStations: null,
   guardiansTalks: null,
   wildEncounters: null,
};

async function loadCachedOptions({
   cacheKey,
   fetchOptions,
   resultKey,
   sortOptions = sortNamedOptions,
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
      fetchOptions: getSpeciesOptions,
      resultKey: 'species',
   });
}

export async function loadExhibits() {
   return loadCachedOptions({
      cacheKey: 'exhibits',
      fetchOptions: getExhibitOptions,
      resultKey: 'exhibits',
   });
}

export async function loadRestaurants() {
   return loadCachedOptions({
      cacheKey: 'restaurants',
      fetchOptions: getRestaurantNameOptions,
      resultKey: 'restaurants',
   });
}

export async function loadRestrooms() {
   return loadCachedOptions({
      cacheKey: 'restrooms',
      fetchOptions: getRestroomNameOptions,
      resultKey: 'restrooms',
   });
}

export async function loadGiftShops() {
   return loadCachedOptions({
      cacheKey: 'giftShops',
      fetchOptions: getGiftShopNameOptions,
      resultKey: 'gift_shops',
   });
}

export async function loadAttractions() {
   return loadCachedOptions({
      cacheKey: 'attractions',
      fetchOptions: getAttractionNameOptions,
      resultKey: 'attractions',
   });
}

export async function loadZoomobileStations() {
   return loadCachedOptions({
      cacheKey: 'zoomobileStations',
      fetchOptions: getZoomobileStationNameOptions,
      resultKey: 'zoomobile_stations',
   });
}

export async function loadGuardiansTalks() {
   return loadCachedOptions({
      cacheKey: 'guardiansTalks',
      fetchOptions: getGuardiansTalkNameOptions,
      resultKey: 'guardians_talks',
   });
}

export async function loadWildEncounters() {
   return loadCachedOptions({
      cacheKey: 'wildEncounters',
      fetchOptions: getWildEncounterNameOptions,
      resultKey: 'wild_encounters',
   });
}
