from __future__ import annotations

from api.models.update import Update
from api.updates.domain.update_type import UpdateType
from api.updates.domain.updates_display_builder import UpdatesDisplayBuilder


def Test_DisplayOrder_TestUpdateTypes_ExpectConfiguredOrder() -> None:
   assert UpdateType.CLOSURE.order == 0
   assert UpdateType.ANIMAL_BIRTH.order == 1
   assert UpdateType.ANIMAL_PASSING.order == 2
   assert UpdateType.NEW_ARRIVAL.order == 3
   assert UpdateType.DEPARTURE.order == 4


def Test_SortForDisplay_TestMixedUpdates_ExpectGroupsByTypeThenEndDate() -> None:
   updates = [
      Update(
         title='Open-ended departure',
         description='',
         update_type='Departure',
         start_date='2026-01-01',
         end_date=None ),
      Update(
         title='Later birth',
         description='',
         update_type='Animal Birth',
         start_date='2026-01-01',
         end_date='2026-08-01' ),
      Update(
         title='Sooner birth',
         description='',
         update_type='Animal Birth',
         start_date='2026-01-01',
         end_date='2026-07-01' ),
      Update(
         title='Closure A',
         description='',
         update_type='Closure',
         start_date='2026-01-01',
         end_date='2026-09-01' ),
      Update(
         title='Closure B',
         description='',
         update_type='Closure',
         start_date='2026-01-01',
         end_date='2026-06-01' ),
      Update(
         title='Passing',
         description='',
         update_type='Animal Passing',
         start_date='2026-01-01',
         end_date='2026-07-15' ),
      Update(
         title='Arrival',
         description='',
         update_type='New Arrival',
         start_date='2026-01-01',
         end_date='2026-07-15' ),
      Update(
         title='Ending departure',
         description='',
         update_type='Departure',
         start_date='2026-01-01',
         end_date='2026-07-01' ),
   ]

   assert [ update.title for update in UpdatesDisplayBuilder.sort_for_display( updates ) ] == [
      'Closure B',
      'Closure A',
      'Sooner birth',
      'Later birth',
      'Passing',
      'Arrival',
      'Ending departure',
      'Open-ended departure',
   ]
