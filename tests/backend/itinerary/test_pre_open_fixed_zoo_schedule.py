from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import entrance_travel_seconds_to_map_location, schedule_time_before_seconds, set_wild_encounter_schedule, WILD_ENCOUNTER, wild_encounter_key

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.walk_graph.domain.map_location_kind import MapLocationKind
from conftest import DbControllers

PRE_OPEN_ENCOUNTER_TIME = '08:45'


def test_set_arrival_before_open_allowed_when_justified_by_wild_encounter(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   set_wild_encounter_schedule( encounter_time=PRE_OPEN_ENCOUNTER_TIME )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( WILD_ENCOUNTER, start_time=PRE_OPEN_ENCOUNTER_TIME ),
      ],
      confirming_wild_encounter_unschedule=True,
   ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   encounter = next(
      saved_encounter
      for saved_encounter in itinerary.wild_encounters
      if saved_encounter.name == WILD_ENCOUNTER )
   encounter_travel_seconds = entrance_travel_seconds_to_map_location(
      MapLocationKind.WILD_ENCOUNTER_MEETING_SPOT,
      encounter.meeting_spot )
   assert itinerary.arrival_time == schedule_time_before_seconds(
      encounter.start_time,
      encounter_travel_seconds )

   assert ItineraryCoordinator.set_departure_time(
      '17:00',
      confirming_short_visit=True,
   ).success
   assert ItineraryCoordinator.set_arrival_time(
      PRE_OPEN_ENCOUNTER_TIME,
      confirming_short_visit=True,
   ).success
   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '8:45 AM'
   assert any(
      encounter.name == WILD_ENCOUNTER and encounter.start_time == '8:45 AM'
      for encounter in itinerary.wild_encounters
   )


def test_set_itinerary_keeps_pre_open_wild_encounter_on_re_save(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   set_wild_encounter_schedule( encounter_time=PRE_OPEN_ENCOUNTER_TIME )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time=PRE_OPEN_ENCOUNTER_TIME,
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( WILD_ENCOUNTER, start_time=PRE_OPEN_ENCOUNTER_TIME ),
      ],
   ).success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time=PRE_OPEN_ENCOUNTER_TIME,
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( WILD_ENCOUNTER, start_time=PRE_OPEN_ENCOUNTER_TIME ),
      ],
   )

   assert result.success
   encounter = next(
      saved_encounter
      for saved_encounter in result.itinerary.wild_encounters
      if saved_encounter.name == WILD_ENCOUNTER )
   assert encounter.start_time == '8:45 AM'
   assert encounter.end_time == '9:30 AM'
