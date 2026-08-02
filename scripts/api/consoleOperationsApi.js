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

export function getRestroomNameOptions() {
   return postJson('/get-restroom-names', {});
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

export function getActiveUpdateOptions() {
   return postJson('/get-active-update-options', {});
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

export function replaceRestaurantOpeningScheduleOverlaps(payload) {
   return postJson('/replace-restaurant-opening-schedule-overlaps', payload);
}

export function trimRestaurantOpeningScheduleOverlaps(payload) {
   return postJson('/trim-restaurant-opening-schedule-overlaps', payload);
}

export function setRestaurantClosed(payload) {
   return postJson('/set-restaurant-closed', payload);
}

export function setRestaurantClosureOverride(payload) {
   return postJson('/set-restaurant-closure-override', payload);
}

export function setRestroomOpen(payload) {
   return postJson('/set-restroom-open', payload);
}

export function setRestroomClosed(payload) {
   return postJson('/set-restroom-closed', payload);
}

export function setRestroomAlert(payload) {
   return postJson('/set-restroom-alert', payload);
}

export function removeRestroomAlert(payload) {
   return postJson('/remove-restroom-alert', payload);
}

export function createUpdate(payload) {
   return postJson('/create-update', payload);
}

export function createEvent(payload) {
   return postJson('/create-event', payload);
}

export function endUpdate(payload) {
   return postJson('/end-update', payload);
}

export function editUpdate(payload) {
   return postJson('/edit-update', payload);
}

export function setGiftShopOpeningSchedule(payload) {
   return postJson('/set-gift-shop-opening-schedule', payload);
}

export function replaceGiftShopOpeningScheduleOverlaps(payload) {
   return postJson('/replace-gift-shop-opening-schedule-overlaps', payload);
}

export function trimGiftShopOpeningScheduleOverlaps(payload) {
   return postJson('/trim-gift-shop-opening-schedule-overlaps', payload);
}

export function setGiftShopClosed(payload) {
   return postJson('/set-gift-shop-closed', payload);
}

export function setGiftShopClosureOverride(payload) {
   return postJson('/set-gift-shop-closure-override', payload);
}

export function setAttractionOpeningSchedule(payload) {
   return postJson('/set-attraction-opening-schedule', payload);
}

export function replaceAttractionOpeningScheduleOverlaps(payload) {
   return postJson('/replace-attraction-opening-schedule-overlaps', payload);
}

export function trimAttractionOpeningScheduleOverlaps(payload) {
   return postJson('/trim-attraction-opening-schedule-overlaps', payload);
}

export function setAttractionClosed(payload) {
   return postJson('/set-attraction-closed', payload);
}

export function setAttractionClosureOverride(payload) {
   return postJson('/set-attraction-closure-override', payload);
}

export function getAttractionHoursScheduleTimeBounds(payload = {}) {
   return postJson('/get-attraction-hours-schedule-time-bounds', payload);
}

export function setAttractionHoursSchedule(payload) {
   return postJson('/set-attraction-hours-schedule', payload);
}

export function replaceAttractionHoursScheduleOverlaps(payload) {
   return postJson('/replace-attraction-hours-schedule-overlaps', payload);
}

export function trimAttractionHoursScheduleOverlaps(payload) {
   return postJson('/trim-attraction-hours-schedule-overlaps', payload);
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

export function replaceGuardiansTalkScheduleOverlaps(payload) {
   return postJson('/replace-guardians-talk-schedule-overlaps', payload);
}

export function trimGuardiansTalkScheduleOverlaps(payload) {
   return postJson('/trim-guardians-talk-schedule-overlaps', payload);
}

export function endGuardiansTalkSchedule(payload) {
   return postJson('/end-guardians-talk-schedule', payload);
}

export function getGuardiansTalkOccurrences(payload) {
   return postJson('/get-guardians-talk-occurrences', payload);
}

export function getGuardiansTalkScheduleTimes(payload) {
   return postJson('/get-guardians-talk-schedule-times', payload);
}

export function cancelGuardiansTalkOccurrence(payload) {
   return postJson('/cancel-guardians-talk-occurrence', payload);
}

export function addGuardiansTalkOccurrence(payload) {
   return postJson('/add-guardians-talk-occurrence', payload);
}

export function setWildEncounterSchedule(payload) {
   return postJson('/set-wild-encounter-schedule', payload);
}

export function replaceWildEncounterScheduleOverlaps(payload) {
   return postJson('/replace-wild-encounter-schedule-overlaps', payload);
}

export function trimWildEncounterScheduleOverlaps(payload) {
   return postJson('/trim-wild-encounter-schedule-overlaps', payload);
}

export function endWildEncounterSchedule(payload) {
   return postJson('/end-wild-encounter-schedule', payload);
}

export function getWildEncounterScheduleTimes(payload) {
   return postJson('/get-wild-encounter-schedule-times', payload);
}

export function getWildEncounterOccurrences(payload) {
   return postJson('/get-wild-encounter-occurrences', payload);
}

export function cancelWildEncounterOccurrence(payload) {
   return postJson('/cancel-wild-encounter-occurrence', payload);
}

export function setDrinkingFountainsClosed(payload) {
   return postJson('/set-drinking-fountains-closed', payload);
}

export function setDrinkingFountainsOpen(payload) {
   return postJson('/set-drinking-fountains-open', payload);
}
