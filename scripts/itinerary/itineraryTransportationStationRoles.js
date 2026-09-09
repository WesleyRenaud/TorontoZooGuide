import { ItineraryTransportationStationRole } from '../shared/enums/itineraryTransportationStationRole.js';

export class ItineraryTransportationStationRoles {
   static itineraryTransportationStationRoles = Object.freeze({ ...ItineraryTransportationStationRole });

   static itineraryTransportationStationOnboardingRoles = Object.freeze([
      ItineraryTransportationStationRole.ONBOARDING,
      ItineraryTransportationStationRole.ROUND_TRIP,
   ]);

   static itineraryTransportationStationOffboardingRoles = Object.freeze([
      ItineraryTransportationStationRole.OFFBOARDING,
      ItineraryTransportationStationRole.ROUND_TRIP,
   ]);

   static getItineraryTransportationStationRoles() {
      return ItineraryTransportationStationRoles.itineraryTransportationStationRoles;
   }

   static getItineraryTransportationStationOnboardingRoles() {
      return ItineraryTransportationStationRoles.itineraryTransportationStationOnboardingRoles;
   }

   static getItineraryTransportationStationOffboardingRoles() {
      return ItineraryTransportationStationRoles.itineraryTransportationStationOffboardingRoles;
   }
}
