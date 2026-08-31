from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.scheduling.items.schedule_item_travel_time_calculator import ScheduleItemTravelTimeCalculator
from api.models import Animal
from api.models import Itinerary
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.domain.map_location_kind import MapLocationKind
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode
from api.walk_graph.map_location_walk_node_lookup import MapLocationWalkNodeLookup
from api.walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver


ENTRANCE_NODE_ID = 'n-entrance'
LION_NODE_ID = 'n-lion'
CAROUSEL_NODE_ID = 'n-carousel'
CHEETAH_NODE_ID = 'n-cheetah'

ARRIVAL_SECONDS = 9 * 3600 + 30 * 60
LION_END_SECONDS = 10 * 3600 + 8 * 60
TRAVEL_MINUTES = 6
TRAVEL_SECONDS = TRAVEL_MINUTES * 60
EDGE_LENGTH_PX = WalkTravelTimeCalculator.WALK_PX_PER_MINUTE * TRAVEL_MINUTES


def _node( node_id: str, x_px: float, y_px: float ) -> WalkGraphNode:
   return {
      'id': node_id,
      'x': x_px / 100.0,
      'y': y_px / 100.0,
      'x_px': x_px,
      'y_px': y_px,
   }


TEST_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': ENTRANCE_NODE_ID,
   'nodes': [
      _node( ENTRANCE_NODE_ID, 0.0, 0.0 ),
      _node( LION_NODE_ID, 10.0, 0.0 ),
      _node( CAROUSEL_NODE_ID, 20.0, 0.0 ),
      _node( CHEETAH_NODE_ID, 30.0, 0.0 ),
   ],
   'edges': [
      {
         'from': ENTRANCE_NODE_ID,
         'to': LION_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
      {
         'from': LION_NODE_ID,
         'to': CAROUSEL_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
      {
         'from': CAROUSEL_NODE_ID,
         'to': CHEETAH_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
   ],
}

CAROUSEL_WALK_NODE = type(
   'WalkNode',
   (),
   { 'walk_node_id': CAROUSEL_NODE_ID },
)()


@pytest.fixture
def stub_schedule_item_travel_time_calculator(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   WalkGraphProvider.fetch.cache_clear()
   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: TEST_GRAPH )
   monkeypatch.setattr(
      ViewingSpotWalkNodeIdResolver,
      'resolve',
      lambda species, exhibit, enclosure_name=None: {
         ( 'African Lion', 'Africa Savanna', None ): LION_NODE_ID,
         ( 'Cheetah', 'Indo-Malaya Outdoor', None ): CHEETAH_NODE_ID,
      }.get( ( species, exhibit, enclosure_name ) ) )
   monkeypatch.setattr(
      MapLocationWalkNodeLookup,
      'for_map_location',
      lambda kind, name: CAROUSEL_WALK_NODE
      if kind == MapLocationKind.ATTRACTION and name == 'Conservation Carousel'
      else None )


def _saved_itinerary() -> SavedItinerary:
   return SavedItinerary(
      date_value='2026-06-20',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ],
   )


def _itinerary_with_lion() -> Itinerary:
   return ItineraryBuilder.build(
      date='2026-06-20',
      selected_exhibits=[],
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:30 AM',
      departure_time='5:00 PM' )


def Test_WalkNodeIdForAnimal_TestKnownAnimal_ExpectResolvedNode(
      stub_schedule_item_travel_time_calculator: None ) -> None:
   assert ScheduleItemTravelTimeCalculator.walk_node_id_for_animal(
      species='African Lion',
      exhibit='Africa Savanna',
      enclosure_name=None ) == LION_NODE_ID


def Test_WalkNodeIdForAttraction_TestKnownAttraction_ExpectResolvedNode(
      stub_schedule_item_travel_time_calculator: None ) -> None:
   assert ScheduleItemTravelTimeCalculator.walk_node_id_for_attraction(
      'Conservation Carousel' ) == CAROUSEL_NODE_ID


def Test_EntranceTravelSecondsToEarliestItem_TestScheduledLion_ExpectTravelFromEntrance(
      stub_schedule_item_travel_time_calculator: None ) -> None:
   assert ScheduleItemTravelTimeCalculator.entrance_travel_seconds_to_earliest_item(
      _itinerary_with_lion() ) == TRAVEL_SECONDS


def Test_EarliestScheduleStartSecondsWithTravel_TestAfterPreviousAnimal_ExpectEndPlusTravel(
      stub_schedule_item_travel_time_calculator: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   itinerary_context = {
      'animal_coordinator': object(),
      'attraction_coordinator': object(),
      'guardians_coordinator': object(),
      'wild_encounter_coordinator': object(),
      'visit_date_temp': 20.0,
   }

   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: _itinerary_with_lion() )

   earliest_start = ScheduleItemTravelTimeCalculator.earliest_schedule_start_seconds_with_travel(
      _saved_itinerary(),
      candidate_walk_node_id=CAROUSEL_NODE_ID,
      visit_anchor_seconds=ARRIVAL_SECONDS,
      itinerary_context=itinerary_context )

   assert earliest_start == LION_END_SECONDS + TRAVEL_SECONDS


def Test_EarliestScheduleStartSecondsWithTravel_TestMissingWalkNode_ExpectAnchor(
      stub_schedule_item_travel_time_calculator: None ) -> None:
   assert ScheduleItemTravelTimeCalculator.earliest_schedule_start_seconds_with_travel(
      _saved_itinerary(),
      candidate_walk_node_id=None,
      visit_anchor_seconds=ARRIVAL_SECONDS,
      itinerary_context={} ) == ARRIVAL_SECONDS
