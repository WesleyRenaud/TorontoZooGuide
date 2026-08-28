from __future__ import annotations

from ..types import Types


class Event:
   def __init__(
         self,
         name: str,
         location: str,
         description: str,
         link: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput ) -> None:
      self.name = name
      self.location = location
      self.description = description
      self.link = link
      self.start_date = start_date
      self.end_date = end_date


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'location': self.location,
         'description': self.description,
         'link': self.link,
         'start_date': self.start_date,
         'end_date': self.end_date,
      }
