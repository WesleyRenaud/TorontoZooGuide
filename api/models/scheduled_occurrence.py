class ScheduledOccurrence:
   def __init__( self, date, time ):
      self.date = date
      self.time = time


   def to_dict( self ):
      return {
         'date': self.date,
         'time': self.time,
      }
