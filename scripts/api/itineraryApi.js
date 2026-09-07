import { ApiClient } from './apiClient.js';
import { ItineraryApiNormalizer } from './itineraryApiNormalizer.js';
import { ValueNormalizer } from './valueNormalizer.js';

export class ItineraryApi {
   static async getItineraryDateRequest() {
      const response = await ApiClient.postJson('/get-itinerary-date', {});
      return ItineraryApiNormalizer.normalizeItineraryDateResponse(response);
   }

   static async getItineraryRequest(temp) {
      const response = await ApiClient.postJson('/get-itinerary', { temp });
      return ItineraryApiNormalizer.normalizeItineraryResponse(response);
   }

   static async getZooHoursRequest({ day, month, year }) {
      const response = await ApiClient.postJson('/get-zoo-hours', { day, month, year });
      return ItineraryApiNormalizer.normalizeZooHoursResponse(response);
   }

   static async setItineraryRequest(payload) {
      const response = await ApiClient.postJson('/set-itinerary', payload);
      return ItineraryApiNormalizer.normalizeItineraryResponse(response);
   }

   static async scheduleItineraryItemRequest(
      request,
      {
         confirmingScheduleItemNotOnItinerary = false,
         confirmingAttractionOutsideOperatingHours = false,
         confirmingGuardiansTalkUnschedule = false,
         confirmingWildEncounterUnschedule = false,
         confirmingFixedTimeItemLongWait = false,
         confirmingGuardiansTalkWithoutAnimal = false,
      } = {}
   ) {
      const response = await ApiClient.postJson('/schedule-itinerary-item', {
         ...request,
         key: ItineraryApiNormalizer.mapScheduleItemKeyToWire(request.itemType, request.key),
         confirmingScheduleItemNotOnItinerary,
         confirmingAttractionOutsideOperatingHours,
         confirmingGuardiansTalkUnschedule,
         confirmingWildEncounterUnschedule,
         confirmingFixedTimeItemLongWait,
         confirmingGuardiansTalkWithoutAnimal,
      });

      return ItineraryApiNormalizer.normalizeScheduleItineraryItemResponse(response);
   }

   static async unscheduleItineraryItemRequest({ itemType, key }) {
      const response = await ApiClient.postJson('/unschedule-itinerary-item', {
         itemType: ValueNormalizer.asTrimmedString(itemType),
         key: ItineraryApiNormalizer.mapScheduleItemKeyToWire(itemType, key),
      });

      return ItineraryApiNormalizer.normalizeScheduleItineraryItemResponse(response);
   }

   static async removeItemFromItineraryRequest({ itemType, key }) {
      const response = await ApiClient.postJson('/remove-item-from-itinerary', {
         itemType: ValueNormalizer.asTrimmedString(itemType),
         key: ItineraryApiNormalizer.mapScheduleItemKeyToWire(itemType, key),
      });

      return ItineraryApiNormalizer.normalizeScheduleItineraryItemResponse(response);
   }

   static async setItineraryArrivalTimeRequest(
      arrivalTime,
      {
         confirmingShortVisit = false,
         confirmingEarlyAdmission = false,
      } = {}
   ) {
      const response = await ApiClient.postJson('/set-itinerary-arrival-time', {
         arrivalTime: ValueNormalizer.asTrimmedString(arrivalTime),
         confirmingShortVisit,
         confirmingEarlyAdmission,
      });

      return ItineraryApiNormalizer.normalizeItineraryTimeSetResponse(response);
   }

   static async setItineraryDepartureTimeRequest(
      departureTime,
      { confirmingShortVisit = false } = {}
   ) {
      const response = await ApiClient.postJson('/set-itinerary-departure-time', {
         departureTime: ValueNormalizer.asTrimmedString(departureTime),
         confirmingShortVisit,
      });

      return ItineraryApiNormalizer.normalizeItineraryTimeSetResponse(response);
   }

   static async suppressItineraryWarningRequest(warningType) {
      const response = await ApiClient.postJson('/suppress-itinerary-warning', {
         warningType: ValueNormalizer.asTrimmedString(warningType),
      });

      return ItineraryApiNormalizer.normalizeItineraryResult(response, { includeItinerary: false });
   }

   static async bulkScheduleItineraryRequest(
      temp,
      { confirmingFixedTimeItemLongWait = false } = {}
   ) {
      const response = await ApiClient.postJson('/bulk-schedule-itinerary', {
         temp,
         confirmingFixedTimeItemLongWait,
      });
      return ItineraryApiNormalizer.normalizeItineraryResponse(response);
   }

   static async unscheduleAllItineraryItemsRequest(temp) {
      const response = await ApiClient.postJson('/unschedule-all-itinerary-items', { temp });
      return ItineraryApiNormalizer.normalizeItineraryResponse(response);
   }

   static async acceptItineraryRequest(
      temp,
      { animalsToKeep = [], attractionsToKeep = [] } = {}
   ) {
      const response = await ApiClient.postJson('/accept-itinerary', {
         temp,
         animalsToKeep,
         attractionsToKeep,
      });
      return ItineraryApiNormalizer.normalizeItineraryResponse(response);
   }

   static clearItineraryRequest() {
      return ApiClient.postJson('/clear-itinerary', {});
   }
}
