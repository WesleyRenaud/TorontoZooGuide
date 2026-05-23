from __future__ import annotations

from ..data_access.update import edit_update_record
from ..data_access.update import fetch_updates
from ..data_access.update import insert_update
from ..data_access.update import update_end_date
from ..logic.update import filter_updates_started_on_or_before
from ..logic.update_creation import build_update_create_input
from ..logic.update_editing import build_update_edit_input
from ..logic.update_ending import build_update_end_input
from ...models import Update
from ...request_connection import get_connection
from ...shared.calendar_dates import CalendarDates
from ...shared.date_values import DateValues
from ...types import DateInput, MonthInput, VisitDay, VisitYear


class UpdateController():


   @classmethod
   def get_updates_for_visit_date(
         cls,
         month: MonthInput,
         day: VisitDay,
         year: VisitYear ) -> list[ Update ]:
      target_date = CalendarDates.visit_target_date(
         month=month,
         day=day,
         year=year )

      updates = fetch_updates( get_connection(), target_date )

      return filter_updates_started_on_or_before(
         updates,
         target_date )


   @classmethod
   def get_unexpired_updates( cls ) -> list[ Update ]:
      as_of_date = DateValues.today_date_key()

      return fetch_updates( get_connection(), as_of_date )


   @classmethod
   def create_update(
         cls,
         title: str,
         description: str,
         update_type: str,
         start_date: DateInput,
         end_date: DateInput ) -> bool:
      update = build_update_create_input(
         title=title,
         description=description,
         update_type=update_type,
         start_date=start_date,
         end_date=end_date )

      return insert_update(
         get_connection(),
         update=update )


   @classmethod
   def end_update(
         cls,
         title: str,
         start_date: DateInput,
         end_date: DateInput ) -> bool:
      update = build_update_end_input(
         title=title,
         start_date=start_date,
         end_date=end_date )

      return update_end_date(
         get_connection(),
         update=update )


   @classmethod
   def edit_update(
         cls,
         title: str,
         start_date: DateInput,
         description: str,
         update_type: str,
         end_date: DateInput ) -> bool:
      update = build_update_edit_input(
         title=title,
         start_date=start_date,
         description=description,
         update_type=update_type,
         end_date=end_date )

      return edit_update_record(
         get_connection(),
         update=update )
