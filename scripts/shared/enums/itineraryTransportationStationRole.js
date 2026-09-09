import itineraryTransportationStationRoleValues from '../../../shared/enums/itineraryTransportationStationRole.json' with { type: 'json' };

export class ItineraryTransportationStationRole {
   static {
      Object.entries(itineraryTransportationStationRoleValues).forEach(([memberName, definition]) => {
         Object.assign(ItineraryTransportationStationRole, {
            [memberName]: Object.freeze({ ...definition }),
         });
      });

      ItineraryTransportationStationRole.ROLE_ENTRIES = Object.freeze(
         Object.keys(itineraryTransportationStationRoleValues).map(
            memberName => ItineraryTransportationStationRole[memberName]
         )
      );
   }

   static onboardingRoleValues() {
      return ItineraryTransportationStationRole.ROLE_ENTRIES
         .filter(entry => entry.onboarding)
         .map(entry => entry.kind);
   }

   static offboardingRoleValues() {
      return ItineraryTransportationStationRole.ROLE_ENTRIES
         .filter(entry => entry.offboarding)
         .map(entry => entry.kind);
   }
}
