from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import guardians_talk_save_entry, LION_ITINERARY_ENTRY, RHINO_ENCOUNTER, set_itinerary_with_turtle_talk_and_lion_at_1430, set_turtle_talk_and_rhino_encounter_schedules_at_1400, TURTLE_TALK

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.shared.enums import ItineraryErrorType
from conftest import DbControllers


def test_set_itinerary_keeps_boundary_animal_when_choosing_talk_over_encounter(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   set_turtle_talk_and_rhino_encounter_schedules_at_1400()
   set_itinerary_with_turtle_talk_and_lion_at_1430(
      freeze_database_today=freeze_database_today )

   conflict = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( TURTLE_TALK ) ],
      wild_encounters=[ RHINO_ENCOUNTER ],
   )

   assert not conflict.success
   assert conflict.status == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert { item.name for item in conflict.reasons[ 0 ].items } == {
      TURTLE_TALK,
      RHINO_ENCOUNTER,
   }

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( TURTLE_TALK ) ],
      wild_encounters=[],
      overriding_conflicting_guardians_talks=True,
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   assert lion.start_time == '14:30'
   assert lion.end_time == '14:45'
   assert [ talk.name for talk in result.itinerary.guardians_talks ] == [ TURTLE_TALK ]
   assert not result.itinerary.wild_encounters

   saved = fetch_saved_itinerary( db.conn )
   animal = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' and row.exhibit == 'Africa Savanna' )
   assert animal.start_time == '14:30'
   assert animal.end_time == '14:45'
   assert saved.guardians_talk_names() == [ TURTLE_TALK ]
   assert not saved.wild_encounter_names()


def test_set_itinerary_empty_animals_removes_lion_after_conflict_resolved(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   set_turtle_talk_and_rhino_encounter_schedules_at_1400()
   set_itinerary_with_turtle_talk_and_lion_at_1430(
      freeze_database_today=freeze_database_today )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( TURTLE_TALK ) ],
      wild_encounters=[],
      overriding_conflicting_guardians_talks=True,
   )

   assert result.success
   assert not result.itinerary.animals

   saved = fetch_saved_itinerary( db.conn )
   assert not saved.animal_rows
