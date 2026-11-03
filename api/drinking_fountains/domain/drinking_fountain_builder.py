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
         likelihood: float,
         is_closed_for_season: bool = False ) -> DrinkingFountain:
      return DrinkingFountain(
         x_coord=record.x_coord,
         y_coord=record.y_coord,
         is_closed=is_closed,
         closed_message=closed_message if is_closed else None,
         likelihood=likelihood,
         is_closed_for_season=is_closed_for_season )


   @classmethod
   def build_drinking_fountains(
         cls,
         fountain_records: list[ DrinkingFountainRecord ],
         is_closed: bool,
         closed_message: str | None,
         likelihood: float,
         is_closed_for_season: bool = False ) -> list[ DrinkingFountain ]:
      return [
         cls.record_to_model(
            record,
            is_closed,
            closed_message,
            likelihood,
            is_closed_for_season )
         for record in fountain_records
      ]
