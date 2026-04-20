import { postJson } from './apiClient.js';
import {
   asArray,
   asObject,
   asTrimmedString,
} from './normalizeValues.js';

function asStringArray(value) {
   return asArray(value)
      .map(asTrimmedString)
      .filter(Boolean);
}

function normalizeRouteResponse(response) {
   const source = asObject(response);

   return {
      route: asTrimmedString(source.route).toLowerCase(),
      zoomobileStations: asArray(source.zoomobile_stations),
   };
}

export async function getVisibleAnimals(payload) {
   const response = await postJson('/get-visible-animals', payload);
   return asArray(asObject(response).animals);
}

export async function getPavilions() {
   const response = await postJson('/get-pavilions', {});
   return asArray(asObject(response).pavilions);
}

export async function getRestaurants(payload) {
   const response = await postJson('/get-restaurants', payload);
   return asArray(asObject(response).restaurants);
}

export async function getRestrooms() {
   const response = await postJson('/get-restrooms', {});
   return asArray(asObject(response).restrooms);
}

export async function getGiftShops(payload) {
   const response = await postJson('/get-gift-shops', payload);
   return asArray(asObject(response).gift_shops);
}

export async function getAttractions(payload) {
   const response = await postJson('/get-attractions', payload);
   return asArray(asObject(response).attractions);
}

export async function getZoomobileRoute(payload) {
   const response = await postJson('/get-zoomobile-route', payload);
   return normalizeRouteResponse(response);
}

export async function getGuardiansTalks(payload) {
   const response = await postJson('/get-guardians-talks', payload);
   return asArray(asObject(response).guardians_talks);
}

export async function getWildEncounters(payload) {
   const response = await postJson('/get-wild-encounters', payload);
   return asArray(asObject(response).wild_encounters);
}

export async function getExhibits() {
   const response = await postJson('/get-exhibits', {});
   return asArray(asObject(response).exhibits);
}

export async function getClosedExhibits(payload) {
   const response = await postJson('/get-closed-exhibits', payload);
   return asStringArray(asObject(response).closed_exhibits);
}
