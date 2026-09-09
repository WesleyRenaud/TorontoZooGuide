from __future__ import annotations

from .restaurant_schedule_mapper import RestaurantScheduleMapper
from .restaurant_schedule_record import RestaurantScheduleRecord
from ..scheduling.restaurant_opening_schedule import RestaurantOpeningSchedule
from ..scheduling.restaurant_schedule_override import RestaurantScheduleOverride
from ...shared.amenity_opening_schedule_provider import AmenityOpeningScheduleProvider
from ...shared.enums import AmenityNameField
from ...types import Types


class RestaurantScheduleProvider():
   _provider = AmenityOpeningScheduleProvider(
      name_field=AmenityNameField.RESTAURANT,
      opening_table='RestaurantOpeningSchedule',
      override_table='RestaurantScheduleOverride',
      map_records=RestaurantScheduleMapper.map_records,
   )


   @classmethod
   def overlaps_existing_schedule(
         cls,
         conn: Types.Connection,
         schedule: RestaurantOpeningSchedule ) -> bool:
      return cls._provider.overlaps_existing_schedule( conn, schedule )


   @classmethod
   def save_opening_schedule(
         cls,
         conn: Types.Connection,
         schedule: RestaurantOpeningSchedule ) -> bool:
      if cls.overlaps_existing_schedule( conn, schedule ):
         return False

      cls.insert_or_update_opening_schedule( conn, schedule )
      conn.commit()
      return True


   @classmethod
   def fetch_opening_schedule_conflicts(
         cls,
         conn: Types.Connection,
         schedule: RestaurantOpeningSchedule ) -> list[ RestaurantScheduleRecord ]:
      return cls._provider.fetch_opening_schedule_conflicts( conn, schedule )


   @classmethod
   def delete_opening_schedule(
         cls,
         conn: Types.Connection,
         schedule: RestaurantScheduleRecord ) -> None:
      cls._provider.delete_opening_schedule( conn, schedule )


   @classmethod
   def update_opening_schedule_dates(
         cls,
         conn: Types.Connection,
         schedule: RestaurantScheduleRecord,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None ) -> None:
      cls._provider.update_opening_schedule_dates( conn, schedule, start_date, end_date )


   @classmethod
   def insert_copied_opening_schedule(
         cls,
         conn: Types.Connection,
         schedule: RestaurantScheduleRecord,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None ) -> None:
      cls._provider.insert_copied_opening_schedule( conn, schedule, start_date, end_date )


   @classmethod
   def insert_or_update_opening_schedule(
         cls,
         conn: Types.Connection,
         schedule: RestaurantOpeningSchedule ) -> None:
      cls._provider.insert_or_update_opening_schedule( conn, schedule )


   @classmethod
   def save_schedule_override(
         cls,
         conn: Types.Connection,
         override: RestaurantScheduleOverride ) -> bool:
      return cls._provider.save_schedule_override( conn, override )
