from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import guardians_talk_save_entry, LION_ITINERARY_ENTRY, LION_KEY, parsed_schedule_item, schedule_itinerary_item
from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.animals.search.species_exhibit_key import SpeciesExhibitKey
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.warnings.guardians_talk_without_animal_warning import build_guardians_talk_without_animal_issue_from_talks
from api.itinerary.warnings.guardians_talk_without_animal_warning import guardians_talk_without_animal_warning_is_required_for_talk
from api.itinerary.warnings.guardians_talk_without_animal_warning import guardians_talks_without_matching_animal
from api.itinerary.warnings.guardians_talk_without_animal_warning import talk_matches_species_exhibit_pairs
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ScheduleItemKind
from conftest import DbControllers

LION_TALK = 'African Lion'
ZEBRA_TALK = "Grevy's Zebra"
NEW_WORLD_PRIMATES_TALK = 'New World Primates'
TAMARIN_ITINERARY_ENTRY = {
   'species': 'Golden Lion Tamarin',
   'exhibit': 'Americas Pavilion',
}


def _set_talk_schedule(
      talk: str,
      *,
      location: str,
      talk_time: str ) -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=talk,
      location=location,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( talk_time, monday=True, tuesday=True, wednesday=True, thursday=True, friday=True, saturday=True, sunday=True ),
      message=None,
   )


def test_guardians_talks_without_matching_animal_skips_deleted_talks(
      db: DbControllers ) -> None:
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[],
      attractions=[],
      guardians_talks=[
         GuardiansTalkDiff(
            name=ZEBRA_TALK,
            is_deleted=True,
            location='Africa Savanna' ),
         GuardiansTalkDiff(
            name=LION_TALK,
            is_deleted=False,
            location='Africa Savanna' ),
      ],
      wild_encounters=[],
      events=[],
   )

   missing = guardians_talks_without_matching_animal( validated, db.conn )

   assert [ talk.name for talk in missing ] == [ LION_TALK ]


def test_talk_without_animal_warning_skips_deleted_talk(
      db: DbControllers ) -> None:
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=True,
      location='Africa Savanna' )

   assert not guardians_talk_without_animal_warning_is_required_for_talk(
      talk,
      set(),
      db.conn,
      confirming_guardians_talk_without_animal=False )


def test_build_guardians_talk_without_animal_issue_from_talks() -> None:
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time='12:00 PM',
      end_time='12:30 PM',
      location='Africa Savanna' )

   issue = build_guardians_talk_without_animal_issue_from_talks( [ talk ] )

   assert issue.code == ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL
   assert len( issue.items ) == 1
   assert issue.items[ 0 ].name == ZEBRA_TALK
   assert issue.items[ 0 ].location == 'Africa Savanna'


def test_set_itinerary_warns_when_talk_has_no_matching_animal(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_talk_schedule(
      ZEBRA_TALK,
      location='Africa Savanna',
      talk_time='12:00' )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( ZEBRA_TALK, start_time='12:00' ) ],
      wild_encounters=[],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL
   assert result.reasons[ 0 ].code == ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ ZEBRA_TALK ]

   confirmed = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( ZEBRA_TALK, start_time='12:00' ) ],
      wild_encounters=[],
      confirming_guardians_talk_without_animal=True,
      confirming_fixed_time_item_long_wait=True,
   )

   assert confirmed.success
   assert [ talk.name for talk in confirmed.itinerary.guardians_talks ] == [
      ZEBRA_TALK,
   ]


def test_set_itinerary_warns_for_each_talk_without_matching_animal(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_talk_schedule(
      ZEBRA_TALK,
      location='Africa Savanna',
      talk_time='12:00' )
   _set_talk_schedule(
      LION_TALK,
      location='Africa Savanna',
      talk_time='14:00' )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry( ZEBRA_TALK, start_time='12:00' ),
         guardians_talk_save_entry( LION_TALK, start_time='14:00' ),
      ],
      wild_encounters=[],
   )

   assert not result.success
   without_animal_reasons = [
      reason
      for reason in result.reasons
      if reason.code == ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL
   ]

   assert len( without_animal_reasons ) == 1
   assert [ item.name for item in without_animal_reasons[ 0 ].items ] == [
      ZEBRA_TALK,
      LION_TALK,
   ]


def test_set_itinerary_skips_without_animal_warning_for_already_saved_talk(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_talk_schedule(
      ZEBRA_TALK,
      location='Africa Savanna',
      talk_time='12:00' )

   confirmed = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( ZEBRA_TALK, start_time='12:00' ) ],
      wild_encounters=[],
      confirming_guardians_talk_without_animal=True,
      confirming_fixed_time_item_long_wait=True,
   )

   assert confirmed.success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( ZEBRA_TALK, start_time='12:00' ) ],
      wild_encounters=[],
      confirming_fixed_time_item_long_wait=True,
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert [ talk.name for talk in result.itinerary.guardians_talks ] == [
      ZEBRA_TALK,
   ]


