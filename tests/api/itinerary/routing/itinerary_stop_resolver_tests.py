from __future__ import annotations

import pytest

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.routing.itinerary_stop import ENTRANCE_ITEM_KEY
from api.itinerary.routing.itinerary_stop_resolver import ItineraryStopResolver
from api.models import Animal
from api.models import Attraction
from api.models import GuardiansTalk
from api.models import Itinerary
from api.models import WildEncounter
from api.shared.enums import Position, ScheduleItemKind
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.domain.map_location_kind import MapLocationKind
from api.walk_graph.domain.map_location_walk_node import MapLocationWalkNode
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode
from api.walk_graph.map_location_walk_node_lookup import MapLocationWalkNodeLookup
from api.walk_graph.viewing_walk_node_id_resolver import ViewingWalkNodeIdResolver


VISIT_DATE = '2026-06-20'
ARRIVAL_TIME = '9:30 AM'
DEPARTURE_TIME = '5:00 PM'

ENTRANCE_NODE_ID = 'n-1'
LION_WALK_NODE_ID = 'n-2001'
ENCOUNTER_WALK_NODE_ID = 'n-3001'

KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'
WALK_THRU_WALK_NODE_ID = 'n-walk-thru'
MEETING_SPOT = 'Wild Encounter - Penguin Meeting Spot'
MISSING_NODE_ID = 'missing-node'


def _node( node_id: str, x: float, y: float ) -> WalkGraphNode:
   return {
      'id': node_id,
      'x': x,
      'y': y,
      'x_px': x,
      'y_px': y,
   }


TEST_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': ENTRANCE_NODE_ID,
   'nodes': [
      _node( ENTRANCE_NODE_ID, 61.414, 91.366 ),
      _node( LION_WALK_NODE_ID, 50.0, 60.0 ),
      _node( ENCOUNTER_WALK_NODE_ID, 40.0, 55.0 ),
   ],
   'edges': [],
}

SCHEDULED_LION = Animal(
   species='African Lion',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
   enclosure_type='Outdoor',
   x_coord=50.0,
   y_coord=60.0,
   start_time='10:00 AM',
   end_time='10:30 AM',
)

SCHEDULED_ENCOUNTER = WildEncounter(
   name='Guardians of White Rhinos',
   meeting_spot=MEETING_SPOT,
   link='https://example.com/rhinos',
   x_coord=40.0,
   y_coord=55.0,
   start_time='11:00 AM',
   end_time='11:45 AM',
)

ENCOUNTER_MAP_LOCATION = MapLocationWalkNode(
   kind=MapLocationKind.WILD_ENCOUNTER_MEETING_SPOT,
   name=MEETING_SPOT,
   location='',
   x=40.0,
   y=55.0,
   walk_node_id=ENCOUNTER_WALK_NODE_ID,
   snap_distance_px=0.0,
)

COVERED_KANGAROO = Animal(
   species='Western Grey Kangaroo',
   exhibit='Australasia Outdoor',
   covered_by_talk=True,
   start_time='11:00 AM',
   end_time='11:30 AM',
)

COVERED_LION = Animal(
   species='African Lion',
   exhibit='Africa Savanna',
   covered_by_talk=True,
   start_time='11:00 AM',
   end_time='11:30 AM',
)

SCHEDULED_WALK_THRU = Attraction(
   name=KANGAROO_WALK_THRU,
   free_with_admission=0,
   likelihood=100,
   start_time='11:00 AM',
   end_time='11:30 AM',
)

WALK_THRU_MAP_LOCATION = MapLocationWalkNode(
   kind=MapLocationKind.ATTRACTION,
   name=KANGAROO_WALK_THRU,
   location='',
   x=45.0,
   y=50.0,
   walk_node_id=WALK_THRU_WALK_NODE_ID,
   snap_distance_px=0.0,
)

TALK_WALK_NODE_ID = 'n-talk'
SCHEDULED_TALK = GuardiansTalk(
   name='Turtle Talk',
   location='Americas Pavilion',
   x_coord=35.0,
   y_coord=45.0,
   start_time='2:00 PM',
   end_time='2:15 PM',
)
DELETED_TALK = GuardiansTalk(
   name='Deleted Talk',
   location='Americas Pavilion',
   x_coord=35.0,
   y_coord=45.0,
   is_deleted=True,
   start_time='3:00 PM',
   end_time='3:15 PM',
)
DELETED_ENCOUNTER = WildEncounter(
   name='Deleted Encounter',
   meeting_spot=MEETING_SPOT,
   link='',
   is_deleted=True,
   start_time='11:00 AM',
   end_time='11:45 AM',
)
TALK_MAP_LOCATION = MapLocationWalkNode(
   kind=MapLocationKind.GUARDIANS_TALK,
   name=SCHEDULED_TALK.name,
   location=SCHEDULED_TALK.location,
   x=35.0,
   y=45.0,
   walk_node_id=TALK_WALK_NODE_ID,
   snap_distance_px=0.0,
)


