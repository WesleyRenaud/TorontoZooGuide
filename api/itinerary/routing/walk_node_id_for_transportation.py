from __future__ import annotations

from ..data_access.itinerary import fetch_itinerary_date_record
from ..data_access.transportation_day_loop import fetch_main_transportation_station
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...request_connection import get_connection
from ...shared.calendar_dates import DateValues
from ...transportation.data_access.transportation_station import fetch_transportation_station_record
from ..transportation.resolve_transportation_day_loop import fetch_transportation_day_loop
from .transportation_boarding_station import boarding_station_for_transportation_legs
from ...walk_graph.data_access.load_walk_graph import load_walk_graph
from ...walk_graph.snap_point import snap_point_to_nearest_walk_node


def walk_node_id_for_transportation(
      transportation_name: str,
      *,
      legs: list[ ItineraryTransportationLeg ] | None = None,
   ) -> str | None:
   station_name = _boarding_station_name( transportation_name, legs=legs )

   if station_name is None:
      return None

   station = fetch_transportation_station_record(
      get_connection(),
      transportation_name,
      station_name )

   if station is None:
      return None

   walk_graph = load_walk_graph()
   walk_node_id, _ = snap_point_to_nearest_walk_node(
      station.x_coord,
      station.y_coord,
      walk_graph )

   return walk_node_id


def _boarding_station_name(
      transportation_name: str,
      *,
      legs: list[ ItineraryTransportationLeg ] | None,
   ) -> str | None:
   if legs:
      station_name = boarding_station_for_transportation_legs( legs )

      if station_name is not None:
         return station_name

   return _default_boarding_station_name( transportation_name )


def _default_boarding_station_name( transportation_name: str ) -> str | None:
   conn = get_connection()

   if conn is None:
      return None

   date_record = fetch_itinerary_date_record( conn )

   if date_record is not None:
      visit_date = DateValues.parse_date_value( date_record.itinerary_date )

      if visit_date is not None:
         day_loop = fetch_transportation_day_loop(
            conn,
            transportation=transportation_name,
            target_date=visit_date )

         if day_loop is not None and day_loop.legs:
            return day_loop.legs[ 0 ].from_station

   return fetch_main_transportation_station( conn, transportation_name )
