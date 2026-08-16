from __future__ import annotations

from ..data_access.transportation_record import TransportationRecord
from ...models.transportation import Transportation


def build_transportation(
      record: TransportationRecord ) -> Transportation:
   return Transportation(
      name=record.name,
      is_also_attraction=record.is_also_attraction,
      free_with_admission=record.free_with_admission,
      description=record.description,
      info_link=record.info_link,
      hyperlink_text=record.hyperlink_text,
      x_coord=record.x_coord,
      y_coord=record.y_coord,
      region=record.region )


def build_transportations(
      records: list[ TransportationRecord ] ) -> list[ Transportation ]:
   return [
      build_transportation( record )
      for record in records
   ]
