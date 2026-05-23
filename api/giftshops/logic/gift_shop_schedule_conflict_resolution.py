from datetime import date
from datetime import timedelta

from ..data_access.gift_shop_schedule import delete_gift_shop_opening_schedule
from ..data_access.gift_shop_schedule import fetch_gift_shop_opening_schedule_conflicts
from ..data_access.gift_shop_schedule import insert_copied_gift_shop_opening_schedule
from ..data_access.gift_shop_schedule import insert_or_update_gift_shop_opening_schedule
from ..data_access.gift_shop_schedule import update_gift_shop_opening_schedule_dates
from ...zoo_util import ZooUtil


def save_gift_shop_opening_schedule_replacing_overlaps( conn, schedule ):
   conflicts = fetch_gift_shop_opening_schedule_conflicts( conn, schedule )

   for conflict in conflicts:
      delete_gift_shop_opening_schedule( conn, conflict )

   insert_or_update_gift_shop_opening_schedule( conn, schedule )
   conn.commit()
   return True


def save_gift_shop_opening_schedule_trimming_overlaps( conn, schedule ):
   conflicts = fetch_gift_shop_opening_schedule_conflicts( conn, schedule )

   for conflict in conflicts:
      trim_gift_shop_opening_schedule_conflict( conn, conflict, schedule )

   insert_or_update_gift_shop_opening_schedule( conn, schedule )
   conn.commit()
   return True


def trim_gift_shop_opening_schedule_conflict( conn, conflict, schedule ):
   new_start_date = ZooUtil.parse_date_value( schedule.start_date )
   new_end_date = parse_opening_schedule_end_date( schedule.end_date )
   conflict_start_date = ZooUtil.parse_date_value( conflict.schedule_start_date )
   conflict_end_date = parse_opening_schedule_end_date(
      conflict.schedule_end_date )

   if conflict_start_date >= new_start_date and conflict_end_date <= new_end_date:
      delete_gift_shop_opening_schedule( conn, conflict )
      return

   if conflict_start_date < new_start_date and conflict_end_date <= new_end_date:
      update_gift_shop_opening_schedule_dates(
         conn,
         conflict,
         start_date=conflict.schedule_start_date,
         end_date=format_opening_schedule_date(
            new_start_date - timedelta( days=1 ) ) )
      return

   if conflict_start_date >= new_start_date and conflict_end_date > new_end_date:
      update_gift_shop_opening_schedule_dates(
         conn,
         conflict,
         start_date=format_opening_schedule_date(
            new_end_date + timedelta( days=1 ) ),
         end_date=conflict.schedule_end_date )
      return

   update_gift_shop_opening_schedule_dates(
      conn,
      conflict,
      start_date=conflict.schedule_start_date,
      end_date=format_opening_schedule_date(
         new_start_date - timedelta( days=1 ) ) )

   if new_end_date == date.max:
      return

   insert_copied_gift_shop_opening_schedule(
      conn,
      conflict,
      start_date=format_opening_schedule_date(
         new_end_date + timedelta( days=1 ) ),
      end_date=conflict.schedule_end_date )


def parse_opening_schedule_end_date( value ):
   if value == None:
      return date.max

   return ZooUtil.parse_date_value( value )


def format_opening_schedule_date( value ):
   if value == date.max:
      return None

   return value.isoformat()
