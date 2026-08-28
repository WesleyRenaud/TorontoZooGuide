from __future__ import annotations

from .guardians_talk_linked_animal import GuardiansTalkLinkedAnimal
from ..shared.text_values import TextValues
from ..shared.value_conversion import ValueConversion
from ..types import Types


class GuardiansTalk:
   def __init__(
         self,
         name: str,
         location: str,
         x_coord: Types.Coordinate,
         y_coord: Types.Coordinate,
         start_time: Types.ScheduleTimeKey = None,
         maximum_duration: int | None = None,
         end_time: Types.ScheduleTimeKey = None,
         is_available: bool = True,
         unavailable_message: str | None = None,
         is_deleted: bool = False,
         linked_animals: list[ GuardiansTalkLinkedAnimal ] | None = None ) -> None:
      self.name = name
      self.location = location
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.start_time = start_time
      self.maximum_duration = maximum_duration
      self.end_time = end_time
      self.is_available = is_available
      self.unavailable_message = unavailable_message
      self.is_deleted = is_deleted
      self.linked_animals = list( linked_animals or [] )


   def name_key( self ) -> str:
      return TextValues.normalize_for_matching( self.name )


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'location': self.location,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'start_time': self.start_time,
         'maximum_duration': self.maximum_duration,
         'end_time': self.end_time,
         'is_available': ValueConversion.as_boolean( self.is_available ),
         'unavailable_message': self.unavailable_message,
         'is_deleted': ValueConversion.as_boolean( self.is_deleted ),
         'linked_animals': [
            linked_animal.to_dict()
            for linked_animal in self.linked_animals
         ],
      }
