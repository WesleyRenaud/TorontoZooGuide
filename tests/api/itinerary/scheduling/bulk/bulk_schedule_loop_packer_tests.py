from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.routing.itinerary_schedule_window import ItineraryScheduleWindow
from api.itinerary.scheduling.bulk.attraction_animal_coverer import AttractionAnimalCoverer
from api.itinerary.scheduling.bulk.bulk_schedule_loop_packer import BulkScheduleLoopPacker
from api.itinerary.scheduling.bulk.bulk_schedule_start_state import BulkScheduleStartState
from api.itinerary.scheduling.bulk.bulk_schedule_window_prep import BulkScheduleWindowPrep
from api.itinerary.scheduling.bulk.guardians_talk_animal_coverer import GuardiansTalkAnimalCoverer
from api.itinerary.scheduling.bulk.loop_schedule_unit import LoopScheduleUnit
from api.walk_graph.domain.walk_graph import WalkGraph


SPLASH_ISLAND = 'Splash Island'
KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'
ENTRANCE_NODE_ID = 'n-entrance'
SPLASH_NODE_ID = 'n-splash'

KANGAROO = ItineraryAnimalRecord(
   species='Western Grey Kangaroo',
   exhibit='Australasia Outdoor',
   old_likelihood=None,
   new_likelihood=100,
)
TIGER = ItineraryAnimalRecord(
   species='Amur Tiger',
   exhibit='Eurasia Wilds',
   old_likelihood=None,
   new_likelihood=100,
)
WALK_THRU = ItineraryAttractionRecord(
   attraction=KANGAROO_WALK_THRU,
   old_likelihood=None,
   new_likelihood=100,
)
SPLASH = ItineraryAttractionRecord(
   attraction=SPLASH_ISLAND,
   old_likelihood=None,
   new_likelihood=100,
)

TEST_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': ENTRANCE_NODE_ID,
   'nodes': [
      {
         'id': ENTRANCE_NODE_ID,
         'x': 0.0,
         'y': 0.0,
         'x_px': 0.0,
         'y_px': 0.0,
      },
      {
         'id': SPLASH_NODE_ID,
         'x': 0.1,
         'y': 0.0,
         'x_px': 10.0,
         'y_px': 0.0,
      },
   ],
   'edges': [
      {
         'from': ENTRANCE_NODE_ID,
         'to': SPLASH_NODE_ID,
         'length_px': 10.0,
      },
   ],
}

WINDOW_PREP = BulkScheduleWindowPrep(
   saved_itinerary=SavedItinerary(
      date_value='2026-06-20',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   ),
   previous_itinerary=ItineraryBuilder.empty(),
   itinerary_context={},
   anchor_seconds=9 * 3600 + 30 * 60,
   day_end_seconds=17 * 3600,
   blockers=[],
   walk_graph=TEST_GRAPH,
   start_state=BulkScheduleStartState(
      start_node_id=ENTRANCE_NODE_ID,
      schedule_anchor_seconds=9 * 3600 + 30 * 60 ),
   schedule_windows=[
      ItineraryScheduleWindow(
         start_seconds=9 * 3600 + 30 * 60,
         end_seconds=17 * 3600 ),
   ],
   loop_pins=[],
   visit_date=None,
   zoo_operating_hours=None,
)


@pytest.fixture
def packer_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def Test_PackStops_TestAttractionOnly_ExpectAttractionLoopUnit(
      packer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   splash_unit = LoopScheduleUnit(
      loop_id='splash',
      stops=[ SPLASH ],
      entry_walk_node_id=SPLASH_NODE_ID,
      exit_walk_node_id=SPLASH_NODE_ID,
      side_cluster_id=None,
      loop_index_in_side_cluster=None,
      traversal=None )
   captured_loop_units: list[ list[ LoopScheduleUnit ] ] = []

   monkeypatch.setattr(
      GuardiansTalkAnimalCoverer,
      'keys_to_cover',
      lambda conn, loop_pins, animals: {} )
   monkeypatch.setattr(
      AttractionAnimalCoverer,
      'keys_to_cover',
      lambda conn, attraction_names, animals: {} )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_packer.MasterRouteLoopStopGrouper.group',
      lambda stops: [ [ SPLASH ] ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_packer.LoopScheduleUnitBuilder.build',
      lambda loop_groups: [ splash_unit ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_packer.BulkScheduleLoopPinAttacher.attach_to_windows',
      lambda schedule_windows, loop_pins: schedule_windows )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_packer.MasterRouteLoopScheduler.schedule',
      lambda conn, loop_units, **kwargs: (
         captured_loop_units.append( loop_units ),
         [],
         kwargs[ 'schedule_cursor_seconds' ],
      )[ 1: ] )

   packing = BulkScheduleLoopPacker.pack_stops(
      packer_conn,
      prep=WINDOW_PREP,
      stops_to_schedule=[ SPLASH ] )

   assert packing.covered_by_talk == {}
   assert packing.covered_by_attraction == {}
   assert len( packing.loop_units ) == 1
   assert packing.loop_units[ 0 ].stops == [ SPLASH ]
   assert packing.remaining_stops == []
   assert captured_loop_units == [ [ splash_unit ] ]


def Test_PackStops_TestWalkThruAndAnimals_ExpectKangarooExcludedFromPackList(
      packer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   covered = {
      KANGAROO.viewing_spot_key(): ( KANGAROO, KANGAROO_WALK_THRU ),
   }
   grouped_stops: list[ list[ object ] ] = []

   monkeypatch.setattr(
      GuardiansTalkAnimalCoverer,
      'keys_to_cover',
      lambda conn, loop_pins, animals: {} )
   monkeypatch.setattr(
      AttractionAnimalCoverer,
      'keys_to_cover',
      lambda conn, attraction_names, animals: covered )
   monkeypatch.setattr(
      AttractionAnimalCoverer,
      'merge_keys',
      lambda covered_by_talk, covered_by_attraction: covered_by_attraction )
   monkeypatch.setattr(
      GuardiansTalkAnimalCoverer,
      'excluding_covered',
      lambda animals, covered_keys: [
         animal
         for animal in animals
         if animal.viewing_spot_key() not in covered_keys
      ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_packer.MasterRouteLoopStopGrouper.group',
      lambda stops: grouped_stops.append( stops ) or [ stops ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_packer.LoopScheduleUnitBuilder.build',
      lambda loop_groups: [] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_packer.BulkScheduleLoopPinAttacher.attach_to_windows',
      lambda schedule_windows, loop_pins: schedule_windows )

   packing = BulkScheduleLoopPacker.pack_stops(
      packer_conn,
      prep=WINDOW_PREP,
      stops_to_schedule=[ KANGAROO, TIGER, WALK_THRU ] )

   assert packing.covered_by_attraction == covered
   assert grouped_stops == [ [ TIGER, WALK_THRU ] ]