def test_set_itinerary_warns_only_for_newly_added_talk_without_animal(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_talk_schedule(
      ZEBRA_TALK,
      location='Africa Savanna',
      talk_time='12:00' )
   _set_talk_schedule(
      LION_TALK,
      location='Africa Savanna',
      talk_time='13:00' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( ZEBRA_TALK, start_time='12:00' ) ],
      wild_encounters=[],
      confirming_guardians_talk_without_animal=True,
      confirming_fixed_time_item_long_wait=True,
   ).success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry( ZEBRA_TALK, start_time='12:00' ),
         guardians_talk_save_entry( LION_TALK, start_time='13:00' ),
      ],
      wild_encounters=[],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ LION_TALK ]


def test_set_itinerary_skips_without_animal_warning_when_animal_matches(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_talk_schedule(
      LION_TALK,
      location='Africa Savanna',
      talk_time='12:00' )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( LION_TALK, start_time='12:00' ) ],
      wild_encounters=[],
      confirming_fixed_time_item_long_wait=True,
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS


def test_schedule_talk_warns_when_no_matching_animal_on_itinerary(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_talk_schedule(
      ZEBRA_TALK,
      location='Africa Savanna',
      talk_time='12:00' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success
   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      LION_KEY,
      start_time='10:30',
   ).success

   result = schedule_itinerary_item(
      ScheduleItemKind.GUARDIANS_TALK.item_type,
      f'{ ZEBRA_TALK }||12:00',
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ ZEBRA_TALK ]

   confirmed = ItineraryCoordinator.schedule_itinerary_item(
      parsed_schedule_item(
         ScheduleItemKind.GUARDIANS_TALK.item_type,
         f'{ ZEBRA_TALK }||12:00' ),
      confirming_guardians_talk_without_animal=True,
      confirming_fixed_time_item_long_wait=True,
   )

   assert confirmed.success
   assert any(
      talk.name == ZEBRA_TALK
      for talk in confirmed.itinerary.guardians_talks
   )


def test_schedule_talk_returns_overlap_and_without_animal_warnings_together(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_talk_schedule(
      ZEBRA_TALK,
      location='Africa Savanna',
      talk_time='12:00' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success
   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      LION_KEY,
      start_time='12:00',
   ).success

   result = schedule_itinerary_item(
      ScheduleItemKind.GUARDIANS_TALK.item_type,
      f'{ ZEBRA_TALK }||12:00',
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS
   assert [ reason.code for reason in result.reasons ] == [
      ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
      ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
   ]
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ ZEBRA_TALK ]
   assert [ item.name for item in result.reasons[ 1 ].items ] == [ ZEBRA_TALK ]

   confirmed = ItineraryCoordinator.schedule_itinerary_item(
      parsed_schedule_item(
         ScheduleItemKind.GUARDIANS_TALK.item_type,
         f'{ ZEBRA_TALK }||12:00' ),
      confirming_guardians_talk_unschedule=True,
      confirming_guardians_talk_without_animal=True,
      confirming_fixed_time_item_long_wait=True,
   )

   assert confirmed.success
   assert any(
      talk.name == ZEBRA_TALK and not talk.is_deleted
      for talk in confirmed.itinerary.guardians_talks
   )


def test_talk_matches_associated_species_exhibit_pairs() -> None:
   tamarin_key = SpeciesExhibitKey.from_values(
      'Golden Lion Tamarin',
      'Americas Pavilion' )

   assert not talk_matches_species_exhibit_pairs(
      [ tamarin_key ],
      linked_animals=[] )
   assert not talk_matches_species_exhibit_pairs(
      [ tamarin_key ],
      linked_animals=[
         SpeciesExhibitKey.from_values(
            'Golden Lion Tamarin',
            'Africa Savanna' ),
      ] )
   assert talk_matches_species_exhibit_pairs(
      [ tamarin_key ],
      linked_animals=[
         SpeciesExhibitKey.from_values(
            'Golden Lion Tamarin',
            'Americas Pavilion' ),
      ] )


def test_set_itinerary_warns_for_new_world_primates_without_linked_animal(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_talk_schedule(
      NEW_WORLD_PRIMATES_TALK,
      location='Americas Pavilion',
      talk_time='12:00' )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry( NEW_WORLD_PRIMATES_TALK, start_time='12:00' ),
      ],
      wild_encounters=[],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL
   assert [ item.name for item in result.reasons[ 0 ].items ] == [
      NEW_WORLD_PRIMATES_TALK,
   ]


def test_set_itinerary_skips_warning_when_linked_new_world_primates_animal_matches(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_talk_schedule(
      NEW_WORLD_PRIMATES_TALK,
      location='Americas Pavilion',
      talk_time='12:00' )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ TAMARIN_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry( NEW_WORLD_PRIMATES_TALK, start_time='12:00' ),
      ],
      wild_encounters=[],
      confirming_fixed_time_item_long_wait=True,
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert [ talk.name for talk in result.itinerary.guardians_talks ] == [
      NEW_WORLD_PRIMATES_TALK,
   ]
