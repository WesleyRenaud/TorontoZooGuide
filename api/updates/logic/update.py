from __future__ import annotations

from datetime import date

from ...models import Update
from ...zoo_util import ZooUtil
from ...types import DateKey


def filter_updates_started_on_or_before(
      updates: list[ Update ],
      as_of_date: date ) -> list[ Update ]:
   return [
      update
      for update in updates
      if ZooUtil.is_date_on_or_after( as_of_date, update.start_date )
   ]
