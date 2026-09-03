import { ApiClient } from './apiClient.js';

export function getSpeciesOptions() {
   return ApiClient.postJson('/get-species', {});
}

export function getExhibitOptions() {
   return ApiClient.postJson('/get-exhibits', {});
}

export function getRestaurantNameOptions() {
   return ApiClient.postJson('/get-restaurant-names', {});
}

export function getRestroomNameOptions() {
   return ApiClient.postJson('/get-restroom-names', {});
}

export function getGiftShopNameOptions() {
   return ApiClient.postJson('/get-gift-shop-names', {});
}

export function getAttractionNameOptions() {
   return ApiClient.postJson('/get-attraction-names', {});
}

export function getTransportationStationNameOptions() {
   return ApiClient.postJson('/get-transportation-station-names', {});
}

export function getGuardiansTalkNameOptions() {
   return ApiClient.postJson('/get-guardians-talk-names', {});
}

export function getWildEncounterNameOptions() {
   return ApiClient.postJson('/get-wild-encounter-names', {});
}

export function getActiveUpdateOptions() {
   return ApiClient.postJson('/get-active-update-options', {});
}

export function setAnimalOffDisplay(payload) {
   return ApiClient.postJson('/set-animal-off-display', payload);
}

export function setAnimalOnDisplay(payload) {
   return ApiClient.postJson('/set-animal-on-display', payload);
}

export function setAnimalViewingAlert(payload) {
   return ApiClient.postJson('/set-animal-viewing-alert', payload);
}

export function removeAnimalViewingAlert(payload) {
   return ApiClient.postJson('/remove-animal-viewing-alert', payload);
}

export function setAnimalVisibilitySchedule(payload) {
   return ApiClient.postJson('/set-animal-visibility-schedule', payload);
}

export function removeAnimalVisibilitySchedule(payload) {
   return ApiClient.postJson('/remove-animal-visibility-schedule', payload);
}

export function setExhibitOpen(payload) {
   return ApiClient.postJson('/set-exhibit-open', payload);
}

export function setExhibitClosed(payload) {
   return ApiClient.postJson('/set-exhibit-closed', payload);
}

export function setRestaurantOpeningSchedule(payload) {
   return ApiClient.postJson('/set-restaurant-opening-schedule', payload);
}

export function replaceRestaurantOpeningScheduleOverlaps(payload) {
   return ApiClient.postJson('/replace-restaurant-opening-schedule-overlaps', payload);
}

export function trimRestaurantOpeningScheduleOverlaps(payload) {
   return ApiClient.postJson('/trim-restaurant-opening-schedule-overlaps', payload);
}

export function setRestaurantClosed(payload) {
   return ApiClient.postJson('/set-restaurant-closed', payload);
}

export function setRestaurantClosureOverride(payload) {
   return ApiClient.postJson('/set-restaurant-closure-override', payload);
}

export function setRestroomOpen(payload) {
   return ApiClient.postJson('/set-restroom-open', payload);
}

export function setRestroomClosed(payload) {
   return ApiClient.postJson('/set-restroom-closed', payload);
}

export function setRestroomAlert(payload) {
   return ApiClient.postJson('/set-restroom-alert', payload);
}

export function removeRestroomAlert(payload) {
   return ApiClient.postJson('/remove-restroom-alert', payload);
}

export function createUpdate(payload) {
   return ApiClient.postJson('/create-update', payload);
}

export function createEvent(payload) {
   return ApiClient.postJson('/create-event', payload);
}

export function endUpdate(payload) {
   return ApiClient.postJson('/end-update', payload);
}

export function editUpdate(payload) {
   return ApiClient.postJson('/edit-update', payload);
}

export function setGiftShopOpeningSchedule(payload) {
   return ApiClient.postJson('/set-gift-shop-opening-schedule', payload);
}

export function replaceGiftShopOpeningScheduleOverlaps(payload) {
   return ApiClient.postJson('/replace-gift-shop-opening-schedule-overlaps', payload);
}

export function trimGiftShopOpeningScheduleOverlaps(payload) {
   return ApiClient.postJson('/trim-gift-shop-opening-schedule-overlaps', payload);
}

export function setGiftShopClosed(payload) {
   return ApiClient.postJson('/set-gift-shop-closed', payload);
}

export function setGiftShopClosureOverride(payload) {
   return ApiClient.postJson('/set-gift-shop-closure-override', payload);
}

