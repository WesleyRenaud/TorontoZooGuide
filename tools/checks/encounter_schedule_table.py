from __future__ import annotations

from datetime import datetime
import re

from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from api.wild_encounters.domain.wild_encounter_link import WildEncounterLink
from .encounter_schedule_slots import EncounterScheduleSlots
from .schedule_slot import ScheduleSlot
from .website_page import WebsitePage


class EncounterScheduleTable():
   TABLE_RE = re.compile( r'(?is)<table.*?</table>' )
   ROW_RE = re.compile( r'(?is)<tr.*?</tr>' )
   CELL_RE = re.compile( r'(?is)<t[dh][^>]*>(?P<cell>.*?)</t[dh]>' )
   CLOCK_WITH_MERIDIEM = '%I:%M %p'
   CLOCK_WITHOUT_MERIDIEM = '%H:%M'
   WEBSITE_NAME_ALIASES = {
      'bactrian camel': 'Bactrian Camels',
      'scales & tales': 'Scales & Tales of Americas',
      'snow leopard': 'Guardians of Snow Leopards',
      'the tiny tour!': 'The Tiny Tour',
   }


   @classmethod
   def apply_website_meridiem( cls, parsed: datetime ) -> datetime:
      if 1 <= parsed.hour <= 7:
         return parsed.replace( hour=parsed.hour + 12 )

      return parsed


   @classmethod
   def parsed_clock( cls, text: str, pattern: str ) -> datetime | None:
      try:
         return datetime.strptime( text, pattern )
      except ValueError:
         return None


   @classmethod
   def website_clock( cls, text: str ) -> datetime | None:
      parsed = cls.parsed_clock( text, cls.CLOCK_WITHOUT_MERIDIEM )

      if parsed == None:
         return None

      return cls.apply_website_meridiem( parsed )


   @classmethod
   def normalize_clock( cls, value: str ) -> str:
      text = value.strip().upper()
      parsed = cls.parsed_clock( text, cls.CLOCK_WITH_MERIDIEM ) or cls.website_clock( text )

      if parsed == None:
         return value.strip()

      return DateValues.format_display_time_value( parsed )


   @classmethod
   def schedule_rows( cls, page_html: str ) -> list[ str ]:
      table = cls.TABLE_RE.search( page_html )
      return cls.ROW_RE.findall( table.group( 0 ) )[ 1: ]


   @classmethod
   def cells( cls, row: str ) -> list[ str ]:
      return [
         WebsitePage.clean_html( match.group( 'cell' ) )
         for match in cls.CELL_RE.finditer( row )
      ]


   @classmethod
   def add_day_slots(
         cls,
         slots: EncounterScheduleSlots,
         cells: list[ str ] ) -> None:
      encounter_time = DateValues.parse_time_value( cls.normalize_clock( cells[ 0 ] ) )

      for column, name in enumerate( cells[ 1:8 ] ):
         if name == '':
            continue

         slots.add( name, ScheduleSlot(
            weekday=CalendarDates.convert_weekday( column, sunday_first=False ),
            time=encounter_time,
         ) )


   @classmethod
   def parse( cls, page_html: str ) -> EncounterScheduleSlots:
      slots = EncounterScheduleSlots()

      for row in cls.schedule_rows( page_html ):
         cells = cls.cells( row )

         if len( cells ) < 8 or cells[ 0 ] == '':
            continue

         cls.add_day_slots( slots, cells )

      return slots


   @classmethod
   def resolve_name( cls, name: str, encounters: list[ WildEncounterLink ] ) -> str:
      alias = cls.WEBSITE_NAME_ALIASES.get( name.casefold(), name )
      return WildEncounterLink.stored_name( alias, encounters )


   @classmethod
   def resolve(
         cls,
         website_slots: EncounterScheduleSlots,
         encounters: list[ WildEncounterLink ] ) -> EncounterScheduleSlots:
      resolved = EncounterScheduleSlots()

      for name in website_slots.names():
         resolved.add_slots(
            cls.resolve_name( name, encounters ),
            website_slots.for_name( name ),
         )

      return resolved
