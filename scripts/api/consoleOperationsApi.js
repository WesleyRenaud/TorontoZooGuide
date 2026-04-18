import { postJson } from './apiClient.js';

export function getSpeciesOptions() {
   return postJson('/get-species', {});
}

export function getExhibitOptions() {
   return postJson('/get-exhibits', {});
}

export function getRestaurantNameOptions() {
   return postJson('/get-restaurant-names', {});
}

export function getGiftShopNameOptions() {
   return postJson('/get-gift-shop-names', {});
}

export function getAttractionNameOptions() {
   return postJson('/get-attraction-names', {});
}

export function getZoomobileStationNameOptions() {
   return postJson('/get-zoomobile-station-names', {});
}

export function getGuardiansTalkNameOptions() {
   return postJson('/get-guardians-talk-names', {});
}

export function getWildEncounterNameOptions() {
   return postJson('/get-wild-encounter-names', {});
}

export function getAnimalNamesByExhibit(payload) {
   return postJson('/get-animal-names-by-exhibit', payload);
}

export function setAnimalOffDisplay(payload) {
   return postJson('/set-animal-off-display', payload);
}

export function setAnimalOnDisplay(payload) {
   return postJson('/set-animal-on-display', payload);
}

export function setAnimalViewingAlert(payload) {
   return postJson('/set-animal-viewing-alert', payload);
}

export function removeAnimalViewingAlert(payload) {
   return postJson('/remove-animal-viewing-alert', payload);
}

export function setAnimalVisibilitySchedule(payload) {
   return postJson('/set-animal-visibility-schedule', payload);
}

export function removeAnimalVisibilitySchedule(payload) {
   return postJson('/remove-animal-visibility-schedule', payload);
}

export function setExhibitOpen(payload) {
   return postJson('/set-exhibit-open', payload);
}

export function setExhibitClosed(payload) {
   return postJson('/set-exhibit-closed', payload);
}

export function setRestaurantOpeningSchedule(payload) {
   return postJson('/set-restaurant-opening-schedule', payload);
}

export function setRestaurantClosed(payload) {
   return postJson('/set-restaurant-closed', payload);
}

export function setGiftShopOpeningSchedule(payload) {
   return postJson('/set-gift-shop-opening-schedule', payload);
}

export function setGiftShopClosed(payload) {
   return postJson('/set-gift-shop-closed', payload);
}

export function setAttractionOpeningSchedule(payload) {
   return postJson('/set-attraction-opening-schedule', payload);
}

export function setAttractionClosed(payload) {
   return postJson('/set-attraction-closed', payload);
}

export function setZoomobileStationOpen(payload) {
   return postJson('/set-zoomobile-station-open', payload);
}

export function setZoomobileStationClosed(payload) {
   return postJson('/set-zoomobile-station-closed', payload);
}

export function setCurrentZoomobileRoute(payload) {
   return postJson('/set-current-zoomobile-route', payload);
}

export function getGuardiansTalkLocations() {
   return postJson('/get-guardians-talk-locations', {});
}

export function getGuardiansTalkNamesAtLocation(payload) {
   return postJson('/get-guardians-talk-names-at-location', payload);
}

export function setGuardiansTalkSchedule(payload) {
   return postJson('/set-guardians-talk-schedule', payload);
}

export function endGuardiansTalkSchedule(payload) {
   return postJson('/end-guardians-talk-schedule', payload);
}

export function getGuardiansTalkOccurrences(payload) {
   return postJson('/get-guardians-talk-occurrences', payload);
}

export function cancelGuardiansTalkOccurrence(payload) {
   return postJson('/cancel-guardians-talk-occurrence', payload);
}

export function setWildEncounterSchedule(payload) {
   return postJson('/set-wild-encounter-schedule', payload);
}

export function endWildEncounterSchedule(payload) {
   return postJson('/end-wild-encounter-schedule', payload);
}

export function getWildEncounterOccurrences(payload) {
   return postJson('/get-wild-encounter-occurrences', payload);
}

export function cancelWildEncounterOccurrence(payload) {
   return postJson('/cancel-wild-encounter-occurrence', payload);
}
