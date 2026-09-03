from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.routing.transit_ride_endpoint import TransitRideEndpoint
from api.itinerary.routing.transportation_walk_node_resolver import TransportationWalkNodeResolver
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.scheduling.items.schedule_item_travel_time_calculator import ScheduleItemTravelTimeCalculator
from api.models import Animal
from api.models import Attraction
from api.models import GuardiansTalk
from api.models import Itinerary
from api.models import ItineraryEvent
from api.models import WildEncounter
from api.models.itinerary_transportation import ItineraryTransportation
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryEventType
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.domain.map_location_kind import MapLocationKind
from api.walk_graph.domain.map_location_walk_node import MapLocationWalkNode
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode
from api.walk_graph.map_location_walk_node_lookup import MapLocationWalkNodeLookup
from api.walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver


ENTRANCE_NODE_ID = 'n-entrance'
LION_NODE_ID = 'n-lion'
CAROUSEL_NODE_ID = 'n-carousel'
CHEETAH_NODE_ID = 'n-cheetah'
TALK_NODE_ID = 'n-talk'
ENCOUNTER_NODE_ID = 'n-encounter'
OFFBOARD_NODE_ID = 'n-offboard'
ONBOARD_NODE_ID = 'n-onboard'

ARRIVAL_SECONDS = 9 * 3600 + 30 * 60
LION_END_SECONDS = 10 * 3600 + 8 * 60
CAROUSEL_END_SECONDS = 11 * 3600 + 15 * 60
TRAVEL_MINUTES = 6
TRAVEL_SECONDS = TRAVEL_MINUTES * 60
EDGE_LENGTH_PX = WalkTravelTimeCalculator.WALK_PX_PER_MINUTE * TRAVEL_MINUTES

