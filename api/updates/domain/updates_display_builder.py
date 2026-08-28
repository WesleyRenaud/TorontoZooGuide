from __future__ import annotations

from datetime import date

from ...models import Update
from ...shared.calendar_dates import DateValues
from ...shared.constants import OPEN_ENDED_SQL_DATE
from ...shared.text_values import TextValues
from .update_type_display_order_resolver import UpdateTypeDisplayOrderResolver


class UpdatesDisplayBuilder():
   @classmethod
   def filter_started_on_or_before(
         cls,
         updates: list[ Update ],
         as_of_date: date ) -> list[ Update ]:
      return [
         update
         for update in updates
         if DateValues.is_date_on_or_after( as_of_date, update.start_date )
      ]


   @classmethod
   def display_sort_key( cls, update: Update ) -> tuple[ int, str, str ]:
      end_date = update.end_date or OPEN_ENDED_SQL_DATE

      return (
         UpdateTypeDisplayOrderResolver.resolve( update.update_type ),
         end_date,
         TextValues.normalize_for_matching( update.title ),
      )


   @classmethod
   def sort_for_display( cls, updates: list[ Update ] ) -> list[ Update ]:
      return sorted( updates, key=cls.display_sort_key )
