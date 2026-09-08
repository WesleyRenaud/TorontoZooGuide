export class ItineraryTransportationStationRoles {
   static itineraryTransportationStationRoles = null;

   static itineraryTransportationStationOnboardingRoles = Object.freeze([]);

   static itineraryTransportationStationOffboardingRoles = Object.freeze([]);

   static updateItineraryTransportationStationRolesFromConfig(
      itineraryConfig = {}
   ) {
      const roles = itineraryConfig?.transportationStationRoles;

      if (roles && typeof roles === 'object') {
         ItineraryTransportationStationRoles.itineraryTransportationStationRoles = Object.freeze({ ...roles });
      }

      const onboardingRoles = itineraryConfig?.transportationStationOnboardingRoles;

      if (Array.isArray(onboardingRoles) && onboardingRoles.length > 0) {
         ItineraryTransportationStationRoles.itineraryTransportationStationOnboardingRoles = Object.freeze([
            ...onboardingRoles,
         ]);
      }

      const offboardingRoles = itineraryConfig?.transportationStationOffboardingRoles;

      if (Array.isArray(offboardingRoles) && offboardingRoles.length > 0) {
         ItineraryTransportationStationRoles.itineraryTransportationStationOffboardingRoles = Object.freeze([
            ...offboardingRoles,
         ]);
      }
   }

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
