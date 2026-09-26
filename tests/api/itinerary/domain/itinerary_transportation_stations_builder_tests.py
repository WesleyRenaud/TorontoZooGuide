from __future__ import annotations

import pytest

from api.itinerary.domain.itinerary_transportation_stations_builder import ItineraryTransportationStationsBuilder
from api.models.itinerary_transportation import ItineraryTransportation
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.shared.enums.itinerary_transportation_station_role import ItineraryTransportationStationRole
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName
from api.transportation.data_access.transportation_station_provider import TransportationStationProvider
from api.transportation.data_access.transportation_station_record import TransportationStationRecord


AFRICA = 'Africa'
AMERICAS = 'Americas'
EURASIA = 'Eurasia'
INDO_MALAYA = 'Indo-Malaya'
CANADIAN_DOMAIN = 'Canadian Domain'
AFRICA_RECORD = TransportationStationRecord(
   name=AFRICA,
   description='Africa station',
   x_coord=1.0,
   y_coord=2.0,
)
AMERICAS_RECORD = TransportationStationRecord(
   name=AMERICAS,
   description='Americas station',
   x_coord=3.0,
   y_coord=4.0,
)
EURASIA_RECORD = TransportationStationRecord(
   name=EURASIA,
   description='Eurasia station',
   x_coord=5.0,
   y_coord=6.0,
)


def _leg(
      *,
      from_station: str,
      to_station: str,
      start_time: str,
      end_time: str ) -> ItineraryTransportationLeg:
   return ItineraryTransportationLeg(
      from_station=from_station,
      to_station=to_station,
      start_time=start_time,
      end_time=end_time,
      transportation=TransportationName.ZOOMOBILE,
      added_as_attraction=False )


def _transportation(
      legs: list[ ItineraryTransportationLeg ] ) -> ItineraryTransportation:
   return ItineraryTransportation(
      name=TransportationName.ZOOMOBILE,
      added_as_attraction=False,
      legs=legs )


@pytest.fixture
def stub_station_records(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationStationProvider,
      'fetch_transportation_station_records',
      lambda conn, transportation: [
         AFRICA_RECORD,
         AMERICAS_RECORD,
         EURASIA_RECORD,
      ] )


def Test_GroupConsecutiveLegSequences_TestContinuousLegs_ExpectOneSequence() -> None:
   first_leg = _leg(
      from_station=AFRICA,
      to_station=AMERICAS,
      start_time='10:00 AM',
      end_time='10:10 AM' )
   second_leg = _leg(
      from_station=AMERICAS,
      to_station=EURASIA,
      start_time=first_leg.end_time,
      end_time='10:20 AM' )
   legs = [ first_leg, second_leg ]

   sequences = ItineraryTransportationStationsBuilder.group_consecutive_leg_sequences( legs )

   assert sequences == [ legs ]


def Test_GroupConsecutiveLegSequences_TestStationGap_ExpectSplitSequences() -> None:
   first_leg = _leg(
      from_station=AFRICA,
      to_station=AMERICAS,
      start_time='10:00 AM',
      end_time='10:10 AM' )
   second_leg = _leg(
      from_station=EURASIA,
      to_station=INDO_MALAYA,
      start_time=first_leg.end_time,
      end_time='10:20 AM' )
   legs = [ first_leg, second_leg ]

   sequences = ItineraryTransportationStationsBuilder.group_consecutive_leg_sequences( legs )

   assert sequences == [
      [ legs[ Position.FIRST ] ],
      [ legs[ Position.SECOND ] ],
   ]


def Test_GroupConsecutiveLegSequences_TestTimeGap_ExpectSplitSequences() -> None:
   first_leg = _leg(
      from_station=EURASIA,
      to_station=INDO_MALAYA,
      start_time='10:10 AM',
      end_time='10:20 AM' )
   second_leg = _leg(
      from_station=INDO_MALAYA,
      to_station=CANADIAN_DOMAIN,
      start_time='11:00 AM',
      end_time='11:10 AM' )
   legs = [ first_leg, second_leg ]

   sequences = ItineraryTransportationStationsBuilder.group_consecutive_leg_sequences( legs )

   assert sequences == [
      [ legs[ Position.FIRST ] ],
      [ legs[ Position.SECOND ] ],
   ]


def Test_UniqueStationNames_TestDuplicatesAndEmpty_ExpectOrderPreservedUniques() -> None:
   names = [ AFRICA, '', AMERICAS, AFRICA, EURASIA, AMERICAS ]

   unique_names = ItineraryTransportationStationsBuilder._unique_station_names( names )

   assert unique_names == [ AFRICA, AMERICAS, EURASIA ]


