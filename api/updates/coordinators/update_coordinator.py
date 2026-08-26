from __future__ import annotations

from ..data_access.update_provider import UpdateProvider
from ..domain.updates_display_builder import UpdatesDisplayBuilder
from ...models import Update
from ..operations.update_create_input_builder import UpdateCreateInputBuilder
from ..operations.update_edit_input_builder import UpdateEditInputBuilder
from ..operations.update_end_input_builder import UpdateEndInputBuilder
from ...request_connection import get_connection
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ...types import DateInput, MonthInput, VisitDay, VisitYear


class UpdateCoordinator():
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

      updates = UpdateProvider.fetch_updates( get_connection(), target_date )

      return UpdatesDisplayBuilder.sort_for_display(
         UpdatesDisplayBuilder.filter_started_on_or_before(
            updates,
            target_date ) )


   @classmethod
   def get_unexpired_updates( cls ) -> list[ Update ]:
      as_of_date = DateValues.today_date_key()

      return UpdatesDisplayBuilder.sort_for_display(
         UpdateProvider.fetch_updates( get_connection(), as_of_date ) )


   @classmethod
   def create_update(
         cls,
         title: str,
         description: str,
         update_type: str,
         start_date: DateInput,
         end_date: DateInput ) -> bool:
      update = UpdateCreateInputBuilder.build(
         title=title,
         description=description,
         update_type=update_type,
         start_date=start_date,
         end_date=end_date )

      return UpdateProvider.insert_update(
         get_connection(),
         update=update )


   @classmethod
   def end_update(
         cls,
         title: str,
         start_date: DateInput,
         end_date: DateInput ) -> bool:
      update = UpdateEndInputBuilder.build(
         title=title,
         start_date=start_date,
         end_date=end_date )

      return UpdateProvider.update_end_date(
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
      update = UpdateEditInputBuilder.build(
         title=title,
         start_date=start_date,
         description=description,
         update_type=update_type,
         end_date=end_date )

      return UpdateProvider.edit_update_record(
         get_connection(),
         update=update )
