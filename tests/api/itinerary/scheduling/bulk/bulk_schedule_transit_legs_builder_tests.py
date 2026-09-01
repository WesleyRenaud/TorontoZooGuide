from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.routing.itinerary_schedule_window import ItineraryScheduleWindow
from api.itinerary.scheduling.bulk.bulk_schedule_start_state import BulkScheduleStartState
from api.itinerary.scheduling.bulk.bulk_schedule_transit_legs_builder import BulkScheduleTransitLegsBuilder
from api.itinerary.scheduling.bulk.bulk_schedule_window_prep import BulkScheduleWindowPrep
from api.itinerary.scheduling.bulk.transportation_transit_ride_applier import TransportationTransitRideApplier
from api.walk_graph.domain.walk_graph import WalkGraph


EMPTY_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': 'n-entrance',
   'nodes': [
      {
         'id': 'n-entrance',
         'x': 0.0,
         'y': 0.0,
         'x_px': 0.0,
         'y_px': 0.0,
      },
   ],
   'edges': [],
}

WINDOW_PREP = BulkScheduleWindowPrep(
   saved_itinerary=SavedItinerary(
      date_value='2026-07-11',
      arrival_time='9:00 AM',
      departure_time='6:00 PM',
      transportation_rows=[
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=100,
            added_as_attraction=False ),
      ],
      animal_rows=[
         ItineraryAnimalRecord(
            species='Wood Bison',
            exhibit='Canadian Domain',
            old_likelihood=None,
            new_likelihood=100,
            start_time='11:00 AM',
            end_time='11:08 AM',
         ),
      ],
   ),
   previous_itinerary=None,
   itinerary_context={},
   anchor_seconds=9 * 3600,
   day_end_seconds=18 * 3600,
   blockers=[],
   walk_graph=EMPTY_GRAPH,
   start_state=BulkScheduleStartState(
      start_node_id='n-entrance',
      schedule_anchor_seconds=9 * 3600 ),
   schedule_windows=[
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=18 * 3600 ),
   ],
   loop_pins=[],
   visit_date='2026-07-11',
   zoo_operating_hours=None,
)


@pytest.fixture
def builder_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def Test_Apply_TestTransitZoomobile_ExpectRideApplierCalled(
      builder_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_transit_legs_builder.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: WINDOW_PREP.saved_itinerary )
   monkeypatch.setattr(
      TransportationTransitRideApplier,
      'apply',
      lambda conn, **kwargs: captured.update( kwargs ) )

   BulkScheduleTransitLegsBuilder.apply(
      builder_conn,
      prep=WINDOW_PREP )

   assert captured[ 'visit_date' ] == '2026-07-11'
   assert captured[ 'schedule_anchor_seconds' ] == 9 * 3600
   assert len( captured[ 'transit_rows' ] ) == 1
   assert captured[ 'transit_rows' ][ 0 ].added_as_attraction is False
   assert len( captured[ 'scheduled_animals' ] ) == 1
