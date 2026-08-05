from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import entrance_travel_seconds_to_map_location
from itinerary.support import expected_departure_time_for_itinerary
from itinerary.support import GUARDIANS_TALK
from itinerary.support import guardians_talk_save_entry
from itinerary.support import guardians_talk_wire
from itinerary.support import LION_ITINERARY_ENTRY
from itinerary.support import schedule_itinerary_item
from itinerary.support import schedule_time_before_seconds
from itinerary.support import set_wild_encounter_schedule
from itinerary.support import WILD_ENCOUNTER
from itinerary.support import wild_encounter_key
from wild_encounter_schedule_support import wire_schedule_rows

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ScheduleItemKind
from api.walk_graph.domain.map_location_kind import MapLocationKind
from conftest import DbControllers


def _set_guardians_talk_schedule( *, talk_time: str = '10:00' ) -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=GUARDIANS_TALK,
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows(
         talk_time,
         monday=True,
         tuesday=True,
         wednesday=True,
         thursday=True,
         friday=True,
         saturday=True,
         sunday=True ),
      message=None,
   )


def test_set_itinerary_with_only_talk_seeds_arrival_and_departure(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_guardians_talk_schedule( talk_time='10:00' )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry( GUARDIANS_TALK, start_time='10:00' ),
      ],
      wild_encounters=[],
      confirming_guardians_talk_without_animal=True,
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.itinerary is not None

   talk = result.itinerary.guardians_talks[ 0 ]
   talk_travel_seconds = entrance_travel_seconds_to_map_location(
      MapLocationKind.GUARDIANS_TALK,
      talk.name )

   assert talk.start_time == '10:00 AM'
   assert talk.end_time is not None
   assert result.itinerary.arrival_time == schedule_time_before_seconds(
      talk.start_time,
      talk_travel_seconds )
   assert result.itinerary.departure_time == expected_departure_time_for_itinerary(
      result.itinerary )


def test_set_itinerary_with_only_wild_encounter_seeds_arrival_and_departure(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   set_wild_encounter_schedule( encounter_time='15:30' )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( WILD_ENCOUNTER, start_time='15:30' ),
      ],
   )

   assert result.success
   assert result.itinerary is not None

   encounter = result.itinerary.wild_encounters[ 0 ]
   encounter_travel_seconds = entrance_travel_seconds_to_map_location(
      MapLocationKind.WILD_ENCOUNTER_MEETING_SPOT,
      encounter.meeting_spot )

   assert encounter.start_time == '3:30 PM'
   assert encounter.end_time is not None
   assert result.itinerary.arrival_time == schedule_time_before_seconds(
      encounter.start_time,
      encounter_travel_seconds )
   assert result.itinerary.departure_time == expected_departure_time_for_itinerary(
      result.itinerary )


def test_set_itinerary_with_unscheduled_animals_does_not_seed_visit_times_from_talk(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_guardians_talk_schedule( talk_time='10:00' )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry( GUARDIANS_TALK, start_time='10:00' ),
      ],
      wild_encounters=[],
   )

   assert result.success
   assert result.itinerary is not None
   assert result.itinerary.arrival_time is None
   assert result.itinerary.departure_time is None
   assert any(
      not animal.start_time
      for animal in result.itinerary.animals
   )


def test_schedule_talk_onto_date_only_itinerary_seeds_arrival_and_departure(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_guardians_talk_schedule( talk_time='10:00' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   before = ItineraryCoordinator.get_itinerary()

   assert before.arrival_time is None
   assert before.departure_time is None

   result = schedule_itinerary_item(
      ScheduleItemKind.GUARDIANS_TALK.item_type,
      guardians_talk_wire( GUARDIANS_TALK, start_time='10:00' ),
      confirming_schedule_item_not_on_itinerary=True,
      confirming_guardians_talk_without_animal=True,
   )

   assert result.success
   assert result.itinerary is not None

   talk = next(
      saved_talk
      for saved_talk in result.itinerary.guardians_talks
      if saved_talk.name == GUARDIANS_TALK )
   talk_travel_seconds = entrance_travel_seconds_to_map_location(
      MapLocationKind.GUARDIANS_TALK,
      talk.name )

   assert talk.start_time == '10:00 AM'
   assert talk.end_time is not None
   assert result.itinerary.arrival_time == schedule_time_before_seconds(
      talk.start_time,
      talk_travel_seconds )
   assert result.itinerary.departure_time == expected_departure_time_for_itinerary(
      result.itinerary )
