let itineraryTransportationStationRoles = null;
let itineraryTransportationStationOnboardingRoles = Object.freeze([]);
let itineraryTransportationStationOffboardingRoles = Object.freeze([]);

export class ItineraryTransportationStationRoles {
   static updateItineraryTransportationStationRolesFromConfig(
      itineraryConfig = {}
   ) {
      const roles = itineraryConfig?.transportationStationRoles;

      if (roles && typeof roles === 'object') {
         itineraryTransportationStationRoles = Object.freeze({ ...roles });
      }

      const onboardingRoles = itineraryConfig?.transportationStationOnboardingRoles;

      if (Array.isArray(onboardingRoles) && onboardingRoles.length > 0) {
         itineraryTransportationStationOnboardingRoles = Object.freeze([
            ...onboardingRoles,
         ]);
      }

      const offboardingRoles = itineraryConfig?.transportationStationOffboardingRoles;

      if (Array.isArray(offboardingRoles) && offboardingRoles.length > 0) {
         itineraryTransportationStationOffboardingRoles = Object.freeze([
            ...offboardingRoles,
         ]);
      }
   }

   static getItineraryTransportationStationRoles() {
      return itineraryTransportationStationRoles;
   }

   static getItineraryTransportationStationOnboardingRoles() {
      return itineraryTransportationStationOnboardingRoles;
   }

   static getItineraryTransportationStationOffboardingRoles() {
      return itineraryTransportationStationOffboardingRoles;
   }
}
