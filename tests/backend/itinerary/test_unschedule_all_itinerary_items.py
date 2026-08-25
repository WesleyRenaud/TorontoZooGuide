from __future__ import annotations

from itinerary.support import ANIMAL_KEY, CAROUSEL, GUARDIANS_TALK, guardians_talk_save_entry, LION_ITINERARY_ENTRY, schedule_itinerary_item, set_guardians_talk_and_wild_encounter_schedules_at_1400, set_wild_encounter_schedule, WILD_ENCOUNTER, wild_encounter_key

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.itinerary.scheduling.bulk.bulk_schedule_itinerary import has_itinerary_schedule_times
from api.shared.enums import ItineraryErrorType
from conftest import DbControllers

def _set_base_itinerary( db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
   ).success


def test_unschedule_all_itinerary_items_clears_schedules_but_keeps_itinerary_rows(
      db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert schedule_itinerary_item( 'animals', ANIMAL_KEY ).success
   assert schedule_itinerary_item(
      'attractions',
      CAROUSEL ).success
   assert schedule_itinerary_item( 'lunch', '' ).success

   result = ItineraryCoordinator.unschedule_all_itinerary_items()

   assert result.success

   saved = fetch_saved_itinerary( db.conn )
   animal_row = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' and row.exhibit == 'Africa Savanna' )
   attraction_row = next(
      row for row in saved.attraction_rows if row.attraction == CAROUSEL )

   assert not has_itinerary_schedule_times(
      animal_row.start_time,
      animal_row.end_time )
   assert not has_itinerary_schedule_times(
      attraction_row.start_time,
      attraction_row.end_time )
   assert not saved.event_rows
   assert len( saved.animal_rows ) == 1
   assert len( saved.attraction_rows ) == 1

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   carousel = next(
      attraction for attraction in result.itinerary.attractions
      if attraction.name == CAROUSEL )

   assert lion.start_time is None
   assert lion.end_time is None
   assert carousel.start_time is None
   assert carousel.end_time is None
   assert result.itinerary.events == []


def test_unschedule_all_itinerary_items_preserves_arrival_and_departure_times(
      db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert schedule_itinerary_item( 'animals', ANIMAL_KEY ).success

   result = ItineraryCoordinator.unschedule_all_itinerary_items()

   assert result.success
   assert result.itinerary.arrival_time == '9:30 AM'
   assert result.itinerary.departure_time == '5:00 PM'


def test_unschedule_all_itinerary_items_preserves_guardians_talks_and_wild_encounters(
      db: DbControllers ) -> None:
   set_guardians_talk_and_wild_encounter_schedules_at_1400()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( GUARDIANS_TALK, start_time='14:00' ) ],
      wild_encounters=[],
   ).success

   assert schedule_itinerary_item( 'animals', ANIMAL_KEY ).success

   result = ItineraryCoordinator.unschedule_all_itinerary_items()

   assert result.success

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   guardians_talk = result.itinerary.guardians_talks[ 0 ]

   assert lion.start_time is None
   assert lion.end_time is None
   assert guardians_talk.name == GUARDIANS_TALK
   assert guardians_talk.start_time is not None
   assert guardians_talk.end_time is not None

   set_wild_encounter_schedule( encounter_time='15:00' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ wild_encounter_key(  WILD_ENCOUNTER, start_time='15:00'  ) ],
   ).success

   assert schedule_itinerary_item( 'animals', ANIMAL_KEY ).success

   result = ItineraryCoordinator.unschedule_all_itinerary_items()

   assert result.success

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   wild_encounter = result.itinerary.wild_encounters[ 0 ]

   assert lion.start_time is None
   assert lion.end_time is None
   assert wild_encounter.name == WILD_ENCOUNTER
   assert wild_encounter.start_time is not None
   assert wild_encounter.end_time is not None


def test_unschedule_all_itinerary_items_returns_error_when_nothing_guest_scheduled(
      db: DbControllers ) -> None:
   _set_base_itinerary( db )

   result = ItineraryCoordinator.unschedule_all_itinerary_items()

   assert not result.success
   assert result.status == ItineraryErrorType.UNSCHEDULE_ALL_NOTHING_SCHEDULED

   saved = fetch_saved_itinerary( db.conn )
   animal_row = saved.animal_rows[ 0 ]

   assert not has_itinerary_schedule_times(
      animal_row.start_time,
      animal_row.end_time )
   assert not saved.event_rows


def test_unschedule_all_itinerary_items_returns_error_after_items_already_unscheduled(
      db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert schedule_itinerary_item( 'animals', ANIMAL_KEY ).success

   first_result = ItineraryCoordinator.unschedule_all_itinerary_items()

   assert first_result.success

   saved_after_first = fetch_saved_itinerary( db.conn )

   second_result = ItineraryCoordinator.unschedule_all_itinerary_items()

   assert not second_result.success
   assert second_result.status == ItineraryErrorType.UNSCHEDULE_ALL_NOTHING_SCHEDULED

   saved_after_second = fetch_saved_itinerary( db.conn )

   assert saved_after_second.animal_rows == saved_after_first.animal_rows
   assert saved_after_second.attraction_rows == saved_after_first.attraction_rows
   assert saved_after_second.event_rows == saved_after_first.event_rows


def test_unschedule_all_itinerary_items_returns_error_when_only_guardians_talk_is_scheduled(
      db: DbControllers ) -> None:
   set_guardians_talk_and_wild_encounter_schedules_at_1400()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( GUARDIANS_TALK, start_time='14:00' ) ],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.unschedule_all_itinerary_items()

   assert not result.success
   assert result.status == ItineraryErrorType.UNSCHEDULE_ALL_NOTHING_SCHEDULED

   guardians_talk = result.itinerary.guardians_talks[ 0 ]

   assert guardians_talk.name == GUARDIANS_TALK
   assert guardians_talk.start_time is not None
   assert guardians_talk.end_time is not None
