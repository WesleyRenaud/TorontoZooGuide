from __future__ import annotations

from datetime import date

from test_transportation_seed import EXPECTED_ROUTE_LEG_MARKERS

from api.itinerary.data_access.itinerary_transportation_provider import ItineraryTransportationProvider
from api.itinerary.data_access.itinerary_transportation_route_marker_provider import ItineraryTransportationRouteMarkerProvider
from api.itinerary.data_access.schedule_itinerary_transportation_provider import ScheduleItineraryTransportationProvider
from api.itinerary.data_access.unschedule_itinerary_item_provider import UnscheduleItineraryItemProvider
from api.itinerary.domain.transportation_route_marker_sequences_builder import TransportationRouteMarkerSequencesBuilder
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.shared.enums.transportation_name import TransportationName
from api.transportation.data_access.transportation_route_leg_marker_provider import TransportationRouteLegMarkerProvider
from conftest import DbControllers


ZOOMOBILE = TransportationName.ZOOMOBILE.value
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'
TUNDRA = 'Tundra Zoomobile Station'
EURASIA = 'Eurasia Zoomobile Station'


def ordered_marker_ids(
      prefix: str,
      start: int,
      end: int,
      maximum: int ) -> list[ str ]:
   marker_numbers = (
      range( start, end + 1 )
      if start <= end
      else [ *range( start, maximum + 1 ), *range( 1, end + 1 ) ]
   )

   return [
      f'{ prefix }-{ str( marker_number ).zfill( 3 ) }'
      for marker_number in marker_numbers
   ]


def test_fetch_transportation_route_leg_marker_ids_preserves_travel_order(
      db: DbControllers ) -> None:
   marker_ids_result = TransportationRouteLegMarkerProvider.fetch_transportation_route_leg_marker_ids(
      db.conn,
      transportation=ZOOMOBILE,
      route='summer',
      legs=[
         ItineraryTransportationLeg(
            transportation=ZOOMOBILE,
            from_station=MAIN,
            to_station=CANADA,
            start_time='10:00 AM',
            end_time='10:20 AM',
            added_as_attraction=False,
         ),
      ],
   )

   assert marker_ids_result == ordered_marker_ids( 'zm-s', 5, 85, 297 )
   assert set( marker_ids_result ) == EXPECTED_ROUTE_LEG_MARKERS[
      ( 'summer', MAIN, CANADA )
   ]


def test_fetch_wraparound_leg_markers_preserve_travel_order(
      db: DbControllers ) -> None:
   marker_ids_result = TransportationRouteLegMarkerProvider.fetch_transportation_route_leg_marker_ids(
      db.conn,
      transportation=ZOOMOBILE,
      route='summer',
      legs=[
         ItineraryTransportationLeg(
            transportation=ZOOMOBILE,
            from_station=EURASIA,
            to_station=MAIN,
            start_time='11:00 AM',
            end_time='11:15 AM',
            added_as_attraction=False,
         ),
      ],
   )

   assert marker_ids_result == ordered_marker_ids( 'zm-s', 252, 4, 297 )
   assert marker_ids_result[ 0 ] == 'zm-s-252'
   assert marker_ids_result[ -1 ] == 'zm-s-004'


def test_build_sequences_splits_discontinuous_legs(
      db: DbControllers ) -> None:
   sequences = TransportationRouteMarkerSequencesBuilder.build(
      db.conn,
      transportation=ZOOMOBILE,
      route='summer',
      legs=[
         ItineraryTransportationLeg(
            transportation=ZOOMOBILE,
            from_station=MAIN,
            to_station=CANADA,
            start_time='10:00 AM',
            end_time='10:20 AM',
            added_as_attraction=False,
         ),
         ItineraryTransportationLeg(
            transportation=ZOOMOBILE,
            from_station=TUNDRA,
            to_station=EURASIA,
            start_time='2:00 PM',
            end_time='2:15 PM',
            added_as_attraction=False,
         ),
      ],
   )

   assert len( sequences ) == 2
   assert sequences[ 0 ] == ordered_marker_ids( 'zm-s', 5, 85, 297 )
   assert sequences[ 1 ] == ordered_marker_ids( 'zm-s', 185, 251, 297 )


