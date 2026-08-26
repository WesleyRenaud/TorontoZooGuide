from __future__ import annotations

from datetime import date

from ...models import Update
from ...shared.calendar_dates import DateValues
from ...shared.constants import OPEN_ENDED_SQL_DATE
from ...shared.name_matching_query import normalize_search_key
from .update_type import update_type_display_order


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
         update_type_display_order( update.update_type ),
         end_date,
         normalize_search_key( update.title ),
      )


   @classmethod
   def sort_for_display( cls, updates: list[ Update ] ) -> list[ Update ]:
      return sorted( updates, key=cls.display_sort_key )
