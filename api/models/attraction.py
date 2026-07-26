from __future__ import annotations

from ..shared.value_conversion import ValueConversion
from ..types import ScheduleTimeKey


class Attraction:
   def __init__(
         self,
         name: str,
         free_with_admission: bool,
         description: str | None = None,
         info_link: str | None = None,
         hyperlink_text: str | None = None,
         x_coord: float | None = None,
         y_coord: float | None = None,
         region: str | None = None,
         is_closed: bool = False,
         closed_message: str | None = None,
         likelihood: int | None = None,
         is_deleted: bool = False,
         old_likelihood: int | None = None,
         start_time: ScheduleTimeKey = None,
         end_time: ScheduleTimeKey = None ) -> None:
      self.name = name
      self.free_with_admission = free_with_admission
      self.description = description
      self.info_link = info_link
      self.hyperlink_text = hyperlink_text
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.region = region
      self.is_closed = is_closed
      self.closed_message = closed_message
      self.likelihood = likelihood
      self.is_deleted = is_deleted
      self.old_likelihood = old_likelihood
      self.start_time = start_time
      self.end_time = end_time


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'free_with_admission': ValueConversion.as_boolean( self.free_with_admission ),
         'description': self.description,
         'info_link': self.info_link,
         'hyperlink_text': self.hyperlink_text,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'region': self.region,
         'is_closed': ValueConversion.as_boolean( self.is_closed ),
         'closed_message': self.closed_message,
         'likelihood': self.likelihood,
         'is_deleted': ValueConversion.as_boolean( self.is_deleted ),
         'old_likelihood': self.old_likelihood,
         'start_time': self.start_time,
         'end_time': self.end_time,
      }
