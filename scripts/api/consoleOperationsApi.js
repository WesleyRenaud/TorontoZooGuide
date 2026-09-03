import { ApiClient } from './apiClient.js';

export class ConsoleOperationsApi {
   static getSpeciesOptions() {
      return ApiClient.postJson('/get-species', {});
   }

   static getExhibitOptions() {
      return ApiClient.postJson('/get-exhibits', {});
   }

   static getRestaurantNameOptions() {
      return ApiClient.postJson('/get-restaurant-names', {});
   }

   static getRestroomNameOptions() {
      return ApiClient.postJson('/get-restroom-names', {});
   }

   static getGiftShopNameOptions() {
      return ApiClient.postJson('/get-gift-shop-names', {});
   }

   static getAttractionNameOptions() {
      return ApiClient.postJson('/get-attraction-names', {});
   }

   static getTransportationStationNameOptions() {
      return ApiClient.postJson('/get-transportation-station-names', {});
   }

   static getGuardiansTalkNameOptions() {
      return ApiClient.postJson('/get-guardians-talk-names', {});
   }

   static getWildEncounterNameOptions() {
      return ApiClient.postJson('/get-wild-encounter-names', {});
   }

   static getActiveUpdateOptions() {
      return ApiClient.postJson('/get-active-update-options', {});
   }

   static setAnimalOffDisplay(payload) {
      return ApiClient.postJson('/set-animal-off-display', payload);
   }

   static setAnimalOnDisplay(payload) {
      return ApiClient.postJson('/set-animal-on-display', payload);
   }

   static setAnimalViewingAlert(payload) {
      return ApiClient.postJson('/set-animal-viewing-alert', payload);
   }

   static removeAnimalViewingAlert(payload) {
      return ApiClient.postJson('/remove-animal-viewing-alert', payload);
   }

   static setAnimalVisibilitySchedule(payload) {
      return ApiClient.postJson('/set-animal-visibility-schedule', payload);
   }

   static removeAnimalVisibilitySchedule(payload) {
      return ApiClient.postJson('/remove-animal-visibility-schedule', payload);
   }

   static setExhibitOpen(payload) {
      return ApiClient.postJson('/set-exhibit-open', payload);
   }

   static setExhibitClosed(payload) {
      return ApiClient.postJson('/set-exhibit-closed', payload);
   }

   static setRestaurantOpeningSchedule(payload) {
      return ApiClient.postJson('/set-restaurant-opening-schedule', payload);
   }

   static replaceRestaurantOpeningScheduleOverlaps(payload) {
      return ApiClient.postJson('/replace-restaurant-opening-schedule-overlaps', payload);
   }

   static trimRestaurantOpeningScheduleOverlaps(payload) {
      return ApiClient.postJson('/trim-restaurant-opening-schedule-overlaps', payload);
   }

   static setRestaurantClosed(payload) {
      return ApiClient.postJson('/set-restaurant-closed', payload);
   }

   static setRestaurantClosureOverride(payload) {
      return ApiClient.postJson('/set-restaurant-closure-override', payload);
   }

   static setRestroomOpen(payload) {
      return ApiClient.postJson('/set-restroom-open', payload);
   }

   static setRestroomClosed(payload) {
      return ApiClient.postJson('/set-restroom-closed', payload);
   }

   static setRestroomAlert(payload) {
      return ApiClient.postJson('/set-restroom-alert', payload);
   }

   static removeRestroomAlert(payload) {
      return ApiClient.postJson('/remove-restroom-alert', payload);
   }

   static createUpdate(payload) {
      return ApiClient.postJson('/create-update', payload);
   }

   static createEvent(payload) {
      return ApiClient.postJson('/create-event', payload);
   }

   static endUpdate(payload) {
      return ApiClient.postJson('/end-update', payload);
   }

   static editUpdate(payload) {
      return ApiClient.postJson('/edit-update', payload);
   }

   static setGiftShopOpeningSchedule(payload) {
      return ApiClient.postJson('/set-gift-shop-opening-schedule', payload);
   }

   static replaceGiftShopOpeningScheduleOverlaps(payload) {
      return ApiClient.postJson('/replace-gift-shop-opening-schedule-overlaps', payload);
   }

   static trimGiftShopOpeningScheduleOverlaps(payload) {
      return ApiClient.postJson('/trim-gift-shop-opening-schedule-overlaps', payload);
   }

   static setGiftShopClosed(payload) {
      return ApiClient.postJson('/set-gift-shop-closed', payload);
   }

