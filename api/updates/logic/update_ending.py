from __future__ import annotations

from ... import zoo
from ...types import DateInput, DateKey
from .update_end_input import UpdateEndInput


def build_update_end_input(
      title: str,
      start_date: DateKey,
      end_date: DateInput ) -> UpdateEndInput:
   if not end_date:
      end_date = zoo.ZooUtil.today_date_key()

   return UpdateEndInput(
      title=title,
      start_date=start_date,
      end_date=end_date )
