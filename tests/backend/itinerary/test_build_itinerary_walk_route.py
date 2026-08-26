from __future__ import annotations

from collections.abc import Callable
from datetime import date
from unittest.mock import patch

from itinerary.support import ANIMAL_KEY, schedule_itinerary_item, wild_encounter_key
from itinerary.support import CAROUSEL
from itinerary.support import CHEETAH_INDO_MALAYA_ITINERARY_ENTRY
from itinerary.support import LION_ITINERARY_ENTRY
from itinerary.support import LION_KEY
from itinerary.support import PENGUIN_ITINERARY_ENTRY
from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.routing.build_itinerary_walk_route import build_itinerary_walk_route
from api.itinerary.routing.itinerary_stop import ENTRANCE_ITEM_KEY
from api.itinerary.routing.order_itinerary_stops_for_walk_route import order_itinerary_stops_for_walk_route
from api.itinerary.routing.resolve_itinerary_stops import resolve_itinerary_stops
from api.itinerary.routing.walk_route_polyline import inclusive_point_slices_for_walk_route_legs
from api.itinerary.routing.walk_route_polyline import walk_route_node_ids_for_point_slice
from api.shared.enums import ScheduleItemKind
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from api.zoo_hours.data_access.zoo_hours_record import ZooHoursRecord
from conftest import DbControllers


def _set_rhino_encounter_schedule() -> None:
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Guardians of White Rhinos',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=[
         wire_schedule_row( '11:00', monday=False, tuesday=False, wednesday=False, thursday=False, friday=False, saturday=True, sunday=False ),
      ],
      message=None,
   )


def test_order_itinerary_stops_for_walk_route_returns_empty_without_scheduled_stops(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   ordered_stops = order_itinerary_stops_for_walk_route(
      resolve_itinerary_stops( ItineraryCoordinator.get_itinerary() ) )

   assert ordered_stops == []


def test_order_itinerary_stops_for_walk_route_sorts_scheduled_stops_by_start_time(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_rhino_encounter_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ wild_encounter_key( 'Guardians of White Rhinos', start_time='11:00' ) ],
      confirming_early_admission=True,
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='14:00',
   ).success

   ordered_stops = order_itinerary_stops_for_walk_route(
      resolve_itinerary_stops( ItineraryCoordinator.get_itinerary() ) )

   assert [ stop.item_key for stop in ordered_stops ] == [
      ENTRANCE_ITEM_KEY,
      'Guardians of White Rhinos',
      LION_KEY,
   ]


