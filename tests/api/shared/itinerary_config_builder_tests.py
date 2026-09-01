from __future__ import annotations

from api.itinerary.domain.itinerary_adjustment_type import ItineraryAdjustmentType
from api.shared.constants import Constants
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItineraryEventType
from api.shared.enums import ItineraryTransportationStationRole
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


def Test_ToDict_TestErrorTypes_ExpectAllErrorTypeValues() -> None:
   assert ItineraryConfigBuilder.to_dict()[ 'itinerary_error_types' ] == {
      error_type.name: error_type.value
      for error_type in ItineraryErrorType
   }


def Test_ToDict_TestAdjustmentTypes_ExpectAllAdjustmentTypeValues() -> None:
   assert ItineraryConfigBuilder.to_dict()[ 'itinerary_adjustment_types' ] == {
      adjustment_type.name: adjustment_type.value
      for adjustment_type in ItineraryAdjustmentType
   }


def Test_ToDict_TestTransportationStationRoles_ExpectRoleConfig() -> None:
   assert ItineraryConfigBuilder.to_dict()[
      'itinerary_transportation_station_roles'
   ] == ItineraryTransportationStationRole.to_config_dict()
   assert ItineraryConfigBuilder.to_dict()[
      'itinerary_transportation_station_onboarding_roles'
   ] == ItineraryTransportationStationRole.onboarding_role_values()
   assert ItineraryConfigBuilder.to_dict()[
      'itinerary_transportation_station_offboarding_roles'
   ] == ItineraryTransportationStationRole.offboarding_role_values()


def Test_ToDict_TestNoConnection_ExpectEmptySuppressedErrorTypes() -> None:
   assert ItineraryConfigBuilder.to_dict()[ 'suppressed_error_types' ] == []


def Test_ToDict_TestNoConnection_ExpectEmptyItineraryStatuses() -> None:
   assert ItineraryConfigBuilder.to_dict()[ 'itinerary_statuses' ] == []
