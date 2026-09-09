from __future__ import annotations

from .attraction_schedule_mapper import AttractionScheduleMapper
from .attraction_schedule_record import AttractionScheduleRecord
from ..scheduling.attraction_opening_schedule import AttractionOpeningSchedule
from ..scheduling.attraction_schedule_override import AttractionScheduleOverride
from ...shared.amenity_opening_schedule_provider import AmenityOpeningScheduleProvider
from ...shared.enums import AmenityNameField
from ...types import Types


class AttractionScheduleProvider():
   _provider = AmenityOpeningScheduleProvider(
      name_field=AmenityNameField.ATTRACTION,
      opening_table='AttractionOpeningSchedule',
      override_table='AttractionScheduleOverride',
      map_records=AttractionScheduleMapper.map_records,
   )


   @classmethod
   def overlaps_existing_schedule(
         cls,
         conn: Types.Connection,
         schedule: AttractionOpeningSchedule ) -> bool:
      return cls._provider.overlaps_existing_schedule( conn, schedule )


   @classmethod
   def save_opening_schedule(
         cls,
         conn: Types.Connection,
         schedule: AttractionOpeningSchedule ) -> bool:
      if cls.overlaps_existing_schedule( conn, schedule ):
         return False

      cls.insert_or_update_opening_schedule( conn, schedule )
      conn.commit()
      return True


   @classmethod
   def fetch_opening_schedule_conflicts(
         cls,
         conn: Types.Connection,
         schedule: AttractionOpeningSchedule ) -> list[ AttractionScheduleRecord ]:
      return cls._provider.fetch_opening_schedule_conflicts( conn, schedule )


   @classmethod
   def delete_opening_schedule(
         cls,
         conn: Types.Connection,
         schedule: AttractionScheduleRecord ) -> None:
      cls._provider.delete_opening_schedule( conn, schedule )


   @classmethod
   def update_opening_schedule_dates(
         cls,
         conn: Types.Connection,
         schedule: AttractionScheduleRecord,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None ) -> None:
      cls._provider.update_opening_schedule_dates( conn, schedule, start_date, end_date )


   @classmethod
   def insert_copied_opening_schedule(
         cls,
         conn: Types.Connection,
         schedule: AttractionScheduleRecord,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None ) -> None:
      cls._provider.insert_copied_opening_schedule( conn, schedule, start_date, end_date )


   @classmethod
   def insert_or_update_opening_schedule(
         cls,
         conn: Types.Connection,
         schedule: AttractionOpeningSchedule ) -> None:
      cls._provider.insert_or_update_opening_schedule( conn, schedule )


   @classmethod
   def save_schedule_override(
         cls,
         conn: Types.Connection,
         override: AttractionScheduleOverride ) -> bool:
      return cls._provider.save_schedule_override( conn, override )
