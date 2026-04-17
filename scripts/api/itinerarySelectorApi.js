import { postJson } from './apiClient.js';

export function getExhibitsByRegionRequest(payload) {
   return postJson('/get-exhibits-by-region', payload);
}

export function getAnimalsByExhibitRequest(payload) {
   return postJson('/get-animals-by-exhibit', payload);
}
