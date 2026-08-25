from __future__ import annotations

from ..data_access.drinking_fountain_record import DrinkingFountainRecord
from ...models import DrinkingFountain


class DrinkingFountainBuilder():
   @classmethod
   def record_to_model(
         cls,
         record: DrinkingFountainRecord,
         is_closed: bool,
         closed_message: str | None,
         likelihood: float ) -> DrinkingFountain:
      return DrinkingFountain(
         x_coord=record.x_coord,
         y_coord=record.y_coord,
         is_closed=is_closed,
         closed_message=closed_message if is_closed else None,
         likelihood=likelihood )


   @classmethod
   def build_drinking_fountains(
         cls,
         fountain_records: list[ DrinkingFountainRecord ],
         is_closed: bool,
         closed_message: str | None,
         likelihood: float ) -> list[ DrinkingFountain ]:
      return [
         cls.record_to_model(
            record,
            is_closed,
            closed_message,
            likelihood )
         for record in fountain_records
      ]
