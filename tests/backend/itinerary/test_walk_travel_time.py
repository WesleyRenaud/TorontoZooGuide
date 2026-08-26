from __future__ import annotations

from itinerary.support import schedule_itinerary_item

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_walk_route_provider import ItineraryWalkRouteProvider
from api.itinerary.routing.build_itinerary_walk_route import build_itinerary_walk_route
from api.itinerary.routing.itinerary_stop import ENTRANCE_ITEM_KEY
from api.itinerary.routing.walk_travel_time import travel_time_minutes_from_length_px
from api.itinerary.routing.walk_travel_time import travel_time_seconds_from_length_px
from api.itinerary.routing.walk_travel_time import WALK_PX_PER_MINUTE
from api.shared.calendar_dates import DateValues
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.shortest_path import shortest_path
from api.walk_graph.shortest_path import shortest_path_distance
from conftest import DbControllers

GRIZZLY_KEY = 'Grizzly Bear||Canadian Domain'
GRIZZLY_ITINERARY_ENTRY = {
   'species': 'Grizzly Bear',
   'exhibit': 'Canadian Domain',
}
GRIZZLY_WALK_NODE_ID = 'v-0623'


def test_travel_time_minutes_from_length_px_uses_floor() -> None:
   assert travel_time_minutes_from_length_px( 0 ) == 0
   assert travel_time_minutes_from_length_px( -10 ) == 0
   assert travel_time_minutes_from_length_px( 0.5 * WALK_PX_PER_MINUTE ) == 0
   assert travel_time_minutes_from_length_px( 1.0 * WALK_PX_PER_MINUTE ) == 1
   assert travel_time_minutes_from_length_px( 1.5 * WALK_PX_PER_MINUTE ) == 1


def test_travel_time_seconds_from_length_px_multiplies_floored_minutes() -> None:
   assert travel_time_seconds_from_length_px( 0.5 * WALK_PX_PER_MINUTE ) == 0
   assert travel_time_seconds_from_length_px( 1.0 * WALK_PX_PER_MINUTE ) == 60
   assert travel_time_seconds_from_length_px( 1.5 * WALK_PX_PER_MINUTE ) == 60


def test_entrance_to_grizzly_bear_travel_time_is_about_thirty_minutes(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='10:00',
      animals=[ GRIZZLY_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   walk_graph = load_walk_graph()
   expected_path = shortest_path(
      walk_graph,
      walk_graph[ 'entrance_node_id' ],
      GRIZZLY_WALK_NODE_ID )
   assert expected_path is not None
   expected_minutes = travel_time_minutes_from_length_px( expected_path.length_px )
   assert 30 <= expected_minutes <= 32

   assert schedule_itinerary_item(
      item_type='animals',
      key=GRIZZLY_KEY,
   ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '10:00 AM'
   animal_start_seconds = DateValues.time_value_in_seconds(
      itinerary.animals[ 0 ].start_time )
   arrival_seconds = DateValues.time_value_in_seconds( itinerary.arrival_time )
   assert animal_start_seconds is not None
   assert arrival_seconds is not None
   assert animal_start_seconds == arrival_seconds + expected_minutes * 60

   walk_route = build_itinerary_walk_route( itinerary )
   first_leg = walk_route.legs[ 0 ]

   assert first_leg.from_item_key == ENTRANCE_ITEM_KEY
   assert first_leg.to_item_key == GRIZZLY_KEY
   assert first_leg.node_ids == expected_path.node_ids
   assert expected_path.length_px == shortest_path_distance(
      walk_graph,
      walk_graph[ 'entrance_node_id' ],
      GRIZZLY_WALK_NODE_ID )
   assert first_leg.travel_time_minutes == expected_minutes

   persisted_leg = ItineraryWalkRouteProvider.fetch_itinerary_walk_route( db.conn ).legs[ 0 ]
   assert persisted_leg.travel_time_minutes == first_leg.travel_time_minutes
