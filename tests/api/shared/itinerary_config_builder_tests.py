from __future__ import annotations

from api.shared.constants import Constants
from api.shared.enums import ItineraryEventType
from api.shared.itinerary_config_builder import ItineraryConfigBuilder


def Test_ToDict_TestAnimalVisibilityChangeThreshold_ExpectConstant() -> None:
   assert ItineraryConfigBuilder.to_dict()[
      'animal_visibility_change_threshold'
   ] == Constants.ANIMAL_VISIBILITY_CHANGE_THRESHOLD


def Test_ToDict_TestItineraryAnimalMinLikelihood_ExpectConstant() -> None:
   assert ItineraryConfigBuilder.to_dict()[
      'itinerary_animal_min_likelihood'
   ] == Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD


def Test_ToDict_TestEventTypes_ExpectAllEventTypeValues() -> None:
   assert ItineraryConfigBuilder.to_dict()[ 'itinerary_event_types' ] == [
      event_type.value for event_type in ItineraryEventType
   ]


def Test_ToDict_TestVisitBoundaryEventTypes_ExpectArrivalAndDeparture() -> None:
   assert ItineraryConfigBuilder.to_dict()[ 'itinerary_visit_boundary_event_types' ] == {
      'arrival': ItineraryEventType.ARRIVAL.value,
      'departure': ItineraryEventType.DEPARTURE.value,
   }


def Test_ToDict_TestNoConnection_ExpectEmptySuppressedErrorTypes() -> None:
   assert ItineraryConfigBuilder.to_dict()[ 'suppressed_error_types' ] == []


def Test_ToDict_TestNoConnection_ExpectEmptyItineraryStatuses() -> None:
   assert ItineraryConfigBuilder.to_dict()[ 'itinerary_statuses' ] == []


def Test_ToDict_TestStaticEnumMaps_ExpectOmitted() -> None:
   config = ItineraryConfigBuilder.to_dict()

   assert 'itinerary_error_types' not in config
   assert 'itinerary_adjustment_types' not in config
   assert 'itinerary_transportation_station_roles' not in config
   assert 'itinerary_transportation_station_onboarding_roles' not in config
   assert 'itinerary_transportation_station_offboarding_roles' not in config
