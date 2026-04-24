import { postJson } from './apiClient.js';
import {
   asArray,
   asObject,
   asTrimmedString,
} from './normalizeValues.js';

const EMPTY_PAYLOAD = Object.freeze({});

function asStringArray(value) {
   return asArray(value)
      .map(asTrimmedString)
      .filter(Boolean);
}

function readResponseCollection(response, responseKey) {
   return asArray(asObject(response)[responseKey]);
}

function normalizeRouteResponse(response) {
   const source = asObject(response);

   return {
      route: asTrimmedString(source.route).toLowerCase(),
      zoomobileStations: readResponseCollection(source, 'zoomobile_stations'),
   };
}

async function fetchCollection(endpoint, responseKey, payload = EMPTY_PAYLOAD) {
   const response = await postJson(endpoint, payload);
   return readResponseCollection(response, responseKey);
}

async function fetchStringCollection(endpoint, responseKey, payload = EMPTY_PAYLOAD) {
   return asStringArray(await fetchCollection(endpoint, responseKey, payload));
}

export async function getVisibleAnimals(payload = EMPTY_PAYLOAD) {
   return await fetchCollection('/get-visible-animals', 'animals', payload);
}

export async function getPavilions() {
   return await fetchCollection('/get-pavilions', 'pavilions');
}

export async function getRestaurants(payload = EMPTY_PAYLOAD) {
   return await fetchCollection('/get-restaurants', 'restaurants', payload);
}

export async function getRestrooms() {
   return await fetchCollection('/get-restrooms', 'restrooms');
}

export async function getGiftShops(payload = EMPTY_PAYLOAD) {
   return await fetchCollection('/get-gift-shops', 'gift_shops', payload);
}

export async function getAttractions(payload = EMPTY_PAYLOAD) {
   return await fetchCollection('/get-attractions', 'attractions', payload);
}

export async function getZoomobileRoute(payload = EMPTY_PAYLOAD) {
   const response = await postJson('/get-zoomobile-route', payload);
   return normalizeRouteResponse(response);
}

export async function getGuardiansTalks(payload = EMPTY_PAYLOAD) {
   return await fetchCollection('/get-guardians-talks', 'guardians_talks', payload);
}

export async function getWildEncounters(payload = EMPTY_PAYLOAD) {
   return await fetchCollection('/get-wild-encounters', 'wild_encounters', payload);
}

export async function getExhibits() {
   return await fetchCollection('/get-exhibits', 'exhibits');
}

export async function getClosedExhibits(payload = EMPTY_PAYLOAD) {
   return await fetchStringCollection('/get-closed-exhibits', 'closed_exhibits', payload);
}
