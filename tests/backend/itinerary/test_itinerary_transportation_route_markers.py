from __future__ import annotations

from datetime import date

from test_transportation_seed import EXPECTED_ROUTE_LEG_MARKERS

from api.itinerary.domain.itinerary_transportation_route_markers import attach_itinerary_transportation_route_markers
from api.models.itinerary_transportation import ItineraryTransportation
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.request_connection import set_connection
from api.shared.enums.transportation_name import TransportationName
from api.transportation.data_access.transportation_route_leg_marker import fetch_transportation_route_leg_marker_ids
from conftest import DbControllers


ZOOMOBILE = TransportationName.ZOOMOBILE.value
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'


def test_fetch_transportation_route_leg_marker_ids_for_single_leg(
      db: DbControllers ) -> None:
   marker_ids = fetch_transportation_route_leg_marker_ids(
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
         ),
      ],
   )

   assert set( marker_ids ) == EXPECTED_ROUTE_LEG_MARKERS[
      ( 'summer', MAIN, CANADA )
   ]


def test_attach_itinerary_transportation_route_markers_uses_scheduled_legs(
      db: DbControllers ) -> None:
   set_connection( db.conn )

   try:
      transportation = ItineraryTransportation(
         name=ZOOMOBILE,
         legs=[
            ItineraryTransportationLeg(
               transportation=ZOOMOBILE,
               from_station=MAIN,
               to_station=CANADA,
               start_time='10:00 AM',
               end_time='10:20 AM',
            ),
            ItineraryTransportationLeg(
               transportation=ZOOMOBILE,
               from_station=CANADA,
               to_station=AFRICA,
               start_time='10:20 AM',
               end_time='10:30 AM',
            ),
         ],
      )

      attach_itinerary_transportation_route_markers(
         [ transportation ],
         target_date=date( 2026, 6, 15 ),
      )

      assert transportation.route == 'summer'
      assert set( transportation.route_markers ) == (
         EXPECTED_ROUTE_LEG_MARKERS[ ( 'summer', MAIN, CANADA ) ]
         | EXPECTED_ROUTE_LEG_MARKERS[ ( 'summer', CANADA, AFRICA ) ]
      )
   finally:
      set_connection( None )


def test_attach_itinerary_transportation_route_markers_skips_unscheduled(
      db: DbControllers ) -> None:
   set_connection( db.conn )

   try:
      transportation = ItineraryTransportation(
         name=ZOOMOBILE,
         legs=[],
      )

      attach_itinerary_transportation_route_markers(
         [ transportation ],
         target_date=date( 2026, 6, 15 ),
      )

      assert transportation.route is None
      assert transportation.route_markers == []
   finally:
      set_connection( None )
