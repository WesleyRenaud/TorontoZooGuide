import { ApiClient } from './apiClient.js';
import { ValueNormalizer } from './valueNormalizer.js';

const EMPTY_PAYLOAD = Object.freeze({});

function asStringArray(value) {
   return ValueNormalizer.asArray(value)
      .map(ValueNormalizer.asTrimmedString)
      .filter(Boolean);
}

function readResponseCollection(response, responseKey) {
   return ValueNormalizer.asArray(ValueNormalizer.asObject(response)[responseKey]);
}

function normalizeRouteResponse(response) {
   const source = ValueNormalizer.asObject(response);

   return {
      route: ValueNormalizer.asTrimmedString(source.route).toLowerCase(),
      transportationStations: readResponseCollection(source, 'transportation_stations'),
   };
}

async function fetchCollection(endpoint, responseKey, payload = EMPTY_PAYLOAD) {
   const response = await ApiClient.postJson(endpoint, payload);
   return readResponseCollection(response, responseKey);
}

async function fetchStringCollection(endpoint, responseKey, payload = EMPTY_PAYLOAD) {
   return asStringArray(await fetchCollection(endpoint, responseKey, payload));
}

function normalizeTransportationRoutesResponse(response) {
   return ValueNormalizer.asArray(ValueNormalizer.asObject(response).transportations)
      .map((entry) => {
         const source = ValueNormalizer.asObject(entry);
         const name = ValueNormalizer.asTrimmedString(source.name);

         if (!name) {
            return null;
         }

         return {
            name,
            routes: asStringArray(source.routes),
         };
      })
      .filter(Boolean);
}

export class MapApi {
   static async getVisibleAnimals(payload = EMPTY_PAYLOAD) {
      return await fetchCollection('/get-visible-animals', 'animals', payload);
   }

   static async getPavilions() {
      return await fetchCollection('/get-pavilions', 'pavilions');
   }

   static async getRestaurants(payload = EMPTY_PAYLOAD) {
      return await fetchCollection('/get-restaurants', 'restaurants', payload);
   }

   static async getRestrooms(payload = EMPTY_PAYLOAD) {
      return await fetchCollection('/get-restrooms', 'restrooms', payload);
   }

   static async getGiftShops(payload = EMPTY_PAYLOAD) {
      return await fetchCollection('/get-gift-shops', 'gift_shops', payload);
   }

   static async getAttractions(payload = EMPTY_PAYLOAD) {
      return await fetchCollection('/get-attractions', 'attractions', payload);
   }

   static async getTransportations(payload = EMPTY_PAYLOAD) {
      return await fetchCollection('/get-transportations', 'transportations', payload);
   }

   static async getTransportationRoute(payload = EMPTY_PAYLOAD) {
      const response = await ApiClient.postJson('/get-transportation-route', payload);
      return normalizeRouteResponse(response);
   }

   static async getTransportationRoutes() {
      const response = await ApiClient.postJson('/get-transportation-routes', EMPTY_PAYLOAD);
      return normalizeTransportationRoutesResponse(response);
   }

   static async getGuardiansTalks(payload) {
      return await fetchCollection('/get-guardians-talks', 'guardians_talks', payload);
   }

   static async getWildEncounters(payload = EMPTY_PAYLOAD) {
      return await fetchCollection('/get-wild-encounters', 'wild_encounters', payload);
   }

   static async getDrinkingFountains(payload = EMPTY_PAYLOAD) {
      return await fetchCollection('/get-drinking-fountains', 'drinking_fountains', payload);
   }

   static async getDefibrillators() {
      return await fetchCollection('/get-defibrillators', 'defibrillators');
   }

   static async getEmergencyIntercoms() {
      return await fetchCollection('/get-emergency-intercoms', 'emergency_intercoms');
   }

   static async getGuestServices() {
      return await fetchCollection('/get-guest-services', 'guest_services');
   }

   static async getPicnicSites() {
      return await fetchCollection('/get-picnic-sites', 'picnic_sites');
   }

   static async getEventSites() {
      return await fetchCollection('/get-event-sites', 'event_sites');
   }

   static async getEvents(payload = EMPTY_PAYLOAD) {
      return await fetchCollection('/get-events', 'events', payload);
   }

   static async getUpdates(payload = EMPTY_PAYLOAD) {
      return await fetchCollection('/get-updates', 'updates', payload);
   }

   static async getExhibits() {
      return await fetchCollection('/get-exhibits', 'exhibits');
   }

   static async getClosedExhibits(payload = EMPTY_PAYLOAD) {
      return await fetchStringCollection('/get-closed-exhibits', 'closed_exhibits', payload);
   }
}
