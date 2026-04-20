import { postJson } from './apiClient.js';
import {
   asArray,
   asBoolean,
   asNullableString,
   asObject,
   asTrimmedString,
} from './normalizeValues.js';

function normalizeAttractionRow(row) {
   const source = asObject(row);

   return {
      ...source,
      name: asTrimmedString(source.name),
      free_with_admission: asBoolean(source.free_with_admission),
      part_of_seasonal_attraction: asBoolean(source.part_of_seasonal_attraction),
      is_closed: asBoolean(source.is_closed),
      info_link: asNullableString(source.info_link),
   };
}

function normalizeGuardiansTalkRow(row) {
   const source = asObject(row);

   return {
      ...source,
      name: asTrimmedString(source.name),
      location: asTrimmedString(source.location),
      time_of_day: asTrimmedString(source.time_of_day),
   };
}

function normalizeWildEncounterRow(row) {
   const source = asObject(row);

   return {
      ...source,
      name: asTrimmedString(source.name),
      meeting_spot: asTrimmedString(source.meeting_spot),
      time_of_day: asTrimmedString(source.time_of_day),
      link: asNullableString(source.link),
   };
}

export function normalizeSearchResponse(response) {
   const source = response && typeof response === 'object'
      ? response
      : {};

   return {
      animals: asArray(source.animals),
      pavilions: asArray(source.pavilions),
      restaurants: asArray(source.restaurants),
      restrooms: asArray(source.restrooms),
      gift_shops: asArray(source.gift_shops),
      attractions: asArray(source.attractions).map(normalizeAttractionRow),
      zoomobile_stations: asArray(source.zoomobile_stations),
      guardians_talks: asArray(source.guardians_talks).map(normalizeGuardiansTalkRow),
      wild_encounters: asArray(source.wild_encounters).map(normalizeWildEncounterRow),
   };
}

export async function searchZoo(payload) {
   const response = await postJson('/search', payload);
   return normalizeSearchResponse(response);
}

export async function searchItineraryItems(endpoint, payload) {
   const response = await postJson(endpoint, payload);

   if (endpoint === '/search') {
      return normalizeSearchResponse(response);
   }

   return response;
}
