import { ConsoleOperationsClient } from '../../api/consoleOperationsClient.js';
import { ConsoleOptionsLoaderHelper } from './consoleOptionsLoaderHelper.js';

export class ConsoleOptionsLoader {
   static async loadSpecies() {
      return ConsoleOptionsLoaderHelper.loadCachedOptions({
         cacheKey: 'species',
         fetchOptions: ConsoleOperationsClient.getSpeciesOptions,
         resultKey: 'species',
      });
   }

   static async loadExhibits() {
      return ConsoleOptionsLoaderHelper.loadCachedOptions({
         cacheKey: 'exhibits',
         fetchOptions: ConsoleOperationsClient.getExhibitOptions,
         resultKey: 'exhibits',
      });
   }

   static async loadRestaurants() {
      return ConsoleOptionsLoaderHelper.loadCachedOptions({
         cacheKey: 'restaurants',
         fetchOptions: ConsoleOperationsClient.getRestaurantNameOptions,
         resultKey: 'restaurants',
      });
   }

   static async loadRestrooms() {
      return ConsoleOptionsLoaderHelper.loadCachedOptions({
         cacheKey: 'restrooms',
         fetchOptions: ConsoleOperationsClient.getRestroomNameOptions,
         resultKey: 'restrooms',
      });
   }

   static async loadGiftShops() {
      return ConsoleOptionsLoaderHelper.loadCachedOptions({
         cacheKey: 'giftShops',
         fetchOptions: ConsoleOperationsClient.getGiftShopNameOptions,
         resultKey: 'gift_shops',
      });
   }

   static async loadAttractions() {
      return ConsoleOptionsLoaderHelper.loadCachedOptions({
         cacheKey: 'attractions',
         fetchOptions: ConsoleOperationsClient.getAttractionNameOptions,
         resultKey: 'attractions',
      });
   }

   static async loadTransportationStations() {
      return ConsoleOptionsLoaderHelper.loadCachedOptions({
         cacheKey: 'transportationStations',
         fetchOptions: ConsoleOperationsClient.getTransportationStationNameOptions,
         resultKey: 'transportation_stations',
      });
   }

   static async loadGuardiansTalks() {
      return ConsoleOptionsLoaderHelper.loadCachedOptions({
         cacheKey: 'guardiansTalks',
         fetchOptions: ConsoleOperationsClient.getGuardiansTalkNameOptions,
         resultKey: 'guardians_talks',
      });
   }

   static async loadWildEncounters() {
      return ConsoleOptionsLoaderHelper.loadCachedOptions({
         cacheKey: 'wildEncounters',
         fetchOptions: ConsoleOperationsClient.getWildEncounterNameOptions,
         resultKey: 'wild_encounters',
      });
   }
}
