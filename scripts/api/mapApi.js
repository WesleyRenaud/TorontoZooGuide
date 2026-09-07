import { ApiClient } from './apiClient.js';
import { MapApiFetcher } from './mapApiFetcher.js';

export class MapApi {
   static async getVisibleAnimals(payload = EMPTY_PAYLOAD) {
      return await MapApiFetcher.fetchCollection('/get-visible-animals', 'animals', payload);
   }

   static async getPavilions() {
      return await MapApiFetcher.fetchCollection('/get-pavilions', 'pavilions');
   }

   static async getRestaurants(payload = EMPTY_PAYLOAD) {
      return await MapApiFetcher.fetchCollection('/get-restaurants', 'restaurants', payload);
   }

   static async getRestrooms(payload = EMPTY_PAYLOAD) {
      return await MapApiFetcher.fetchCollection('/get-restrooms', 'restrooms', payload);
   }

   static async getGiftShops(payload = EMPTY_PAYLOAD) {
      return await MapApiFetcher.fetchCollection('/get-gift-shops', 'gift_shops', payload);
   }

   static async getAttractions(payload = EMPTY_PAYLOAD) {
      return await MapApiFetcher.fetchCollection('/get-attractions', 'attractions', payload);
   }

   static async getTransportations(payload = EMPTY_PAYLOAD) {
      return await MapApiFetcher.fetchCollection('/get-transportations', 'transportations', payload);
   }

   static async getTransportationRoute(payload = EMPTY_PAYLOAD) {
      const response = await ApiClient.postJson('/get-transportation-route', payload);
      return MapApiFetcher.normalizeRouteResponse(response);
   }

   static async getTransportationRoutes() {
      const response = await ApiClient.postJson('/get-transportation-routes', EMPTY_PAYLOAD);
      return MapApiFetcher.normalizeTransportationRoutesResponse(response);
   }

   static async getGuardiansTalks(payload) {
      return await MapApiFetcher.fetchCollection('/get-guardians-talks', 'guardians_talks', payload);
   }

   static async getWildEncounters(payload = EMPTY_PAYLOAD) {
      return await MapApiFetcher.fetchCollection('/get-wild-encounters', 'wild_encounters', payload);
   }

   static async getDrinkingFountains(payload = EMPTY_PAYLOAD) {
      return await MapApiFetcher.fetchCollection('/get-drinking-fountains', 'drinking_fountains', payload);
   }

   static async getDefibrillators() {
      return await MapApiFetcher.fetchCollection('/get-defibrillators', 'defibrillators');
   }

   static async getEmergencyIntercoms() {
      return await MapApiFetcher.fetchCollection('/get-emergency-intercoms', 'emergency_intercoms');
   }

   static async getGuestServices() {
      return await MapApiFetcher.fetchCollection('/get-guest-services', 'guest_services');
   }

   static async getPicnicSites() {
      return await MapApiFetcher.fetchCollection('/get-picnic-sites', 'picnic_sites');
   }

   static async getEventSites() {
      return await MapApiFetcher.fetchCollection('/get-event-sites', 'event_sites');
   }

   static async getEvents(payload = EMPTY_PAYLOAD) {
      return await MapApiFetcher.fetchCollection('/get-events', 'events', payload);
   }

   static async getUpdates(payload = EMPTY_PAYLOAD) {
      return await MapApiFetcher.fetchCollection('/get-updates', 'updates', payload);
   }

   static async getExhibits() {
      return await MapApiFetcher.fetchCollection('/get-exhibits', 'exhibits');
   }

   static async getClosedExhibits(payload = EMPTY_PAYLOAD) {
      return await MapApiFetcher.fetchStringCollection('/get-closed-exhibits', 'closed_exhibits', payload);
   }
}
