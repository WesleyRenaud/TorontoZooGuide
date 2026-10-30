from __future__ import annotations

from ...itinerary.schedule_item_key_separator import ScheduleItemKeySeparator


class GuardiansTalkIdentity():
   @classmethod
   def enclosure_name( cls, value: str | None ) -> str | None:
      enclosure_name = ( value or '' ).strip()

      if not enclosure_name:
         return None

      return enclosure_name


   @classmethod
   def item_key( cls, name: str, enclosure_name: str | None ) -> str:
      if not enclosure_name:
         return name

      return ScheduleItemKeySeparator.VALUE.join( [ name, enclosure_name ] )


   @classmethod
   def parse_item_key( cls, item_key: str ) -> tuple[ str, str | None ]:
      name, separator, enclosure_name = item_key.partition(
         ScheduleItemKeySeparator.VALUE )

      if not separator or not enclosure_name:
         return name, None

      return name, enclosure_name