def test_build_sequences_concatenates_consecutive_legs(
      db: DbControllers ) -> None:
   sequences = TransportationRouteMarkerSequencesBuilder.build(
      db.conn,
      transportation=ZOOMOBILE,
      route='summer',
      legs=[
         ItineraryTransportationLeg(
            transportation=ZOOMOBILE,
            from_station=MAIN,
            to_station=CANADA,
            start_time='10:00 AM',
            end_time='10:20 AM',
            added_as_attraction=False,
         ),
         ItineraryTransportationLeg(
            transportation=ZOOMOBILE,
            from_station=CANADA,
            to_station=AFRICA,
            start_time='10:20 AM',
            end_time='10:30 AM',
            added_as_attraction=False,
         ),
      ],
   )

   assert len( sequences ) == 1
   assert sequences[ 0 ] == (
      ordered_marker_ids( 'zm-s', 5, 85, 297 )
      + ordered_marker_ids( 'zm-s', 86, 127, 297 )
   )


def test_schedule_persists_route_marker_sequences(
      db: DbControllers ) -> None:
   cur = db.conn.cursor()

   try:
      ItineraryTransportationProvider.insert_itinerary_transportation(
         cur,
         transportation=ZOOMOBILE,
         old_likelihood=None,
         new_likelihood=3,
         added_as_attraction=True )
      applied = ScheduleItineraryTransportationProvider.apply_itinerary_transportation_schedule(
         cur,
         name=ZOOMOBILE,
         added_as_attraction=True,
         start_time='10:00 AM',
         route='summer',
         legs=[
            TransportationRouteLegSegment(
               from_station=MAIN,
               to_station=CANADA,
               duration_minutes=20,
            ),
            TransportationRouteLegSegment(
               from_station=TUNDRA,
               to_station=EURASIA,
               duration_minutes=15,
            ),
         ],
      )
      db.conn.commit()

      assert applied is True

      route = cur.execute(
         """   SELECT ROUTE
               FROM ItineraryTransportation
               WHERE TRANSPORTATION = ?;
         """,
         ( ZOOMOBILE, ),
      ).fetchone()[ 'ROUTE' ]
      markers = [
         marker
         for marker in ItineraryTransportationRouteMarkerProvider.fetch_itinerary_transportation_route_markers( db.conn )
         if marker.transportation == ZOOMOBILE
      ]

      assert route == 'summer'
      assert { marker.sequence for marker in markers } == { 0, 1 }
      assert len( markers ) > 0
   finally:
      cur.close()


def test_clear_transportation_schedule_removes_route_markers(
      db: DbControllers ) -> None:
   cur = db.conn.cursor()

   try:
      ItineraryTransportationProvider.insert_itinerary_transportation(
         cur,
         transportation=ZOOMOBILE,
         old_likelihood=None,
         new_likelihood=3,
         route='summer',
         added_as_attraction=True )
      ItineraryTransportationProvider.insert_itinerary_transportation_legs(
         cur,
         transportation=ZOOMOBILE,
         added_as_attraction=True,
         legs=[
            ItineraryTransportationLeg(
               transportation=ZOOMOBILE,
               from_station=MAIN,
               to_station=CANADA,
               start_time='10:00 AM',
               end_time='10:20 AM',
               added_as_attraction=True,
            ),
         ],
      )
      ItineraryTransportationRouteMarkerProvider.insert_itinerary_transportation_route_markers(
         cur,
         transportation=ZOOMOBILE,
         added_as_attraction=True,
         route_marker_sequences=[
            ordered_marker_ids( 'zm-s', 5, 85, 297 ),
         ],
      )
      UnscheduleItineraryItemProvider.clear_itinerary_transportation_schedule(
         cur,
         name=ZOOMOBILE,
         added_as_attraction=True )
      db.conn.commit()

      route = cur.execute(
         """   SELECT ROUTE
               FROM ItineraryTransportation
               WHERE TRANSPORTATION = ?;
         """,
         ( ZOOMOBILE, ),
      ).fetchone()[ 'ROUTE' ]

      assert route is None
      assert ItineraryTransportationRouteMarkerProvider.fetch_itinerary_transportation_route_markers( db.conn ) == []
   finally:
      cur.close()
