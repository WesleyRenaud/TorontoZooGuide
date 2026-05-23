from __future__ import annotations

from datetime import date

from ... import zoo
from ...types import DateKey


def filter_updates_started_on_or_before(
      updates: list[ zoo.Update ],
      as_of_date: date ) -> list[ zoo.Update ]:
   return [
      update
      for update in updates
      if zoo.ZooUtil.is_date_on_or_after( as_of_date, update.start_date )
   ]
