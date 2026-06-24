from __future__ import annotations

from itinerary.support import CAROUSEL, CHEETAH_ITINERARY_ENTRY, CHEETAH_KEY, GUARDIANS_TALK, guardians_talk_save_entry, LION_ITINERARY_ENTRY, LION_KEY, set_wild_encounter_schedule, WILD_ENCOUNTER

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItineraryEventType
from conftest import DbControllers


def test_set_itinerary_rejects_invalid_departure_on_date_change_without_adjustment(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='18:30',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-22',
      arrival_time='09:30',
      departure_time='19:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.TIME_OUT_OF_BOUNDS

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.date == '2026-06-20'
   assert itinerary.departure_time == '18:30'


def test_date_change_with_adjusted_arrival_reschedules_animals_and_clears_guest_schedules(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:15',
      departure_time='17:00',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='09:20',
   ).success
   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=CHEETAH_KEY,
      start_time='10:30',
   ).success
   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='attractions',
      key=CAROUSEL,
      start_time='10:10',
   ).success

   set_wild_encounter_schedule( encounter_time='09:20' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:15',
      departure_time='17:00',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[
         guardians_talk_save_entry(
            GUARDIANS_TALK,
            start_time='09:20',
            end_time='09:30',
         ),
      ],
      wild_encounters=[ WILD_ENCOUNTER ],
      confirming_early_admission=True,
      confirming_wild_encounter_unschedule=True,
   ).success

   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type=ItineraryEventType.LUNCH.value,
      key='',
   ).success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-22',
      arrival_time='09:15',
      departure_time='17:00',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[
         guardians_talk_save_entry(
            GUARDIANS_TALK,
            start_time='09:20',
            end_time='09:30',
         ),
      ],
      wild_encounters=[ WILD_ENCOUNTER ],
      confirming_wild_encounter_unschedule=True,
   )

   itinerary = result.itinerary

   assert result.success
   assert itinerary is not None
   assert itinerary.arrival_time == '09:30'
   assert [
      ( animal.species, animal.start_time, animal.end_time )
      for animal in itinerary.animals
   ] == [
      ( 'African Lion', '09:30', '09:38' ),
      ( 'Cheetah', '09:38', '09:43' ),
   ]
   assert itinerary.attractions[ 0 ].name == CAROUSEL
   assert itinerary.attractions[ 0 ].start_time is None
   assert itinerary.attractions[ 0 ].end_time is None
   assert itinerary.guardians_talks == []
   assert itinerary.wild_encounters == []
   assert itinerary.events == []


def test_date_change_with_adjusted_departure_reschedules_animals_and_clears_guest_schedules(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='18:30',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='15:45',
   ).success
   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='attractions',
      key=CAROUSEL,
      start_time='15:54',
   ).success
   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=CHEETAH_KEY,
      start_time='18:15',
   ).success

   set_wild_encounter_schedule( encounter_time='18:15' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='18:30',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[
         guardians_talk_save_entry(
            GUARDIANS_TALK,
            start_time='18:15',
            end_time='18:30',
         ),
      ],
      wild_encounters=[ WILD_ENCOUNTER ],
      confirming_wild_encounter_unschedule=True,
   ).success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-22',
      arrival_time='09:30',
      departure_time='18:30',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[
         guardians_talk_save_entry(
            GUARDIANS_TALK,
            start_time='18:15',
            end_time='18:30',
         ),
      ],
      wild_encounters=[ WILD_ENCOUNTER ],
      confirming_wild_encounter_unschedule=True,
   )

   itinerary = result.itinerary

   assert result.success
   assert itinerary is not None
   assert itinerary.departure_time == '18:00'
   assert [
      ( animal.species, animal.start_time, animal.end_time )
      for animal in itinerary.animals
   ] == [
      ( 'African Lion', '09:30', '09:38' ),
      ( 'Cheetah', '09:38', '09:43' ),
   ]
   assert itinerary.attractions[ 0 ].name == CAROUSEL
   assert itinerary.attractions[ 0 ].start_time is None
   assert itinerary.attractions[ 0 ].end_time is None
   assert itinerary.guardians_talks == []
   assert itinerary.wild_encounters == []
