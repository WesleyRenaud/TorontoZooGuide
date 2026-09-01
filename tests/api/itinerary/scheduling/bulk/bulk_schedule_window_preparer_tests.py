from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.routing.itinerary_schedule_window import ItineraryScheduleWindow
from api.itinerary.scheduling.bulk.bulk_schedule_window_preparer import BulkScheduleWindowPreparer
from api.itinerary.scheduling.items.prepared_schedule_window import PreparedScheduleWindow
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver


EMPTY_SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-20',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
)

SAVED_ITINERARY_WITH_TALK = SavedItinerary(
   date_value='2026-06-15',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
   guardians_talk_rows=[
      ItineraryGuardiansTalkRecord(
         talk_name="Grevy's Zebra",
         start_time='2:00 PM',
         end_time='2:30 PM',
         is_deleted=False,
      ),
   ],
)


def Test_HasItemsToRebuild_TestEmptyGuestItems_ExpectFalse() -> None:
   assert not BulkScheduleWindowPreparer.has_items_to_rebuild( EMPTY_SAVED_ITINERARY )


def Test_HasItemsToRebuild_TestGuardiansTalkOnly_ExpectTrue() -> None:
   assert BulkScheduleWindowPreparer.has_items_to_rebuild( SAVED_ITINERARY_WITH_TALK )


def Test_HasItemsToRebuild_TestAnimalRow_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
   )

   assert BulkScheduleWindowPreparer.has_items_to_rebuild( saved )


def Test_HasItemsToRebuild_TestAttractionRow_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      attraction_rows=[
         ItineraryAttractionRecord(
            attraction='Conservation Carousel',
            old_likelihood=None,
            new_likelihood=None,
         ),
      ],
   )

   assert BulkScheduleWindowPreparer.has_items_to_rebuild( saved )


def Test_HasItemsToRebuild_TestTransportationRow_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      transportation_rows=[
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=None,
            added_as_attraction=False,
         ),
      ],
   )

   assert BulkScheduleWindowPreparer.has_items_to_rebuild( saved )


def Test_HasItemsToRebuild_TestWildEncounterRow_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      wild_encounter_rows=[
         ItineraryWildEncounterRecord(
            wild_encounter='Grizzly Bear',
            start_time='2:00 PM',
            end_time='2:45 PM',
            is_deleted=False,
         ),
      ],
   )

   assert BulkScheduleWindowPreparer.has_items_to_rebuild( saved )


CAROUSEL = 'Conservation Carousel'
ENTRANCE_NODE_ID = 'n-entrance'
LION_NODE_ID = 'n-lion'
OPEN_ANCHOR_SECONDS = 9 * 3600 + 30 * 60

LION = ItineraryAnimalRecord(
   species='African Lion',
   exhibit='Africa Savanna',
   old_likelihood=None,
   new_likelihood=100,
)
PENGUIN = ItineraryAnimalRecord(
   species='African Penguin',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
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
         'id': LION_NODE_ID,
         'x': 0.1,
         'y': 0.0,
         'x_px': 10.0,
         'y_px': 0.0,
      },
   ],
   'edges': [
      {
         'from': ENTRANCE_NODE_ID,
         'to': LION_NODE_ID,
         'length_px': 10.0,
      },
   ],
}


def Test_PrepareWindows_TestScheduledGuestItems_ExpectClearAllBeforeRepack(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   from datetime import date

   prepared_window = PreparedScheduleWindow(
      saved_itinerary=SavedItinerary(
         date_value='2026-06-20',
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
      ),
      window=( 9 * 3600 + 30 * 60, 17 * 3600 ),
      visit_date=date( 2026, 6, 20 ),
   )
   cleared: list[ str ] = []

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_window_preparer.ItineraryBuilder.build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_window_preparer.ItineraryScheduleClearer.clear_all',
      lambda conn: cleared.append( 'clear_all' ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_window_preparer.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-20',
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
         animal_rows=[
            ItineraryAnimalRecord(
               species='African Lion',
               exhibit='Africa Savanna',
               old_likelihood=None,
               new_likelihood=100 ),
         ],
         attraction_rows=[
            ItineraryAttractionRecord(
               attraction=CAROUSEL,
               old_likelihood=None,
               new_likelihood=100 ),
         ],
      ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_window_preparer.WalkGraphProvider.fetch',
      lambda: {
         'map_width_px': 100,
         'map_height_px': 100,
         'entrance_node_id': 'n-1',
         'nodes': [],
         'edges': [],
      } )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_window_preparer.ItineraryStopResolver.resolve_fixed_time',
      lambda itinerary: [] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_window_preparer.BulkScheduleLoopPinAttacher.separate_boundaries_and_pins',
      lambda conn, itinerary, fixed_time_stops: ( [], [] ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_window_preparer.ItineraryScheduleWindowPartitioner.partition',
      lambda schedule_anchor_seconds, day_end_seconds, boundary_stops: [
         ItineraryScheduleWindow(
            start_seconds=schedule_anchor_seconds,
            end_seconds=day_end_seconds ),
      ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_window_preparer.BulkScheduleLoopPinAttacher.keep_completable',
      lambda schedule_windows, loop_pins: loop_pins )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_window_preparer.ItineraryProvider.fetch_itinerary_date',
      lambda conn: '2026-06-20' )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_window_preparer.ZooHoursProvider.fetch_zoo_hours_record',
      lambda conn, visit_date: None )

   BulkScheduleWindowPreparer.prepare_windows(
      sqlite3.connect( ':memory:' ),
      prepared_window=prepared_window,
      itinerary_context={} )

   assert cleared == [ 'clear_all' ]


def Test_StartState_TestUnscheduledAnimals_ExpectEntranceAnchor(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ViewingSpotWalkNodeIdResolver,
      'resolve',
      lambda species, exhibit, enclosure_name=None: (
         LION_NODE_ID
         if species == 'African Lion' and exhibit == 'Africa Savanna'
         else None ) )

   start_state = BulkScheduleWindowPreparer.start_state(
      TEST_GRAPH,
      [ LION, PENGUIN ],
      OPEN_ANCHOR_SECONDS )

   assert start_state.start_node_id == ENTRANCE_NODE_ID
   assert start_state.schedule_anchor_seconds == OPEN_ANCHOR_SECONDS


def Test_StartState_TestPreviouslyScheduledAnimal_ExpectResumeAfterLastEnd(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   scheduled_lion = ItineraryAnimalRecord(
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100,
      start_time='9:00 AM',
      end_time='9:08 AM',
   )

   monkeypatch.setattr(
      ViewingSpotWalkNodeIdResolver,
      'resolve',
      lambda species, exhibit, enclosure_name=None: (
         LION_NODE_ID
         if species == 'African Lion' and exhibit == 'Africa Savanna'
         else None ) )

   start_state = BulkScheduleWindowPreparer.start_state(
      TEST_GRAPH,
      [ scheduled_lion, PENGUIN ],
      OPEN_ANCHOR_SECONDS )

   assert start_state.start_node_id == LION_NODE_ID
   assert start_state.schedule_anchor_seconds == OPEN_ANCHOR_SECONDS