export function setAttractionOpeningSchedule(payload) {
   return ApiClient.postJson('/set-attraction-opening-schedule', payload);
}

export function replaceAttractionOpeningScheduleOverlaps(payload) {
   return ApiClient.postJson('/replace-attraction-opening-schedule-overlaps', payload);
}

export function trimAttractionOpeningScheduleOverlaps(payload) {
   return ApiClient.postJson('/trim-attraction-opening-schedule-overlaps', payload);
}

export function setAttractionClosed(payload) {
   return ApiClient.postJson('/set-attraction-closed', payload);
}

export function setAttractionClosureOverride(payload) {
   return ApiClient.postJson('/set-attraction-closure-override', payload);
}

export function getAttractionHoursScheduleTimeBounds(payload = {}) {
   return ApiClient.postJson('/get-attraction-hours-schedule-time-bounds', payload);
}

export function setAttractionHoursSchedule(payload) {
   return ApiClient.postJson('/set-attraction-hours-schedule', payload);
}

export function replaceAttractionHoursScheduleOverlaps(payload) {
   return ApiClient.postJson('/replace-attraction-hours-schedule-overlaps', payload);
}

export function trimAttractionHoursScheduleOverlaps(payload) {
   return ApiClient.postJson('/trim-attraction-hours-schedule-overlaps', payload);
}

export function setTransportationStationOpen(payload) {
   return ApiClient.postJson('/set-transportation-station-open', payload);
}

export function setTransportationStationClosed(payload) {
   return ApiClient.postJson('/set-transportation-station-closed', payload);
}

export function setCurrentTransportationRoute(payload) {
   return ApiClient.postJson('/set-current-transportation-route', payload);
}

export function getGuardiansTalkLocations() {
   return ApiClient.postJson('/get-guardians-talk-locations', {});
}

export function getGuardiansTalkNamesAtLocation(payload) {
   return ApiClient.postJson('/get-guardians-talk-names-at-location', payload);
}

export function setGuardiansTalkSchedule(payload) {
   return ApiClient.postJson('/set-guardians-talk-schedule', payload);
}

export function replaceGuardiansTalkScheduleOverlaps(payload) {
   return ApiClient.postJson('/replace-guardians-talk-schedule-overlaps', payload);
}

export function trimGuardiansTalkScheduleOverlaps(payload) {
   return ApiClient.postJson('/trim-guardians-talk-schedule-overlaps', payload);
}

export function endGuardiansTalkSchedule(payload) {
   return ApiClient.postJson('/end-guardians-talk-schedule', payload);
}

export function getGuardiansTalkOccurrences(payload) {
   return ApiClient.postJson('/get-guardians-talk-occurrences', payload);
}

export function getGuardiansTalkScheduleTimes(payload) {
   return ApiClient.postJson('/get-guardians-talk-schedule-times', payload);
}

export function cancelGuardiansTalkOccurrence(payload) {
   return ApiClient.postJson('/cancel-guardians-talk-occurrence', payload);
}

export function addGuardiansTalkOccurrence(payload) {
   return ApiClient.postJson('/add-guardians-talk-occurrence', payload);
}

export function setWildEncounterSchedule(payload) {
   return ApiClient.postJson('/set-wild-encounter-schedule', payload);
}

export function replaceWildEncounterScheduleOverlaps(payload) {
   return ApiClient.postJson('/replace-wild-encounter-schedule-overlaps', payload);
}

export function trimWildEncounterScheduleOverlaps(payload) {
   return ApiClient.postJson('/trim-wild-encounter-schedule-overlaps', payload);
}

export function endWildEncounterSchedule(payload) {
   return ApiClient.postJson('/end-wild-encounter-schedule', payload);
}

export function getWildEncounterScheduleTimes(payload) {
   return ApiClient.postJson('/get-wild-encounter-schedule-times', payload);
}

export function getWildEncounterOccurrences(payload) {
   return ApiClient.postJson('/get-wild-encounter-occurrences', payload);
}

export function cancelWildEncounterOccurrence(payload) {
   return ApiClient.postJson('/cancel-wild-encounter-occurrence', payload);
}

export function setDrinkingFountainsClosed(payload) {
   return ApiClient.postJson('/set-drinking-fountains-closed', payload);
}

export function setDrinkingFountainsOpen(payload) {
   return ApiClient.postJson('/set-drinking-fountains-open', payload);
}
