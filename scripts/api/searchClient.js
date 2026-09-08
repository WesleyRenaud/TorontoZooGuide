import { ApiClient } from './apiClient.js';
import { SearchApiNormalizer } from './searchApiNormalizer.js';
import { ValueNormalizer } from './valueNormalizer.js';

export class SearchClient {
   static normalizeSearchResponse(response) {
      const source = ValueNormalizer.asObject(response);

      return {
         animals: ValueNormalizer.asArray(source.animals),
         pavilions: ValueNormalizer.asArray(source.pavilions),
         restaurants: ValueNormalizer.asArray(source.restaurants),
         restrooms: ValueNormalizer.asArray(source.restrooms),
         gift_shops: ValueNormalizer.asArray(source.gift_shops),
         attractions: ValueNormalizer.asArray(source.attractions).map(SearchApiNormalizer.normalizeAttractionRow),
         transportations: ValueNormalizer.asArray(source.transportations).map(SearchApiNormalizer.normalizeTransportationRow),
         transportation_stations: ValueNormalizer.asArray(source.transportation_stations),
         guardians_talks: ValueNormalizer.asArray(source.guardians_talks).map(SearchApiNormalizer.normalizeGuardiansTalkRow),
         wild_encounters: ValueNormalizer.asArray(source.wild_encounters).map(SearchApiNormalizer.normalizeWildEncounterRow),
      };
   }

   static async searchItineraryItems(endpoint, payload) {
      const response = await ApiClient.postJson(endpoint, payload);
      return SearchApiNormalizer.normalizeSearchEndpointResponse(endpoint, response);
   }

   static async searchZoo(payload) {
      return await SearchClient.searchItineraryItems('/search', payload);
   }
}
