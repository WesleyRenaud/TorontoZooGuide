import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { ConsoleOperationsClient } from '../../../scripts/api/consoleOperationsClient.js';
import { ApiClient } from '../../../scripts/api/apiClient.js';

const _originalPostJson = ApiClient.postJson;

function _echoPostJson() {
   ApiClient.postJson = async (url, payload) => ({ ok: true, url, payload });
}

afterEach(() => {
   ApiClient.postJson = _originalPostJson;
});


test('Test_GetSpeciesOptions_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-animal-species-names';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getSpeciesOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetExhibitOptions_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-exhibits';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getExhibitOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetClosedExhibitOptions_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-closed-exhibit-options';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getClosedExhibitOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetRestaurantNameOptions_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-restaurant-names';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getRestaurantNameOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetRestroomNameOptions_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-restroom-names';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getRestroomNameOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetClosedRestroomOptions_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-closed-restroom-options';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getClosedRestroomOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetRestroomAlertOptions_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-restroom-alert-options';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getRestroomAlertOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetGiftShopNameOptions_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-gift-shop-names';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getGiftShopNameOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetAttractionNameOptions_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-attraction-names';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getAttractionNameOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetTransportationStationNameOptions_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-transportation-station-names';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getTransportationStationNameOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetClosedTransportationStationOptions_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-closed-transportation-station-options';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getClosedTransportationStationOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetGuardiansTalkNameOptions_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-guardians-talk-names';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getGuardiansTalkNameOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetWildEncounterNameOptions_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-wild-encounter-names';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getWildEncounterNameOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetWildEncounterScheduleOptions_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-wild-encounter-schedule-options';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getWildEncounterScheduleOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetActiveUpdateOptions_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-active-update-options';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getActiveUpdateOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetGuardiansTalkLocations_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-guardians-talk-locations';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getGuardiansTalkLocations();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetGuardiansTalkScheduleLocationOptions_TestNoArgs_ExpectPosted', async () => {
   const url = '/get-guardians-talk-schedule-location-options';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getGuardiansTalkScheduleLocationOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetAnimalOffDisplay_TestPayload_ExpectPosted', async () => {
   const url = '/set-animal-off-display';
   const payload = { method: 'setAnimalOffDisplay' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setAnimalOffDisplay(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetAnimalOnDisplay_TestPayload_ExpectPosted', async () => {
   const url = '/set-animal-on-display';
   const payload = { method: 'setAnimalOnDisplay' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setAnimalOnDisplay(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetExhibitsForSpecies_TestPayload_ExpectPosted', async () => {
   const url = '/get-exhibits-for-species';
   const payload = { method: 'getExhibitsForSpecies' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.getExhibitsForSpecies(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetOffDisplayAnimalOptions_TestPayload_ExpectPosted', async () => {
   const url = '/get-off-display-animal-options';
   const payload = { method: 'getOffDisplayAnimalOptions' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.getOffDisplayAnimalOptions(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetOffDisplayExhibitOptions_TestPayload_ExpectPosted', async () => {
   const url = '/get-off-display-exhibit-options';
   const payload = { method: 'getOffDisplayExhibitOptions' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.getOffDisplayExhibitOptions(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetOffDisplayViewingScopeOptions_TestPayload_ExpectPosted', async () => {
   const url = '/get-off-display-viewing-scope-options';
   const payload = { method: 'getOffDisplayViewingScopeOptions' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.getOffDisplayViewingScopeOptions(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetAnimalVisibilityScheduleOptions_TestPayload_ExpectPosted', async () => {
   const url = '/get-animal-visibility-schedule-options';
   const payload = { method: 'getAnimalVisibilityScheduleOptions' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.getAnimalVisibilityScheduleOptions(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetAnimalVisibilityScheduleExhibitOptions_TestPayload_ExpectPosted', async () => {
   const url = '/get-animal-visibility-schedule-exhibit-options';
   const payload = { method: 'getAnimalVisibilityScheduleExhibitOptions' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.getAnimalVisibilityScheduleExhibitOptions(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetAnimalViewingAlertOptions_TestPayload_ExpectPosted', async () => {
   const url = '/get-animal-viewing-alert-options';
   const payload = { method: 'getAnimalViewingAlertOptions' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.getAnimalViewingAlertOptions(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetAnimalViewingAlertExhibitOptions_TestPayload_ExpectPosted', async () => {
   const url = '/get-animal-viewing-alert-exhibit-options';
   const payload = { method: 'getAnimalViewingAlertExhibitOptions' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.getAnimalViewingAlertExhibitOptions(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetAnimalViewingAlert_TestPayload_ExpectPosted', async () => {
   const url = '/set-animal-viewing-alert';
   const payload = { method: 'setAnimalViewingAlert' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setAnimalViewingAlert(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_RemoveAnimalViewingAlert_TestPayload_ExpectPosted', async () => {
   const url = '/remove-animal-viewing-alert';
   const payload = { method: 'removeAnimalViewingAlert' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.removeAnimalViewingAlert(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetAnimalVisibilitySchedule_TestPayload_ExpectPosted', async () => {
   const url = '/set-animal-visibility-schedule';
   const payload = { method: 'setAnimalVisibilitySchedule' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setAnimalVisibilitySchedule(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_RemoveAnimalVisibilitySchedule_TestPayload_ExpectPosted', async () => {
   const url = '/remove-animal-visibility-schedule';
   const payload = { method: 'removeAnimalVisibilitySchedule' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.removeAnimalVisibilitySchedule(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetExhibitOpen_TestPayload_ExpectPosted', async () => {
   const url = '/set-exhibit-open';
   const payload = { method: 'setExhibitOpen' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setExhibitOpen(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetExhibitClosed_TestPayload_ExpectPosted', async () => {
   const url = '/set-exhibit-closed';
   const payload = { method: 'setExhibitClosed' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setExhibitClosed(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetRestaurantOpeningSchedule_TestPayload_ExpectPosted', async () => {
   const url = '/set-restaurant-opening-schedule';
   const payload = { method: 'setRestaurantOpeningSchedule' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setRestaurantOpeningSchedule(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_ReplaceRestaurantOpeningScheduleOverlaps_TestPayload_ExpectPosted', async () => {
   const url = '/replace-restaurant-opening-schedule-overlaps';
   const payload = { method: 'replaceRestaurantOpeningScheduleOverlaps' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.replaceRestaurantOpeningScheduleOverlaps(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_TrimRestaurantOpeningScheduleOverlaps_TestPayload_ExpectPosted', async () => {
   const url = '/trim-restaurant-opening-schedule-overlaps';
   const payload = { method: 'trimRestaurantOpeningScheduleOverlaps' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.trimRestaurantOpeningScheduleOverlaps(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetRestaurantClosed_TestPayload_ExpectPosted', async () => {
   const url = '/set-restaurant-closed';
   const payload = { method: 'setRestaurantClosed' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setRestaurantClosed(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetRestaurantClosureOverride_TestPayload_ExpectPosted', async () => {
   const url = '/set-restaurant-closure-override';
   const payload = { method: 'setRestaurantClosureOverride' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setRestaurantClosureOverride(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetRestroomOpen_TestPayload_ExpectPosted', async () => {
   const url = '/set-restroom-open';
   const payload = { method: 'setRestroomOpen' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setRestroomOpen(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetRestroomClosed_TestPayload_ExpectPosted', async () => {
   const url = '/set-restroom-closed';
   const payload = { method: 'setRestroomClosed' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setRestroomClosed(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetRestroomAlert_TestPayload_ExpectPosted', async () => {
   const url = '/set-restroom-alert';
   const payload = { method: 'setRestroomAlert' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setRestroomAlert(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_RemoveRestroomAlert_TestPayload_ExpectPosted', async () => {
   const url = '/remove-restroom-alert';
   const payload = { method: 'removeRestroomAlert' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.removeRestroomAlert(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_CreateUpdate_TestPayload_ExpectPosted', async () => {
   const url = '/create-update';
   const payload = { method: 'createUpdate' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.createUpdate(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_CreateEvent_TestPayload_ExpectPosted', async () => {
   const url = '/create-event';
   const payload = { method: 'createEvent' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.createEvent(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_EndUpdate_TestPayload_ExpectPosted', async () => {
   const url = '/end-update';
   const payload = { method: 'endUpdate' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.endUpdate(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_EditUpdate_TestPayload_ExpectPosted', async () => {
   const url = '/edit-update';
   const payload = { method: 'editUpdate' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.editUpdate(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetGiftShopOpeningSchedule_TestPayload_ExpectPosted', async () => {
   const url = '/set-gift-shop-opening-schedule';
   const payload = { method: 'setGiftShopOpeningSchedule' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setGiftShopOpeningSchedule(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_ReplaceGiftShopOpeningScheduleOverlaps_TestPayload_ExpectPosted', async () => {
   const url = '/replace-gift-shop-opening-schedule-overlaps';
   const payload = { method: 'replaceGiftShopOpeningScheduleOverlaps' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.replaceGiftShopOpeningScheduleOverlaps(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_TrimGiftShopOpeningScheduleOverlaps_TestPayload_ExpectPosted', async () => {
   const url = '/trim-gift-shop-opening-schedule-overlaps';
   const payload = { method: 'trimGiftShopOpeningScheduleOverlaps' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.trimGiftShopOpeningScheduleOverlaps(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetGiftShopClosed_TestPayload_ExpectPosted', async () => {
   const url = '/set-gift-shop-closed';
   const payload = { method: 'setGiftShopClosed' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setGiftShopClosed(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetGiftShopClosureOverride_TestPayload_ExpectPosted', async () => {
   const url = '/set-gift-shop-closure-override';
   const payload = { method: 'setGiftShopClosureOverride' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setGiftShopClosureOverride(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetAttractionOpeningSchedule_TestPayload_ExpectPosted', async () => {
   const url = '/set-attraction-opening-schedule';
   const payload = { method: 'setAttractionOpeningSchedule' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setAttractionOpeningSchedule(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_ReplaceAttractionOpeningScheduleOverlaps_TestPayload_ExpectPosted', async () => {
   const url = '/replace-attraction-opening-schedule-overlaps';
   const payload = { method: 'replaceAttractionOpeningScheduleOverlaps' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.replaceAttractionOpeningScheduleOverlaps(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_TrimAttractionOpeningScheduleOverlaps_TestPayload_ExpectPosted', async () => {
   const url = '/trim-attraction-opening-schedule-overlaps';
   const payload = { method: 'trimAttractionOpeningScheduleOverlaps' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.trimAttractionOpeningScheduleOverlaps(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetAttractionClosed_TestPayload_ExpectPosted', async () => {
   const url = '/set-attraction-closed';
   const payload = { method: 'setAttractionClosed' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setAttractionClosed(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetAttractionClosureOverride_TestPayload_ExpectPosted', async () => {
   const url = '/set-attraction-closure-override';
   const payload = { method: 'setAttractionClosureOverride' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setAttractionClosureOverride(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetAttractionHoursScheduleTimeBounds_TestPayload_ExpectPosted', async () => {
   const url = '/get-attraction-hours-schedule-time-bounds';
   const payload = { method: 'getAttractionHoursScheduleTimeBounds' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.getAttractionHoursScheduleTimeBounds(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetAttractionHoursSchedule_TestPayload_ExpectPosted', async () => {
   const url = '/set-attraction-hours-schedule';
   const payload = { method: 'setAttractionHoursSchedule' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setAttractionHoursSchedule(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_ReplaceAttractionHoursScheduleOverlaps_TestPayload_ExpectPosted', async () => {
   const url = '/replace-attraction-hours-schedule-overlaps';
   const payload = { method: 'replaceAttractionHoursScheduleOverlaps' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.replaceAttractionHoursScheduleOverlaps(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_TrimAttractionHoursScheduleOverlaps_TestPayload_ExpectPosted', async () => {
   const url = '/trim-attraction-hours-schedule-overlaps';
   const payload = { method: 'trimAttractionHoursScheduleOverlaps' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.trimAttractionHoursScheduleOverlaps(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetTransportationStationOpen_TestPayload_ExpectPosted', async () => {
   const url = '/set-transportation-station-open';
   const payload = { method: 'setTransportationStationOpen' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setTransportationStationOpen(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetTransportationStationClosed_TestPayload_ExpectPosted', async () => {
   const url = '/set-transportation-station-closed';
   const payload = { method: 'setTransportationStationClosed' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setTransportationStationClosed(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetCurrentTransportationRoute_TestPayload_ExpectPosted', async () => {
   const url = '/set-current-transportation-route';
   const payload = { method: 'setCurrentTransportationRoute' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setCurrentTransportationRoute(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetGuardiansTalkNamesAtLocation_TestPayload_ExpectPosted', async () => {
   const url = '/get-guardians-talk-names-at-location';
   const payload = { method: 'getGuardiansTalkNamesAtLocation' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.getGuardiansTalkNamesAtLocation(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetGuardiansTalkScheduleOptions_TestPayload_ExpectPosted', async () => {
   const url = '/get-guardians-talk-schedule-options';
   const payload = { method: 'getGuardiansTalkScheduleOptions' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.getGuardiansTalkScheduleOptions(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetGuardiansTalkSchedule_TestPayload_ExpectPosted', async () => {
   const url = '/set-guardians-talk-schedule';
   const payload = { method: 'setGuardiansTalkSchedule' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setGuardiansTalkSchedule(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_ReplaceGuardiansTalkScheduleOverlaps_TestPayload_ExpectPosted', async () => {
   const url = '/replace-guardians-talk-schedule-overlaps';
   const payload = { method: 'replaceGuardiansTalkScheduleOverlaps' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.replaceGuardiansTalkScheduleOverlaps(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_TrimGuardiansTalkScheduleOverlaps_TestPayload_ExpectPosted', async () => {
   const url = '/trim-guardians-talk-schedule-overlaps';
   const payload = { method: 'trimGuardiansTalkScheduleOverlaps' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.trimGuardiansTalkScheduleOverlaps(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_EndGuardiansTalkSchedule_TestPayload_ExpectPosted', async () => {
   const url = '/end-guardians-talk-schedule';
   const payload = { method: 'endGuardiansTalkSchedule' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.endGuardiansTalkSchedule(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetGuardiansTalkOccurrences_TestPayload_ExpectPosted', async () => {
   const url = '/get-guardians-talk-occurrences';
   const payload = { method: 'getGuardiansTalkOccurrences' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.getGuardiansTalkOccurrences(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetGuardiansTalkScheduleTimes_TestPayload_ExpectPosted', async () => {
   const url = '/get-guardians-talk-schedule-times';
   const payload = { method: 'getGuardiansTalkScheduleTimes' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.getGuardiansTalkScheduleTimes(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_CancelGuardiansTalkOccurrence_TestPayload_ExpectPosted', async () => {
   const url = '/cancel-guardians-talk-occurrence';
   const payload = { method: 'cancelGuardiansTalkOccurrence' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.cancelGuardiansTalkOccurrence(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_AddGuardiansTalkOccurrence_TestPayload_ExpectPosted', async () => {
   const url = '/add-guardians-talk-occurrence';
   const payload = { method: 'addGuardiansTalkOccurrence' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.addGuardiansTalkOccurrence(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetWildEncounterSchedule_TestPayload_ExpectPosted', async () => {
   const url = '/set-wild-encounter-schedule';
   const payload = { method: 'setWildEncounterSchedule' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setWildEncounterSchedule(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_ReplaceWildEncounterScheduleOverlaps_TestPayload_ExpectPosted', async () => {
   const url = '/replace-wild-encounter-schedule-overlaps';
   const payload = { method: 'replaceWildEncounterScheduleOverlaps' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.replaceWildEncounterScheduleOverlaps(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_TrimWildEncounterScheduleOverlaps_TestPayload_ExpectPosted', async () => {
   const url = '/trim-wild-encounter-schedule-overlaps';
   const payload = { method: 'trimWildEncounterScheduleOverlaps' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.trimWildEncounterScheduleOverlaps(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_EndWildEncounterSchedule_TestPayload_ExpectPosted', async () => {
   const url = '/end-wild-encounter-schedule';
   const payload = { method: 'endWildEncounterSchedule' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.endWildEncounterSchedule(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetWildEncounterScheduleTimes_TestPayload_ExpectPosted', async () => {
   const url = '/get-wild-encounter-schedule-times';
   const payload = { method: 'getWildEncounterScheduleTimes' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.getWildEncounterScheduleTimes(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetWildEncounterOccurrences_TestPayload_ExpectPosted', async () => {
   const url = '/get-wild-encounter-occurrences';
   const payload = { method: 'getWildEncounterOccurrences' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.getWildEncounterOccurrences(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_CancelWildEncounterOccurrence_TestPayload_ExpectPosted', async () => {
   const url = '/cancel-wild-encounter-occurrence';
   const payload = { method: 'cancelWildEncounterOccurrence' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.cancelWildEncounterOccurrence(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetDrinkingFountainsClosed_TestPayload_ExpectPosted', async () => {
   const url = '/set-drinking-fountains-closed';
   const payload = { method: 'setDrinkingFountainsClosed' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setDrinkingFountainsClosed(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_SetDrinkingFountainsOpen_TestPayload_ExpectPosted', async () => {
   const url = '/set-drinking-fountains-open';
   const payload = { method: 'setDrinkingFountainsOpen' };
   _echoPostJson();

   const result = await ConsoleOperationsClient.setDrinkingFountainsOpen(payload);

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetAttractionHoursScheduleTimeBounds_TestDefaultPayload_ExpectEmptyPosted', async () => {
   const url = '/get-attraction-hours-schedule-time-bounds';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getAttractionHoursScheduleTimeBounds();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetOffDisplayAnimalOptions_TestDefaultPayload_ExpectEmptyPosted', async () => {
   const url = '/get-off-display-animal-options';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getOffDisplayAnimalOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetAnimalVisibilityScheduleOptions_TestDefaultPayload_ExpectEmptyPosted', async () => {
   const url = '/get-animal-visibility-schedule-options';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getAnimalVisibilityScheduleOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetAnimalViewingAlertOptions_TestDefaultPayload_ExpectEmptyPosted', async () => {
   const url = '/get-animal-viewing-alert-options';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getAnimalViewingAlertOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetExhibitsForSpecies_TestDefaultPayload_ExpectEmptyPosted', async () => {
   const url = '/get-exhibits-for-species';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getExhibitsForSpecies();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetOffDisplayExhibitOptions_TestDefaultPayload_ExpectEmptyPosted', async () => {
   const url = '/get-off-display-exhibit-options';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getOffDisplayExhibitOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetAnimalVisibilityScheduleExhibitOptions_TestDefaultPayload_ExpectEmptyPosted', async () => {
   const url = '/get-animal-visibility-schedule-exhibit-options';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getAnimalVisibilityScheduleExhibitOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetAnimalViewingAlertExhibitOptions_TestDefaultPayload_ExpectEmptyPosted', async () => {
   const url = '/get-animal-viewing-alert-exhibit-options';
   const payload = {};
   _echoPostJson();

   const result = await ConsoleOperationsClient.getAnimalViewingAlertExhibitOptions();

   assert.deepEqual(result, { ok: true, url, payload });
});


test('Test_GetWildEncounterNameOptions_TestPostJsonThrows_ExpectPropagates', async () => {
   const message = 'network down';
   ApiClient.postJson = async () => {
      throw new Error(message);
   };

   const request = ConsoleOperationsClient.getWildEncounterNameOptions();

   await assert.rejects(request, { message });
});


test('Test_SetExhibitClosed_TestPostJsonThrows_ExpectPropagates', async () => {
   const message = 'network down';
   const exhibit = 'Savanna';
   const payload = { exhibit };
   ApiClient.postJson = async () => {
      throw new Error(message);
   };

   const request = ConsoleOperationsClient.setExhibitClosed(payload);

   await assert.rejects(request, { message });
});
