class ZooHours:
   def __init__(
         self,
         date,
         early_admission_time,
         open_time,
         last_admission_time,
         close_time ):

      self.date = date
      self.early_admission_time = early_admission_time
      self.open_time = open_time
      self.last_admission_time = last_admission_time
      self.close_time = close_time


   def to_dict( self ):
      return {
         'date': self.date,
         'earlyAdmissionTime': self.early_admission_time,
         'openTime': self.open_time,
         'lastAdmissionTime': self.last_admission_time,
         'closeTime': self.close_time,
      }
