from __future__ import annotations

from ..types import Types


class Update:
   def __init__(
         self,
         title: str,
         description: str,
         update_type: str,
         start_date: Types.DateKey,
         end_date: Types.DateKey ) -> None:
      self.title = title
      self.description = description
      self.update_type = update_type
      self.start_date = start_date
      self.end_date = end_date


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'title': self.title,
         'description': self.description,
         'type': self.update_type,
         'start_date': self.start_date,
         'end_date': self.end_date
      }
