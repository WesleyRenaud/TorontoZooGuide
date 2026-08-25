from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import guardians_talk_save_entry
from itinerary.support import itinerary_animals_for_exhibits
from itinerary.support import wild_encounter_key
from wild_encounter_schedule_support import wire_schedule_rows

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_transportation_input import ItineraryTransportationInput
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers

CAMEL_TALK = 'Bactrian Camel'
CAMEL_ENCOUNTER = 'Bactrian Camels'
VISIT = '2026-06-20'
KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'
INDO_EXHIBITS = [
   'Indo-Malaya Pavilion',
   'Indo-Malaya Outdoor',
   'Malayan Woods Pavilion',
]


def _hours(
      attraction: str,
      *,
      weekday_start: str,
      weekday_end: str ) -> dict:
   return {
      'attraction': attraction,
      'start_date': '2026-06-01',
      'end_date': '2026-06-30',
      'weekday_start_time': weekday_start,
      'weekday_end_time': weekday_end,
      'weekend_holiday_start_time': weekday_start,
      'weekend_holiday_end_time': weekday_end,
   }


def _set_schedules() -> None:
   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours(
         'Zoomobile',
         weekday_start='10:00 AM',
         weekday_end='6:00 PM' ) )
   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours(
         KANGAROO_WALK_THRU,
         weekday_start='11:00 AM',
         weekday_end='3:00 PM' ) )

   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=CAMEL_TALK,
      location='Eurasia Wilds',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows(
         '12:30',
         monday=True,
         tuesday=True,
         wednesday=True,
         thursday=True,
         friday=True,
         saturday=True,
         sunday=True ),
      message=None,
   )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=CAMEL_ENCOUNTER,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows(
         '15:30',
         monday=True,
         tuesday=True,
         wednesday=True,
         thursday=True,
         friday=True,
         saturday=True,
         sunday=True ),
      message=None,
   )


def test_bulk_schedule_progressive_soft_pins_avoid_morning_dead_gaps(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   """Tightest soft pin activates first; both late-place into usable gaps.

   Walk-Thru (11:00–3:00) must not sit at arrival/open leaving a hole before the
   camel corridor. Zoomobile (10:00–6:00) stays inactive until Walk-Thru places,
   then fills leftover afternoon space before the camel wild encounter when it
   fits — not first-open at 10:00 / 1:00.
   """
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_schedules()

   indo = itinerary_animals_for_exhibits( INDO_EXHIBITS, visit_date=VISIT )
   africa = itinerary_animals_for_exhibits(
      [ 'Africa Savanna', 'African Rainforest Pavilion' ],
      visit_date=VISIT )

   assert ItineraryCoordinator.set_itinerary(
      date=VISIT,
      arrival_time='11:00 AM',
      departure_time='17:00',
      animals=[ *indo, *africa ],
      attractions=[
         KANGAROO_WALK_THRU,
         'Greenhouse',
         'Wildlife Health & Science Centre',
      ],
      transportations=[
         ItineraryTransportationInput(
            name='Zoomobile',
            added_as_attraction=True ),
      ],
      guardians_talks=[
         guardians_talk_save_entry( CAMEL_TALK, start_time='12:30' ),
      ],
      wild_encounters=[
         wild_encounter_key( CAMEL_ENCOUNTER, start_time='15:30' ),
      ],
      selected_exhibits=[
         *INDO_EXHIBITS,
         'Africa Savanna',
         'African Rainforest Pavilion',
      ],
      confirming_early_admission=True,
      confirming_guardians_talk_without_animal=True,
      confirming_attraction_without_animal=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary(
      confirming_fixed_time_item_long_wait=True )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS

   kangaroo = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == KANGAROO_WALK_THRU )
   zoomobile = next(
      transportation
      for transportation in result.itinerary.transportations
      if transportation.name == 'Zoomobile' )
   greenhouse = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == 'Greenhouse' )
   talk = next(
      item
      for item in result.itinerary.guardians_talks
      if item.name == CAMEL_TALK )
   encounter = next(
      item
      for item in result.itinerary.wild_encounters
      if item.name == CAMEL_ENCOUNTER )

   assert kangaroo.start_time is not None
   assert kangaroo.end_time is not None
   assert zoomobile.start_time is not None
   assert zoomobile.end_time is not None
   assert greenhouse.start_time is not None
   assert talk.start_time is not None
   assert talk.end_time is not None
   assert encounter.start_time is not None

   kangaroo_start = DateValues.time_value_in_seconds( kangaroo.start_time )
   kangaroo_end = DateValues.time_value_in_seconds( kangaroo.end_time )
   zoomobile_start = DateValues.time_value_in_seconds( zoomobile.start_time )
   zoomobile_end = DateValues.time_value_in_seconds( zoomobile.end_time )
   greenhouse_start = DateValues.time_value_in_seconds( greenhouse.start_time )
   talk_start = DateValues.time_value_in_seconds( talk.start_time )
   talk_end = DateValues.time_value_in_seconds( talk.end_time )
   encounter_start = DateValues.time_value_in_seconds( encounter.start_time )
   assert kangaroo_start is not None
   assert kangaroo_end is not None
   assert zoomobile_start is not None
   assert zoomobile_end is not None
   assert greenhouse_start is not None
   assert talk_start is not None
   assert talk_end is not None
   assert encounter_start is not None

   assert kangaroo_start >= DateValues.time_value_in_seconds( '11:00 AM' )
   assert kangaroo_end <= talk_start
   greenhouse_end = DateValues.time_value_in_seconds( greenhouse.end_time )
   assert greenhouse_end is not None
   assert greenhouse_end <= talk_start
   # Greenhouse stays on the camel corridor with Walk-Thru — not at arrival
   # with a long blank gap before the rest of the morning.
   arrival = DateValues.time_value_in_seconds( '11:00 AM' )
   assert arrival is not None
   assert greenhouse_start >= arrival
   assert (
      abs( greenhouse_start - kangaroo_end ) <= 45 * 60
      or abs( greenhouse_end - kangaroo_start ) <= 45 * 60 )

   # Zoomobile may fill the wait before Walk-Thru opens, the pre-talk corridor
   # gap, or the Africa→encounter gap — not sit unused while leaving dead space.
   assert (
      zoomobile_end <= kangaroo_start
      or ( kangaroo_end <= zoomobile_start and zoomobile_end <= talk_start )
      or ( talk_end <= zoomobile_start and zoomobile_end <= encounter_start ) )

   africa_before_encounter = [
      animal
      for animal in result.itinerary.animals
      if animal.exhibit == 'Africa Savanna'
      and animal.end_time is not None
      and DateValues.time_value_in_seconds( animal.end_time ) is not None
      and DateValues.time_value_in_seconds( animal.end_time ) <= encounter_start
   ]
   if africa_before_encounter:
      last_africa_end = max(
         DateValues.time_value_in_seconds( animal.end_time )
         for animal in africa_before_encounter
         if DateValues.time_value_in_seconds( animal.end_time ) is not None )
      assert last_africa_end is not None
      assert zoomobile_start >= last_africa_end or zoomobile_end <= last_africa_end
