from ..zoo_util import ZooUtil


class WildEncounterDiff:
   def __init__( self, name, is_deleted, start_time=None, end_time=None ):
      self.name = name
      self.is_deleted = is_deleted
      self.start_time = start_time
      self.end_time = end_time


   def to_dict( self ):
      return {
         'name': self.name,
         'is_deleted': ZooUtil.as_boolean( self.is_deleted ),
         'start_time': self.start_time,
         'end_time': self.end_time,
      }
