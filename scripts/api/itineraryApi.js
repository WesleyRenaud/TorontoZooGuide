import { postJson } from './apiClient.js';

export function getItineraryRequest() {
   return postJson('/get-itinerary', {});
}

export function setItineraryRequest(payload) {
   return postJson('/set-itinerary', payload);
}

export function clearItineraryRequest() {
   return postJson('/clear-itinerary', {});
}

export function validateItineraryDraftRequest(payload) {
   return postJson('/validate-itinerary', payload);
}