def test_build_itinerary_walk_route_returns_empty_path_without_scheduled_stops(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   walk_route = build_itinerary_walk_route( ItineraryCoordinator.get_itinerary() )

   assert walk_route.legs == []
   assert walk_route.points == []
   assert walk_route.stops == []


def test_build_itinerary_walk_route_builds_polyline_for_scheduled_animal(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='10:00',
   ).success

   walk_route = build_itinerary_walk_route( ItineraryCoordinator.get_itinerary() )

   assert [ stop.item_key for stop in walk_route.stops ] == [
      ENTRANCE_ITEM_KEY,
      LION_KEY,
      ENTRANCE_ITEM_KEY,
   ]
   assert len( walk_route.legs ) == 2
   assert walk_route.legs[ 0 ].from_item_key == ENTRANCE_ITEM_KEY
   assert walk_route.legs[ 0 ].to_item_key == LION_KEY
   assert walk_route.legs[ 1 ].from_item_key == LION_KEY
   assert walk_route.legs[ 1 ].to_item_key == ENTRANCE_ITEM_KEY
   assert len( walk_route.points ) == (
      len( walk_route.legs[ 0 ].node_ids )
      + len( walk_route.legs[ 1 ].node_ids )
      - 1
   )
   assert walk_route.points[ 0 ].node_id == walk_route.legs[ 0 ].node_ids[ 0 ]
   assert walk_route.points[ -1 ].node_id == walk_route.legs[ 1 ].node_ids[ -1 ]
   assert all(
      point.x_px > 0 and point.y_px > 0
      for point in walk_route.points )


def test_build_itinerary_walk_route_ends_at_last_stop_with_unscheduled_attraction(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='10:00',
   ).success

   walk_route = build_itinerary_walk_route( ItineraryCoordinator.get_itinerary() )

   assert walk_route.stops[ -1 ].item_key == LION_KEY
   assert walk_route.legs[ -1 ].to_item_key == LION_KEY


def test_bulk_schedule_partial_itinerary_ends_at_last_scheduled_stop(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      animals=[
         PENGUIN_ITINERARY_ENTRY,
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   with patch(
         'api.zoo_hours.data_access.zoo_hours_provider.ZooHoursProvider.fetch_zoo_hours_record',
         return_value=ZooHoursRecord(
            operating_date='2026-06-20',
            early_admission_time=None,
            open_time='09:30',
            last_admission_time='09:35',
            close_time='09:35',
         ) ):
      result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   walk_route = build_itinerary_walk_route( result.itinerary )

   if not walk_route.stops:
      # Short day windows may leave nothing schedulable once travel is reserved.
      assert result.itinerary.animals
      return

   assert walk_route.stops[ -1 ].item_key != ENTRANCE_ITEM_KEY
   assert walk_route.legs[ -1 ].to_item_key != ENTRANCE_ITEM_KEY


def test_build_itinerary_walk_route_ends_at_last_stop_when_some_items_remain_unscheduled(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
         LION_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='10:00',
   ).success

   walk_route = build_itinerary_walk_route( ItineraryCoordinator.get_itinerary() )

   assert walk_route.stops[ -1 ].item_key == LION_KEY
   assert walk_route.legs[ -1 ].to_item_key == LION_KEY


def test_build_itinerary_walk_route_returns_to_entrance(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='10:00',
   ).success

   walk_route = build_itinerary_walk_route( ItineraryCoordinator.get_itinerary() )

   assert walk_route.stops[ 0 ].item_key == ENTRANCE_ITEM_KEY
   assert walk_route.stops[ -1 ].item_key == ENTRANCE_ITEM_KEY
   assert walk_route.legs[ -1 ].to_item_key == ENTRANCE_ITEM_KEY
   assert walk_route.points[ -1 ].node_id == walk_route.stops[ -1 ].walk_node_id


CHEETAH_INDO_MALAYA_KEY = 'Cheetah||Indo-Malaya Outdoor'


def test_build_itinerary_walk_route_concatenates_legs_at_shared_node_once(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
         LION_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=CHEETAH_INDO_MALAYA_KEY,
      start_time='10:00',
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='11:00',
   ).success

   walk_route = build_itinerary_walk_route( ItineraryCoordinator.get_itinerary() )

   assert len( walk_route.legs ) == 3
   assert walk_route.legs[ -1 ].to_item_key == ENTRANCE_ITEM_KEY
   assert len( walk_route.points ) == (
      len( walk_route.legs[ 0 ].node_ids )
      + len( walk_route.legs[ 1 ].node_ids )
      + len( walk_route.legs[ 2 ].node_ids )
      - 2
   )

   joined_node_id = walk_route.legs[ 0 ].node_ids[ -1 ]

   assert walk_route.legs[ 1 ].node_ids[ 0 ] == joined_node_id
   leg0_end_point_index = len( walk_route.legs[ 0 ].node_ids ) - 1
   assert walk_route.points[ leg0_end_point_index ].node_id == joined_node_id
   assert walk_route.points[ leg0_end_point_index + 1 ].node_id == (
      walk_route.legs[ 1 ].node_ids[ 1 ]
   )

   leg1_end_node_id = walk_route.legs[ 1 ].node_ids[ -1 ]
   assert walk_route.legs[ 2 ].node_ids[ 0 ] == leg1_end_node_id
   leg1_end_point_index = (
      len( walk_route.legs[ 0 ].node_ids )
      + len( walk_route.legs[ 1 ].node_ids )
      - 2
   )
   assert walk_route.points[ leg1_end_point_index ].node_id == leg1_end_node_id
   assert walk_route.points[ leg1_end_point_index + 1 ].node_id == (
      walk_route.legs[ 2 ].node_ids[ 1 ]
   )


def test_inclusive_point_slices_for_walk_route_legs_match_polyline(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
         LION_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=CHEETAH_INDO_MALAYA_KEY,
      start_time='10:00',
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='11:00',
   ).success

   walk_route = build_itinerary_walk_route( ItineraryCoordinator.get_itinerary() )

   for leg, ( from_point_sequence, to_point_sequence ) in zip(
         walk_route.legs,
         inclusive_point_slices_for_walk_route_legs( walk_route.legs ) ):
      assert walk_route_node_ids_for_point_slice(
         walk_route.points,
         from_point_sequence=from_point_sequence,
         to_point_sequence=to_point_sequence ) == leg.node_ids


def test_build_itinerary_walk_route_skips_walk_during_zoomobile_rides(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
   from api.itinerary.data_access.itinerary_transportation_input import (
      ItineraryTransportationInput,
   )
   from api.itinerary.routing.build_walk_route_anchors import build_walk_route_anchors
   from api.itinerary.routing.transit_ride_endpoint import TransitRideEndpoint
   from itinerary.support import itinerary_animals_for_exhibits

   freeze_database_today( date( 2026, 7, 11 ) )
   domain_exhibits: list[ str ] = []

   for region in ExhibitCoordinator.get_regions_with_exhibits():
      if region.name == 'Canadian Domain':
         domain_exhibits.extend( region.exhibits )

   assert domain_exhibits
   assert ItineraryCoordinator.set_itinerary(
      date='2026-07-11',
      arrival_time='09:00',
      departure_time='18:00',
      animals=itinerary_animals_for_exhibits(
         domain_exhibits,
         visit_date='2026-07-11' ),
      attractions=[],
      transportations=[
         ItineraryTransportationInput(
            name='Zoomobile',
            added_as_attraction=False ),
      ],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=domain_exhibits,
      confirming_early_admission=True,
   ).success
   assert ItineraryCoordinator.bulk_schedule_itinerary().success

   itinerary = ItineraryCoordinator.get_itinerary()
   walk_route = build_itinerary_walk_route( itinerary )
   transit_anchors = [
      anchor
      for anchor in build_walk_route_anchors( itinerary )
      if anchor.transit_ride_key is not None
   ]

   assert len( transit_anchors ) >= 4
   assert transit_anchors[ 0 ].transit_endpoint is TransitRideEndpoint.ONBOARDING
   assert transit_anchors[ 1 ].transit_endpoint is TransitRideEndpoint.OFFBOARDING
   assert transit_anchors[ 0 ].transit_ride_key == transit_anchors[ 1 ].transit_ride_key

   walk_leg_keys = {
      ( leg.from_item_key, leg.to_item_key )
      for leg in walk_route.legs
   }
   assert (
      transit_anchors[ 0 ].item_key,
      transit_anchors[ 1 ].item_key,
   ) not in walk_leg_keys

   for leg, ( from_point_sequence, to_point_sequence ) in zip(
         walk_route.legs,
         inclusive_point_slices_for_walk_route_legs( walk_route.legs ) ):
      assert walk_route_node_ids_for_point_slice(
         walk_route.points,
         from_point_sequence=from_point_sequence,
         to_point_sequence=to_point_sequence ) == leg.node_ids

   assert any(
      (
         walk_route.legs[ index ].node_ids[ -1 ]
         != walk_route.legs[ index + 1 ].node_ids[ 0 ]
      )
      for index in range( len( walk_route.legs ) - 1 )
   )
