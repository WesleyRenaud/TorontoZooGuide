from __future__ import annotations

from api.models.update import Update
from api.updates.domain.update_type import UpdateType
from api.updates.domain.updates_display_builder import UpdatesDisplayBuilder


def Test_DisplayOrder_TestUpdateTypes_ExpectConfiguredOrder() -> None:
   update_types = list( UpdateType )

   orders = [ update_type.order for update_type in update_types ]

   assert orders == list( range( len( update_types ) ) )


def Test_SortForDisplay_TestMixedUpdates_ExpectGroupsByTypeThenEndDate() -> None:
   open_ended_departure = Update(
      title='Open-ended departure',
      description='',
      update_type=UpdateType.DEPARTURE.value,
      start_date='2026-01-01',
      end_date=None )
   later_birth = Update(
      title='Later birth',
      description='',
      update_type=UpdateType.ANIMAL_BIRTH.value,
      start_date='2026-01-01',
      end_date='2026-08-01' )
   sooner_birth = Update(
      title='Sooner birth',
      description='',
      update_type=UpdateType.ANIMAL_BIRTH.value,
      start_date='2026-01-01',
      end_date='2026-07-01' )
   closure_a = Update(
      title='Closure A',
      description='',
      update_type=UpdateType.CLOSURE.value,
      start_date='2026-01-01',
      end_date='2026-09-01' )
   closure_b = Update(
      title='Closure B',
      description='',
      update_type=UpdateType.CLOSURE.value,
      start_date='2026-01-01',
      end_date='2026-06-01' )
   passing = Update(
      title='Passing',
      description='',
      update_type=UpdateType.ANIMAL_PASSING.value,
      start_date='2026-01-01',
      end_date='2026-07-15' )
   arrival = Update(
      title='Arrival',
      description='',
      update_type=UpdateType.NEW_ARRIVAL.value,
      start_date='2026-01-01',
      end_date='2026-07-15' )
   ending_departure = Update(
      title='Ending departure',
      description='',
      update_type=UpdateType.DEPARTURE.value,
      start_date='2026-01-01',
      end_date='2026-07-01' )
   updates = [
      open_ended_departure,
      later_birth,
      sooner_birth,
      closure_a,
      closure_b,
      passing,
      arrival,
      ending_departure,
   ]

   sorted_updates = UpdatesDisplayBuilder.sort_for_display( updates )

   assert [ update.title for update in sorted_updates ] == [
      closure_b.title,
      closure_a.title,
      sooner_birth.title,
      later_birth.title,
      passing.title,
      arrival.title,
      ending_departure.title,
      open_ended_departure.title,
   ]
