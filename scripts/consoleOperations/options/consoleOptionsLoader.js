import { ConsoleOperationsApi } from '../../api/consoleOperationsApi.js';
import { ConsoleOptionsLoaderHelpers } from './consoleOptionsLoaderHelpers.js';

export class ConsoleOptionsLoader {
   static async loadSpecies() {
      return ConsoleOptionsLoaderHelpers.loadCachedOptions({
         cacheKey: 'species',
         fetchOptions: ConsoleOperationsApi.getSpeciesOptions,
         resultKey: 'species',
      });
   }

   static async loadExhibits() {
      return ConsoleOptionsLoaderHelpers.loadCachedOptions({
         cacheKey: 'exhibits',
         fetchOptions: ConsoleOperationsApi.getExhibitOptions,
         resultKey: 'exhibits',
      });
   }

   static async loadRestaurants() {
      return ConsoleOptionsLoaderHelpers.loadCachedOptions({
         cacheKey: 'restaurants',
         fetchOptions: ConsoleOperationsApi.getRestaurantNameOptions,
         resultKey: 'restaurants',
      });
   }

   static async loadRestrooms() {
      return ConsoleOptionsLoaderHelpers.loadCachedOptions({
         cacheKey: 'restrooms',
         fetchOptions: ConsoleOperationsApi.getRestroomNameOptions,
         resultKey: 'restrooms',
      });
   }

   static async loadGiftShops() {
      return ConsoleOptionsLoaderHelpers.loadCachedOptions({
         cacheKey: 'giftShops',
         fetchOptions: ConsoleOperationsApi.getGiftShopNameOptions,
         resultKey: 'gift_shops',
      });
   }

   static async loadAttractions() {
      return ConsoleOptionsLoaderHelpers.loadCachedOptions({
         cacheKey: 'attractions',
         fetchOptions: ConsoleOperationsApi.getAttractionNameOptions,
         resultKey: 'attractions',
      });
   }

   static async loadTransportationStations() {
      return ConsoleOptionsLoaderHelpers.loadCachedOptions({
         cacheKey: 'transportationStations',
         fetchOptions: ConsoleOperationsApi.getTransportationStationNameOptions,
         resultKey: 'transportation_stations',
      });
   }

   static async loadGuardiansTalks() {
      return ConsoleOptionsLoaderHelpers.loadCachedOptions({
         cacheKey: 'guardiansTalks',
         fetchOptions: ConsoleOperationsApi.getGuardiansTalkNameOptions,
         resultKey: 'guardians_talks',
      });
   }

   static async loadWildEncounters() {
      return ConsoleOptionsLoaderHelpers.loadCachedOptions({
         cacheKey: 'wildEncounters',
         fetchOptions: ConsoleOperationsApi.getWildEncounterNameOptions,
         resultKey: 'wild_encounters',
      });
   }
}
