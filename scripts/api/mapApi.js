import { postJson } from './apiClient.js';

export function getVisibleAnimals(payload) {
   return postJson('/get-visible-animals', payload);
}

export function getPavilions() {
   return postJson('/get-pavilions', {});
}

export function getRestaurants(payload) {
   return postJson('/get-restaurants', payload);
}

export function getRestrooms() {
   return postJson('/get-restrooms', {});
}

export function getGiftShops(payload) {
   return postJson('/get-gift-shops', payload);
}

export function getAttractions(payload) {
   return postJson('/get-attractions', payload);
}

export function getZoomobileRoute(payload) {
   return postJson('/get-zoomobile-route', payload);
}

export function getGuardiansTalks(payload) {
   return postJson('/get-guardians-talks', payload);
}

export function getWildEncounters(payload) {
   return postJson('/get-wild-encounters', payload);
}

export function getExhibits() {
   return postJson('/get-exhibits', {});
}

export function getClosedExhibits(payload) {
   return postJson('/get-closed-exhibits', payload);
}
