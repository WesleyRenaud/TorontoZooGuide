from __future__ import annotations

import pytest

from api.itinerary.domain.itinerary_transportation_stations_builder import ItineraryTransportationStationsBuilder
from api.models.itinerary_transportation import ItineraryTransportation
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.shared.enums.itinerary_transportation_station_role import ItineraryTransportationStationRole
from api.transportation.data_access.transportation_station_provider import TransportationStationProvider
from api.transportation.data_access.transportation_station_record import TransportationStationRecord

ZOOMOBILE = 'Zoomobile'
AFRICA = 'Africa'
AMERICAS = 'Americas'
EURASIA = 'Eurasia'
INDO_MALAYA = 'Indo-Malaya'

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
      transportation=ZOOMOBILE,
      added_as_attraction=False )


def _transportation(
      legs: list[ ItineraryTransportationLeg ] ) -> ItineraryTransportation:
   return ItineraryTransportation(
      name=ZOOMOBILE,
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
   legs = [
      _leg(
         from_station=AFRICA,
         to_station=AMERICAS,
         start_time='10:00 AM',
         end_time='10:10 AM' ),
      _leg(
         from_station=AMERICAS,
         to_station=EURASIA,
         start_time='10:10 AM',
         end_time='10:20 AM' ),
   ]

   sequences = ItineraryTransportationStationsBuilder.group_consecutive_leg_sequences( legs )

   assert len( sequences ) == 1
   assert [ ( leg.from_station, leg.to_station ) for leg in sequences[ 0 ] ] == [
      ( AFRICA, AMERICAS ),
      ( AMERICAS, EURASIA ),
   ]


def Test_GroupConsecutiveLegSequences_TestStationOrTimeGap_ExpectSplitSequences() -> None:
   legs = [
      _leg(
         from_station=AFRICA,
         to_station=AMERICAS,
         start_time='10:00 AM',
         end_time='10:10 AM' ),
      _leg(
         from_station=EURASIA,
         to_station=INDO_MALAYA,
         start_time='10:10 AM',
         end_time='10:20 AM' ),
      _leg(
         from_station=INDO_MALAYA,
         to_station='Canadian Domain',
         start_time='11:00 AM',
         end_time='11:10 AM' ),
   ]

   sequences = ItineraryTransportationStationsBuilder.group_consecutive_leg_sequences( legs )

   assert [
      [ ( leg.from_station, leg.to_station ) for leg in sequence ]
      for sequence in sequences
   ] == [
      [ ( AFRICA, AMERICAS ) ],
      [ ( EURASIA, INDO_MALAYA ) ],
      [ ( INDO_MALAYA, 'Canadian Domain' ) ],
   ]


def Test_UniqueStationNames_TestDuplicatesAndEmpty_ExpectOrderPreservedUniques() -> None:
   assert ItineraryTransportationStationsBuilder._unique_station_names(
      [ AFRICA, '', AMERICAS, AFRICA, EURASIA, AMERICAS ]
   ) == [ AFRICA, AMERICAS, EURASIA ]


def Test_StationRolesForTransportation_TestSingleRide_ExpectOnboardAndOffboard() -> None:
   transportation = _transportation(
      [
         _leg(
            from_station=AFRICA,
            to_station=AMERICAS,
            start_time='10:00 AM',
            end_time='10:10 AM' ),
         _leg(
            from_station=AMERICAS,
            to_station=EURASIA,
            start_time='10:10 AM',
            end_time='10:20 AM' ),
      ] )

   roles = ItineraryTransportationStationsBuilder._station_roles_for_transportation(
      transportation )

   assert roles == {
      AFRICA: ItineraryTransportationStationRole.ONBOARDING,
      EURASIA: ItineraryTransportationStationRole.OFFBOARDING,
   }


def Test_StationRolesForTransportation_TestReturnRide_ExpectRoundTripStations() -> None:
   transportation = _transportation(
      [
         _leg(
            from_station=AFRICA,
            to_station=AMERICAS,
            start_time='10:00 AM',
            end_time='10:10 AM' ),
         _leg(
            from_station=AMERICAS,
            to_station=AFRICA,
            start_time='11:00 AM',
            end_time='11:10 AM' ),
      ] )

   roles = ItineraryTransportationStationsBuilder._station_roles_for_transportation(
      transportation )

   assert roles == {
      AFRICA: ItineraryTransportationStationRole.ROUND_TRIP,
      AMERICAS: ItineraryTransportationStationRole.ROUND_TRIP,
   }


def Test_StationRolesForTransportation_TestEmptyLegs_ExpectEmptyRoles() -> None:
   assert ItineraryTransportationStationsBuilder._station_roles_for_transportation(
      _transportation( [] ) ) == {}


def Test_StationRecordByName_TestRecords_ExpectNameKeyedMap() -> None:
   records = [ AFRICA_RECORD, AMERICAS_RECORD ]

   assert ItineraryTransportationStationsBuilder._station_record_by_name( records ) == {
      AFRICA: AFRICA_RECORD,
      AMERICAS: AMERICAS_RECORD,
   }


def Test_BuildStationsForTransportation_TestOnboardOffboard_ExpectStationsFromRecords(
      stub_station_records: None ) -> None:
   transportation = _transportation(
      [
         _leg(
            from_station=AFRICA,
            to_station=AMERICAS,
            start_time='10:00 AM',
            end_time='10:10 AM' ),
         _leg(
            from_station=AMERICAS,
            to_station=EURASIA,
            start_time='10:10 AM',
            end_time='10:20 AM' ),
      ] )

   stations = ItineraryTransportationStationsBuilder.build_stations_for_transportation(
      transportation )

   assert [
      ( station.name, station.role, station.description, station.x_coord, station.y_coord )
      for station in stations
   ] == [
      ( AFRICA, ItineraryTransportationStationRole.ONBOARDING, 'Africa station', 1.0, 2.0 ),
      ( EURASIA, ItineraryTransportationStationRole.OFFBOARDING, 'Eurasia station', 5.0, 6.0 ),
   ]


def Test_BuildStationsForTransportation_TestNoRoles_ExpectEmptyList(
      stub_station_records: None ) -> None:
   assert ItineraryTransportationStationsBuilder.build_stations_for_transportation(
      _transportation( [] ) ) == []


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

   assert [
      ( station.name, station.role )
      for station in first.stations
   ] == [
      ( AFRICA, ItineraryTransportationStationRole.ONBOARDING ),
      ( AMERICAS, ItineraryTransportationStationRole.OFFBOARDING ),
   ]
   assert [
      ( station.name, station.role )
      for station in second.stations
   ] == [
      ( AMERICAS, ItineraryTransportationStationRole.ROUND_TRIP ),
      ( EURASIA, ItineraryTransportationStationRole.ROUND_TRIP ),
   ]
   assert [ station.name for station in flattened ] == [
      AFRICA,
      AMERICAS,
      AMERICAS,
      EURASIA,
   ]
