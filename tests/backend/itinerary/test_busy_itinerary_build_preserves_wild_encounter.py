from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import guardians_talk_save_entry, wild_encounter_key
from wild_encounter_schedule_support import wire_schedule_row

from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers

VISIT_DATE = '2026-07-09'
OTTER_TALK = 'North American River Otter'
KANGAROO_ENCOUNTER = 'Kangaroo'
KANGAROO_ENCOUNTER_TIME = '3:30 PM'
BUSY_ITINERARY_REGIONS = (
   'Africa',
   'Americas',
   'Australasia',
   'Eurasia',
   'Indo-Malaya',
   'Tundra Trek',
)


def _set_july_ninth_schedules() -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=OTTER_TALK,
      location='Americas Pavilion',
      start_date='2026-07-01',
      end_date='2026-07-31',
      monday_time=None,
      tuesday_time=None,
      wednesday_time=None,
      thursday_time='14:00',
      friday_time=None,
      saturday_time=None,
      sunday_time=None,
      message=None,
   )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=KANGAROO_ENCOUNTER,
      start_date='2026-07-01',
      end_date='2026-07-31',
      schedule_rows=[
         wire_schedule_row(
            '15:30',
            monday=False,
            tuesday=False,
            wednesday=False,
            thursday=True,
            friday=False,
            saturday=False,
            sunday=False,
         ),
      ],
      message=None,
   )


def _selected_exhibits_for_busy_regions() -> list[ str ]:
   selected_exhibits: list[ str ] = []

   for region in ExhibitCoordinator.get_regions_with_exhibits():
      if region.name in BUSY_ITINERARY_REGIONS:
         selected_exhibits.extend( region.exhibits )

   assert selected_exhibits

   return selected_exhibits


def test_busy_itinerary_build_preserves_kangaroo_encounter_schedule(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 7, 9 ) )
   _set_july_ninth_schedules()
   selected_exhibits = _selected_exhibits_for_busy_regions()

   initial_result = ItineraryCoordinator.set_itinerary(
      date=VISIT_DATE,
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( OTTER_TALK ) ],
      wild_encounters=[
         wild_encounter_key(
            KANGAROO_ENCOUNTER,
            start_time=KANGAROO_ENCOUNTER_TIME,
         ),
      ],
      confirming_guardians_talk_long_wait=True,
      confirming_guardians_talk_without_animal=True,
   )

   assert initial_result.success
   assert initial_result.status == ItineraryErrorType.SUCCESS

   kangaroo = next(
      encounter
      for encounter in initial_result.itinerary.wild_encounters
      if encounter.name == KANGAROO_ENCOUNTER )
   assert kangaroo.start_time is not None
   assert kangaroo.end_time is not None
   assert not kangaroo.is_deleted

   build_result = ItineraryCoordinator.set_itinerary(
      date=VISIT_DATE,
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( OTTER_TALK ) ],
      wild_encounters=[
         wild_encounter_key(
            KANGAROO_ENCOUNTER,
            start_time=KANGAROO_ENCOUNTER_TIME,
         ),
      ],
      selected_exhibits=selected_exhibits,
      confirming_guardians_talk_without_animal=True,
   )

   assert build_result.success
   assert build_result.status == ItineraryErrorType.SUCCESS

   rebuilt_kangaroo = next(
      encounter
      for encounter in build_result.itinerary.wild_encounters
      if encounter.name == KANGAROO_ENCOUNTER )

   assert rebuilt_kangaroo.start_time is not None
   assert rebuilt_kangaroo.end_time is not None
   assert not rebuilt_kangaroo.is_deleted


def test_one_shot_busy_itinerary_build_preserves_kangaroo_encounter_schedule(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 7, 9 ) )
   _set_july_ninth_schedules()
   selected_exhibits = _selected_exhibits_for_busy_regions()

   result = ItineraryCoordinator.set_itinerary(
      date=VISIT_DATE,
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( OTTER_TALK ) ],
      wild_encounters=[
         wild_encounter_key(
            KANGAROO_ENCOUNTER,
            start_time=KANGAROO_ENCOUNTER_TIME,
         ),
      ],
      selected_exhibits=selected_exhibits,
      confirming_guardians_talk_without_animal=True,
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS

   kangaroo = next(
      encounter
      for encounter in result.itinerary.wild_encounters
      if encounter.name == KANGAROO_ENCOUNTER )

   assert kangaroo.start_time is not None
   assert kangaroo.end_time is not None
   assert not kangaroo.is_deleted

   saved_row = db.conn.execute(
      """   SELECT START_TIME, END_TIME, IS_DELETED
            FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = ?;
      """,
      ( KANGAROO_ENCOUNTER, ),
   ).fetchone()

   assert saved_row is not None
   assert saved_row[ 'START_TIME' ] is not None
   assert saved_row[ 'END_TIME' ] is not None
   assert saved_row[ 'IS_DELETED' ] == 0


def _set_overlapping_kangaroo_schedules() -> None:
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=KANGAROO_ENCOUNTER,
      start_date='2026-06-28',
      end_date='2026-07-05',
      schedule_rows=[
         wire_schedule_row(
            '3:30 PM',
            monday=True,
            tuesday=True,
            wednesday=True,
            thursday=True,
            friday=True,
            saturday=True,
            sunday=True,
         ),
      ],
      message=None,
   )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=KANGAROO_ENCOUNTER,
      start_date='2026-07-06',
      end_date=None,
      schedule_rows=[
         wire_schedule_row(
            '3:30 PM',
            monday=True,
            tuesday=True,
            wednesday=True,
            thursday=True,
            friday=True,
            saturday=True,
            sunday=True,
         ),
      ],
      message=None,
   )


def test_busy_itinerary_build_keeps_kangaroo_when_expired_schedule_row_also_exists(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 7, 9 ) )
   _set_overlapping_kangaroo_schedules()
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=OTTER_TALK,
      location='Americas Pavilion',
      start_date='2026-07-01',
      end_date='2026-07-31',
      monday_time=None,
      tuesday_time=None,
      wednesday_time=None,
      thursday_time='14:00',
      friday_time=None,
      saturday_time=None,
      sunday_time=None,
      message=None,
   )
   selected_exhibits = _selected_exhibits_for_busy_regions()

   result = ItineraryCoordinator.set_itinerary(
      date=VISIT_DATE,
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( OTTER_TALK ) ],
      wild_encounters=[
         wild_encounter_key(
            KANGAROO_ENCOUNTER,
            start_time=KANGAROO_ENCOUNTER_TIME,
         ),
      ],
      selected_exhibits=selected_exhibits,
      confirming_guardians_talk_without_animal=True,
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS

   kangaroo = next(
      encounter
      for encounter in result.itinerary.wild_encounters
      if encounter.name == KANGAROO_ENCOUNTER )

   assert kangaroo.start_time == KANGAROO_ENCOUNTER_TIME
   assert kangaroo.end_time is not None
   assert not kangaroo.is_deleted

   saved_row = db.conn.execute(
      """   SELECT START_TIME, END_TIME, IS_DELETED
            FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = ?;
      """,
      ( KANGAROO_ENCOUNTER, ),
   ).fetchone()

   assert saved_row is not None
   assert saved_row[ 'IS_DELETED' ] == 0