def Test_StationRolesForTransportation_TestSingleRide_ExpectOnboardAndOffboard() -> None:
   first_leg = _leg(
      from_station=AFRICA,
      to_station=AMERICAS,
      start_time='10:00 AM',
      end_time='10:10 AM' )
   second_leg = _leg(
      from_station=AMERICAS,
      to_station=EURASIA,
      start_time=first_leg.end_time,
      end_time='10:20 AM' )
   transportation = _transportation( [ first_leg, second_leg ] )

   roles = ItineraryTransportationStationsBuilder._station_roles_for_transportation(
      transportation )

   assert roles == {
      first_leg.from_station: ItineraryTransportationStationRole.ONBOARDING,
      second_leg.to_station: ItineraryTransportationStationRole.OFFBOARDING,
   }


def Test_StationRolesForTransportation_TestReturnRide_ExpectRoundTripStations() -> None:
   outbound = _leg(
      from_station=AFRICA,
      to_station=AMERICAS,
      start_time='10:00 AM',
      end_time='10:10 AM' )
   return_ride = _leg(
      from_station=AMERICAS,
      to_station=AFRICA,
      start_time='11:00 AM',
      end_time='11:10 AM' )
   transportation = _transportation( [ outbound, return_ride ] )

   roles = ItineraryTransportationStationsBuilder._station_roles_for_transportation(
      transportation )

   assert roles == {
      outbound.from_station: ItineraryTransportationStationRole.ROUND_TRIP,
      outbound.to_station: ItineraryTransportationStationRole.ROUND_TRIP,
   }


def Test_StationRolesForTransportation_TestEmptyLegs_ExpectEmptyRoles() -> None:
   transportation = _transportation( [] )

   roles = ItineraryTransportationStationsBuilder._station_roles_for_transportation(
      transportation )

   assert roles == {}


def Test_StationRecordByName_TestRecords_ExpectNameKeyedMap() -> None:
   records = [ AFRICA_RECORD, AMERICAS_RECORD ]

   records_by_name = ItineraryTransportationStationsBuilder._station_record_by_name(
      records )

   assert records_by_name == {
      record.name: record
      for record in records
   }


def Test_BuildStationsForTransportation_TestOnboardOffboard_ExpectStationsFromRecords(
      stub_station_records: None ) -> None:
   first_leg = _leg(
      from_station=AFRICA,
      to_station=AMERICAS,
      start_time='10:00 AM',
      end_time='10:10 AM' )
   second_leg = _leg(
      from_station=AMERICAS,
      to_station=EURASIA,
      start_time=first_leg.end_time,
      end_time='10:20 AM' )
   transportation = _transportation( [ first_leg, second_leg ] )

   stations = ItineraryTransportationStationsBuilder.build_stations_for_transportation(
      transportation )

   onboard = stations[ Position.FIRST ]
   offboard = stations[ Position.SECOND ]

   assert onboard.name == AFRICA_RECORD.name
   assert onboard.role == ItineraryTransportationStationRole.ONBOARDING
   assert onboard.description == AFRICA_RECORD.description
   assert onboard.x_coord == AFRICA_RECORD.x_coord
   assert onboard.y_coord == AFRICA_RECORD.y_coord
   assert offboard.name == EURASIA_RECORD.name
   assert offboard.role == ItineraryTransportationStationRole.OFFBOARDING
   assert offboard.description == EURASIA_RECORD.description
   assert offboard.x_coord == EURASIA_RECORD.x_coord
   assert offboard.y_coord == EURASIA_RECORD.y_coord


def Test_BuildStationsForTransportation_TestNoRoles_ExpectEmptyList(
      stub_station_records: None ) -> None:
   transportation = _transportation( [] )

   stations = ItineraryTransportationStationsBuilder.build_stations_for_transportation(
      transportation )

   assert stations == []


def Test_AttachToTransportations_TestMultipleRides_ExpectStationsAttachedAndFlattened(
      stub_station_records: None ) -> None:
   first = _transportation(
      [
         _leg(
            from_station=AFRICA,
            to_station=AMERICAS,
            start_time='10:00 AM',
            end_time='10:10 AM' ),
      ] )
   second = _transportation(
      [
         _leg(
            from_station=AMERICAS,
            to_station=EURASIA,
            start_time='11:00 AM',
            end_time='11:10 AM' ),
         _leg(
            from_station=EURASIA,
            to_station=AMERICAS,
            start_time='12:00 PM',
            end_time='12:10 PM' ),
      ] )

   flattened = ItineraryTransportationStationsBuilder.attach_to_transportations(
      [ first, second ] )

   first_onboard = first.stations[ Position.FIRST ]
   first_offboard = first.stations[ Position.SECOND ]
   second_americas = second.stations[ Position.FIRST ]
   second_eurasia = second.stations[ Position.SECOND ]

   assert first_onboard.name == AFRICA
   assert first_onboard.role == ItineraryTransportationStationRole.ONBOARDING
   assert first_offboard.name == AMERICAS
   assert first_offboard.role == ItineraryTransportationStationRole.OFFBOARDING
   assert second_americas.name == AMERICAS
   assert second_americas.role == ItineraryTransportationStationRole.ROUND_TRIP
   assert second_eurasia.name == EURASIA
   assert second_eurasia.role == ItineraryTransportationStationRole.ROUND_TRIP
   assert flattened == first.stations + second.stations