ZOOMOBILE = 'Zoomobile'
CAROUSEL = 'Conservation Carousel'
ZEBRA_TALK = "Grevy's Zebra"
MEETING_SPOT = 'Wild Encounter - Africa Meeting Spot'


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
      _node( TALK_NODE_ID, 40.0, 0.0 ),
      _node( ENCOUNTER_NODE_ID, 50.0, 0.0 ),
      _node( ONBOARD_NODE_ID, 60.0, 0.0 ),
      _node( OFFBOARD_NODE_ID, 70.0, 0.0 ),
   ],
   'edges': [
      {
         'from': ENTRANCE_NODE_ID,
         'to': LION_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
      {
         'from': LION_NODE_ID,
         'to': ENTRANCE_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
      {
         'from': LION_NODE_ID,
         'to': CAROUSEL_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
      {
         'from': CAROUSEL_NODE_ID,
         'to': LION_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
      {
         'from': CAROUSEL_NODE_ID,
         'to': CHEETAH_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
      {
         'from': CHEETAH_NODE_ID,
         'to': CAROUSEL_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
      {
         'from': CHEETAH_NODE_ID,
         'to': TALK_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
      {
         'from': TALK_NODE_ID,
         'to': CHEETAH_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
      {
         'from': TALK_NODE_ID,
         'to': ENCOUNTER_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
      {
         'from': ENCOUNTER_NODE_ID,
         'to': TALK_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
      {
         'from': ENCOUNTER_NODE_ID,
         'to': ONBOARD_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
      {
         'from': ONBOARD_NODE_ID,
         'to': ENCOUNTER_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
      {
         'from': ONBOARD_NODE_ID,
         'to': OFFBOARD_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
      {
         'from': OFFBOARD_NODE_ID,
         'to': ONBOARD_NODE_ID,
         'length_px': EDGE_LENGTH_PX,
      },
   ],
}

def _walk_node(
      kind: MapLocationKind,
      name: str,
      node_id: str ) -> MapLocationWalkNode:
   return MapLocationWalkNode(
      kind=kind,
      name=name,
      location=name,
      x=0.0,
      y=0.0,
      walk_node_id=node_id,
      snap_distance_px=0.0 )

CAROUSEL_WALK_NODE = _walk_node(
   MapLocationKind.ATTRACTION,
   CAROUSEL,
   CAROUSEL_NODE_ID )
TALK_WALK_NODE = _walk_node(
   MapLocationKind.GUARDIANS_TALK,
   ZEBRA_TALK,
   TALK_NODE_ID )
ENCOUNTER_WALK_NODE = _walk_node(
   MapLocationKind.WILD_ENCOUNTER_MEETING_SPOT,
   MEETING_SPOT,
   ENCOUNTER_NODE_ID )


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

   def _for_map_location(
         kind: MapLocationKind,
         name: str ) -> MapLocationWalkNode | None:
      if kind == MapLocationKind.ATTRACTION and name == CAROUSEL:
         return CAROUSEL_WALK_NODE

      if kind == MapLocationKind.GUARDIANS_TALK and name == ZEBRA_TALK:
         return TALK_WALK_NODE

      if (
            kind == MapLocationKind.WILD_ENCOUNTER_MEETING_SPOT
            and name == MEETING_SPOT ):
         return ENCOUNTER_WALK_NODE

      return None

   monkeypatch.setattr(
      MapLocationWalkNodeLookup,
      'for_map_location',
      _for_map_location )

   def _resolve_transport(
         transportation_name: str,
         *,
         legs: list[ ItineraryTransportationLeg ] | None = None,
         endpoint: TransitRideEndpoint = TransitRideEndpoint.ONBOARDING ) -> str | None:
      if transportation_name != ZOOMOBILE:
         return None

      if endpoint == TransitRideEndpoint.OFFBOARDING:
         return OFFBOARD_NODE_ID

      return ONBOARD_NODE_ID

   monkeypatch.setattr( TransportationWalkNodeResolver, 'resolve', _resolve_transport )


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


def _empty_itinerary() -> Itinerary:
   return ItineraryBuilder.build(
      date='2026-06-20',
      selected_exhibits=[],
      animals=[],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:30 AM',
      departure_time='5:00 PM' )


def _event_only_itinerary() -> Itinerary:
   return ItineraryBuilder.build(
      date='2026-06-20',
      selected_exhibits=[],
      animals=[],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[
         ItineraryEvent(
            event_type=ItineraryEventType.LUNCH,
            start_time='12:00 PM',
            end_time='12:30 PM' ),
      ],
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
      CAROUSEL ) == CAROUSEL_NODE_ID


def Test_WalkNodeIdForAttraction_TestUnknownAttraction_ExpectNone(
      stub_schedule_item_travel_time_calculator: None ) -> None:
   assert ScheduleItemTravelTimeCalculator.walk_node_id_for_attraction(
      'Unknown Ride' ) is None


def Test_EntranceTravelSecondsToEarliestItem_TestScheduledLion_ExpectTravelFromEntrance(
      stub_schedule_item_travel_time_calculator: None ) -> None:
   assert ScheduleItemTravelTimeCalculator.entrance_travel_seconds_to_earliest_item(
      _itinerary_with_lion() ) == TRAVEL_SECONDS


def Test_EntranceTravelSecondsToEarliestItem_TestEmptyItinerary_ExpectZero(
      stub_schedule_item_travel_time_calculator: None ) -> None:
   assert ScheduleItemTravelTimeCalculator.entrance_travel_seconds_to_earliest_item(
      _empty_itinerary() ) == 0


def Test_EntranceTravelSecondsFromLatestItem_TestScheduledLion_ExpectTravelToEntrance(
      stub_schedule_item_travel_time_calculator: None ) -> None:
   assert ScheduleItemTravelTimeCalculator.entrance_travel_seconds_from_latest_item(
      _itinerary_with_lion() ) == TRAVEL_SECONDS


def Test_EntranceTravelSecondsFromLatestItem_TestEmptyItinerary_ExpectZero(
      stub_schedule_item_travel_time_calculator: None ) -> None:
   assert ScheduleItemTravelTimeCalculator.entrance_travel_seconds_from_latest_item(
      _empty_itinerary() ) == 0


def Test_WalkNodeIdForLatestScheduledItem_TestTransportationOffboard_ExpectOffboardNode(
      stub_schedule_item_travel_time_calculator: None ) -> None:
   itinerary = _empty_itinerary()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   itinerary.transportations = [
      ItineraryTransportation(
         name=ZOOMOBILE,
         added_as_attraction=False,
         start_time='11:00 AM',
         end_time='11:30 AM',
         legs=[
            ItineraryTransportationLeg(
               from_station='Africa',
               to_station='Americas',
               start_time='11:00 AM',
               end_time='11:30 AM',
               transportation=ZOOMOBILE,
               added_as_attraction=False ),
         ] ),
   ]

   assert ScheduleItemTravelTimeCalculator.walk_node_id_for_latest_scheduled_item(
      itinerary ) == OFFBOARD_NODE_ID


def Test_WalkNodeIdForEarliestScheduledItem_TestCoveredByTalkExcluded_ExpectAttractionNode(
      stub_schedule_item_travel_time_calculator: None ) -> None:
   itinerary = _empty_itinerary()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM',
         covered_by_talk=True ),
   ]
   itinerary.attractions = [
      Attraction(
         name=CAROUSEL,
         free_with_admission=True,
         start_time='10:30 AM',
         end_time='10:45 AM' ),
   ]

   assert ScheduleItemTravelTimeCalculator.walk_node_id_for_earliest_scheduled_item(
      itinerary ) == CAROUSEL_NODE_ID


def Test_ScheduledStopsWithWalkNodes_TestTalkAndEncounter_ExpectWalkNodes(
      stub_schedule_item_travel_time_calculator: None ) -> None:
   itinerary = _empty_itinerary()
   itinerary.guardians_talks = [
      GuardiansTalk(
         name=ZEBRA_TALK,
         location='Africa Savanna',
         x_coord=0.0,
         y_coord=0.0,
         start_time='12:00 PM',
         end_time='12:30 PM' ),
   ]
   itinerary.wild_encounters = [
      WildEncounter(
         name='African Rainforest',
         meeting_spot=MEETING_SPOT,
         link='african-rainforest',
         x_coord=0.0,
         y_coord=0.0,
         start_time='1:00 PM',
         end_time='1:45 PM' ),
   ]

   stops = ScheduleItemTravelTimeCalculator._scheduled_stops_with_walk_nodes( itinerary )

   assert [ ( stop.walk_node_id, stop.start_seconds ) for stop in stops ] == [
      ( TALK_NODE_ID, 12 * 3600 ),
      ( ENCOUNTER_NODE_ID, 13 * 3600 ),
   ]


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


def Test_EarliestScheduleStartSecondsWithTravel_TestOpenAnchorAtNineThirty_ExpectTravelOffset(
      stub_schedule_item_travel_time_calculator: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   empty_saved_itinerary = SavedItinerary(
      date_value='2026-06-22',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )
   open_seconds = 9 * 3600 + 30 * 60

   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.build(
         date=saved_itinerary.date_value or '',
         selected_exhibits=[],
         animals=[],
         attractions=[],
         transportations=[],
         transportation_stations=[],
         guardians_talks=[],
         wild_encounters=[],
         events=[],
         arrival_time=saved_itinerary.arrival_time,
         departure_time=saved_itinerary.departure_time ) )

   earliest_start = ScheduleItemTravelTimeCalculator.earliest_schedule_start_seconds_with_travel(
      empty_saved_itinerary,
      candidate_walk_node_id=LION_NODE_ID,
      visit_anchor_seconds=open_seconds,
      itinerary_context={} )

   assert earliest_start == open_seconds + TRAVEL_SECONDS
   assert DateValues.schedule_time_key_from_seconds( earliest_start ) == '9:36 AM'


def Test_EarliestScheduleStartSecondsWithTravel_TestStartTimeFilter_ExpectEarlierStopOnly(
      stub_schedule_item_travel_time_calculator: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   itinerary = _empty_itinerary()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   itinerary.attractions = [
      Attraction(
         name=CAROUSEL,
         free_with_admission=True,
         start_time='11:00 AM',
         end_time='11:15 AM' ),
   ]

   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: itinerary )

   earliest_start = ScheduleItemTravelTimeCalculator.earliest_schedule_start_seconds_with_travel(
      _saved_itinerary(),
      candidate_walk_node_id=CHEETAH_NODE_ID,
      visit_anchor_seconds=ARRIVAL_SECONDS,
      itinerary_context={},
      start_time='10:45 AM' )

   assert earliest_start == LION_END_SECONDS + ( 2 * TRAVEL_SECONDS )
   assert earliest_start != CAROUSEL_END_SECONDS + TRAVEL_SECONDS


def Test_WalkNodeIdForEarliestScheduledItem_TestOnlyEventTimed_ExpectNone() -> None:
   assert ScheduleItemTravelTimeCalculator.walk_node_id_for_earliest_scheduled_item(
      _event_only_itinerary() ) is None


def Test_WalkNodeIdForLatestScheduledItem_TestOnlyEventTimed_ExpectNone() -> None:
   assert ScheduleItemTravelTimeCalculator.walk_node_id_for_latest_scheduled_item(
      _event_only_itinerary() ) is None


def Test_WalkNodeIdForLatestScheduledItem_TestEarlierTransportSkipped_ExpectLaterStop(
      stub_schedule_item_travel_time_calculator: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   earlier = ItineraryTransportation(
      name=ZOOMOBILE,
      added_as_attraction=False,
      start_time='10:00 AM',
      end_time='10:20 AM',
      legs=[
         ItineraryTransportationLeg(
            'Main Zoomobile Station',
            'Canadian Domain Zoomobile Station',
            '10:00 AM',
            '10:20 AM',
            ZOOMOBILE,
            False ),
      ] )
   later_attraction = Attraction(
      name=CAROUSEL,
      free_with_admission=0,
      likelihood=100,
      start_time='11:00 AM',
      end_time='11:15 AM' )

   monkeypatch.setattr(
      TransportationWalkNodeResolver,
      'resolve',
      lambda name, legs=None, endpoint=None: (
         OFFBOARD_NODE_ID
         if endpoint == TransitRideEndpoint.OFFBOARDING
         else ONBOARD_NODE_ID ) )
   monkeypatch.setattr(
      MapLocationWalkNodeLookup,
      'for_map_location',
      lambda kind, name, *, location='': (
         MapLocationWalkNode(
            kind=MapLocationKind.ATTRACTION,
            name=CAROUSEL,
            location='',
            x=20.0,
            y=0.0,
            walk_node_id=CAROUSEL_NODE_ID,
            snap_distance_px=0.0 )
         if kind == MapLocationKind.ATTRACTION and name == CAROUSEL
         else None ) )

   itinerary = ItineraryBuilder.build(
      date='2026-06-20',
      selected_exhibits=[],
      animals=[],
      attractions=[ later_attraction ],
      transportations=[ earlier ],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:30 AM',
      departure_time='5:00 PM' )

   assert ScheduleItemTravelTimeCalculator.walk_node_id_for_latest_scheduled_item(
      itinerary ) == CAROUSEL_NODE_ID


def Test_ScheduledStopsWithWalkNodes_TestTransportDeletedTalkEncounterAndMissingNode_ExpectFiltered(
      stub_schedule_item_travel_time_calculator: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationWalkNodeResolver,
      'resolve',
      lambda name, legs=None, endpoint=None: ONBOARD_NODE_ID )
   monkeypatch.setattr(
      MapLocationWalkNodeLookup,
      'for_map_location',
      lambda kind, name, *, location='': None )

   itinerary = ItineraryBuilder.build(
      date='2026-06-20',
      selected_exhibits=[],
      animals=[],
      attractions=[
         Attraction(
            name='Unknown Attraction',
            free_with_admission=0,
            likelihood=100,
            start_time='11:00 AM',
            end_time='11:15 AM' ),
      ],
      transportations=[
         ItineraryTransportation(
            name=ZOOMOBILE,
            added_as_attraction=False,
            start_time='10:00 AM',
            end_time='10:20 AM',
            legs=[
               ItineraryTransportationLeg(
                  'Main Zoomobile Station',
                  'Canadian Domain Zoomobile Station',
                  '10:00 AM',
                  '10:20 AM',
                  ZOOMOBILE,
                  False ),
            ] ),
      ],
      transportation_stations=[],
      guardians_talks=[
         GuardiansTalk(
            name=ZEBRA_TALK,
            location='Africa',
            x_coord=0.0,
            y_coord=0.0,
            start_time='1:00 PM',
            end_time='1:15 PM',
            is_deleted=True ),
      ],
      wild_encounters=[
         WildEncounter(
            name='Deleted Encounter',
            meeting_spot=MEETING_SPOT,
            link='',
            start_time='2:00 PM',
            end_time='2:30 PM',
            is_deleted=True ),
      ],
      events=[],
      arrival_time='9:30 AM',
      departure_time='5:00 PM' )

   stops = ScheduleItemTravelTimeCalculator._scheduled_stops_with_walk_nodes( itinerary )

   assert [ stop.walk_node_id for stop in stops ] == [ ONBOARD_NODE_ID ]