   static setGiftShopClosureOverride(payload) {
      return ApiClient.postJson('/set-gift-shop-closure-override', payload);
   }

   static setAttractionOpeningSchedule(payload) {
      return ApiClient.postJson('/set-attraction-opening-schedule', payload);
   }

   static replaceAttractionOpeningScheduleOverlaps(payload) {
      return ApiClient.postJson('/replace-attraction-opening-schedule-overlaps', payload);
   }

   static trimAttractionOpeningScheduleOverlaps(payload) {
      return ApiClient.postJson('/trim-attraction-opening-schedule-overlaps', payload);
   }

   static setAttractionClosed(payload) {
      return ApiClient.postJson('/set-attraction-closed', payload);
   }

   static setAttractionClosureOverride(payload) {
      return ApiClient.postJson('/set-attraction-closure-override', payload);
   }

   static getAttractionHoursScheduleTimeBounds(payload = {}) {
      return ApiClient.postJson('/get-attraction-hours-schedule-time-bounds', payload);
   }

   static setAttractionHoursSchedule(payload) {
      return ApiClient.postJson('/set-attraction-hours-schedule', payload);
   }

   static replaceAttractionHoursScheduleOverlaps(payload) {
      return ApiClient.postJson('/replace-attraction-hours-schedule-overlaps', payload);
   }

   static trimAttractionHoursScheduleOverlaps(payload) {
      return ApiClient.postJson('/trim-attraction-hours-schedule-overlaps', payload);
   }

   static setTransportationStationOpen(payload) {
      return ApiClient.postJson('/set-transportation-station-open', payload);
   }

   static setTransportationStationClosed(payload) {
      return ApiClient.postJson('/set-transportation-station-closed', payload);
   }

   static setCurrentTransportationRoute(payload) {
      return ApiClient.postJson('/set-current-transportation-route', payload);
   }

   static getGuardiansTalkLocations() {
      return ApiClient.postJson('/get-guardians-talk-locations', {});
   }

   static getGuardiansTalkNamesAtLocation(payload) {
      return ApiClient.postJson('/get-guardians-talk-names-at-location', payload);
   }

   static setGuardiansTalkSchedule(payload) {
      return ApiClient.postJson('/set-guardians-talk-schedule', payload);
   }

   static replaceGuardiansTalkScheduleOverlaps(payload) {
      return ApiClient.postJson('/replace-guardians-talk-schedule-overlaps', payload);
   }

   static trimGuardiansTalkScheduleOverlaps(payload) {
      return ApiClient.postJson('/trim-guardians-talk-schedule-overlaps', payload);
   }

   static endGuardiansTalkSchedule(payload) {
      return ApiClient.postJson('/end-guardians-talk-schedule', payload);
   }

   static getGuardiansTalkOccurrences(payload) {
      return ApiClient.postJson('/get-guardians-talk-occurrences', payload);
   }

   static getGuardiansTalkScheduleTimes(payload) {
      return ApiClient.postJson('/get-guardians-talk-schedule-times', payload);
   }

   static cancelGuardiansTalkOccurrence(payload) {
      return ApiClient.postJson('/cancel-guardians-talk-occurrence', payload);
   }

   static addGuardiansTalkOccurrence(payload) {
      return ApiClient.postJson('/add-guardians-talk-occurrence', payload);
   }

   static setWildEncounterSchedule(payload) {
      return ApiClient.postJson('/set-wild-encounter-schedule', payload);
   }

   static replaceWildEncounterScheduleOverlaps(payload) {
      return ApiClient.postJson('/replace-wild-encounter-schedule-overlaps', payload);
   }

   static trimWildEncounterScheduleOverlaps(payload) {
      return ApiClient.postJson('/trim-wild-encounter-schedule-overlaps', payload);
   }

   static endWildEncounterSchedule(payload) {
      return ApiClient.postJson('/end-wild-encounter-schedule', payload);
   }

   static getWildEncounterScheduleTimes(payload) {
      return ApiClient.postJson('/get-wild-encounter-schedule-times', payload);
   }

   static getWildEncounterOccurrences(payload) {
      return ApiClient.postJson('/get-wild-encounter-occurrences', payload);
   }

   static cancelWildEncounterOccurrence(payload) {
      return ApiClient.postJson('/cancel-wild-encounter-occurrence', payload);
   }

   static setDrinkingFountainsClosed(payload) {
      return ApiClient.postJson('/set-drinking-fountains-closed', payload);
   }

   static setDrinkingFountainsOpen(payload) {
      return ApiClient.postJson('/set-drinking-fountains-open', payload);
   }
}
