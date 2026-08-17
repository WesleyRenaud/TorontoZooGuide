from __future__ import annotations

from datetime import date

from itinerary.support import schedule_itinerary_item, unschedule_itinerary_item

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.itinerary.data_access.itinerary_transportation_input import ItineraryTransportationInput
from api.itinerary.transportation.resolve_transportation_day_loop import fetch_transportation_day_loop
from api.itinerary.transportation.resolve_transportation_day_loop import order_route_legs_from_station
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from conftest import DbControllers


ZOOMOBILE = 'Zoomobile'
SUMMER_LEG_STATIONS = [
   ( 'Main Zoomobile Station', 'Canadian Domain Zoomobile Station' ),
   ( 'Canadian Domain Zoomobile Station', 'Africa Zoomobile Station' ),
   ( 'Africa Zoomobile Station', 'Tundra Zoomobile Station' ),
   ( 'Tundra Zoomobile Station', 'Eurasia Zoomobile Station' ),
   ( 'Eurasia Zoomobile Station', 'Main Zoomobile Station' ),
]
WINTER_LEG_STATIONS = [
   ( 'Main Zoomobile Station', 'Indo-Malaya Zoomobile Station' ),
   ( 'Indo-Malaya Zoomobile Station', 'Tundra Zoomobile Station' ),
   ( 'Tundra Zoomobile Station', 'Eurasia Zoomobile Station' ),
   ( 'Eurasia Zoomobile Station', 'Main Zoomobile Station' ),
]


def test_order_route_legs_from_station_forms_closed_loop() -> None:
   unordered = [
      TransportationRouteLegSegment(
         from_station='Africa Zoomobile Station',
         to_station='Tundra Zoomobile Station',
         duration_minutes=15 ),
      TransportationRouteLegSegment(
         from_station='Main Zoomobile Station',
         to_station='Canadian Domain Zoomobile Station',
         duration_minutes=20 ),
      TransportationRouteLegSegment(
         from_station='Eurasia Zoomobile Station',
         to_station='Main Zoomobile Station',
         duration_minutes=15 ),
      TransportationRouteLegSegment(
         from_station='Canadian Domain Zoomobile Station',
         to_station='Africa Zoomobile Station',
         duration_minutes=10 ),
      TransportationRouteLegSegment(
         from_station='Tundra Zoomobile Station',
         to_station='Eurasia Zoomobile Station',
         duration_minutes=15 ),
   ]

   ordered = order_route_legs_from_station(
      unordered,
      start_station='Main Zoomobile Station' )

   assert [
      ( leg.from_station, leg.to_station )
      for leg in ordered
   ] == SUMMER_LEG_STATIONS
   assert sum( leg.duration_minutes for leg in ordered ) == 75


def test_fetch_transportation_day_loop_summer_and_winter(
      db: DbControllers ) -> None:
   summer_loop = fetch_transportation_day_loop(
      db.conn,
      transportation=ZOOMOBILE,
      target_date=date( 2026, 6, 15 ) )
   winter_loop = fetch_transportation_day_loop(
      db.conn,
      transportation=ZOOMOBILE,
      target_date=date( 2026, 1, 15 ) )

   assert summer_loop is not None
   assert summer_loop.route == 'summer'
   assert summer_loop.main_station == 'Main Zoomobile Station'
   assert [
      ( leg.from_station, leg.to_station )
      for leg in summer_loop.legs
   ] == SUMMER_LEG_STATIONS
   assert summer_loop.duration_minutes() == 75

   assert winter_loop is not None
   assert winter_loop.route == 'winter'
   assert [
      ( leg.from_station, leg.to_station )
      for leg in winter_loop.legs
   ] == WINTER_LEG_STATIONS
   assert winter_loop.duration_minutes() == 60


def test_set_itinerary_saves_zoomobile_as_transportation_not_attraction(
      db: DbControllers ) -> None:
   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      transportations=[
         ItineraryTransportationInput(
            name=ZOOMOBILE,
            added_as_attraction=True ),
      ],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert result.success is True
   assert result.itinerary.attractions == []
   assert [ t.name for t in result.itinerary.transportations ] == [ ZOOMOBILE ]
   assert result.itinerary.transportations[ 0 ].added_as_attraction is True
   assert result.itinerary.transportations[ 0 ].to_dict()[ 'added_as_attraction' ] is True

   attraction_rows = db.conn.execute(
      'SELECT ATTRACTION FROM ItineraryAttraction;'
   ).fetchall()
   transportation_rows = db.conn.execute(
      """   SELECT TRANSPORTATION, ADDED_AS_ATTRACTION
            FROM ItineraryTransportation;
      """
   ).fetchall()
   leg_rows = db.conn.execute(
      'SELECT COUNT(*) AS count FROM ItineraryTransportationLeg;'
   ).fetchone()

   assert attraction_rows == []
   assert [ row[ 'TRANSPORTATION' ] for row in transportation_rows ] == [ ZOOMOBILE ]
   assert transportation_rows[ 0 ][ 'ADDED_AS_ATTRACTION' ] == 1
   assert leg_rows[ 'count' ] == 0


def test_schedule_zoomobile_expands_timed_legs(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      transportations=[
         ItineraryTransportationInput(
            name=ZOOMOBILE,
            added_as_attraction=True ),
      ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert schedule_itinerary_item(
      'attractions',
      ZOOMOBILE,
      start_time='10:00 AM',
   ).success

   saved = fetch_saved_itinerary( db.conn )
   assert len( saved.transportation_rows ) == 1
   transportation = saved.transportation_rows[ 0 ]
   assert transportation.start_time == '10:00 AM'
   assert transportation.end_time == '11:15 AM'
   assert len( transportation.legs ) == 5
   assert [
      ( leg.from_station, leg.to_station, leg.start_time, leg.end_time )
      for leg in transportation.legs
   ] == [
      ( 'Main Zoomobile Station', 'Canadian Domain Zoomobile Station', '10:00 AM', '10:20 AM' ),
      ( 'Canadian Domain Zoomobile Station', 'Africa Zoomobile Station', '10:20 AM', '10:30 AM' ),
      ( 'Africa Zoomobile Station', 'Tundra Zoomobile Station', '10:30 AM', '10:45 AM' ),
      ( 'Tundra Zoomobile Station', 'Eurasia Zoomobile Station', '10:45 AM', '11:00 AM' ),
      ( 'Eurasia Zoomobile Station', 'Main Zoomobile Station', '11:00 AM', '11:15 AM' ),
   ]

   attraction_count = db.conn.execute(
      'SELECT COUNT(*) AS count FROM ItineraryAttraction;'
   ).fetchone()[ 'count' ]
   assert attraction_count == 0


def test_unschedule_zoomobile_clears_parent_times_and_legs(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      transportations=[
         ItineraryTransportationInput(
            name=ZOOMOBILE,
            added_as_attraction=True ),
      ],
      guardians_talks=[],
      wild_encounters=[],
   ).success
   assert schedule_itinerary_item(
      'attractions',
      ZOOMOBILE,
      start_time='10:00 AM',
   ).success

   assert unschedule_itinerary_item( 'attractions', ZOOMOBILE ).success

   saved = fetch_saved_itinerary( db.conn )
   transportation = saved.transportation_rows[ 0 ]
   assert transportation.start_time is None
   assert transportation.end_time is None
   assert transportation.legs == []

   leg_count = db.conn.execute(
      'SELECT COUNT(*) AS count FROM ItineraryTransportationLeg;'
   ).fetchone()[ 'count' ]
   assert leg_count == 0
