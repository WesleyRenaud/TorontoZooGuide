import { ApiClient } from './apiClient.js';
import { NormalizeGuardiansTalkLinkedAnimals } from '../guardians/normalizeGuardiansTalkLinkedAnimals.js';
import { ValueNormalizer } from './valueNormalizer.js';

function normalizeAttractionRow(row) {
   const source = ValueNormalizer.asObject(row);

   return {
      ...source,
      name: ValueNormalizer.asTrimmedString(source.name),
      free_with_admission: ValueNormalizer.asBoolean(source.free_with_admission),
      part_of_seasonal_attraction: ValueNormalizer.asBoolean(source.part_of_seasonal_attraction),
      is_closed: ValueNormalizer.asBoolean(source.is_closed),
      is_also_transportation: ValueNormalizer.asBoolean(source.is_also_transportation),
      route_duration_minutes: ValueNormalizer.normalizeNumber(source.route_duration_minutes),
      info_link: ValueNormalizer.asNullableString(source.info_link),
      open_time: ValueNormalizer.asNullableString(source.open_time),
      close_time: ValueNormalizer.asNullableString(source.close_time),
   };
}

function normalizeGuardiansTalkRow(row) {
   const source = ValueNormalizer.asObject(row);

   return {
      ...source,
      name: ValueNormalizer.asTrimmedString(source.name),
      location: ValueNormalizer.asTrimmedString(source.location),
      start_time: ValueNormalizer.asTrimmedString(source.start_time),
      linked_animals: NormalizeGuardiansTalkLinkedAnimals.normalizeGuardiansTalkLinkedAnimals(source.linked_animals),
   };
}

function normalizeWildEncounterRow(row) {
   const source = ValueNormalizer.asObject(row);

   return {
      ...source,
      name: ValueNormalizer.asTrimmedString(source.name),
      meeting_spot: ValueNormalizer.asTrimmedString(source.meeting_spot),
      start_time: ValueNormalizer.asTrimmedString(source.start_time),
      link: ValueNormalizer.asNullableString(source.link),
   };
}

function normalizeTransportationRow(row) {
   const source = ValueNormalizer.asObject(row);

   return {
      ...source,
      name: ValueNormalizer.asTrimmedString(source.name),
      free_with_admission: ValueNormalizer.asBoolean(source.free_with_admission),
      is_also_attraction: ValueNormalizer.asBoolean(source.is_also_attraction),
      info_link: ValueNormalizer.asNullableString(source.info_link),
      open_time: ValueNormalizer.asNullableString(source.open_time),
      close_time: ValueNormalizer.asNullableString(source.close_time),
   };
}

function normalizeSearchEndpointResponse(endpoint, response) {
   if (endpoint === '/search') {
      return SearchApi.normalizeSearchResponse(response);
   }

   return response;
}

export class SearchApi {
   static normalizeSearchResponse(response) {
      const source = ValueNormalizer.asObject(response);

      return {
         animals: ValueNormalizer.asArray(source.animals),
         pavilions: ValueNormalizer.asArray(source.pavilions),
         restaurants: ValueNormalizer.asArray(source.restaurants),
         restrooms: ValueNormalizer.asArray(source.restrooms),
         gift_shops: ValueNormalizer.asArray(source.gift_shops),
         attractions: ValueNormalizer.asArray(source.attractions).map(normalizeAttractionRow),
         transportations: ValueNormalizer.asArray(source.transportations).map(normalizeTransportationRow),
         transportation_stations: ValueNormalizer.asArray(source.transportation_stations),
         guardians_talks: ValueNormalizer.asArray(source.guardians_talks).map(normalizeGuardiansTalkRow),
         wild_encounters: ValueNormalizer.asArray(source.wild_encounters).map(normalizeWildEncounterRow),
      };
   }

   static async searchItineraryItems(endpoint, payload) {
      const response = await ApiClient.postJson(endpoint, payload);
      return normalizeSearchEndpointResponse(endpoint, response);
   }

   static async searchZoo(payload) {
      return await SearchApi.searchItineraryItems('/search', payload);
   }
}
