import assert from 'node:assert/strict';
import test, { afterEach } from 'node:test';

import { ItineraryTransportationStationRoles } from '../../../scripts/itinerary/itineraryTransportationStationRoles.js';

function _resetRoles() {
   ItineraryTransportationStationRoles.itineraryTransportationStationRoles = null;
   ItineraryTransportationStationRoles.itineraryTransportationStationOnboardingRoles = Object.freeze([]);
   ItineraryTransportationStationRoles.itineraryTransportationStationOffboardingRoles = Object.freeze([]);
}

afterEach(() => {
   _resetRoles();
});

test('Test_UpdateItineraryTransportationStationRolesFromConfig_TestRoles_ExpectStored', () => {
   ItineraryTransportationStationRoles.updateItineraryTransportationStationRolesFromConfig({
      transportationStationRoles: { Main: 'hub' },
      transportationStationOnboardingRoles: ['board'],
      transportationStationOffboardingRoles: ['exit'],
   });

   assert.deepEqual(
      ItineraryTransportationStationRoles.getItineraryTransportationStationRoles(),
      { Main: 'hub' }
   );
   assert.deepEqual(
      ItineraryTransportationStationRoles.getItineraryTransportationStationOnboardingRoles(),
      ['board']
   );
   assert.deepEqual(
      ItineraryTransportationStationRoles.getItineraryTransportationStationOffboardingRoles(),
      ['exit']
   );
});

test('Test_UpdateItineraryTransportationStationRolesFromConfig_TestEmpty_ExpectUnchangedDefaults', () => {
   ItineraryTransportationStationRoles.updateItineraryTransportationStationRolesFromConfig({});
   assert.equal(ItineraryTransportationStationRoles.getItineraryTransportationStationRoles(), null);
   assert.deepEqual(
      ItineraryTransportationStationRoles.getItineraryTransportationStationOnboardingRoles(),
      []
   );
   assert.deepEqual(
      ItineraryTransportationStationRoles.getItineraryTransportationStationOffboardingRoles(),
      []
   );
});
