let itineraryTransportationStationRoles = null;
let itineraryTransportationStationOnboardingRoles = Object.freeze([]);
let itineraryTransportationStationOffboardingRoles = Object.freeze([]);

export function updateItineraryTransportationStationRolesFromConfig(
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

export function getItineraryTransportationStationRoles() {
   return itineraryTransportationStationRoles;
}

export function getItineraryTransportationStationOnboardingRoles() {
   return itineraryTransportationStationOnboardingRoles;
}

export function getItineraryTransportationStationOffboardingRoles() {
   return itineraryTransportationStationOffboardingRoles;
}
