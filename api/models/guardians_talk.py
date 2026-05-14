from ..zoo_util import ZooUtil


class GuardiansTalk:
   def __init__(
         self,
         name,
         location,
         x_coord,
         y_coord,
         start_time=None,
         maximum_duration=None,
         end_time=None,
         is_available=True,
         unavailable_message=None,
         is_deleted=False ):
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


   def to_dict( self ):
      return {
         'name': self.name,
         'location': self.location,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'start_time': self.start_time,
         'maximum_duration': self.maximum_duration,
         'end_time': self.end_time,
         'is_available': ZooUtil.as_boolean( self.is_available ),
         'unavailable_message': self.unavailable_message,
         'is_deleted': ZooUtil.as_boolean( self.is_deleted )
      }
