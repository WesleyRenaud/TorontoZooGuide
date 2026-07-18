from __future__ import annotations

from ...models import Update
from ...shared.constants import OPEN_ENDED_SQL_DATE
from ...shared.name_matching_query import normalize_search_key
from .update_type import update_type_display_order


def update_display_sort_key( update: Update ) -> tuple[ int, str, str ]:
   end_date = update.end_date or OPEN_ENDED_SQL_DATE

   return (
      update_type_display_order( update.update_type ),
      end_date,
      normalize_search_key( update.title ),
   )


def sort_updates_for_display( updates: list[ Update ] ) -> list[ Update ]:
   return sorted( updates, key=update_display_sort_key )
