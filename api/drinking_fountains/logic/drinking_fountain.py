from __future__ import annotations

from ... import zoo
from ..data_access.drinking_fountain_record import DrinkingFountainRecord


def drinking_fountain_record_to_model(
      record: DrinkingFountainRecord,
      is_closed: bool,
      closed_message: str | None,
      likelihood: float ) -> zoo.DrinkingFountain:
   return zoo.DrinkingFountain(
      x_coord=record.x_coord,
      y_coord=record.y_coord,
      is_closed=is_closed,
      closed_message=closed_message if is_closed else None,
      likelihood=likelihood )



def build_drinking_fountains(
      fountain_records: list[ DrinkingFountainRecord ],
      is_closed: bool,
      closed_message: str | None,
      likelihood: float ) -> list[ zoo.DrinkingFountain ]:
   return [
      drinking_fountain_record_to_model(
         record,
         is_closed,
         closed_message,
         likelihood )
      for record in fountain_records
   ]
