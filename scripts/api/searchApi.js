import { postJson } from './apiClient.js';

export function searchZoo(payload) {
   return postJson('/search', payload);
}

export function searchItineraryItems(endpoint, payload) {
   return postJson(endpoint, payload);
}
