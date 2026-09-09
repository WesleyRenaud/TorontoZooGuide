import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryTransportationStationRoles } from '../../../scripts/itinerary/itineraryTransportationStationRoles.js';

test('Test_GetItineraryTransportationStationRoles_TestSharedEnum_ExpectFrozenMap', () => {
   assert.deepEqual(
      ItineraryTransportationStationRoles.getItineraryTransportationStationRoles(),
      {
         OFFBOARDING: 'offboarding_station',
         ONBOARDING: 'onboarding_station',
         ROUND_TRIP: 'round_trip',
      }
   );
   assert.equal(
      Object.isFrozen(ItineraryTransportationStationRoles.getItineraryTransportationStationRoles()),
      true
   );
});

test('Test_GetItineraryTransportationStationBoardingRoles_TestSharedEnum_ExpectRoundTripIncluded', () => {
   assert.deepEqual(
      ItineraryTransportationStationRoles.getItineraryTransportationStationOnboardingRoles(),
      ['onboarding_station', 'round_trip']
   );
   assert.deepEqual(
      ItineraryTransportationStationRoles.getItineraryTransportationStationOffboardingRoles(),
      ['offboarding_station', 'round_trip']
   );
});
