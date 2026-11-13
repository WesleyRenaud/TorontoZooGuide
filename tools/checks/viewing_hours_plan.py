from __future__ import annotations

from datetime import date

from api.animals.domain.animal_visibility_schedule import AnimalVisibilitySchedule
from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from .viewing_hours import ViewingHours


class ViewingHoursPlan():
   added: list[ ViewingHours ]
   removed: list[ ViewingHours ]
   extended: list[ ViewingHours ]
   trimmed: list[ ViewingHours ]
   realigned: list[ ViewingHours ]


   def __init__(
         self,
         added: list[ ViewingHours ],
         removed: list[ ViewingHours ],
         extended: list[ ViewingHours ],
         trimmed: list[ ViewingHours ],
         realigned: list[ ViewingHours ] ) -> None:
      self.added = added
      self.removed = removed
      self.extended = extended
      self.trimmed = trimmed
      self.realigned = realigned


   def count( self ) -> int:
      return (
         len( self.added )
         + len( self.removed )
         + len( self.extended )
         + len( self.trimmed )
         + len( self.realigned )
      )


   @classmethod
   def key( cls, species: str, exhibit: str ) -> tuple[ str, str ]:
      return ( species.casefold(), exhibit.casefold() )


   @classmethod
   def by_key(
         cls,
         hours: list[ ViewingHours ] ) -> dict[ tuple[ str, str ], ViewingHours ]:
      found: dict[ tuple[ str, str ], ViewingHours ] = {}

      for item in hours:
         identity = cls.key( item.species, item.exhibit )

         if identity not in found:
            found[ identity ] = item

      return found


   @classmethod
   def stored_end( cls, schedule: AnimalVisibilitySchedule ) -> date | None:
      if schedule.end_date in ( None, '' ):
         return None

      return DateValues.parse_date_value( schedule.end_date )


   @classmethod
   def stored_start( cls, schedule: AnimalVisibilitySchedule, today: date ) -> date:
      if schedule.start_date in ( None, '' ):
         return today

      start = DateValues.parse_date_value( schedule.start_date )

      if start == None:
         return today

      return start


   @classmethod
   def same_time( cls, left: str, right: str ) -> bool:
      try:
         return (
            DateValues.time_value_in_seconds( left )
            == DateValues.time_value_in_seconds( right )
         )
      except ValueError:
         return False


   @classmethod
   def clock( cls, value: str ) -> str:
      try:
         display = DateValues.format_display_time_value( value )
      except ValueError:
         return value

      if display == None:
         return value

      return display


   @classmethod
   def times_differ(
         cls,
         schedule: AnimalVisibilitySchedule,
         website: ViewingHours ) -> bool:
      return (
         not cls.same_time( schedule.daily_start_time, website.opens )
         or not cls.same_time( schedule.daily_end_time, website.closes )
      )


   @classmethod
   def addition( cls, website: ViewingHours, today: date ) -> ViewingHours:
      return ViewingHours(
         website.species,
         website.exhibit,
         today,
         CalendarDates.one_month_later( today ),
         cls.clock( website.opens ),
         cls.clock( website.closes ),
         website.subject,
      )


   @classmethod
   def removal(
         cls,
         schedule: AnimalVisibilitySchedule,
         today: date ) -> ViewingHours:
      return ViewingHours(
         schedule.species,
         schedule.exhibit,
         cls.stored_start( schedule, today ),
         cls.stored_end( schedule ) or today,
         schedule.daily_start_time,
         schedule.daily_end_time,
      )


   @classmethod
   def replacement(
         cls,
         schedule: AnimalVisibilitySchedule,
         website: ViewingHours,
         today: date ) -> ViewingHours:
      start = cls.stored_start( schedule, today )
      horizon = CalendarDates.one_month_later( today )

      if start > horizon:
         start = today

      return ViewingHours(
         schedule.species,
         schedule.exhibit,
         start,
         horizon,
         cls.clock( website.opens ),
         cls.clock( website.closes ),
         website.subject,
      )


   @classmethod
   def added(
         cls,
         website: list[ ViewingHours ],
         stored: list[ AnimalVisibilitySchedule ],
         today: date ) -> list[ ViewingHours ]:
      have = { cls.key( item.species, item.exhibit ) for item in stored }
      return [
         cls.addition( hours, today )
         for identity, hours in cls.by_key( website ).items()
         if identity not in have
      ]


   @classmethod
   def removed(
         cls,
         website: list[ ViewingHours ],
         stored: list[ AnimalVisibilitySchedule ],
         today: date ) -> list[ ViewingHours ]:
      web = cls.by_key( website )
      return [
         cls.removal( item, today )
         for item in stored
         if cls.key( item.species, item.exhibit ) not in web
      ]


   @classmethod
   def extended(
         cls,
         website: list[ ViewingHours ],
         stored: list[ AnimalVisibilitySchedule ],
         today: date ) -> list[ ViewingHours ]:
      web = cls.by_key( website )
      horizon = CalendarDates.one_month_later( today )
      changes = []

      for item in stored:
         hours = web.get( cls.key( item.species, item.exhibit ) )

         if hours == None:
            continue

         end = cls.stored_end( item )

         if end != None and end < horizon:
            changes.append( cls.replacement( item, hours, today ) )

      return changes


   @classmethod
   def trimmed(
         cls,
         website: list[ ViewingHours ],
         stored: list[ AnimalVisibilitySchedule ],
         today: date ) -> list[ ViewingHours ]:
      web = cls.by_key( website )
      horizon = CalendarDates.one_month_later( today )
      changes = []

      for item in stored:
         hours = web.get( cls.key( item.species, item.exhibit ) )

         if hours == None:
            continue

         end = cls.stored_end( item )

         if end == None or end > horizon:
            changes.append( cls.replacement( item, hours, today ) )

      return changes


   @classmethod
   def realigned(
         cls,
         website: list[ ViewingHours ],
         stored: list[ AnimalVisibilitySchedule ],
         today: date ) -> list[ ViewingHours ]:
      web = cls.by_key( website )
      horizon = CalendarDates.one_month_later( today )
      changes = []

      for item in stored:
         hours = web.get( cls.key( item.species, item.exhibit ) )

         if hours == None or cls.stored_end( item ) != horizon:
            continue

         if cls.times_differ( item, hours ):
            changes.append( cls.replacement( item, hours, today ) )

      return changes


   @classmethod
   def build(
         cls,
         website: list[ ViewingHours ],
         stored: list[ AnimalVisibilitySchedule ],
         today: date ) -> ViewingHoursPlan:
      return cls(
         cls.added( website, stored, today ),
         cls.removed( website, stored, today ),
         cls.extended( website, stored, today ),
         cls.trimmed( website, stored, today ),
         cls.realigned( website, stored, today ),
      )
