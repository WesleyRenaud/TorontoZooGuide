from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import guardians_talk_save_entry
from itinerary.support import guardians_talk_wire
from itinerary.support import unschedule_itinerary_item
from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from conftest import DbControllers

ZEBRA_TALK = "Grevy's Zebra"
AFRICA_SAVANNA = 'Africa Savanna'


def _selected_exhibits_for_africa_savanna() -> list[ str ]:
   from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator

   for region in ExhibitCoordinator.get_regions_with_exhibits():
      if AFRICA_SAVANNA in region.exhibits:
         return [ AFRICA_SAVANNA ]

   raise AssertionError( f'{ AFRICA_SAVANNA } exhibit not found in seed data' )


def _set_saturday_zebra_talk_schedule(
      *,
      talk_time: str = '11:00' ) -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=ZEBRA_TALK,
      location=AFRICA_SAVANNA,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( talk_time, monday=False, tuesday=False, wednesday=False, thursday=False, friday=False, saturday=True, sunday=False ),
      message=None,
   )


def test_bulk_schedule_packs_non_pinned_loops_before_guardians_talk_and_shifts_arrival(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_saturday_zebra_talk_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( ZEBRA_TALK, start_time='11:00' ) ],
      wild_encounters=[],
      selected_exhibits=_selected_exhibits_for_africa_savanna(),
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.reasons == ()
   assert len( result.adjustments ) == 1
   assert result.adjustments[ 0 ].type.value == 'arrivalTimeAdjusted'
   assert result.adjustments[ 0 ].previous_value == '9:00 AM'

   giraffe = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'Masai Giraffe'
      and animal.enclosure_name == 'Outdoor' )
   talk = next(
      talk for talk in result.itinerary.guardians_talks
      if talk.name == ZEBRA_TALK )

   original_arrival_seconds = DateValues.time_value_in_seconds( '9:00 AM' )
   adjusted_arrival_seconds = DateValues.time_value_in_seconds(
      result.itinerary.arrival_time )
   giraffe_start_seconds = DateValues.time_value_in_seconds( giraffe.start_time )
   talk_start_seconds = DateValues.time_value_in_seconds( talk.start_time )

   assert original_arrival_seconds is not None
   assert adjusted_arrival_seconds is not None
   assert giraffe_start_seconds is not None
   assert talk_start_seconds is not None

   assert adjusted_arrival_seconds > original_arrival_seconds
   assert giraffe_start_seconds == adjusted_arrival_seconds
   assert giraffe_start_seconds < talk_start_seconds

   scheduled_animals = [
      animal
      for animal in result.itinerary.animals
      if animal.start_time is not None and animal.end_time is not None
   ]

   assert scheduled_animals

   earliest_start_seconds = min(
      DateValues.time_value_in_seconds( animal.start_time )
      for animal in scheduled_animals )

   assert earliest_start_seconds == adjusted_arrival_seconds

   latest_end_seconds = max(
      [
         DateValues.time_value_in_seconds( animal.end_time )
         for animal in scheduled_animals
      ]
      + [ DateValues.time_value_in_seconds( talk.end_time ) ]
   )
   assert DateValues.time_value_in_seconds(
      result.itinerary.departure_time ) == latest_end_seconds


def _schedule_africa_savanna_with_zebra_talk(
      *,
      talk_time: str = '11:00' ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( ZEBRA_TALK, start_time=talk_time ) ],
      wild_encounters=[],
      selected_exhibits=_selected_exhibits_for_africa_savanna(),
      confirming_early_admission=True,
   ).success


def test_bulk_schedule_pulls_arrival_earlier_after_pinned_talk_removed_and_rescheduled(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_saturday_zebra_talk_schedule()
   _schedule_africa_savanna_with_zebra_talk()

   with_talk = ItineraryCoordinator.bulk_schedule_animals()

   assert with_talk.success
   assert len( with_talk.adjustments ) == 1
   assert with_talk.adjustments[ 0 ].type.value == 'arrivalTimeAdjusted'

   pushed_arrival_seconds = DateValues.time_value_in_seconds(
      with_talk.itinerary.arrival_time )

   assert pushed_arrival_seconds is not None
   assert pushed_arrival_seconds > DateValues.time_value_in_seconds( '9:00 AM' )

   assert unschedule_itinerary_item(
      item_type='guardians_talks',
      key=guardians_talk_wire( ZEBRA_TALK, start_time='11:00' ),
   ).success

   without_talk = ItineraryCoordinator.bulk_schedule_animals()

   assert without_talk.success

   scheduled_animals = [
      animal
      for animal in without_talk.itinerary.animals
      if animal.start_time is not None and animal.end_time is not None
   ]

   earliest_start_seconds = min(
      DateValues.time_value_in_seconds( animal.start_time )
      for animal in scheduled_animals )
   arrival_seconds = DateValues.time_value_in_seconds(
      without_talk.itinerary.arrival_time )

   assert earliest_start_seconds is not None
   assert arrival_seconds is not None
   assert arrival_seconds == earliest_start_seconds
   assert arrival_seconds < pushed_arrival_seconds