def _clear_walk_graph_provider_cache() -> None:
   WalkGraphProvider.fetch.cache_clear()


def _itinerary(
      *,
      animals: list[ Animal ] | None = None,
      attractions: list[ Attraction ] | None = None,
      guardians_talks: list[ GuardiansTalk ] | None = None,
      wild_encounters: list[ WildEncounter ] | None = None ) -> Itinerary:
   return ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=animals or [],
      attractions=attractions or [],
      transportations=[],
      transportation_stations=[],
      guardians_talks=guardians_talks or [],
      wild_encounters=wild_encounters or [],
      events=[],
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME )


def _animal_item_key( animal: Animal ) -> str:
   return AnimalScheduleItemKey.wire(
      species=animal.species,
      exhibit=animal.exhibit,
      enclosure_name=animal.enclosure_name )


def _graph_node( node_id: str ) -> WalkGraphNode:
   return next( node for node in TEST_GRAPH[ 'nodes' ] if node[ 'id' ] == node_id )


@pytest.fixture
def stub_itinerary_stop_dependencies( monkeypatch: pytest.MonkeyPatch ) -> None:
   _clear_walk_graph_provider_cache()
   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: TEST_GRAPH )
   monkeypatch.setattr(
      ViewingWalkNodeIdResolver,
      'resolve',
      lambda *args, **kwargs: LION_WALK_NODE_ID )
   monkeypatch.setattr(
      MapLocationWalkNodeLookup,
      'for_map_location',
      lambda kind, name, *, location='': (
         ENCOUNTER_MAP_LOCATION
         if kind == MapLocationKind.WILD_ENCOUNTER_MEETING_SPOT
         else None ) )
   yield


def Test_Entrance_TestWalkGraph_ExpectEntranceStop(
      stub_itinerary_stop_dependencies: None ) -> None:
   entrance_node = _graph_node( TEST_GRAPH[ 'entrance_node_id' ] )

   entrance_stop = ItineraryStopResolver.entrance()

   assert entrance_stop.schedule_item_kind == ScheduleItemKind.ENTRANCE
   assert entrance_stop.item_key == ENTRANCE_ITEM_KEY
   assert entrance_stop.walk_node_ids == [ entrance_node[ 'id' ] ]
   assert entrance_stop.x_coord == entrance_node[ 'x' ]
   assert entrance_stop.y_coord == entrance_node[ 'y' ]


def Test_Resolve_TestAnimal_ExpectEntranceAndAnimalStops(
      stub_itinerary_stop_dependencies: None ) -> None:
   itinerary = _itinerary( animals=[ SCHEDULED_LION ] )
   animal_item_key = _animal_item_key( SCHEDULED_LION )

   stops = ItineraryStopResolver.resolve( itinerary )
   lion_stop = next(
      stop
      for stop in stops
      if stop.item_key == animal_item_key )

   assert stops[ Position.FIRST ].schedule_item_kind == ScheduleItemKind.ENTRANCE
   assert lion_stop.schedule_item_kind == ScheduleItemKind.ANIMAL
   assert lion_stop.walk_node_ids == [ LION_WALK_NODE_ID ]


def Test_Resolve_TestWildEncounter_ExpectMeetingSpotWalkNode(
      stub_itinerary_stop_dependencies: None ) -> None:
   itinerary = _itinerary( wild_encounters=[ SCHEDULED_ENCOUNTER ] )

   stops = ItineraryStopResolver.resolve( itinerary )
   encounter_stop = next(
      stop
      for stop in stops
      if stop.schedule_item_kind == ScheduleItemKind.WILD_ENCOUNTER )

   assert encounter_stop.item_key == SCHEDULED_ENCOUNTER.name
   assert encounter_stop.meeting_spot == SCHEDULED_ENCOUNTER.meeting_spot
   assert encounter_stop.walk_node_ids == [ ENCOUNTER_MAP_LOCATION.walk_node_id ]
   assert encounter_stop.is_fixed_time
   assert encounter_stop.start_time == SCHEDULED_ENCOUNTER.start_time
   assert encounter_stop.end_time == SCHEDULED_ENCOUNTER.end_time


