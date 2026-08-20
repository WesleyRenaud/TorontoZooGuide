from __future__ import annotations

from ...models.itinerary_transportation import ItineraryTransportation
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...models.itinerary_transportation_station import ItineraryTransportationStation
from ...request_connection import get_connection
from ...shared.enums.itinerary_transportation_station_role import ItineraryTransportationStationRole
from ...shared.enums.sequence_index import SequenceIndex
from ...transportation.data_access.transportation_station import fetch_transportation_station_records
from ...transportation.data_access.transportation_station_record import TransportationStationRecord


def group_consecutive_transportation_leg_sequences(
      legs: list[ ItineraryTransportationLeg ],
) -> list[ list[ ItineraryTransportationLeg ] ]:
   sequences: list[ list[ ItineraryTransportationLeg ] ] = []
   current_sequence: list[ ItineraryTransportationLeg ] = []

   for leg in legs:
      if (
            current_sequence
            and current_sequence[ SequenceIndex.LAST ].to_station != leg.from_station
      ):
         sequences.append( current_sequence )
         current_sequence = []

      current_sequence.append( leg )

   if current_sequence:
      sequences.append( current_sequence )

   return sequences


def _unique_station_names( names: list[ str ] ) -> list[ str ]:
   unique_names: list[ str ] = []
   seen_names: set[ str ] = set()

   for name in names:
      if not name or name in seen_names:
         continue

      seen_names.add( name )
      unique_names.append( name )

   return unique_names


def _station_roles_for_transportation(
      transportation: ItineraryTransportation,
) -> dict[ str, ItineraryTransportationStationRole ]:
   onboard_names: list[ str ] = []
   offboard_names: list[ str ] = []

   for sequence in group_consecutive_transportation_leg_sequences(
         transportation.legs ):
      onboard_names.append( sequence[ SequenceIndex.FIRST ].from_station )
      offboard_names.append( sequence[ SequenceIndex.LAST ].to_station )

   roles_by_name: dict[ str, ItineraryTransportationStationRole ] = {}

   for name in _unique_station_names( onboard_names ):
      roles_by_name[ name ] = ItineraryTransportationStationRole.ONBOARDING

   for name in _unique_station_names( offboard_names ):
      if name in roles_by_name:
         roles_by_name[ name ] = ItineraryTransportationStationRole.ROUND_TRIP
      else:
         roles_by_name[ name ] = ItineraryTransportationStationRole.OFFBOARDING

   return roles_by_name


def _station_record_by_name(
      records: list[ TransportationStationRecord ],
) -> dict[ str, TransportationStationRecord ]:
   return {
      record.name: record
      for record in records
   }


def build_stations_for_transportation(
      transportation: ItineraryTransportation,
) -> list[ ItineraryTransportationStation ]:
   roles_by_name = _station_roles_for_transportation( transportation )

   if not roles_by_name:
      return []

   records_by_name = _station_record_by_name(
      fetch_transportation_station_records(
         get_connection(),
         transportation.name,
      ) )
   stations: list[ ItineraryTransportationStation ] = []

   for name, role in roles_by_name.items():
      record = records_by_name[ name ]
      stations.append(
         ItineraryTransportationStation(
            name=name,
            transportation=transportation.name,
            role=role,
            description=record.description,
            x_coord=record.x_coord,
            y_coord=record.y_coord,
         )
      )

   return stations


def attach_itinerary_transportation_stations(
      transportations: list[ ItineraryTransportation ],
) -> list[ ItineraryTransportationStation ]:
   stations: list[ ItineraryTransportationStation ] = []

   for transportation in transportations:
      transportation.stations = build_stations_for_transportation(
         transportation )
      stations.extend( transportation.stations )

   return stations