def Test_ResolveFixedTime_TestWildEncounter_ExpectOnlyFixedTimeStops(
      stub_itinerary_stop_dependencies: None ) -> None:
   itinerary = _itinerary( wild_encounters=[ SCHEDULED_ENCOUNTER ] )

   fixed_time_stops = ItineraryStopResolver.resolve_fixed_time( itinerary )

   assert [
      stop.item_key
      for stop in fixed_time_stops
   ] == [ SCHEDULED_ENCOUNTER.name ]


def Test_Resolve_TestCoveredKangarooWithWalkThru_ExpectAttractionStopOnly(
      stub_itinerary_stop_dependencies: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      MapLocationWalkNodeLookup,
      'for_map_location',
      lambda kind, name, *, location='': (
         WALK_THRU_MAP_LOCATION
         if kind == MapLocationKind.ATTRACTION and name == SCHEDULED_WALK_THRU.name
         else (
            ENCOUNTER_MAP_LOCATION
            if kind == MapLocationKind.WILD_ENCOUNTER_MEETING_SPOT
            else None
         ) ) )
   itinerary = _itinerary(
      animals=[ COVERED_KANGAROO ],
      attractions=[ SCHEDULED_WALK_THRU ] )

   stops = ItineraryStopResolver.resolve( itinerary )
   animal_stops = [
      stop
      for stop in stops
      if (
         stop.schedule_item_kind == ScheduleItemKind.ANIMAL
         and COVERED_KANGAROO.species in stop.item_key )
   ]
   attraction_stops = [
      stop
      for stop in stops
      if (
         stop.schedule_item_kind == ScheduleItemKind.ATTRACTION
         and stop.item_key == SCHEDULED_WALK_THRU.name )
   ]

   assert animal_stops == []
   assert [ stop.item_key for stop in attraction_stops ] == [ SCHEDULED_WALK_THRU.name ]
   assert attraction_stops[ Position.FIRST ].start_time == SCHEDULED_WALK_THRU.start_time
   assert attraction_stops[ Position.FIRST ].end_time == SCHEDULED_WALK_THRU.end_time
   assert attraction_stops[ Position.FIRST ].walk_node_ids == [
      WALK_THRU_MAP_LOCATION.walk_node_id
   ]


def Test_Resolve_TestCoveredLionTalk_ExpectNoAnimalStop(
      stub_itinerary_stop_dependencies: None ) -> None:
   itinerary = _itinerary( animals=[ COVERED_LION ] )

   stops = ItineraryStopResolver.resolve( itinerary )
   animal_stops = [
      stop
      for stop in stops
      if (
         stop.schedule_item_kind == ScheduleItemKind.ANIMAL
         and COVERED_LION.species in stop.item_key )
   ]

   assert animal_stops == []


def Test_Resolve_TestGuardiansTalk_ExpectTalkStop(
      stub_itinerary_stop_dependencies: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   def for_map_location(
         kind: MapLocationKind,
         name: str,
         *,
         location: str = '' ) -> MapLocationWalkNode | None:
      if kind == MapLocationKind.GUARDIANS_TALK and name == SCHEDULED_TALK.name:
         return TALK_MAP_LOCATION
      return None

   monkeypatch.setattr( MapLocationWalkNodeLookup, 'for_map_location', for_map_location )
   itinerary = _itinerary( guardians_talks=[ SCHEDULED_TALK, DELETED_TALK ] )

   stops = ItineraryStopResolver.resolve( itinerary )
   talk_stops = [
      stop
      for stop in stops
      if stop.schedule_item_kind == ScheduleItemKind.GUARDIANS_TALK
   ]

   assert [ stop.item_key for stop in talk_stops ] == [ SCHEDULED_TALK.name ]
   assert talk_stops[ Position.FIRST ].walk_node_ids == [ TALK_MAP_LOCATION.walk_node_id ]


def Test_Resolve_TestDeletedWildEncounter_ExpectSkipped(
      stub_itinerary_stop_dependencies: None ) -> None:
   itinerary = _itinerary( wild_encounters=[ DELETED_ENCOUNTER ] )

   stops = ItineraryStopResolver.resolve( itinerary )
   encounter_stops = [
      stop
      for stop in stops
      if stop.schedule_item_kind == ScheduleItemKind.WILD_ENCOUNTER
   ]

   assert encounter_stops == []


def Test_WalkGraphNodeById_TestMissingNode_ExpectValueError() -> None:
   missing_node_id = MISSING_NODE_ID

   with pytest.raises( ValueError, match='not found' ):
      ItineraryStopResolver._walk_graph_node_by_id( TEST_GRAPH, missing_node_id )
